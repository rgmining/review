Review data structure for Review Graph Mining
=============================================

|GPLv3| |Build Status| |wercker status|\ |Code Climate| |Release|

This package defines a data structure of review data. We assume review
data consist of reviews and summaries. A review is a set of information
a user posts to a product. On the other hand, a summary is computed from
a set of reviews.

This package defines two types of reviews and those summaries; scalar
review and vector review.

See `documents <https://rgmining.github.io/review/>`__ for more
information.

Installation
------------

Use ``pip`` to install this package.

.. code:: shell

    pip install --upgrade rgmining-review

License
-------

This software is released under The GNU General Public License Version
3, see `COPYING <COPYING>`__ for more detail.

.. |GPLv3| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://www.gnu.org/copyleft/gpl.html
.. |Build Status| image:: https://travis-ci.org/rgmining/review.svg?branch=master
   :target: https://travis-ci.org/rgmining/review
.. |wercker status| image:: https://app.wercker.com/status/afc19091fbf86b8e5888486c638ac05a/s/master
   :target: https://app.wercker.com/project/byKey/afc19091fbf86b8e5888486c638ac05a
.. |Code Climate| image:: https://codeclimate.com/github/rgmining/review/badges/gpa.svg
   :target: https://codeclimate.com/github/rgmining/review
.. |Release| image:: https://img.shields.io/badge/release-0.9.3-brightgreen.svg
   :target: https://github.com/rgmining/review/releases/tag/v0.9.3
