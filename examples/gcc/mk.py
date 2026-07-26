import mk

mk.Pipeline(
    [
        mk.compilers.GNUCCompiler(),
        mk.linkers.GNUCLinker(TARGET="output", TARGET_EXTENSION=".exe"),
    ]
).run()
