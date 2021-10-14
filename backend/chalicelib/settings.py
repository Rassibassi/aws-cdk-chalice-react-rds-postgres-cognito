import os


class Settings:
    CHALICE_STAGE = os.environ["CHALICE_STAGE"]
    COGNITO_ARN = os.environ["COGNITO_ARN"]    

    if CHALICE_STAGE == "production":
        DATABASE_SECRET_NAME = os.environ["DATABASE_SECRET_NAME"]
    else:
        DATABASE_URL = os.environ["DATABASE_URL"]

