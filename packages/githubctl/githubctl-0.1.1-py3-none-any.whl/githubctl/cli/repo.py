import typer
from typing import Optional

from githubctl._github import get_repos
from githubctl.utils import print_beauty
from githubctl.utils import filter_list_of_dicts
from githubctl.utils import sort_list_of_dicts
from githubctl.constants import PrintFormatOptions

repo_app = typer.Typer()


@repo_app.command("list", help="List all repositories")
def list_repos(
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
    repo = get_repos(username="xiaopeng163123")
    if query:
        repo = filter_list_of_dicts(repo, query)
    if sort_by:
        repo = sort_list_of_dicts(repo, sort_by)
    print_beauty(repo, output=output)
