import sys

import typer

from githubctl.cli.repo import repo_app


app = typer.Typer()
app.add_typer(repo_app, name="repo")


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(str(e))
        sys.exit(1)
