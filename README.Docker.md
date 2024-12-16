### Building and running postgres

Start database:
`docker compose up --build -d`.

Stop database:
`docker compose down`

Stop AND DROP database:
`docker compose down -v`

### Exec into database and run test queries with psql CLI:
1. Get the container id:
`docker ps`
```txt
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS                   PORTS                    NAMES
852a333a9170   pgvector/pgvector:pg17   "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:5432->5432/tcp   social_data_mining-db-1
```
2. Exec into db:
`docker exec -it 1aac9778979f bash`
3. Enter psql mode
`psql sdm`

#### Helpful psql commands
List databases:
`\l`

Show relationships:
`\d`

List tables:
`\dt`

Connect to particular database:
`\c postgres` or to connect to our main db `\c sdm`

Run raw queries:
`SELECT COUNT(*) FROM tablename;`

Exit:
`\q`
