import mk

mk.Pipeline(
    CONTEXT=mk.Context(),
    TRANSFORMERS=[
        mk.compilers.GNUCCompiler(),
        mk.linkers.GNUCLinker(TARGET="output", TARGET_EXTENSION=".exe"),
    ],
).run()
