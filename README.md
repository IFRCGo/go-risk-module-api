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

## Run Migrations
`docker compose exec server bash -c python manage.py migrate`

Navigate with server `localhost:9001`
