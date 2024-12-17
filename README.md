# Mining of Social Data Labs

Each week we get a small lab to do some social data mining on and then we get to write a lil' report.


## Dependency Management and Venvs
Switched to [try out uv](https://docs.astral.sh/uv/). Started messing with with [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) and got carried away. Super cool but definitely overkill. Anyway the directory structure is:
```txt
social_data_mining
├── packages
│   ├── network-analysis
│   │   ├── pyproject.toml
│   │   └── src
│   │       └── network_anlysis
│   │           ├── __init__.py
│   │           ├── data.py (lab specific queries)
│   │           └── utils.py (graph specific queries)
│   └── text-mining
│       ├── pyproject.toml
│       └── src
│           └── text_mining
│               ├── __init__.py
│               └── utils.py (TODO: add utils for this lab here)
├── pyproject.toml
├── README.md
├── uv.lock
└── src
    └── sdm
        └── /lab_scripts (jupyter notbooks)
        └── /project_scripts (jupyter notbooks)
        ├── config.py
        ├── __init__.py (currently has main function)
        ├── config.py
        ├── crud.py (db queryies and stuff)
        └── main.py (TODO?)
```
## [Managing Deps](https://docs.astral.sh/uv/concepts/projects/dependencies/)
Use uv to manage project requirements ie:
install deps
```bash
uv sync
```

add a new dep
```bash
uv add <package name>
```
uv becomes our entry point for commands within our project
ex:
```bash
# instead of running `python` and entering python env
uv run python
# and it will make all the packages (including our own) importable in the python cli
```
uv also automatically manages python environment and packaging.
ie if you want to activate our project environment, the `.venv` folder is fully managed by uv

If you want to run commands from within our project environment (and skip using uv as the entrypoint to commands like `uv run blah`), then activate the uv-managed .venv (which should appear after `uv sync`
```bash
source .venv/bin/activate
```
Then with your activated env (should be called sdm), you can run whatever `python src/sdm/somescript.py` or `jupyter lab` etc

uv also support scripts (but I havent played with it). They are in `pyproject.toml` under `[project.scripts]` and allow you to create aliases for certain scripts (kinda like make or many other package managers)

We can run scripts (main as defined in scripts section of toml) with just
```bash
uv run sdm
```
Also added a script for ingesting data from accounts.tsv into the accounts table:
```bash
uv run inaccounts
