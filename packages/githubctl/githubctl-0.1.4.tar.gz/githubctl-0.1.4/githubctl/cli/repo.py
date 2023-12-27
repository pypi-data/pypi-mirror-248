import typer
from typing import Optional

from githubctl._github import get_all_user_repositories
from githubctl.utils import print_beauty
from githubctl.utils import filter_list_of_dicts
from githubctl.utils import sort_list_of_dicts
from githubctl.constants import PrintFormatOptions

repo_app = typer.Typer()


@repo_app.command("list")
def list_repos(
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
    """List all repositories
    
    EXAMPLES

    - To list all repositories for a user, print as table:

    githubctl repo list -u xiaopeng163 --output=table

    - list all repositories with language is Python and not forked:

    githubctl repo list -u xiaopeng163 --query="[?(language=='Python' && fork=='False')]" --output=table

    - list all repositories with language is Python and not forked, sort by stars by descending:
    
    githubctl repo list -u xiaopeng163 --query="[?(language=='Python' && fork=='False')]" --sort-by=~stars --output=table
    """
    repo = get_all_user_repositories(username=user)
    if query:
        repo = filter_list_of_dicts(repo, query)
    if sort_by:
        repo = sort_list_of_dicts(repo, sort_by)
    print_beauty(repo, output=output)
