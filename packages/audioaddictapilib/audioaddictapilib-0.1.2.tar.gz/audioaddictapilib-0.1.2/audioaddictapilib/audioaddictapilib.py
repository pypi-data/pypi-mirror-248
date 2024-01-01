#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: audioaddictapilib.py
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
Main code for audioaddictapilib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import json
import logging
import time
import urllib.parse
from dataclasses import dataclass
from datetime import datetime

from functools import cached_property

import pytz
import requests
from bs4 import BeautifulSoup as Bfs

from sonosaudioservicelib.sonosaudioservicelib import SonosAudioService, SonosAudioChannel, SonosAggregatedAudioService

from .audioaddictapilibexceptions import (LogoTypeNotSupported,
                                          ServiceNotSupported,
                                          InsufficientCredentials,
                                          AuthenticationError,
                                          InvalidListenKey,
                                          MissingCsrfToken,
                                          MarkerNotFound,
                                          InvalidData)
from .configuration import API_BASE_URL, LISTEN_BASE_URL, LOGO_TYPES, SERVICES

__author__ = '''Jenda Brands <jenda@brnds.eu>'''
__docformat__ = '''google'''
__date__ = '''22-12-2023'''
__copyright__ = '''Copyright 2023, Jenda Brands'''
__credits__ = ["Jenda Brands"]
__license__ = '''MIT'''
__maintainer__ = '''Jenda Brands'''
__email__ = '''<jenda@brnds.eu>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''audioaddictapilib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

# USER_AGENT = 'audioaddictlib'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'


class AggregatedService(SonosAggregatedAudioService):
    def __init__(self, username=None, password=None, listen_key=None, services=None):
        self.username = username
        self.password = password
        self.listen_key = listen_key
        if services is None:
            services = SERVICES
        self._services = self._initialize_services(username=username,
                                                   password=password,
                                                   listen_key=listen_key,
                                                   services=services)

    @staticmethod
    def _initialize_services(username, password, listen_key, services):
        return [Service(service.get('name'),
                        username=username,
                        password=password,
                        listen_key=listen_key) for service in services]

    @cached_property
    def channels(self):
        return [channel for service in self.services for channel in service.channels]

    def get_channel_by_id(self, channel_id):
        return next((channel for channel in self.channels if channel.id == channel_id), None)

    def get_channels_by_service_id(self, service_id):
        return next(
            (channel for service in self.services for channel in service.channels if service.name == service_id), None)

    @cached_property
    def favorites(self):
        return [channel for service in self.services for channel in service.favorites]

    @property
    def services(self):
        return self._services


class Service(SonosAudioService):

    def __init__(self, name, username=None, password=None, listen_key=None,  # pylint: disable=too-many-arguments
                 api_base_url=API_BASE_URL):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')
        self._name = self._validate_name(name)
        self._base_url = f"{api_base_url}/{self.name}"
        self.session = requests.Session()
        self._csrf_token, self._configuration = self._parse_initial_page(self.domain)
        self._listen_key = self._get_listen_key(username, password, listen_key)

    @property
    def authenticated(self):
        return self._configuration.get('user', {}).get('authenticated') if self._configuration.get('user', {}).get(
            'audio_token') else False

    @property
    def got_listenkey(self):
        return bool(self._listen_key)

    @property
    def name(self):
        return self._name.get('name')

    @property
    def display_name(self):
        return self._name.get('display_name')

    @property
    def domain(self):
        return self._name.get('domain')

    @property
    def logo(self):
        return self._name.get('logo_url')

    @property
    def _channel_url_prefix(self):
        return self._name.get('channel_url_prefix', '')

    @property
    def _audio_token(self):
        return self._configuration.get('user', {}).get('audio_token')

    @property
    def _favorites_from_config(self):
        return self._configuration.get('user', {}).get('favorites')

    @cached_property
    def favorites(self):
        return [{'channel': self.get_channel_by_id(channel.get('channel_id')), 'position': channel.get('position')}
                for channel in self._favorites_from_config]

    @property
    def _session_key(self):
        return self._configuration.get('user', {}).get('session_key')

    def _validate_listen_key(self, listen_key):
        # we randomly get the first channel
        url = f'{self.channels[0]._media_uri}?{listen_key}'  # noqa
        try:
            _ = requests.get(url, timeout=0.5)
        except requests.exceptions.ConnectionError as exc:
            if 'Read timed out' in str(exc):
                # if we hit the timeout it means that we are requesting a stream and that the key
                # is valid. In any other case we assume the key to be invalid.
                return listen_key
            self.logger.exception('No time out exception.')
        raise InvalidListenKey(listen_key)

    def _get_listen_key(self, username, password, listen_key):
        if not any([username, password, listen_key]):
            return None
        listen_key = listen_key if listen_key else self.authenticate_for_listen_key(username,
                                                                                    password,
                                                                                    self.domain)
        return self._validate_listen_key(listen_key)

    @staticmethod
    def _parse_configuration_from_source(text):
        start_marker = 'di.app.start('
        # in classicalradio there are channel info that have parentheses which breaks our parsing
        # in order to be sure we target the actual end of the payload we will target the last curly brace also.
        # we need to add the last curly brace back to the parsed payload so it can load properly as json.
        end_marker = '});'
        start = text.find(start_marker)
        if start == -1:
            raise MarkerNotFound(f'Could not find starting marker {start_marker} in text: {text}')
        start = start + len(start_marker)
        end = text.find(end_marker, start)
        if end == -1:
            raise MarkerNotFound(f'Could not find end marker {end_marker} in text: {text}')
        # we add the last curly brace to fix the above matching.
        data = f'{text[start: end]}}}'
        try:
            data = json.loads(data)
        except ValueError as err:
            LOGGER.error('Unable to parse data as json.')
            raise InvalidData(data) from err
        return data

    def _parse_initial_page(self, domain):
        url = f'https://www.{domain}'
        self.session.headers.update({'X-Requested-With': 'XMLHttpRequest', 'User-Agent': USER_AGENT})
        response = self.session.get(url)
        soup = Bfs(response.text, 'html.parser')
        csrf_token = soup.find('meta', {'name': 'csrf-token'}).get('content')
        if not csrf_token:
            raise MissingCsrfToken()
        configuration = Service._parse_configuration_from_source(response.text)
        return csrf_token, configuration

    def authenticate_for_listen_key(self, username, password, domain):
        if not all([username, password]):
            logging.info('Both username and password are required to authenticate.')
            raise InsufficientCredentials()
        payload = {'member_session[username]': username,
                   'member_session[password]': password,
                   'member_session[remember_me]': 1}
        self.session.headers.update({'X-Requested-With': 'XMLHttpRequest', 'User-Agent': USER_AGENT})
        response = self.session.post(url=f'https://www.{domain}/login', data=payload)
        response.raise_for_status()
        if not response.json().get('auth'):
            raise AuthenticationError(response.json().get('errors'))
        self._configuration = self.update_config(domain)
        return response.json().get('listen_key')

    def update_config(self, domain):
        response = self.session.get(url=f'https://www.{domain}/member/profile')
        configuration = self._parse_configuration_from_source(response.text)
        return configuration

    @staticmethod
    def _validate_name(name):
        """Validate whether the supplied brand name is valid.

        Args:
            name: The name to check

        Returns:
            name if valid, raises exception otherwise

        """
        supported_services = [service.get('name') for service in SERVICES]
        if name not in supported_services:
            raise ServiceNotSupported(f"Service name {name} is not in the list of supported services, "
                                      f"{supported_services}")
        return next(service for service in SERVICES if service.get('name') == name)

    @staticmethod
    def _execute_api_request(url, params=None, headers=None):
        params = params or {}
        headers = headers or {}
        headers.update({'User-Agent': USER_AGENT})
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    @cached_property
    def channels(self):
        return [Channel(self, channel) for channel in self._execute_api_request(f"{self._base_url}/channels")]

    def total_channels_number(self):
        return len(self.channels)

    def get_channel_by_id(self, channel_id):
        return next((channel for channel in self.channels if channel.id == channel_id), None)

    def get_channel_by_key(self, key):
        return next((channel for channel in self.channels if channel.key == key), None)


class Channel(SonosAudioChannel):
    def __init__(self, service, data):
        self.service = service
        self._data = data

    @property
    def _authenticated_base_url(self):
        return LISTEN_BASE_URL.format(domain=self.service.domain)

    @property
    def _unauthenticated_base_url(self):
        return f'{API_BASE_URL}/{self.service.name}'

    @property
    def to_json(self):
        return self._data

    @property
    def id(self):
        return int(self._data.get('id'))

    @property
    def key(self):
        return self._data.get('key')

    @property
    def _channel_url_prefix(self):
        return self.service._channel_url_prefix  # noqa

    @property
    def images(self):
        return self._data.get('images')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def name_encoded(self):
        return urllib.parse.quote(self._data.get('name'))

    @property
    def _media_uri(self):
        return f'{self._authenticated_base_url}/{self._channel_url_prefix}{self.key}'

    @property
    def media_uri(self):
        if self.service.got_listenkey:
            return f'{self._media_uri}?{self.service._listen_key}'  # noqa
        return self._get_channel_content()

    @property
    def playlist(self):
        if not self.service.got_listenkey:
            return None
        return (f'https://listen.{self.service.domain}/premium/{self.key}.pls?'
                f'listen_key={self.service._listen_key}')  # noqa

    def _get_channel_content(self):
        url = f'{self._unauthenticated_base_url}/routines/channel/{self.id}'
        params = {'tune_id': 'true',
                  'audio_token': self.service._audio_token,  # noqa
                  '_': int(time.time()) * 1000}
        data = self.service._execute_api_request(url, params=params)  # noqa
        url = data.get('tracks', [{}])[0].get('content', {}).get('assets', [{}])[0].get('url')
        if not url:
            raise InvalidData(f'Could not get content url from data {data}')
        return f'https:{url}'

    @property
    def description(self):
        return self._data.get('description')

    @property
    def description_encoded(self):
        return urllib.parse.quote(self._data.get('description'))

    @property
    def currently_playing(self):
        url = f"{self.service._base_url}/currently_playing"  # noqa
        data = self.service._execute_api_request(url)  # noqa
        channel_data = next((item for item in data if self.id == item['channel_id']), None)
        if channel_data:
            return Track(self, channel_data.get('track'))
        return None

    @property
    def logo(self):
        return self.get_logo_by_type('default')

    def get_logo_by_type(self, logo_type):
        """Returns the URL for the request logo type."""
        try:
            url = self.images[self._validate_logo_type(logo_type)]
            logo = f"http://{url.strip('/').removesuffix('{?size,height,width,quality,pad}')}"
        except KeyError:
            logo = None
        return logo

    @staticmethod
    def _validate_logo_type(logo_type):
        """Validate whether the supplied logo type is valid.

        Args:
            logo_type: The logo type to check

        Returns:
            logo_type is valid, raises exception otherwise

        """
        if logo_type not in LOGO_TYPES:
            raise LogoTypeNotSupported(f"LogoType {logo_type} is not in the list of supported logo types")
        return logo_type


@dataclass
class Artist:
    artist_id: int
    name: str
    asset_url: str
    images: dict


class Track:
    def __init__(self, channel, data):
        self.channel = channel
        self._data = data

    @property
    def title(self):
        return self._data.get('display_title')

    @property
    def to_json(self):
        return self._data

    @staticmethod
    def time_to_datetime(time_):
        return datetime.strptime(time_)

    @property
    def seconds_remaining(self):
        diff = datetime.now(pytz.utc) - datetime.strptime(self._data.get('start_time'), '%Y-%m-%dT%H:%M:%S%z')
        return self._data.get('duration') - float(f"{diff.seconds}.{diff.microseconds}")
