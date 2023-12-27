import sys
import os

import typer
from dotenv import load_dotenv

from githubctl.cli.repo import repo_app
from githubctl.cli.stars import stars_app

# first check if .env file exists in the current directory
if os.path.isfile('.env'):
    load_dotenv('.env')

# then check if .env file exists in the user's home directory
elif os.path.isfile(os.path.join(os.path.expanduser('~'), '.env')):
    load_dotenv(os.path.join(os.path.expanduser('~'), '.env'))

# if both not found, then will try to use the environment variables are set


app = typer.Typer()
app.add_typer(repo_app, name="repo", help="Manage repositories")
app.add_typer(stars_app, name="stars", help="Manage stars")


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(str(e))
        sys.exit(1)
