# Plum Project

An in house ETL framework for moving data to where it has to go.

## Development

You need to supply a `.env` file under `test_databases/postgres` for the database setup.

Running the postgres database independantly...

```sh
docker rmi postgres-postgres -f && \
docker system prune -f && \
docker compose -f ./test_databases/postgres/docker-compose.yml up
```