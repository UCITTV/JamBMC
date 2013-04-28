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


STRINGS = {
    # Root menu entries
    'browse': 30000,
    'search': 30001,
    'show_tracks': 30002,
    'show_albums': 30003,
    'show_artists': 30004,
    'show_radios': 30005,
    'show_playlists': 30006,
    'search_tracks': 30007,
    'search_albums': 30008,
    'search_artists': 30009,
    # Misc strings
    'page': 30020,
    # Context menu
    'album_info': 30030,
    'song_info': 30031,
    'show_tracks_in_this_album': 30032,
    'show_albums_by_this_artist': 30033,
    'show_similar_tracks': 30034,
    'addon_settings': 30035,
    # Dialogs
    'search_heading_album': 30040,
    'search_heading_artist': 30041,
    'search_heading_tracks': 30042,
    # Info dialog
    'language': 30050,
    'instruments': 30051,
    'vartags': 30052,
    # Error dialogs
    'network_error': 30060,
    # Notifications
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
api = JamendoApi(
    client_id='de0f381a',
    limit=plugin.get_setting('limit', int)
)


@plugin.route('/')
def root_menu():
    items = [
        {'label': _('browse'),
         'path': plugin.url_for(endpoint='browse_root')},
        {'label': _('search'),
         'path': plugin.url_for(endpoint='search_root')},
        {'label': _('show_radios'),
         'path': plugin.url_for(endpoint='show_radios')},
    ]
    return plugin.finish(items)


@plugin.route('/search/')
def search_root():
    items = [
        {'label': _('search_tracks'),
         'path': plugin.url_for(endpoint='search_tracks')},
        {'label': _('search_albums'),
         'path': plugin.url_for(endpoint='search_albums')},
        {'label': _('search_artists'),
         'path': plugin.url_for(endpoint='search_artists')},
    ]
    return plugin.finish(items)


@plugin.route('/browse/')
def browse_root():
    items = [
        {'label': _('show_tracks'),
         'path': plugin.url_for(endpoint='show_tracks')},
        {'label': _('show_albums'),
         'path': plugin.url_for(endpoint='show_albums')},
        {'label': _('show_artists'),
         'path': plugin.url_for(endpoint='show_artists')},
        {'label': _('show_playlists'),
         'path': plugin.url_for(endpoint='show_playlists')},
    ]
    return plugin.finish(items)


@plugin.route('/albums/')
def show_albums():
    plugin.set_content('albums')
    page = int(args_get('page', 1))
    sort_method = args_get('sort_method')
    albums = api.get_albums(page=page, sort_method=sort_method)
    items = format_albums(albums)
    items.append(sort_method_switcher_item('albums'))
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/albums/search/')
def search_albums():
    query = args_get('query') or plugin.keyboard(heading=_('search_heading_album'))
    if not query:
        return
    plugin.set_content('albums')
    albums = api.get_albums(search_terms=query)
    items = format_albums(albums)
    return add_items(items)


@plugin.route('/albums/<artist_id>/')
def show_albums_by_artist(artist_id):
    plugin.set_content('albums')
    page = int(args_get('page', 1))
    albums = api.get_albums(page=page, artist_id=artist_id)
    items = format_albums(albums)
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/playlists/')
def show_playlists():
    plugin.set_content('music')
    page = int(args_get('page', 1))
    playlists = api.get_playlists(page=page)
    items = format_playlists(playlists)
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/artists/')
def show_artists():
    plugin.set_content('artists')
    page = int(args_get('page', 1))
    sort_method = args_get('sort_method')
    artists = api.get_artists(page=page, sort_method=sort_method)
    items = format_artists(artists)
    items.append(sort_method_switcher_item('artists'))
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/artists/search/')
def search_artists():
    query = args_get('query') or plugin.keyboard(heading=_('search_heading_artist'))
    if not query:
        return
    plugin.set_content('artists')
    artists = api.get_artists(search_terms=query)
    items = format_artists(artists)
    return add_items(items)


@plugin.route('/radios/')
def show_radios():
    plugin.set_content('music')
    page = int(args_get('page', 1))
    radios = api.get_radios(page=page)
    items = format_radios(radios)
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/tracks/')
def show_tracks():
    plugin.set_content('songs')
    page = int(args_get('page', 1))
    sort_method = args_get('sort_method', 'buzzrate')
    tracks = api.get_tracks(page=page, sort_method=sort_method)
    items = format_tracks(tracks)
    items.append(sort_method_switcher_item('tracks'))
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/tracks/search/')
def search_tracks():
    query = args_get('query') or plugin.keyboard(heading=_('search_heading_tracks'))
    if not query:
        return
    plugin.set_content('songs')
    tracks = api.search_tracks(search_terms=query)
    items = format_tracks(tracks)
    return add_items(items)


@plugin.route('/tracks/album/<album_id>/')
def show_tracks_in_album(album_id):
    plugin.set_content('songs')
    tracks = api.get_tracks(filter_dict={'album_id': album_id})
    items = format_tracks(tracks)
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/tracks/playlist/<playlist_id>/')
def show_tracks_in_playlist(playlist_id):
    plugin.set_content('songs')
    playlist, tracks = api.get_playlist_tracks(playlist_id=playlist_id)
    items = format_playlist_tracks(playlist, tracks)
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/tracks/similar/<track_id>/')
def show_similar_tracks(track_id):
    plugin.set_content('songs')
    page = int(args_get('page', 1))
    tracks = api.get_similar_tracks(track_id=track_id, page=page)
    items = format_similar_tracks(tracks)
    items.extend(pagination_items(len(items)))
    return add_items(items)


@plugin.route('/sort_methods/<entity>/')
def show_sort_methods(entity):
    sort_methods = api.get_sort_methods(entity)
    items = format_sort_methods(sort_methods, entity)
    return plugin.finish(items, update_listing=True)


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


def format_tracks(tracks):
    items = [{
        'label': '%s - %s (%s)' % (
            track['artist_name'],
            track['name'],
            track['album_name']
        ),
        'info': {
            'count': i + 2,
            'title': track['name'],
            'album': track['album_name'],
            'duration': track['duration'],
            'artist': track['artist_name'],
            'genre': ', '.join(track['musicinfo']['tags']['genres']),
            'comment': get_comment(track['musicinfo']),
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
    return items


def format_albums(albums):
    items = [{
        'label': '%s - %s' % (album['artist_name'], album['name']),
        'info': {
            'count': i + 2,
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
    return items


def format_playlists(playlists):
    items = [{
        'label': '%s (%s)' % (playlist['name'], playlist['user_name']),
        'info': {
            'count': i + 2,
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
    return items


def format_artists(artists):
    items = [{
        'label': artist['name'],
        'info': {
            'count': i + 2,
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
    return items


def format_radios(radios):
    items = [{
        'label': radio['dispname'],
        'info': {
            'count': i + 2,
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
    return items


def format_playlist_tracks(playlist, tracks):
    items = [{
        'label': track['name'],
        'info': {
            'count': i + 2,
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
    return items


def format_similar_tracks(tracks):
    items = [{
        'label': '%s - %s (%s)' % (
            track['artist_name'],
            track['name'],
            track['album_name']
        ),
        'info': {
            'count': i + 2,
            'title': track['name'],
            'album': track['album_name'],
            'duration': track['duration'],
            'artist': track['artist_name'],
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
    return items


def format_sort_methods(sort_methods, entity):
    items = [{
        'label': _('sort_method_%s' % sort_method),
        'info': {
            'count': i,
        },
        'context_menu': sort_method_context_menu(),
        'replace_context_menu': True,
        'path': plugin.url_for(
            endpoint='show_%s' % entity,
            is_update='true',
            **dict(plugin.request.view_params, sort_method=sort_method)
        )
    } for i, sort_method in enumerate(sort_methods)]
    return items


def get_comment(musicinfo):
    return '[CR]'.join((
        '[B]%s[/B]: %s' % (
            _('language'),
            musicinfo['lang']
        ),
        '[B]%s[/B]: %s' % (
            _('instruments'),
            ', '.join(musicinfo['tags']['instruments'])
        ),
        '[B]%s[/B]: %s' % (
            _('vartags'),
            ', '.join(musicinfo['tags']['vartags'])
        ),
    ))


def sort_method_switcher_item(entity):
    current_sort_method = args_get('sort_method') or 'default'
    return {
        'label': '[B][[ %s ]][/B]' % _('sort_method_%s' % current_sort_method),
        'info': {
            'count': 0,
        },
        'path': plugin.url_for(
            endpoint='show_sort_methods',
            entity=entity,
            is_update='true',
        ),
    }


def pagination_items(items_len):
    current_page = int(args_get('page', 1))
    has_next_page = items_len >= api.current_limit
    has_previous_page = current_page > 1
    original_params = plugin.request.view_params
    extra_params = {}
    if 'sort_method' in plugin.request.args:
        extra_params['sort_method'] = args_get('sort_method')
    items = []
    if has_next_page:
        next_page = int(current_page) + 1
        extra_params['page'] = next_page
        items.append({
            'label': '>> %s %d >>' % (_('page'), next_page),
            'info': {
                'count': items_len + 2,
            },
            'path': plugin.url_for(
                endpoint=plugin.request.view,
                is_update='true',
                **dict(original_params, **extra_params)
            )
        })
    if has_previous_page:
        previous_page = int(current_page) - 1
        extra_params['page'] = previous_page
        items.append({
            'label': '<< %s %d <<' % (_('page'), previous_page),
            'info': {
                'count': 1,
            },
            'path': plugin.url_for(
                endpoint=plugin.request.view,
                is_update='true',
                **dict(original_params, **extra_params)
            )
        })
    return items


def add_items(items):
    is_update = 'is_update' in plugin.request.args
    finish_kwargs = {
        'update_listing': is_update,
        'sort_methods': ('playlist_order', )
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


def sort_method_context_menu():
    return [
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def album_context_menu(artist_id, album_id):
    return [
        (_('album_info'),
         _action('info')),
        (_('show_tracks_in_this_album'),
         _view(endpoint='show_tracks_in_album',
               album_id=album_id)),
        (_('show_albums_by_this_artist'),
         _view(endpoint='show_albums_by_artist',
               artist_id=artist_id)),
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def artist_context_menu(artist_id):
    return [
        (_('show_albums_by_this_artist'),
         _view(endpoint='show_albums_by_artist',
               artist_id=artist_id)),
        (_('addon_settings'),
         _run(endpoint='open_settings')),
    ]


def track_context_menu(artist_id, track_id, album_id):
    return [
        (_('song_info'),
         _action('info')),
        (_('show_albums_by_this_artist'),
         _view(endpoint='show_albums_by_artist',
               artist_id=artist_id)),
        (_('show_similar_tracks'),
         _view(endpoint='show_similar_tracks',
               track_id=track_id)),
        (_('show_tracks_in_this_album'),
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
    return plugin.request.args.get(arg_name, [default])[0]


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
