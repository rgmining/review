#
# histogram_test.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
#
# This file is part of rgmining-review.
#
# rgmining-review is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-review is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Unit tests for review.scalar module.
"""
import random
import unittest

import numpy as np

from review.histogram import HistoReview as Review
from review.histogram import HistoSummary as Summary


class TestReview(unittest.TestCase):
    """Test case for AverageReview class.
    """

    def setUp(self):
        """Set up for tests.
        """
        self.a = random.random() * 100
        self.b = random.random() * 100
        while self.b == 0. or round(self.a) == round(self.b):
            self.b = random.random()

    def test_create(self):
        """Test creating a review.
        """
        r = Review(self.a)
        self.assertEqual(r[round(self.a)], 1)

        r2 = Review({self.a: 1, self.b: 2})
        self.assertEqual(r2[round(self.a)], 1)
        self.assertEqual(r2[round(self.b)], 2)

    def test_create_with_non_number(self):
        """Test __init__ method with non numbers.
        """
        with self.assertRaises(TypeError):
            _ = Review("non number")

    def test_add(self):
        """Test __add__ method.
        """
        ans = Review(self.a) + Review(self.b)
        self.assertEqual(ans[round(self.a)], 1)
        self.assertEqual(ans[round(self.b)], 1)
        self.assertEqual(ans.score, round(self.a) + round(self.b))

        ans2 = Review(self.a) + Review(self.a)
        self.assertEqual(ans2[round(self.a)], 2)

    def test_add_with_non_review(self):
        """Test __add__ method with non review values.
        """
        r = Review(self.a)
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
        ans = Review(self.a) - Review(self.b)
        self.assertEqual(ans[round(self.a)], 1)
        self.assertEqual(ans[round(self.b)], -1)
        self.assertEqual(ans.score, round(self.a) - round(self.b))

        ans2 = Review(self.a) - Review(self.a)
        self.assertEqual(ans2[round(self.a)], 0)

    def test_sub_with_non_reivew(self):
        """Test __sub__ method with non review values.
        """
        r = Review(self.a)
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
        ans = self.a * Review(self.b)
        self.assertEqual(ans.score, self.a * round(self.b))
        ans2 = Review(self.b) * self.a
        self.assertEqual(ans2.score, self.a * round(self.b))

    def test_mul_with_non_number(self):
        """Test __mul__ method with non review values.
        """
        r = Review(self.a)
        with self.assertRaises(TypeError):
            _ = r * Review(self.b)
        with self.assertRaises(TypeError):
            _ = r * "self.b"
        with self.assertRaises(TypeError):
            _ = Review(self.b) * r
        with self.assertRaises(TypeError):
            _ =  "self.b" * r

    def test_div(self):
        """Test __div__ method.
        """
        ans = Review(self.a) / self.b
        self.assertAlmostEqual(ans.score, round(self.a) / self.b)
        with self.assertRaises(ZeroDivisionError):
            _ = Review(self.a) / 0.

    def test_div_with_non_number(self):
        """Test __div__ method with non review values.
        """
        r = Review(self.a)
        with self.assertRaises(TypeError):
            _ = r / Review(self.b)
        with self.assertRaises(TypeError):
            _ = r / "self.b"

    def test_eq(self):
        """Test __eq__ method.
        """
        self.assertEqual(Review(self.a), Review(self.a))

    def test_neq(self):
        """Test __neq__ method.
        """
        self.assertNotEqual(Review(self.a), Review(self.b))

    def test_eq_with_non_review(self):
        """Test __eq__ method with non review values.
        """
        self.assertNotEqual(Review(self.a), self.a)
        self.assertNotEqual(Review(self.a), "self.a")

    def test_inner_product(self):
        """Test inner_product method.
        """
        r = Review({self.a: 1, self.b: 2})
        c = random.random() * 100
        r2 = Review({self.a: 1, c: 2})
        ans = r.inner_product(r2)
        if round(self.b) == round(c):
            self.assertEqual(ans, 5)
        else:
            self.assertEqual(ans, 1)


class TestSummary(unittest.TestCase):
    """Test case for AverageSummary class.
    """

    def test_create_with_single_value(self):
        """Test __init__method with a single value.
        """
        v = random.random() * 100
        summary = Summary(v)
        self.assertEqual(summary.score, round(v))

    def test_create_with_single_review(self):
        """Test __init__method with a single review.
        """
        v = random.random() * 100
        summary = Summary(Review(v))
        self.assertEqual(summary.score, round(v))

    def test_create_with_list(self):
        """Test __init__method with a list.
        """
        l = [random.random() * 100 for _ in range(10)]
        summary = Summary(l)
        self.assertAlmostEqual(summary.score, np.mean([round(v) for v in l]))

    def test_create_with_review_list(self):
        """Test __init__method with a review list.
        """
        l = [random.random() * 100 for _ in range(10)]
        summary = Summary([Review(v) for v in l])
        self.assertAlmostEqual(summary.score, np.mean([round(v) for v in l]))

    def test_create_with_iterator(self):
        """Test __init__method with an iterator.
        """
        l = [random.random() * 100 for _ in range(10)]
        summary = Summary(iter(l))
        self.assertAlmostEqual(summary.score, np.mean([round(v) for v in l]))

    def test_create_with_review_iterator(self):
        """Test __init__method with an iterator of reviews.
        """
        l = [random.random() * 100 for _ in range(10)]
        summary = Summary(iter([Review(v) for v in l]))
        self.assertAlmostEqual(summary.score, np.mean([round(v) for v in l]))

    def test_create_with_wrong_single_value(self):
        """Test __init__method with a non number.
        """
        with self.assertRaises(TypeError):
            _ = Summary("value")

    def test_create_with_wrong_iterative(self):
        """Test __init__method with a non number list.
        """
        with self.assertRaises(TypeError):
            _ = Summary(["v" for _ in range(10)])

    def test_difference(self):
        """Test difference method.
        """
        a = random.random() * 100
        b = random.random() * 100
        s = Summary(Review(a))
        ans = s.difference(Review(b))
        if a == b:
            self.assertEqual(ans, 0.)
        else:
            self.assertEqual(ans, 1.)

    def test_difference_with_non_review(self):
        """Test difference method with a non review value.
        """
        s = Summary(random.random())
        with self.assertRaises(TypeError):
            _ = s.difference("b")

    def test_review_class(self):
        """Test review_class method.
        """
        self.assertEqual(Summary.review_class(), Review)


if __name__ == "__main__":
    unittest.main()
