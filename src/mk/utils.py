import subprocess
import sys


def run_silent(*args: str) -> subprocess.CompletedProcess:
    """Runs a subprocess silently.

    Args:
        args: A tuple of strings
    Returns:
        result: The completed process result
    """
    if isinstance(args[0], tuple):
        args = args[0]
    cmd = []
    for arg in args:
        cmd += arg.split()

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    return result


def log(*args: str, end: str = "\n") -> None:
    """Logs a message to the console."""
    print("mk:", " ".join(args), end=end)


def run(*args: str) -> subprocess.CompletedProcess:
    """Runs a process with arguments.

    Args:
        args: Process with its arguments
    Returns:
        result: The completed process
    """
    log(*args)
    result = run_silent(*args)
    print(result.stdout, end="")
    print(result.stderr, end="")

    if len(result.stderr) > 0:
        log("build error!")
        sys.exit(1)

    return result
