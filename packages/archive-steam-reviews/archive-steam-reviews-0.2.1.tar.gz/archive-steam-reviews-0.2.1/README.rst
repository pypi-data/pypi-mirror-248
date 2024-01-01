========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - license
      - |license|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |license| image:: https://img.shields.io/github/license/manuelgrabowski/archive-steam-reviews
    :target: https://github.com/manuelgrabowski/archive-steam-reviews
    :alt: MIT License

.. |version| image:: https://img.shields.io/pypi/v/archive-steam-reviews.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/archive-steam-reviews

.. |wheel| image:: https://img.shields.io/pypi/wheel/archive-steam-reviews.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/archive-steam-reviews

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/archive-steam-reviews.svg
    :alt: Supported versions
    :target: https://pypi.org/project/archive-steam-reviews

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/archive-steam-reviews.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/archive-steam-reviews

.. |commits-since| image:: https://img.shields.io/github/commits-since/manuelgrabowski/archive-steam-reviews/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/manuelgrabowski/archive-steam-reviews/compare/v0.1.0...main



.. end-badges

Scrape all Steam reviews from a specific profile

This script uses BeautifulSoup to do some very basic web-scraping and retrieve the reviews for a given user account. The profile must be set to public visibility.

* Free software: MIT license

Installation
============

::

    pip install archive-steam-reviews


Usage
=====

By default it will only retrieve the first page of reviews, and print to stdout. As the review page is sorted by most recently changed, usually the ``--all`` switch is only be needed for an initial dump of all existing reviews. If more than ten reviews are published and/or edited between running the script, the parameter is needed to get all changes.

When using ``--save``\ , each review will be stored in a text file named with the `Steam App ID <https://steamdb.info/apps/>`_ the review is for (unfortunately the game name itself is not available for scraping without an additional request). The file will have a `YAML frontmatter <https://gohugo.io/content-management/front-matter/>`_ with some metadata (Steam URL, playtime, date of review, …) and the review (converted to Markdown) as the post body. As such, it is ready for use in `Hugo <https://gohugo.io/>`_\ , similar static site generators or other purposes.


