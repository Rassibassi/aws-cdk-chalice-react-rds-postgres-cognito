# Cheatsheet
Always `cd` into the respective directory!!!

Docker compose alias for your `.bashrc`, `alias dc='docker-compose'`


## Activate environment
```
. venv/bin/activate
deactivate
```

## Local development environment
Access database server via terminal and come cli function to populate the database.
The cli function only work in the local development environment
```
dc exec api-db psql -U postgres
dc exec api python cli.py recreate-db
dc exec api python cli.py drop-db
dc exec api python cli.py seed-db
```

## Deploy infrastructure
First, `cd` to the `infrastructure` directory
```
cdk deploy
```

## Deploy backend
First, `cd` to the `backend` directory
```
chalice deploy --stage prod
```

## Node deployment
First, `cd` to the `frontend` directory
```
DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --output . .

aws s3api create-bucket --bucket my_bucket --region moon-east-1 --create-bucket-configuration LocationConstraint=moon-central-1

aws s3 sync ./build s3://my_bucket

aws s3 website s3://my_bucket --index-document index.html --error-document error.html
```