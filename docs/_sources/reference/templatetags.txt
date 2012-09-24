=========================
Template Tags and Filters
=========================

.. contents::
   :local:

add_qs_param
============

**Usage:** ``{% add_qs_param url varname value %}``

This tag intelligently adds or replaces the query string parameter ``varname`` and assigns it ``value``.

``url``, ``varname``, and ``value`` can be static values or variables

Examples
--------

**Adding a single query string parameter**

.. code-block:: django

    {% add_qs_param http://example.com/ q 1 %}

generates::

    http://example.com/?q=1

**Adding a query string parameter to a URL with a query string.**

.. code-block:: django

    {% add_qs_param http://example.com/?sort=asc q 1 %}

generates::

    http://example.com/?sort=asc&q=1

**Adding a query string parameter to a URL that already has that parameter.**

.. code-block:: django

    {% add_qs_param http://example.com/?q=5 q 1 %}

generates::

    http://example.com/?q=1

**Adding a query string parameter to a URL that has a page fragment.**

.. code-block:: django

    {% add_qs_param http://example.com/#gohere q 1 %}

generates::

    http://example.com/?q=1#gohere

add_fragment
============

**Usage:** ``{{ url|add_fragment:variable }}`` or ``{{ url|add_fragment:"fragment" }}``

This tag intelligently adds or replaces the URL fragment. You can pass a variable as the parameter to ``add_fragment`` or a static value. You must quote static values.

Example
-------

.. code-block:: django

    {{ url|add_fragment:"gohere" }}

generates::

    http://example.com/#gohere


absurl
======

Just like Django's `url tag`_ but adds the domain of the current site.

.. _url tag: https://docs.djangoproject.com/en/1.4/ref/templates/builtins/#url

link
====

**Usage:** ``{{ object|link }}``

Outputs the object in a anchor tag which is the equivalent of ``<a href="{{ object.get_absolute_url }}">{{ object }}</a>``
