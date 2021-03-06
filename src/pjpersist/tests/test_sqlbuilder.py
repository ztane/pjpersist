##############################################################################
#
# Copyright (c) 2011 Zope Foundation and Contributors.
# Copyright (c) 2014 Shoobx, Inc.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import doctest
import unittest

from pjpersist import testing, sqlbuilder as sb


def run(expr):
    return expr.__sqlrepr__('postgres')


def doctest_sqlbuilder():
    r"""We have functions that correspond to the JSON operators:

        >>> run(sb.Select(
        ...         sb.JSON_GETITEM(sb.table.stakeholder.data, "address")))
        "SELECT ((stakeholder.data) -> ('address')) FROM stakeholder"

        >>> run(sb.JSON_GETITEM_TEXT(sb.table.person.data, "address"))
        "((person.data) ->> ('address'))"

        >>> run(sb.JSON_PATH(sb.table.person.data,
        ...                  ["address", "zip"]))
        "((person.data) #> (array['address', 'zip']))"

        >>> run(sb.JSON_PATH_TEXT(sb.table.person.data,
        ...                       ["address", "zip"]))
        "((person.data) #>> (array['address', 'zip']))"

    We can cast JSON strings to the JSONB type:

        >>> print run(sb.JSONB('{"universe": {"answer": 42}}'))
        '{"universe": {"answer": 42}}'::jsonb

    And perform JSONB "set operations" on the objects:

        >>> run(sb.JSONB_SUBSET(
        ...     sb.JSONB('{"address": {"zip": 22401}}'),
        ...     sb.table.Frob.data))
        '((\'{"address": {"zip": 22401}}\'::jsonb) <@ (Frob.data))'

        >>> run(sb.JSONB_SUPERSET(
        ...     sb.table.Frob.data,
        ...     sb.JSONB('{"address": {"zip": 22401}}')))
        '((Frob.data) @> (\'{"address": {"zip": 22401}}\'::jsonb))'

    Arrays work only on Postgres:

        >>> sb.JSON_PATH(sb.table.person.data,
        ...                  ["address", "zip"]).__sqlrepr__('sqlite')
        Traceback (most recent call last):
          ...
        AssertionError: Postgres-specific feature, sorry.

    """


def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite(
            optionflags=testing.OPTIONFLAGS),
        doctest.DocTestSuite(
            module=sb,
            optionflags=testing.OPTIONFLAGS),
        ])
