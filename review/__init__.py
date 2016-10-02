"""Review data model consisting of review and summary.

This module defines abstract :class:`review.base.Review` and
:class:`review.base.Summary`, and those implementations.
:class:`review.base.Review` represents review itself and
:class:`review.base.Summary` is a summarized reviews given to a same object.

This module assumes each review is representable in one scalar value,
and those review values are in a multipliable additive group.
With the assumption, this module implements two types of summarization methods.
One of them is average of reviews and the other one is making a vector,
in other words histogram, of reviews.

This module has the following aliases:

- :class:`AverageReview <review.scalar.AverageReview>`
- :class:`AverageSummary <review.scalar.AverageSummary>`
- :class:`HistoReview <review.histogram.HistoReview>`
- :class:`HistoSummary <review.histogram.HistoSummary>`

"""
from __future__ import absolute_import
from review.scalar import AverageReview
from review.scalar import AverageSummary
from review.histogram import HistoReview
from review.histogram import HistoSummary
