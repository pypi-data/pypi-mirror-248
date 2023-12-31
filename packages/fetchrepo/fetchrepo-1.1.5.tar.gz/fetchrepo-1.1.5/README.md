# Repo Fetches
fetches the contents that are present in the github repo through by passing the parameters as repo link, branch and access token(for private repo)
## Example
from FetchRepo.RepoFetcher import harvest_github_repo

repo_link = "https://your repo link"
access_token = "your access token"
code = harvest_github_repo(repo_link,branch="main",access_token=access_token)
print(code)
