# GO Risk Module Backend

## Backend Server Setup

```
# Copy sample/development .env
cp .env-sample .env

# Build docker image
docker compose build

# Start container
docker compose-up
```

Navigate with server `localhost:9001`

## Run Migrations

`docker compose exec server bash -c python manage.py migrate`

## Update openapi schema (openapi-schema.yaml)

```bash
docker compose run --rm server ./manage.py spectacular --file /ci-share/openapi-schema-latest.yaml
```
