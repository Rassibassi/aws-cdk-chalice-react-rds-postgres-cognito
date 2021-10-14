import json
from urllib.parse import urlparse
import boto3
from peewee import PostgresqlDatabase

from chalicelib.settings import Settings

if Settings.CHALICE_STAGE == "production":
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=Settings.DATABASE_SECRET_NAME)
    db_credentials = json.loads(response["SecretString"])

    database_name = db_credentials["dbname"]
    user = db_credentials["username"]
    password = db_credentials["password"]
    host = db_credentials["host"]
    port = db_credentials["port"]
    
else:
    parse_result = urlparse(Settings.DATABASE_URL)
    database_name = parse_result.path[1:]
    user = parse_result.username
    password = parse_result.password
    host = parse_result.hostname
    port = parse_result.port



db = PostgresqlDatabase(
    database_name, user=user, password=password, host=host, port=port
)
