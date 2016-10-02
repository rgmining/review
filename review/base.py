#
# base.py
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
"""Defines abstract Review and Summary classes.
"""
import math
import numbers


class _ImmutableAdditiveGroup(object):
    """Immutable additive group.

    Subclass must implement __add__, __neg__, and __eq__, then this class
    complements __sub__ and __ne__.
    """
    __slots__ = ()

    def __add__(self, _):
        raise NotImplementedError("Subclasses must implement __add__.")

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        raise NotImplementedError("Subclasses must implement __neg__.")

    def __eq__(self, _):
        raise NotImplementedError("Subclasses must implement __eq__.")

    def __ne__(self, other):
        return not self == other


class _MultipliableImmutableAdditiveGroup(_ImmutableAdditiveGroup):
    """Multipliable immutable additive group.

    This is a subclass of _ImmutableAdditiveGroup.
    Subclass must implement __add__, __rmul__, and __eq__, then this class
    complements __div__ and __neg__.
    """
    __slots__ = ()

    def __rmul__(self, _):
        # value must be a number.
        raise NotImplementedError("Subclasses must implement __rmul__")

    def __div__(self, value):
        return self.__truediv__(value)

    def __truediv__(self, value):
        if not isinstance(value, numbers.Number):
            raise TypeError("value must be an instance of numbers.Number")
        return (1. / value) * self

    def __floordiv__(self, value):
        if not isinstance(value, numbers.Number):
            raise TypeError("value must be an instance of numbers.Number")
        return math.floor((1. / value) * self)

    def __neg__(self):
        return -1 * self


class Review(_MultipliableImmutableAdditiveGroup):
    """Abstruct class of Review.

    Review is defined on a multipliable immutable additive group.
    Subclass must implement the following methods;

    - _eq_:
    - _add_:
    - _rmul_:

    Review also needs to implement a property `score` to return the review
    score itselt. The returned score must be a float number.
    """
    __slots__ = ()

    def __mul__(self, other):
        return self.__rmul__(other)

    @property
    def score(self):
        """A float value representing score of this review. """
        raise NotImplementedError


class Summary(object):
    """ Abstract class of summary of reviews.

    Summary only needs to define `differenct` and `norm` methods.
    `difference` computes difference between a summary and a review.
    `norm` maps a summary to a float value.

    Each summary type might be related to a review type.
    Summary must implements a class method `review_class` to return the
    associated review class.
    """
    __slots__ = ()

    def difference(self, r):
        """Compute a difference between this summary and a given review score.

        Args:
          An instance of Review.

        Returns:
          The difference between of the summary and the given review.
        """
        raise NotImplementedError

    @property
    def score(self):
        """Return a float value representing this summary.
        """
        raise NotImplementedError

    @classmethod
    def review_class(cls):
        """A review class associated with this summary. """
        raise NotImplementedError
