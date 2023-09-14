import unittest

from pathlib import Path
from unittest.mock import patch

from shared.commit_checker.commit_checker_handler import _commits_comply_with_conventional
from shared.commit_checker.commit_checker_handler import _handle


@unittest.skip("Should be executed manually")
class TestHandler(unittest.TestCase):
    @patch("shared.commit_checker.commit_checker_handler._commits_comply_with_conventional")
    def test_handler(self, mock_commits_comply_with_conventional):
        mock_commits_comply_with_conventional.return_value = True
        repo_url = "https://github.com/willianantunes/testing-repository"
        pr_id = 2
        self.assertTrue(_handle(repo_url, pr_id))


@unittest.skip("Should be executed manually")
class TestCommitCheckerHandler(unittest.TestCase):
    path = Path("./../../../shared/commit_checker").resolve()

    def test_valid_commits_when_all_comply(self):
        commits = [
            {"messageBody": "", "messageHeadline": "chore(pipeline): change contract"},
            {"messageBody": "T1", "messageHeadline": "feat: this is an honest test"},
            {"messageBody": "", "messageHeadline": "Merge branch 'develop' into feature/horizontal-view-update"},
            {"messageBody": "", "messageHeadline": "Merge pull request #796 from xyz/acme"},
            {"messageBody": "T1\nT2\nT3", "messageHeadline": "fix: this is an honest test"},
            {"messageBody": "Don't look downstairs!", "messageHeadline": "refactor: this is an honest test"},
            {"messageBody": "Don't look downstairs, again!", "messageHeadline": "docs: this is an honest test"},
        ]
        self.assertEquals((True, 0), _commits_comply_with_conventional(commits, self.path))

    def test_invalid_commits_when_one_is_invalid(self):
        commits = [
            {"messageBody": "", "messageHeadline": "chore(pipeline): change contract"},
            {"messageBody": "", "messageHeadline": "change contract"},
        ]
        self.assertEquals((False, 1), _commits_comply_with_conventional(commits, self.path))

    def test_valid_commit_when_the_single_one_comply(self):
        # It has length 72
        commit = "feat: so i'm back in high school, i'm standing in the middle of the acme"
        commits = [
            {"messageBody": "", "messageHeadline": commit},
        ]
        self.assertEquals((True, 0), _commits_comply_with_conventional(commits, self.path))

    def test_invalid_commit_when_commit_has_invalid_length(self):
        # It has length 73
        commit = "feat: so i'm back in high school, i'm standing in the middle of the xyz 1"
        commits = [
            {"messageBody": "", "messageHeadline": commit},
        ]
        self.assertEquals((False, 1), _commits_comply_with_conventional(commits, self.path))
