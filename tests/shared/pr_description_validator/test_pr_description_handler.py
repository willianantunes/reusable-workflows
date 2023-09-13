import unittest

from shared.pr_description_validator.pr_description_handler import _handle
from shared.pr_description_validator.pr_description_handler import _valid_description


class TestHandler(unittest.TestCase):
    def test_invalid_description_when_text_has_no_required_text(self):
        text = "'This is a sample text.\r\n\r\n```\r\nsomething\r\n```'"
        result = _valid_description(text)
        self.assertFalse(result)

    def test_invalid_description_when_text_required_text_does_not_match_regex(self):
        text = "'This https://wig.monday.com/boards/XXX/pulses/XXX is a sample text.\r\n\r\n```\r\nsomething\r\n```'"
        result = _valid_description(text)
        self.assertFalse(result)

    def test_valid_description_when_text_has_required_text_with_new_line(self):
        text = "'Th\nis https://rop.monday.com/boards/3957397225/pulses/5054449935.\r\n\r\n```\r\nsomething\r\n```'"
        result = _valid_description(text)
        self.assertTrue(result)

    def test_valid_description_when_text_has_required_text_with_without_line(self):
        text = "'The wig https://rop.monday.com/boards/3957397225/pulses/5054449935.\r\n\r\n```\r\nsomething\r\n```'"
        result = _valid_description(text)
        self.assertTrue(result)

    @unittest.skip("Should be executed manually")
    def test_handle(self):
        repo_url = "https://github.com/willianantunes/testing-repository"
        pr_id = 2
        _handle(repo_url, pr_id)
