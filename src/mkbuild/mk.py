import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


def run_silent(*args) -> subprocess.CompletedProcess:
    if isinstance(args[0], tuple):
        args = args[0]
    cmd = []
    for arg in args:
        cmd += arg.split()

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    return result


def run(*args) -> subprocess.CompletedProcess:
    print("mk:", " ".join(args))
    result = run_silent(args)
    print(result.stdout, end="")
    print(result.stderr, end="")

    if len(result.stderr) > 0:
        print("mk: build error!")
        sys.exit(1)

    return result


def preprocess(filename) -> str:
    result = run_silent(CC, "-E", CFLAGS, filename)
    return result.stdout


def hashfile(filename) -> str:
    data = preprocess(filename).encode()
    return hashlib.sha256(data).hexdigest()


def load_hashes() -> dict:
    try:
        with open(os.path.join(BIN_DIR, ".mkhashes")) as f:
            hashes = json.load(f)
    except FileNotFoundError:
        hashes = {}

    return hashes


def dump_hashes(hashes: dict):
    with open(os.path.join(BIN_DIR, ".mkhashes"), "w") as f:
        json.dump(hashes, f)


def get_new_hashes_and_changed_sources(
    hashes: dict, sources: list[str]
) -> tuple[dict, list[str]]:
    new_hashes = {src: hashfile(src) for src in sources}
    changed_sources = []
    for src, value in new_hashes.items():
        if hashes.get(src) and value == hashes[src]:
            continue
        changed_sources.append(src)

    return new_hashes, changed_sources


def get_identifier_no_extension(path: str) -> str:
    identifier = path.replace("\\", ".").replace("/", ".")
    return ".".join(identifier.split(".")[:-1])


# if len(sys.argv) != 2:
#     raise Exception(
#         'Invalid system input! Program takes exactly one argument: "debug" or "release"!'
#     )

CC = "gcc"
NAME = "pineapple2"
SRC_DIR = "src"
BIN_DIR = "bin"

DEBUG = sys.argv[1] == "debug"

CFLAGS = "-std=c23 -Wall -Iinclude"
CFLAGS += " -g -DDEBUG" if DEBUG else " -O3"
LDFLAGS = "-Llib -lSDL3_net -lSDL3 -lchelp -Wl,-rpath,$ORIGIN/../lib"

TARGET_OS = platform.system()
if TARGET_OS == "Windows":
    EXE = ".exe"
    LDFLAGS += " -lopengl32 -lgdi32"
elif TARGET_OS == "Linux":
    LDFLAGS += " -lGL"
    EXE = ".elf"


SOURCES = []
for root, _, files in os.walk(SRC_DIR):
    SOURCES += [Path(root, file) for file in files]

OBJECTS = [
    str(Path(BIN_DIR, get_identifier_no_extension(src) + ".o"))
    for src in SOURCES
]

hashes = load_hashes()
hashes, changed_sources = get_new_hashes_and_changed_sources(hashes, SOURCES)

run("mkdir -p", BIN_DIR)

changed_objects = [
    os.path.join(BIN_DIR, get_identifier_no_extension(src) + ".o")
    for src in changed_sources
]

for src, obj in zip(changed_sources, changed_objects):
    run(CC, "-c", src, CFLAGS, "-o", obj)


outfile = os.path.join(BIN_DIR, NAME + EXE)
run(CC, " ".join(OBJECTS), CFLAGS, LDFLAGS, "-o", outfile)

dump_hashes(hashes)
