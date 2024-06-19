import glob
import os
import re

import click

from db.common import connect
from db.user import accept_pending_user

migration_file_pattern = re.compile(r"V(.*)__.*\.sql")

def check_version(cur):
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS version (
                id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(128),
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
    )

    cur.execute("SELECT name FROM version ORDER BY created_on DESC LIMIT 1")
    
    result = cur.fetchone()

    if result is not None and len(result) == 1:
        return result[0]
    
    return None


def get_migrations():
    return sorted(list(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "db/migrations/*.sql"))))


def get_version_name(migration):
    match = migration_file_pattern.match(os.path.basename(migration))
    if match is None:
        return None

    return match.group(1)


def migrate_to(version, cur):
    for migration in get_migrations():
        migration_version = get_version_name(migration)
        if migration_version is None or (version is not None and migration_version <= version):
            continue

        with open(migration, encoding="utf-8") as sql_file_handle:
            sql = sql_file_handle.read()
            cur.execute(sql)
            cur.execute("INSERT INTO version (name) VALUES (%s)", (migration_version,))


def is_latest_version(version):
    migrations = get_migrations()
    if len(migrations) <= 0:
        return True
    
    return version == get_version_name(migrations[-1])


@click.group()
def cli():
    pass


@cli.command()
def migrate():
    with connect() as conn:
        with conn.cursor() as cur:
            version = check_version(cur)

            if not is_latest_version(version):
                migrate_to(version, cur)


@cli.command()
@click.option("--user", help="User's sub.")
def accept(user):
    accept_pending_user(user)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("./.env")

    cli()
