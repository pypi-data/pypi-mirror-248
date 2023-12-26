import os

from github import Github
from rich import print, inspect

# Authentication is defined via github.Auth
from github import Auth


def get_repos(username=None):
    # using an access token

    if os.environ.get("GITHUB_TOKEN"):
        auth = Auth.Token(os.environ.get("GITHUB_TOKEN"))
    else:
        auth = None

    # First create a Github instance:
    # Public Web Github
    g = Github(auth=None)

    repos = []
    for repo in g.get_user(username).get_repos():
        repos.append(
            {
                "name": repo.name,
                "url": repo.html_url,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks,
                "fork": str(repo.fork),
                "created_at": repo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    # To close connections after use
    g.close()

    return repos
