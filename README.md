# What is This?
This repository is an opinonated project template for using aws-cdk, Chalice and React in concert. Where aws-cdk and Chalice are in Python and React is in Javascript. The idea is to quickly build an API in Python with Chalice, deploy it easily with aws-cdk, and then access resources through a React frontend app including user authentication via AWS Cognito.

This is still under active development but some steps towards a full integration are done. It can be developed and run locally via docker compose. Infrastructure and Chalice deployments are still seperate and some copy and pasta is necessary to pass runtime parameters to the right places, but the aim is to have it fully integrated at some point. 

The cognito user pool is not part of the infractructure (aws-cdk), yet, and has to be created manually, e.g. in the web UI.

The following files need to be edited with custom AWS parameters and some renamed:
```
backend/.chalice/config_sample.json
backend/.chalice/policy_sample.json
backend/app.py # cognito ids
backend/cli.py # cognito ids

frontend/env.development.local_sample
frontend/env.production.local_sample
```

Things still Todo:
- Figure out how to run the create table command after deployment
- Create Todo list CRUD backend
- Create Todo list CRUD frontend
- Integrate Chalice into aws-cdk code, using `from chalice.cdk import Chalice`

Checkout cheatsheet.md for some useful CLI commands.

## Quickstart

First, you'll need to install the AWS CDK if you haven't already.
The CDK requires Node.js and npm to run.

```
$ npm install -g aws-cdk
```

Next you'll need to install the requirements for the project.

```
$ pip install -r requirements.txt
```

There's also separate requirements files in the `infrastructure`
and `backend` directories if you'd prefer to have separate virtual
environments for your CDK and Chalice app.

To deploy the application, `cd` to the `infrastructure` directory.
If this is you're first time using the CDK you'll need to bootstrap
your environment.

```
$ cdk bootstrap
```

Then you can deploy your infrastructure using the CDK.

```
$ cdk deploy
```

Now `cd` into the `backend` folder and then you can deploy your application using Chalice.

```
$ chalice deploy --stage prod
```

## Node deployment
Now `cd` into the `frontend` folder

```
DOCKER_BUILDKIT=1 docker build -f Dockerfile.build --output . .

aws s3api create-bucket --bucket my_bucket --region moon-east-1 --create-bucket-configuration LocationConstraint=moon-central-1

aws s3 sync ./build s3://my_bucket

aws s3 website s3://my_bucket --index-document index.html --error-document error.html
```

## Project layout
This project template combines a CDK application, a Chalice application and a React application.

These correspond to the `infrastructure`, `backend` and `frontend` directory, respectively.  To run any CDK CLI commands, ensure you're in the `infrastructure` directory, to run any Chalice CLI commands ensure you're in the `backend` directory, and to run React CLI commands ensure you are in the `frontend` directory.