import argparse
import json
import subprocess

from shlex import split


def _run_command(command: str) -> dict:
    result = subprocess.run(split(command), capture_output=True, text=True)
    return_code = result.returncode
    if return_code != 0:
        print(f"The terminal returned {return_code} from the command: {command}")
        exit(1)
    return json.loads(result.stdout)


def _has_required_labels(labels: list[dict]) -> bool:
    database = {"type": [], "enhancement": [], "bug-priority": []}
    has_type_bug = False

    for label in labels:
        name = label["name"]
        if "[type]" in name:
            database["type"].append(name)
            if "[type] bug" == name:
                has_type_bug = True
        if "enhancement" in name:
            database["enhancement"].append(name)
        elif name.startswith("bug priority:"):
            database["bug-priority"].append(name)

    number_of_labels_kind_type = len(database["type"])
    number_of_labels_kind_feature = len(database["enhancement"])
    number_of_labels_kind_bug = len(database["bug-priority"])

    label_type_not_provided = number_of_labels_kind_type == 0
    if label_type_not_provided:
        print("You should provide at least one label that has '[type]' in its name.")
        return False

    invalid_number_of_enhancements = number_of_labels_kind_feature > 1
    if invalid_number_of_enhancements:
        print("Only one label of type enhancement is allowed. Pick just one 👮")
        return False

    missing_bug_type = not has_type_bug and number_of_labels_kind_bug > 0
    if missing_bug_type:
        print("'[type] bug' is required when bug severity is informed.")
        return False

    invalid_number_of_bugs = number_of_labels_kind_bug > 1
    if has_type_bug and invalid_number_of_bugs:
        print("Only one label of type bug severity is allowed. Pick just one 👮")
        return False

    print("LGTM 👀")
    return True


def _handle(repository_url: str, pr_id: int) -> bool:
    command = f"gh pr view {pr_id} --repo {repository_url} --json labels"
    pr_details = _run_command(command)
    labels = pr_details["labels"]
    return _has_required_labels(labels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--pull-request-id", type=int, required=True)
    args = parser.parse_args()

    repo = args.repo
    pull_request_id = args.pull_request_id
    print(f"Does the PR {pull_request_id} has have required labels 🤔? Target repository: {repo}")

    valid = _handle(repo, pull_request_id)
    if not valid:
        exit(1)
