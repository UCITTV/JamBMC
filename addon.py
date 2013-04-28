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

from xbmcswift2 import Plugin, xbmc, xbmcgui, NotFoundException
from resources.lib.api import JamendoApi

# TODO
# Add Fanart
# Add Tag search
# Add search
# Add login/favorites
# Translation

STRINGS = {
    # Root menu entries

    # Context menu
    'addon_settings': 30100,

    # Dialogs

    # Error dialogs
    'connection_error': 30120,
    'wrong_credentials': 30121,
    'want_set_now': 30122,
    # Noticications

    # Help Dialog

}


class Plugin_patched(Plugin):

    def _dispatch(self, path):
        for rule in self._routes:
            try:
                view_func, items = rule.match(path)
            except NotFoundException:
                continue
            self._request.view = view_func.__name__  # added
            self._request.view_params = items  # added
            listitems = view_func(**items)
            if not self._end_of_directory and self.handle >= 0:
                if listitems is None:
                    self.finish(succeeded=False)
                else:
                    listitems = self.finish(listitems)
            return listitems
        raise NotFoundException('No matching view found for %s' % path)


plugin = Plugin_patched()
api = JamendoApi(client_id='b6747d04')


@plugin.route('/')
def show_root():
    items = [
        {'label': _('show_albums'),
         'path': plugin.url_for(endpoint='show_albums')},
        {'label': _('show_artists'),
         'path': plugin.url_for(endpoint='show_artists')},
        {'label': _('show_radios'),
         'path': plugin.url_for(endpoint='show_radios')},
        {'label': _('show_playlists'),
         'path': plugin.url_for(endpoint='show_playlists')},
    ]
    return plugin.finish(items)


@plugin.route('/albums/<artist_id>/', name='show_albums_by_artist')
@plugin.route('/albums/')
def show_albums(artist_id=None):
    plugin.set_content('albums')

    page = int(args_get('page', 1))
    albums = api.get_albums(page=page, artist_id=artist_id)

    items = [{
        'label': '%s - %s' % (album['artist_name'], album['name']),
        'info': {
            'count': i,
            'artist': album['artist_name'],
            'album': album['name'],
            'year': int(album.get('releasedate', '0-0-0').split('-')[0]),
        },
        'context_menu': album_context_menu(
            artist_id=album['artist_id'],
            album_id=album['id'],
        ),
        'replace_context_menu': True,
        'thumbnail': album['image'],
        'path': plugin.url_for(
            endpoint='show_tracks_in_album',
            album_id=album['id']
        )
    } for i, album in enumerate(albums)]

    return add_items_paginated(items)


@plugin.route('/playlists/')
def show_playlists():
    plugin.set_content('music')

    page = int(args_get('page', 1))
    playlists = api.get_playlists(page=page)

    items = [{
        'label': '%s (%s)' % (playlist['name'], playlist['user_name']),
        'info': {
            'count': i,
            'artist': playlist['user_name'],
            'album': playlist['name'],
            'year': int(playlist.get('creationdate', '0-0-0').split('-')[0]),
        },
        'context_menu': playlist_context_menu(),
        'replace_context_menu': True,
        'path': plugin.url_for(
            endpoint='show_tracks_in_playlist',
            playlist_id=playlist['id']
        )
    } for i, playlist in enumerate(playlists)]

    return add_items_paginated(items)


@plugin.route('/artists/')
def show_artists():
    plugin.set_content('artists')

    page = int(args_get('page', 1))
    artists = api.get_artists(page=page)

    items = [{
        'label': artist['name'],
        'info': {
            'count': i,
            'artist': artist['name'],
        },
        'context_menu': artist_context_menu(artist['id']),
        'replace_context_menu': True,
        'thumbnail': image_helper(artist['image']),
        'path': plugin.url_for(
            endpoint='show_albums_by_artist',
            artist_id=artist['id'],
        )
    } for i, artist in enumerate(artists)]

    return add_items_paginated(items)


@plugin.route('/radios/')
def show_radios():
    plugin.set_content('music')

    page = int(args_get('page', 1))
    radios = api.get_radios(page=page)

    items = [{
        'label': radio['dispname'],
        'info': {
            'count': i,
        },
        'context_menu': radio_context_menu(),
        'replace_context_menu': True,
        'thumbnail': radio['image'],
        'is_playable': True,
        'path': plugin.url_for(
            endpoint='play_radio',
            radio_id=radio['id'],
        )
    } for i, radio in enumerate(radios)]

    return add_items_paginated(items)


@plugin.route('/tracks/album/<album_id>/')
def show_tracks_in_album(album_id):
    plugin.set_content('songs')

    album, tracks = api.get_album_tracks(album_id=album_id)

    items = [{
        'label': '%s - %s' % (album['artist_name'], track['name']),
        'info': {
            'count': i,
            'tracknumber': i + 1,
            'duration': track['duration'],
            'artist': album['artist_name'],
            'album': album['name'],
            'year': int(album.get('releasedate', '0-0-0').split('-')[0]),
        },
        'context_menu': track_context_menu(
            artist_id=album['artist_id'],
            track_id=track['id'],
            album_id=album['id']
        ),
        'replace_context_menu': True,
        'is_playable': True,
        'thumbnail': album['image'],
        'path': plugin.url_for(
            endpoint='play_song',
            track_id=track['id']
        )
    } for i, track in enumerate(tracks)]

    return add_items_paginated(items)


