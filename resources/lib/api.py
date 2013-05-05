#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import requests


API_URL = '%(scheme)s://api.jamendo.com/v3.0/'
USER_AGENT = 'XBMC Jamendo API'
SORT_METHODS = {
    'albums': (
        'releasedate_desc', 'releasedate_asc', 'popularity_total',
        'popularity_month', 'popularity_week'
    ),
    'artists': (
        'name', 'joindate_asc', 'joindate_desc', 'popularity_total',
        'popularity_month', 'popularity_week'
    ),
    'tracks': (
        'buzzrate', 'downloads_week', 'downloads_month', 'downloads_total',
        'listens_week', 'listens_month', 'listens_total', 'popularity_week',
        'popularity_month', 'popularity_total', 'releasedate_asc',
        'releasedate_desc'
    ),
}
AUDIO_FORMATS = {
    'mp3': 'mp32',
    'ogg': 'ogg',
    'flac': 'flac'
}


class AuthError(Exception):
    pass


class ApiError(Exception):
    pass


class ConnectionError(Exception):
    pass


class JamendoApi():

    def __init__(self, client_id, use_https=True, limit=100,
                 audioformat=None):
        self._client_id = client_id
        self._use_https = bool(use_https)
        self._audioformat = AUDIO_FORMATS.get(audioformat, 'mp32')
        self._limit = min(int(limit), 100)

    def get_albums(self, page=1, artist_id=None, sort_method=None,
                   search_terms=None):
        path = 'albums'
        params = {
            'imagesize': 400,
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1),
        }
        if artist_id:
            params['artist_id'] = [artist_id]
        if sort_method:
            params['order'] = sort_method
        if search_terms:
            params['namesearch'] = search_terms
        albums = self._api_call(path, params)
        return albums

    def get_playlists(self, page=1, search_terms=None):
        path = 'playlists'
        params = {
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1)
        }
        if search_terms:
            params['namesearch'] = search_terms
        playlists = self._api_call(path, params)
        return playlists

    def get_artists(self, page=1, sort_method=None, search_terms=None):
        path = 'artists'
        params = {
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1),
        }
        if sort_method:
            params['order'] = sort_method
        if search_terms:
            params['namesearch'] = search_terms
        artists = self._api_call(path, params)
        return artists

    def get_tracks(self, page=1, sort_method=None, filter_dict=None,
                   audioformat=None):
        path = 'tracks'
        params = {
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1),
            'include': 'musicinfo',
            'audioformat': AUDIO_FORMATS.get(audioformat) or self._audioformat,
        }
        if sort_method:
            params['order'] = sort_method
        if filter_dict:
            params.update(filter_dict)
        tracks = self._api_call(path, params)
        return tracks

    def get_radios(self, page=1):
        path = 'radios'
        params = {
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1),
            'imagesize': 150,
            'type': 'www'
        }
        radios = self._api_call(path, params)
        return radios

    def get_playlist_tracks(self, playlist_id):
        path = 'playlists/tracks'
        params = {'id': [playlist_id]}
        playlists = self._api_call(path, params)
        playlist = playlists[0] if playlists else {}
        tracks = playlist.get('tracks', [])
        return playlist, tracks

    def get_similar_tracks(self, track_id, page=1):
        path = 'tracks/similar'
        params = {
            'id': track_id,
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1),
            'imagesize': 400,
        }
        tracks = self._api_call(path, params)
        return tracks

    def search_tracks(self, search_terms, page=1):
        filter_dict = {
            'search': search_terms
        }
        return self.get_tracks(page=page, filter_dict=filter_dict)

    def get_track(self, track_id, audioformat=None):
        tracks = self.get_tracks(
            filter_dict={'id': track_id}, audioformat=audioformat
        )
        return tracks[0]

    def get_track_url(self, track_id, audioformat=None):
        path = 'tracks/file'
        params = {
            'audioformat': AUDIO_FORMATS.get(audioformat) or self._audioformat,
            'id': track_id
        }
        track_url = self._get_redirect_location(path, params)
        self.log('get_track_url track_url: %s' % track_url)
        return track_url

    def get_radio_url(self, radio_id):
        path = 'radios/stream'
        params = {
            'id': radio_id
        }
        radios = self._api_call(path, params)
        radio = radios[0] if radios else {}
        return radio.get('stream')

    def _get_redirect_location(self, path, params={}):
        headers = {
            'user-agent': USER_AGENT
        }
        params.update({
            'client_id': self._client_id,
        })
        request = requests.get(
            self._api_url + path,
            headers=headers,
            params=params,
            verify=False,
            allow_redirects=False
        )
        return request.headers['Location']

    def _api_call(self, path, params={}):
        headers = {
            'content-type': 'application/json',
            'user-agent': USER_AGENT
        }
        params.update({
            'client_id': self._client_id,
            'format': 'json'
        })
        request = requests.get(
            self._api_url + path,
            headers=headers,
            params=params,
            verify=False  # XBMCs requests' SSL certificates are too old
        )
        self.log(u'_api_call using URL: %s' % request.url)
        json_data = request.json()
        return_code = json_data.get('headers', {}).get('code')
        if not return_code == 0:
            if return_code == 5:
                raise AuthError(json_data['headers']['error_message'])
            else:
                raise ApiError(json_data['headers']['error_message'])
        if json_data.get('headers', {}).get('warnings'):
            self.log('API-Warning: %s' % json_data['headers']['warnings'])
        self.log(u'_api_call got %d bytes response' % len(request.text))
        return json_data.get('results', [])

    @property
    def current_limit(self):
        return self._limit

    @property
    def _api_url(self):
        scheme = 'https' if self._use_https else 'http'
        return API_URL % {'scheme': scheme}

    @staticmethod
    def get_sort_methods(entity):
        return SORT_METHODS.get(entity, [])

    def log(self, message):
        print u'[%s]: %s' % (self.__class__.__name__, repr(message))
