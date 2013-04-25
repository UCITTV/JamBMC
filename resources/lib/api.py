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

import json
import requests


API_URL = 'api.jamendo.com/v3.0/'
USER_AGENT = 'XBMC Jamendo API'


class AuthenticationError(Exception):
    pass


class ConnectionError(Exception):
    pass


class JamendoApi():

    def __init__(self, client_id, **properties):
        self._client_id = client_id
        self._reset_properties()
        if properties:
            self.set_properties(**properties)

    def _reset_properties(self):
        self._username = None
        self._password = None
        self._use_https = False
        self._audioformat = 'ogg'  # fixme
        self._limit = 100

    def set_properties(self, username=None, password=None, use_https=True,
                       limit=100, audioformat='ogg'):
        self._username = username
        self._password = password
        self._use_https = use_https
        self._audioformat = audioformat
        self._limit = limit

    def get_albums(self, page=1, artist_id=None):
        path = 'albums'
        params = {
            'imagesize': 400,
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1)
        }
        if artist_id:
            params['artist_id'] = [artist_id]
        albums = self._api_call(path, params).get('results', [])
        return albums

    def get_artists(self, page=1):
        path = 'artists'
        params = {
            'limit': self._limit,
            'offset': self._limit * (int(page) - 1)
        }
        artists = self._api_call(path, params).get('results', [])
        return artists

    def get_album_tracks(self, album_id):
        path = 'albums/tracks'
        params = {'id': [album_id]}
        albums = self._api_call(path, params).get('results', [])
        album = albums[0] if albums else {}
        tracks = album.get('tracks', [])
        return album, tracks

    def get_track_url(self, track_id):
        path = 'tracks/file'
        params = {
            'audioformat': self._audioformat,
            'id': track_id
        }
        target_url = self._api_head(path, params)
        log('get_track_url target_url: %s' % target_url)
        return target_url

    def _api_head(self, path, params={}):
        headers = {
            'user-agent': USER_AGENT
        }
        params.update({
            'client_id': self._client_id,
        })
        url = self._api_url + path
        request = requests.get(url, headers=headers, params=params)
        return request.url

    def _api_call(self, path, params={}, post={}, auth=False):
        headers = {
            'content-type': 'application/json',
            'user-agent': USER_AGENT
        }
        params.update({
            'client_id': self._client_id,
            'format': 'json'
        })
        url = self._api_url + path
        data = json.dumps(post) if post else None
        method = 'POST' if post else 'GET'
        request = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data
        )
        self.log(u'_api_call using URL: %s' % request.url)
        json_data = request.json()
        return_code = json_data.get('headers', {}).get('code')
        if not return_code == 0:
            if return_code == 5:
                raise AuthenticationError()
            else:
                raise Exception
            if json_data.get('headers'):
                pass
        self.log(u'_api_call got %d bytes response' % len(request.text))
        return json_data

    @property
    def current_limit(self):
        return self._limit

    @property
    def _api_url(self):
        scheme = 'https' if self._use_https else 'http'
        return '%s://%s' % (scheme, API_URL)

    def log(self, message):
        print u'[%s]: %s' % (self.__class__.__name__, repr(message))


def test():
    api = JamendoApi(client_id='b6747d04')
    #print api.get_albums()
    print api.get_album_tracks(174)


if __name__ == '__main__':
    test()
