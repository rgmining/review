#
# scalar.py
#
# Copyright (c) 2016 Junpei Kawamoto
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
"""Implementations of scalar review and summary classes.
"""
from __future__ import absolute_import
import numbers
import numpy as np

from review.base import Review
from review.base import Summary


class AverageReview(Review):
    """Scalar review.

    Args:
      v: a float value representing review score.

    The review score is a scalar value.
    """
    __slots__ = ("_v")

    def __init__(self, v):
        """Construct average review class.

        Args:
          v: a float value representing review score.
        """
        if not isinstance(v, numbers.Number):
            raise TypeError("v ({0}) is not a scalar value.".format(type(v)))
        self._v = float(v)

    @property
    def score(self):
        """A float value representing score of this review. """
        return self._v

    def __eq__(self, other):
        if not isinstance(other, AverageReview):
            return False
        return self.score == other.score

    def __add__(self, other):
        if not isinstance(other, AverageReview):
            raise TypeError(
                "other is {0}, not AverageReview".format(type(other)))
        return AverageReview(self.score + other.score)

    def __rmul__(self, other):
        if not isinstance(other, numbers.Number):
            raise TypeError(
                "other is {0}, not numbers.Number".format(type(other)))
        return AverageReview(other * self.score)

    def __str__(self):
        return str(self.score)

    def __hash__(self):
        return hash(self.score)


class AverageSummary(Summary):
    """Scalar summary.

    The summary is an average of given reviews.
    """
    __slots__ = ("_v")  # _v : an instance of AgerageReview

    def __init__(self, scores):
        if hasattr(scores, "__iter__"):
            v = np.mean(list(scores))
            if isinstance(v, AverageReview):
                self._v = v
            else:
                self._v = AverageReview(v)
        elif isinstance(scores, AverageReview):
            self._v = scores
        else:
            self._v = AverageReview(scores)

    def difference(self, r):
        """Difference between this summary and a given review.

        Args:
          r: a review.

        Returns:
          a non-negative float value or 0 representing the difference between
          this summary and the given value.
        """
        if not isinstance(r, AverageReview):
            raise TypeError("r is {0}, not AverageReview".format(type(r)))
        return abs(self._v.score - r.score)

    @property
    def score(self):
        """Float value representing this summary.
        """
        return self._v.score

    @property
    def v(self):
        """Summary score.
        """
        return self._v.score

    def __str__(self):
        return str(self._v)

    @classmethod
    def review_class(cls):
        """A review class associated with this summary. """
        return AverageReview
