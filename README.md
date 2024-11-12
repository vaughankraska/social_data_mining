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

## Neo4j and Twitter Data
Looks like we are putting the twitter data in a database because it's clunky and slow in plain old pandas/native file formats.

Helpful reources:
- [neo4j apoc json docs](https://neo4j.com/docs/apoc/current/overview/apoc.load/apoc.load.json/)
- [Medium article on setting it up in Docker](https://medium.com/@matthewghannoum/simple-graph-database-setup-with-neo4j-and-docker-compose-061253593b5a)
- [The graph-database plugin on Github](https://github.com/neo4j/graph-data-science)
    - [and the python client for that plugin](https://github.com/neo4j/graph-data-science-client)



### Setup
(assumes data has been downloaded from uppsala.box.com and put in ./data)
1. Start Docker with `docker compose up --build -d`
2. Copy tweets.dat to the neo4j workspace `cp data/tweets.dat data/neo4j_db/import/tweets.dat`
3. Run some import script that we havent created yet.
