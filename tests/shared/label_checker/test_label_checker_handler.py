import unittest

from shared.label_checker.label_checker_handler import _has_required_labels


class TestRequiredLabels(unittest.TestCase):
    def test_has_not_required_labels_given_label_describing_type(self):
        labels = [
            {"name": "documentation"},
        ]
        result = _has_required_labels(labels)
        self.assertFalse(result)

    def test_has_required_labels_given_label_type(self):
        labels = [
            {"name": "documentation"},
            {"name": "[type] project maintenance"},
        ]
        result = _has_required_labels(labels)
        self.assertTrue(result)

    def test_has_not_required_labels_given_two_labels_of_type_enhancement(self):
        labels = [
            {"name": "documentation"},
            {"name": "[type] enhancement: planned"},
            {"name": "[type] enhancement: not planned"},
        ]
        result = _has_required_labels(labels)
        self.assertFalse(result)

    def test_has_required_labels_given_one_labels_of_type_enhancement(self):
        labels = [
            {"name": "documentation"},
            {"name": "[type] enhancement: not planned"},
        ]
        result = _has_required_labels(labels)
        self.assertTrue(result)

    def test_has_not_required_labels_given_two_labels_of_type_feature(self):
        labels = [
            {"name": "documentation"},
            {"name": "maintenance"},
            {"name": "feature: planned"},
            {"name": "feature: not planned"},
        ]
        result = _has_required_labels(labels)
        self.assertFalse(result)

    def test_has_not_required_labels_given_one_label_of_type_bug_is_missing(self):
        labels = [
            {"name": "documentation"},
            {"name": "maintenance"},
            {"name": "bug priority: critical"},
        ]
        result = _has_required_labels(labels)
        self.assertFalse(result)

    def test_has_required_labels_given_one_label_of_type_bug_is_informed_together_with_severity(self):
        labels = [
            {"name": "documentation"},
            {"name": "maintenance"},
            {"name": "bug priority: critical"},
            {"name": "[type] bug"},
        ]
        result = _has_required_labels(labels)
        self.assertTrue(result)

    def test_has_not_required_labels_given_one_label_of_type_bug_with_two_severities(self):
        labels = [
            {"name": "documentation"},
            {"name": "maintenance"},
            {"name": "bug priority: critical"},
            {"name": "bug priority: low"},
            {"name": "[type] bug"},
        ]
        result = _has_required_labels(labels)
        self.assertFalse(result)
