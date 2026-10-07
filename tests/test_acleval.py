import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from acleval import core


class AclEvalTest(unittest.TestCase):
    def test_bits_roundtrip(self):
        self.assertEqual(core._to_text(core._to_bits("rwx")), "rwx")

    def test_empty_acl(self):
        self.assertEqual(core.evaluate({}, "a", "b", [], core.Counter()), "---")

    def test_owner_exact(self):
        a = {"entries": [("user", "", "rwx")]}
        self.assertEqual(core.evaluate(a, "a", "a", [], core.Counter()), "rwx")

    def test_result_is_three_chars(self):
        a = {"entries": [("other", "", "r--")]}
        self.assertEqual(len(core.evaluate(a, "a", "b", [], core.Counter())), 3)

    def test_missing_user(self):
        a = {"entries": [("user", "bob", "rwx")]}
        self.assertEqual(core.evaluate(a, "a", "b", [], core.Counter()), "---")

    def test_counter_counts(self):
        a = {"entries": [("user", "", "rwx")]}
        counter = core.Counter()
        core.evaluate(a, "a", "a", [], counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
