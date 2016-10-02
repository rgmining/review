"""Unit tests for review.scalar module.
"""
import random
import unittest

import numpy as np

from review.scalar import AverageReview
from review.scalar import AverageSummary


class TestAverageReview(unittest.TestCase):
    """Test case for AverageReview class.
    """

    def setUp(self):
        """Set up for tests.
        """
        self.a = random.random()
        self.b = random.random()
        while self.b == 0. or self.a == self.b:
            self.b = random.random()

    def test_create_with_non_number(self):
        """Test __init__ method with non numbers.
        """
        with self.assertRaises(TypeError):
            _ = AverageReview("non number")

    def test_add(self):
        """Test __add__ method.
        """
        ans = AverageReview(self.a) + AverageReview(self.b)
        self.assertEqual(ans.score, self.a + self.b)

    def test_add_with_non_review(self):
        """Test __add__ method with non review values.
        """
        r = AverageReview(self.a)
        with self.assertRaises(TypeError):
            _ = r + self.b
        with self.assertRaises(TypeError):
            _ = r + "self.b"
        with self.assertRaises(TypeError):
            _ = self.b + r
        with self.assertRaises(TypeError):
            _ =  "self.b" + r

    def test_sub(self):
        """Test __sub__ method.
        """
        ans = AverageReview(self.a) - AverageReview(self.b)
        self.assertEqual(ans.score, self.a - self.b)

    def test_sub_with_non_reivew(self):
        """Test __sub__ method with non review values.
        """
        r = AverageReview(self.a)
        with self.assertRaises(TypeError):
            _ = r - self.b
        with self.assertRaises(TypeError):
            _ = r - "self.b"
        with self.assertRaises(TypeError):
            _ = self.b - r
        with self.assertRaises(TypeError):
            _ =  "self.b" - r

    def test_mul(self):
        """Test __mul__ method.
        """
        ans = self.a * AverageReview(self.b)
        self.assertEqual(ans.score, self.a * self.b)
        ans2 = AverageReview(self.b) * self.a
        self.assertEqual(ans2.score, self.a * self.b)

    def test_mul_with_non_number(self):
        """Test __mul__ method with non review values.
        """
        r = AverageReview(self.a)
        with self.assertRaises(TypeError):
            _ = r * AverageReview(self.b)
        with self.assertRaises(TypeError):
            _ = r * "self.b"
        with self.assertRaises(TypeError):
            _ = AverageReview(self.b) * r
        with self.assertRaises(TypeError):
            _ =  "self.b" * r

    def test_div(self):
        """Test __div__ method.
        """
        ans = AverageReview(self.a) / self.b
        self.assertAlmostEqual(ans.score, self.a / self.b)
        with self.assertRaises(ZeroDivisionError):
            _ = AverageReview(self.a) / 0.

    def test_div_with_non_number(self):
        """Test __div__ method with non review values.
        """
        r = AverageReview(self.a)
        with self.assertRaises(TypeError):
            _ = r / AverageReview(self.b)
        with self.assertRaises(TypeError):
            _ = r / "self.b"

    def test_eq(self):
        """Test __eq__ method.
        """
        self.assertEqual(AverageReview(self.a), AverageReview(self.a))

    def test_neq(self):
        """Test __neq__ method.
        """
        self.assertNotEqual(AverageReview(self.a), AverageReview(self.b))

    def test_eq_with_non_review(self):
        """Test __eq__ method with non review values.
        """
        self.assertNotEqual(AverageReview(self.a), self.a)
        self.assertNotEqual(AverageReview(self.a), "self.a")


class TestAverageSummary(unittest.TestCase):
    """Test case for AverageSummary class.
    """

    def test_create_with_single_value(self):
        """Test __init__method with a single value.
        """
        v = random.random()
        summary = AverageSummary(v)
        self.assertEqual(summary.score, v)

    def test_create_with_single_review(self):
        """Test __init__method with a single review.
        """
        v = random.random()
        summary = AverageSummary(AverageReview(v))
        self.assertEqual(summary.score, v)

    def test_create_with_list(self):
        """Test __init__method with a list.
        """
        l = [random.random() for _ in range(10)]
        summary = AverageSummary(l)
        self.assertEqual(summary.score, np.mean(l))

    def test_create_with_review_list(self):
        """Test __init__method with a review list.
        """
        l = [AverageReview(random.random()) for _ in range(10)]
        summary = AverageSummary(l)
        self.assertEqual(summary.score, np.mean(l).score)

    def test_create_with_iterator(self):
        """Test __init__method with an iterator.
        """
        l = [random.random() for _ in range(10)]
        summary = AverageSummary(iter(l))
        self.assertEqual(summary.score, np.mean(l))

    def test_create_with_review_iterator(self):
        """Test __init__method with an iterator of reviews.
        """
        l = [AverageReview(random.random()) for _ in range(10)]
        summary = AverageSummary(iter(l))
        self.assertEqual(summary.score, np.mean(l).score)

    def test_create_with_wrong_single_value(self):
        """Test __init__method with a non number.
        """
        with self.assertRaises(TypeError):
            _ = AverageSummary("value")

    def test_create_with_wrong_iterative(self):
        """Test __init__method with a non number list.
        """
        with self.assertRaises(TypeError):
            _ = AverageSummary(["v" for _ in range(10)])

    def test_difference(self):
        """Test difference method.
        """
        a = AverageReview(random.random())
        b = AverageReview(random.random())
        s = AverageSummary(a)
        self.assertEqual(s.difference(b), abs(a.score - b.score))

    def test_difference_with_non_review(self):
        """Test difference method with a non review value.
        """
        s = AverageSummary(random.random())
        with self.assertRaises(TypeError):
            _ = s.difference("b")

    def test_review_class(self):
        """Test review_class method.
        """
        self.assertEqual(AverageSummary.review_class(), AverageReview)


if __name__ == "__main__":
    unittest.main()
