import json
from functools import wraps
from urllib.parse import urlparse

import boto3
from chalice import Chalice, CognitoUserPoolAuthorizer, ForbiddenError

from chalicelib.models import User, db, db_models
from chalicelib.settings import Settings

app = Chalice(app_name="sampleapp")
app.debug = True
authorizer = CognitoUserPoolAuthorizer(
    "cognito_user_pool", provider_arns=[Settings.COGNITO_ARN]
)


def is_in_group(group):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = app.current_request
            groups = request.context["authorizer"]["claims"].get("cognito:groups", "")
            if group not in groups:
                raise ForbiddenError(f"User must be in the {group} group")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/ping", methods=["GET"], cors=True)
def ping():
    return {"status": "success", "message": "ping!"}


@app.route("/setupdb", methods=["GET"], cors=True)
def setupdb():
    # for debugging purposes
    db.drop_tables(db_models)
    db.create_tables(db_models)
    # ids in your user pool that already exist
    ids = [
        "88888888-cognitoid1-88888888",
        "88888888-cognitoid2-88888888",
        "88888888-cognitoid3-88888888",
    ]
    for name in ids:
        user = User(name=name)
        user.save()

    return {"status": "success"}


@app.route("/pong", methods=["GET"], authorizer=authorizer, cors=True)
@is_in_group("admin")
def pong():
    # context in this variable: app.current_request.context
    return {
        "status": "success",
        "message": "Authorized pong!",
    }

@app.lambda_function(name="post_authentication_create_user")
def post_authentication_create_user(event, context):
    """
        Set cognito post authentication trigger to chalice lambda function:
        ```
            aws cognito-idp update-user-pool \
            --user-pool-id xxx \
            --lambda-config PostAuthentication=arn:aws:lambda:xxx:xxx:function:sampleapp-prod-post_authentication_create_user
        ```
    """
    create_user(username)
    return event