import requests
from config import git_token


def orgs(token):
    response = requests.get('https://api.github.com/organizations', headers={
    'Authorization': 'token ' +  token,
    'X-GitHub-Api-Version': '2022-11-28'
    })
    return print(response.json())


orgs(git_token)
