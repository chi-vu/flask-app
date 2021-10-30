import requests
import sys


class InvalidUser(Exception):
    pass


def get_github_repos(user_name):
    try:
        resp = requests.get(
            'https://api.github.com/users/{}/repos'.format(user_name))
        status_code = resp.status_code
        if status_code == 200:
            repos = [user['name'] for user in resp.json()]
            if len(repos) == 0:
                print("This user has no Github repositories")
            elif len(repos) == 1:
                print("This user has 1 Github repository: {}".format(repos[0]))
            else:
                print("This user has {} Github repositories: {}"
                      .format(len(repos), repos))
        elif status_code == 404:
            raise InvalidUser
    except InvalidUser:
        print("Username is invalid")


def main():
    if len(sys.argv) < 2:
        print("Please input the username")
        sys.exit(1)
    user_name = sys.argv[1]
    get_github_repos(user_name)


if __name__ == "__main__":
    main()