@plugin.route('/tracks/playlist/<playlist_id>/')
def show_tracks_in_playlist(playlist_id):
    plugin.set_content('songs')

    playlist, tracks = api.get_playlist_tracks(playlist_id=playlist_id)

    items = [{
        'label': track['name'],
        'info': {
            'count': i,
            'tracknumber': int(track['position']),
            'duration': track['duration'],
            'playlist': playlist['name'],
        },
        'context_menu': track_context_menu(
            artist_id=track['artist_id'],
            track_id=track['id'],
            album_id=track['album_id'],
        ),
        'replace_context_menu': True,
        'is_playable': True,
        'path': plugin.url_for(
            endpoint='play_song',
            track_id=track['id']
        )
    } for i, track in enumerate(tracks)]

    return add_items_paginated(items)


@plugin.route('/tracks/similar/<track_id>/')
def show_similar_tracks(track_id):
    plugin.set_content('songs')

    page = int(args_get('page', 1))
    tracks = api.get_similar_tracks(track_id=track_id, page=page)

    items = [{
        'label': '%s - %s (%s)' % (
            track['artist_name'],
            track['name'],
            track['album_name']
        ),
        'info': {
            'count': i,
            'tracknumber': i + 1,
            'duration': track['duration'],
            'artist': track['artist_name'],
            'track': track['name'],
            'year': int(track.get('releasedate', '0-0-0').split('-')[0]),
        },
        'context_menu': track_context_menu(
            artist_id=track['artist_id'],
            track_id=track['id'],
            album_id=track['album_id']
        ),
        'replace_context_menu': True,
        'is_playable': True,
        'thumbnail': track['album_image'],
        'path': plugin.url_for(
            endpoint='play_song',
            track_id=track['id']
        )
    } for i, track in enumerate(tracks)]

    return add_items_paginated(items)


@plugin.route('/play/track/<track_id>')
def play_song(track_id):
    stream_url = api.get_track_url(track_id)
    return plugin.set_resolved_url(stream_url)


@plugin.route('/play/radio/<radio_id>')
def play_radio(radio_id):
    stream_url = api.get_radio_url(radio_id)
    return plugin.set_resolved_url(stream_url)


@plugin.route('/settings')
def open_settings():
    plugin.open_settings()


def add_items_paginated(items):
    page = int(args_get('page', 1))
    is_update = 'is_update' in plugin.request.args
    has_next_page = len(items) == api.current_limit
    has_previous_page = page > 1

    if has_next_page:
        next_page = int(page) + 1
        items.append({
            'label': '>> %s %d >>' % (_('page'), next_page),
            'path': plugin.url_for(
                endpoint=plugin.request.view,
                is_update='true',
                **dict(plugin.request.view_params, page=next_page)
            )
        })

    if has_previous_page:
        previous_page = int(page) - 1
        items.insert(0, {
            'label': '<< %s %d <<' % (_('page'), previous_page),
            'path': plugin.url_for(
                endpoint=plugin.request.view,
                is_update='true',
                **dict(plugin.request.view_params, page=previous_page)
            )
        })

    finish_kwargs = {
        'update_listing': is_update
    }
    if plugin.get_setting('force_viewmode', bool):
        finish_kwargs['view_mode'] = 'thumbnail'
    return plugin.finish(items, **finish_kwargs)


def radio_context_menu():
    return [
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def playlist_context_menu():
    return [
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def album_context_menu(artist_id, album_id):
    return [
        (_('album_info'),
         _action('info')),
        (_('all_tracks_in_this_album'),
         _view(endpoint='show_tracks_in_album',
               album_id=album_id)),
        (_('all_albums_by_this_artist'),
         _view(endpoint='show_albums_by_artist',
               artist_id=artist_id)),
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def artist_context_menu(artist_id):
    return [
        (_('all_albums_by_this_artist'),
         _view(endpoint='show_albums_by_artist',
               artist_id=artist_id)),
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def track_context_menu(artist_id, track_id, album_id):
    return [
        (_('song_info'),
         _action('info')),
        (_('all_albums_by_this_artist'),
         _view(endpoint='show_albums_by_artist',
               artist_id=artist_id)),
        (_('show_similar_tracks'),
         _view(endpoint='show_similar_tracks',
               track_id=track_id)),
        (_('all_tracks_in_this_album'),
         _view(endpoint='show_tracks_in_album',
               album_id=album_id)),
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def _run(*args, **kwargs):
    return 'XBMC.RunPlugin(%s)' % plugin.url_for(*args, **kwargs)


def _view(*args, **kwargs):
    return 'XBMC.Container.Update(%s)' % plugin.url_for(*args, **kwargs)


def _action(arg):
    return 'XBMC.Action(%s)' % arg


def args_get(arg_name, default=None):
    return plugin.request.args.get('page', [default])[0]


def image_helper(url):
    if url:
        # fix whitespace in some image urls
        return url.replace(' ', '%20')
    else:
        addon_id = plugin._addon.getAddonInfo('id')
        icon = 'special://home/addons/%s/icon.png' % addon_id
        return icon


def log(text):
    plugin.log.info(text)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id])
    else:
        #log('String is missing: %s' % string_id)
        return string_id

if __name__ == '__main__':
    plugin.run()
