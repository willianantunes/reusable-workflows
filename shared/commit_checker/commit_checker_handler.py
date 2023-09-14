import argparse
import json
import shlex
import subprocess

from pathlib import Path


def _execute_command(command: list[str] | str, path=None) -> str | dict:
    if not path:
        path = Path("./").resolve()

    subprocess_params = {"capture_output": True, "encoding": "utf8", "cwd": str(path)}
    if type(command) is not str:
        result = subprocess.run(command, **subprocess_params)
        return_code = result.returncode
        print(f"The command returned {return_code} for the command: {command}")
        return result.stdout if result.stdout else result.stderr  # type: ignore
    else:
        process_list = list()
        previous_process = None
        for command_part in command.split("|"):
            arguments = shlex.split(command_part)
            if previous_process is None:
                process = subprocess.Popen(arguments, stdout=subprocess.PIPE, cwd=str(path))
            else:
                process = subprocess.Popen(
                    arguments, stdin=previous_process.stdout, stdout=subprocess.PIPE, cwd=str(path)
                )
            process_list.append(process)
            previous_process = process
        last_process = process_list[-1]
        output, errors = last_process.communicate()
        assert errors is None
        return json.loads(output.decode("utf-8", "ignore"))


def _commits_comply_with_conventional(commits: list[dict[str, str]], path=None) -> tuple[bool, int]:
    command_template = 'echo "{0}" | npx commitlint -o commitlint-format-json'
    message_template = "The commit message:\n\n{0}\n\n Is valid? {1}\nError count: {2}\nResult: {3}"
    number_of_problematic_commits = 0
    for commit_details in commits:
        commit = commit_details["messageHeadline"]
        skip_merge_commit = commit.startswith("Merge branch") or commit.startswith("Merge pull")
        if skip_merge_commit:
            continue
        if commit_details["messageBody"]:
            commit = f"{commit}\n\n{commit_details['messageBody']}"
        command = command_template.format(commit)
        output = _execute_command(command, path)
        valid_commit = output["valid"]
        print(message_template.format(commit, valid_commit, output["errorCount"], output["results"]))
        if not valid_commit:
            number_of_problematic_commits += 1
    following_conventional_commits = number_of_problematic_commits == 0
    if not following_conventional_commits:
        print(f"We found {following_conventional_commits} issues in your commits 😥. Please check them 👍")
    return number_of_problematic_commits == 0, number_of_problematic_commits


def _handle(repository_url: str, pr_id: int) -> bool:
    command_retrieve_commits = f"gh pr view {pr_id} --repo {repository_url} --json commits"
    pr_details = _execute_command(command_retrieve_commits)
    commits = pr_details["commits"]
    return _commits_comply_with_conventional(commits)[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--pull-request-id", type=int, required=True)
    args = parser.parse_args()

    repo = args.repo
    pull_request_id = args.pull_request_id
    print(f"Are all the commits from the PR {pull_request_id} following conventional commits 🤔? Repository: {repo}")

    valid = _handle(repo, pull_request_id)
    if not valid:
        exit(1)
