from django.test import SimpleTestCase

from shop.utils.validators import clean_text, parse_bool, parse_rating


class ValidatorTests(SimpleTestCase):
    # -------------------------
    # clean_text
    # -------------------------
    def test_clean_text_returns_trimmed_string(self):
        self.assertEqual(clean_text("  hello  "), "hello")

    def test_clean_text_returns_none_for_empty_string(self):
        self.assertIsNone(clean_text(""))

    def test_clean_text_returns_none_for_whitespace_only_string(self):
        self.assertIsNone(clean_text("   "))

    def test_clean_text_returns_none_for_non_string_value(self):
        self.assertIsNone(clean_text(123))
        self.assertIsNone(clean_text(None))
        self.assertIsNone(clean_text(True))
        self.assertIsNone(clean_text(["hello"]))

    # -------------------------
    # parse_bool
    # -------------------------
    def test_parse_bool_returns_default_when_value_is_none(self):
        self.assertFalse(parse_bool(None))
        self.assertTrue(parse_bool(None, default=True))

    def test_parse_bool_returns_same_value_for_bool_input(self):
        self.assertTrue(parse_bool(True))
        self.assertFalse(parse_bool(False))

    def test_parse_bool_returns_none_for_non_bool_input(self):
        self.assertIsNone(parse_bool("true"))
        self.assertIsNone(parse_bool("false"))
        self.assertIsNone(parse_bool(1))
        self.assertIsNone(parse_bool(0))
        self.assertIsNone(parse_bool([]))

    # -------------------------
    # parse_rating - valid values
    # -------------------------
    def test_parse_rating_accepts_valid_integer_values(self):
        self.assertEqual(parse_rating(1), 1)
        self.assertEqual(parse_rating(3), 3)
        self.assertEqual(parse_rating(5), 5)

    def test_parse_rating_accepts_valid_numeric_strings(self):
        self.assertEqual(parse_rating("1"), 1)
        self.assertEqual(parse_rating("4"), 4)
        self.assertEqual(parse_rating("5"), 5)

    # -------------------------
    # parse_rating - boundary values
    # -------------------------
    def test_parse_rating_returns_none_for_out_of_range_values(self):
        self.assertIsNone(parse_rating(0))
        self.assertIsNone(parse_rating(6))
        self.assertIsNone(parse_rating("-1"))
        self.assertIsNone(parse_rating("10"))

    # -------------------------
    # parse_rating - invalid types
    # -------------------------
    def test_parse_rating_returns_none_for_bool_values(self):
        self.assertIsNone(parse_rating(True))
        self.assertIsNone(parse_rating(False))

    def test_parse_rating_returns_none_for_float_values(self):
        self.assertIsNone(parse_rating(1.0))
        self.assertIsNone(parse_rating(4.5))

    def test_parse_rating_returns_none_for_non_numeric_values(self):
        self.assertIsNone(parse_rating("abc"))
        self.assertIsNone(parse_rating(""))
        self.assertIsNone(parse_rating(None))
        self.assertIsNone(parse_rating([]))
        self.assertIsNone(parse_rating({}))