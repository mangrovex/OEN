#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from math import sqrt
from decimal import Decimal


def round_sie(data, digits):
    if digits == u'4':
        x = (float(data) * 10000) + 0.5
        result = int(float(str(x))) / 10000.0
    elif digits == u'5':
        x = (float(data) * 100000) + 0.5
        result = int(float(str(x))) / 100000.0
    elif digits == u'6':
        x = (float(data) * 1000000) + 0.5
        result = int(float(str(x))) / 1000000.0
    elif digits == u'7':
        x = (float(data) * 10000000) + 0.5
        result = int(float(str(x))) / 10000000.0
    elif digits == u'9':
        x = (float(data) * 1000000000) + 0.5
        result = int(float(str(x))) / 1000000000.0
    else:
        x = (float(data) * 1000) + 0.5
        result = int(float(str(x))) / 1000.0
    return result


def format_sie(data, digits):
    if digits == u'4':
        result = str("%.4f" % data)
    elif digits == u'5':
        result = str("%.5f" % data)
    elif digits == u'6':
        result = str("%.6f" % data)
    else:
        result = str("%.3f" % data)
    return result


def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        result = "---"
    else:
        result = sum(data) / Decimal(n)
    return result


def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x - c) ** 2 for x in data)
    return ss


def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        result = "---"
    else:
        ss = _ss(data)
        pvar = ss / n  # the population variance
        result = sqrt(pvar)
    return result


def get_elements(data):
    size = len(data)
    elements = [i for i in range(size - 1)]
    z = 0
    for row in data:
        longitude = len(row)
        if data.index(row) != 0:
            if row[longitude - 2] == '--':
                elements[z] = Decimal('0.0')
            else:
                elements[z] = Decimal(row[longitude - 2])
            z += 1
    return elements
