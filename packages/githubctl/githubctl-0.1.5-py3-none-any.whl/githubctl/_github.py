import os
import requests


def get_all_user_repositories(username):
    base_url = f"https://api.github.com/users/{username}/repos"
    repos = []
    if os.environ.get("GITHUB_TOKEN"):
        headers = {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
    else:
        headers = None
    try:
        page = 1
        while True:
            params = {"page": page, "per_page": 100}  # Adjust per_page as needed
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()

            repositories = response.json()
            if not repositories:
                break  # No more repositories

            for repo in repositories:
                print(repo)
                repo_info = {
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "fork": repo["fork"],
                    "created_at": repo["created_at"],
                }
                repos.append(repo_info)

            page += 1

        return repos
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories for user {username}: {e}")
        return None
