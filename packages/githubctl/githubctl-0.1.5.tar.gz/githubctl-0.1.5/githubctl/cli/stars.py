import typer
from typing import Optional

from githubctl.constants import PrintFormatOptions

stars_app = typer.Typer()


@stars_app.command("list")
def list_stars(
    user: str = typer.Option(..., "--user", "-u", help="github user name"),
    query: str = typer.Option(
        None,
        "--query",
        "-q",
        help="JMESPath query string. See http://jmespath.org/ for more information and examples",
    ),
    output: PrintFormatOptions = typer.Option(
        PrintFormatOptions.json,
        "--output",
        help="Sets the format for printing command output resources",
    ),
    sort_by: Optional[str] = typer.Option(
        None, help="Comma-separated list of resource field key names to sort by"
    ),
):
    pass