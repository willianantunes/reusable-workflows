import argparse
import json
import re
import subprocess

from shlex import split


def _run_command(command: str) -> dict:
    result = subprocess.run(split(command), capture_output=True, text=True)
    return_code = result.returncode
    if return_code != 0:
        print(f"The terminal returned {return_code} from the command: {command}")
        exit(1)
    return json.loads(result.stdout)


def _valid_description(text: str) -> bool:
    pattern = re.compile(r".*(https:\/\/[a-z]+\.monday\.com\/boards\/[0-9]+\/(views|pulses)\/[0-9]+)", re.M | re.DOTALL)
    match = pattern.match(text)

    if not match:
        print("You don't have a valid entry 😔")
        return False

    valid_text = match.groups()[0]
    print(f"You have a valid entry in your text: {valid_text}")
    return True


def _handle(repository_url: str, pr_id: int) -> bool:
    command = f"gh pr view {pr_id} --repo {repository_url} --json body"
    pr_details = _run_command(command)
    description = pr_details["body"]
    return _valid_description(description)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--pull-request-id", type=int, required=True)
    args = parser.parse_args()

    repo = args.repo
    pull_request_id = args.pull_request_id
    print(f"Is the description of PR {pull_request_id} valid 🤔? Target repository: {repo}")

    valid = _handle(repo, pull_request_id)
    if not valid:
        exit(1)
