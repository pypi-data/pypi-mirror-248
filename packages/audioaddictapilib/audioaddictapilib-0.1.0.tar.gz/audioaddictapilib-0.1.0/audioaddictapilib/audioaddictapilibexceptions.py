#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: audioaddictapilibexceptions.py
#
# Copyright 2023 Jenda Brands
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Custom exception code for audioaddictapilib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

__author__ = '''Jenda Brands <jenda@brnds.eu>'''
__docformat__ = '''google'''
__date__ = '''22-12-2023'''
__copyright__ = '''Copyright 2023, Jenda Brands'''
__credits__ = ["Jenda Brands"]
__license__ = '''MIT'''
__maintainer__ = '''Jenda Brands'''
__email__ = '''<jenda@brnds.eu>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


class ServiceNotSupportedError(Exception):
    """Provided service is not supported in this library."""


class LogoTypeNotSupported(Exception):
    """Provided logo type is not supported in this library."""


class NoLogoException(Exception):
    """Channel object has no logo."""


class ServiceNotSupported(Exception):
    """Provided Brand is not supported."""


class MissingCredentials(Exception):
    """No credentials provided."""


class NoListenKey(Exception):
    """No listen key could be found."""


class InsufficientCredentials(Exception):
    """Both username and password are required."""


class AuthenticationError(Exception):
    """Unable to authenticate."""


class InvalidListenKey(Exception):
    """The listen key is invalid."""


class MissingCsrfToken(Exception):
    """The CSRF token is missing from the initial page, something is wrong with the authentication flow."""


class MarkerNotFound(Exception):
    """The marker for the configuration was not found in the source of the page."""


class InvalidData(Exception):
    """The data parsed is not valid json data."""
