#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: sonosaudioservicelib.py
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
Main code for sonosaudioservicelib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
from abc import ABC, abstractmethod

__author__ = '''Jenda Brands <jenda@brnds.eu>'''
__docformat__ = '''google'''
__date__ = '''07-11-2023'''
__copyright__ = '''Copyright 2023, Jenda Brands'''
__credits__ = ["Jenda Brands"]
__license__ = '''MIT'''
__maintainer__ = '''Jenda Brands'''
__email__ = '''<jenda@brnds.eu>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''sonosaudioservicelib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class SonosAudioService(ABC):

    @property
    @abstractmethod
    def channels(self):
        """Should return a list of channels supported by the service."""

    @abstractmethod
    def get_channel_by_id(self, channel_id):
        """Should retrieve a channel by the provided id."""

    @property
    @abstractmethod
    def favorites(self):
        """Should return a list of channels that are marked as favorite."""


class SonosAggregatedAudioService(SonosAudioService):

    @abstractmethod
    def get_channels_by_service_id(self, service_id):
        """Should return a list of Channel objects by its service_id."""

    @property
    @abstractmethod
    def services(self):
        """Should return a list of Service objects."""


class SonosAudioChannel(ABC):

    @property
    @abstractmethod
    def id(self):
        """The id of the channel."""

    @property
    @abstractmethod
    def name(self):
        """The name of the channel."""

    @property
    @abstractmethod
    def media_uri(self):
        """The uri of the media of the channel."""

    @property
    @abstractmethod
    def description(self):
        """The description of the channel."""

    @property
    @abstractmethod
    def logo(self):
        """The logo of the channel."""
