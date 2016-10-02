#
# histogram.py
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
"""Implementations of histogram review and summary classes.
"""
from __future__ import absolute_import
from collections import defaultdict
import numbers

import numpy as np

from review.base import Review
from review.base import Summary


class HistoReview(Review):
    """Vector Review.
    """
    __slots__ = ("_v")

    def __init__(self, v, quantizer=round):
        self._v = {}
        if isinstance(v, dict):
            for key, value in v.items():
                self._v[quantizer(key)] = float(value)
        else:
            self._v[quantizer(v)] = 1.

    @property
    def score(self):
        """A float value representing score of this review. """
        res = 0.
        for k in self:
            res += k * self[k]
        return res

    @property
    def vector(self):
        """ Raw vector.
        """
        return self._v

    def norm(self):
        """ 1-Norm of this vector.
        """
        return sum(self._v.values(), 0.)

    def inner_product(self, other):
        """ Inner product of two vectors.

        Args:
          other: a HistogramReview instance.

        Returns:
          the inner product between this and the other.
        """
        if not isinstance(other, HistoReview):
            raise TypeError(
                "other must be an HistoReview: {0}".format(type(other)))
        res = 0.
        for k in set(self.vector.keys()) & set(other.vector.keys()):
            res += self.vector[k] * other.vector[k]
        return res

    def __eq__(self, other):
        if not isinstance(other, HistoReview):
            return False
        if self.vector.keys() != other.vector.keys():
            return False
        for k in self:
            if self[k] != other[k]:
                return False
        return True

    def __add__(self, other):
        if not isinstance(other, HistoReview):
            raise TypeError(
                "other is {0}, not HistoReview".format(type(other)))
        res = defaultdict(float, self._v)
        for k in other:
            res[k] += other[k]
        return HistoReview(res)

    def __rmul__(self, other):
        if not isinstance(other, numbers.Number):
            raise TypeError("other is {0}, not a number".format(type(other)))
        res = self._v.copy()
        for k in res:
            res[k] *= other
        return HistoReview(res)

    def __getitem__(self, key):
        return self._v[key]

    def __iter__(self):
        return self._v.__iter__()

    def __contains__(self, v):
        return v in self._v

    def __str__(self):
        return ", ".join(["{0}:{1}".format(i, self[i]) for i in self])


class HistoSummary(Summary):
    """ Vector summary.
    """
    __slots__ = ("_histo")  # _histo: an instance of HistoReview

    def __init__(self, reviews):
        if hasattr(reviews, "__iter__"):
            reviews = list(reviews)
            if not isinstance(reviews[0], HistoReview):
                reviews = [HistoReview(r) for r in reviews]
            self._histo = np.mean(reviews)
        elif isinstance(reviews, HistoReview):
            self._histo = reviews
        else:
            self._histo = HistoReview(reviews)

    def difference(self, r):
        """Compute a difference between this summary and a given review score.

        Args:
          An instance of Review.

        Returns:
          The difference between of the summary and the given review.
        """
        if not isinstance(r, HistoReview):
            raise TypeError("r must be an HistoReview: {0}".format(type(r)))
        return abs(1 - self._histo.inner_product(r))

    @property
    def score(self):
        """Return a float value representing this summary.
        """
        return self._histo.score

    def __str__(self):
        return ", ".join(["{0}:{1}".format(i, self._histo[i]) for i in self._histo])

    @classmethod
    def review_class(cls):
        """A review class associated with this summary. """
        return HistoReview
