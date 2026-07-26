# mkbuild

A build system scripting service.

NOTE: This project is in alpha.

For example:
```py
import mkbuild as mk

mk.Pipeline(
    CONTEXT=mk.Context(),
    TRANSFORMERS=[
        mk.compilers.GNUCCompiler(
            FLAGS=mk.Flags("-std=c23 -Wall -Iinclude"),
            DEBUG_FLAGS=mk.Flags("-g -DDEBUG"),
            RELEASE_FLAGS=mk.Flags("-O2"),
        ),
        mk.linkers.GNUCLinker(
            FLAGS=mk.OSFlags(
                FLAGS="-Llib -lSDL3_net -lSDL3 -lchelp -Wl,-rpath,$ORIGIN/../lib",
                WINDOWS="-lopengl32 -lgdi32",
                LINUX="-lGL",
            ),
            DEBUG_FLAGS=mk.Flags("-g -DDEBUG"),
            RELEASE_FLAGS=mk.Flags("-O2"),
            TARGET="Pineapple2",
            TARGET_EXTENSION=".elf"
        )
    ]
).run()
```

Then run the build file (must be named "mk.py"):
```bash
python mk.py debug # Or release
```