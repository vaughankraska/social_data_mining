# Mining of Social Data Labs

Each week we get a small lab to do some social data mining on and then we get to write a lil' report.


## Dependency Management and Venvs
Use miniconda to manage the python environment for __python 3.11__

Use poetry to manage project requirements ie:
install deps
```bash
poetry install
```
add a new dep
```bash
poetry add <package name>
```


### Setup
(assumes data has been downloaded from uppsala.box.com and put in ./data)
1. Start Docker with `docker compose up --build -d`
2. Run some import script that we havent created yet.
