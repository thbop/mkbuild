## Build Instuctions

Install [uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) and prek:
```bash
uv add tool prek
uv sync --dev # Install required packages
```

Typecheck and lint using:
```bash
prek run --all-files
```

Build using:
```bash
uv build
```

## Git
Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) without scopes.