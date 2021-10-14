import json
import os

import click
from chalice.config import Config

with open(".chalice/config.json") as f:
    config_json = json.load(f)
    config = Config(config_from_disk=config_json)

    for key, value in config.environment_variables.items():
        os.environ[key] = value

from chalicelib.models import User, db, db_models


@click.group()
def cli():
    pass


@click.command()
def recreate_db():
    db.drop_tables(db_models)
    db.create_tables(db_models)
    click.echo("Initialized the database")


@click.command()
def seed_db():
    # ids in your user pool that already exist
    ids = [
        "88888888-cognitoid1-88888888",
        "88888888-cognitoid2-88888888",
        "88888888-cognitoid3-88888888",
    ]
    for name in ids:
        user = User(name=name)
        user.save()
    click.echo("Database seeded")


@click.command()
def drop_db():
    db.drop_tables(db_models)
    click.echo("Database dropped")


cli.add_command(recreate_db)
cli.add_command(seed_db)
cli.add_command(drop_db)

if __name__ == "__main__":
    cli()
