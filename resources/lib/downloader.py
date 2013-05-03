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

import os
from urllib import urlretrieve

import xbmc
import xbmcaddon
import xbmcgui

STRINGS = {
    'progress_head': 30080,
    'preparing_download': 30081,
    'downloading_to_s': 30082,
    'current_progress_s_mb': 30083,
    'current_file_s': 30084,
}

addon = xbmcaddon.Addon()


class JamendoDownloader(object):

    def __init__(self, download_path, show_progress=True):
        log('__init__ with path="%s"' % download_path)
        self.download_path = download_path
        self.show_progress = show_progress
        if self.show_progress:
            self.progress_dialog = xbmcgui.DialogProgress()
            self.progress_dialog.create(_('progress_head'))
            self.progress_dialog.update(1, _('preparing_download'))
        else:
            self.progress_dialog = None

    def download(self, items):
        self.total_count = len(items)
        line3 = _('downloading_to_s') % self.download_path
        if self.show_progress:
            self.progress_dialog.update(2, '', '', line3)
        if not os.path.isdir(self.download_path):
            os.mkdir(self.download_path)
        downloaded_items = []
        for i, (track_url, filename) in enumerate(items):
            self.current_item_count = i + 1
            self.current_filename = filename
            filename = os.path.join(self.download_path, filename)
            log('Downloading "%s" to "%s"' % (track_url, filename))
            try:
                urlretrieve(track_url, filename, self.update_progress)
            except IOError, e:
                log('IOError: "%s"' % str(e))
                break
            except KeyboardInterrupt:
                break
            log('Item Done')
            if self.show_progress and self.progress_dialog.iscanceled():
                log('Canceled')
                return
            downloaded_items.append(filename)
        log('All Done')
        return downloaded_items

    def update_progress(self, block_count, block_size, item_size):
        if self.show_progress:
            if self.progress_dialog.iscanceled():
                raise KeyboardInterrupt
            percent = int(self.current_item_count * 100 / self.total_count)
            current_mb = (block_count * block_size / 1024.0 / 1024.0)
            line1 = _('current_progress_s_mb') % '%0.2f' % current_mb
            line2 = _('current_file_s') % self.current_filename
            self.progress_dialog.update(percent, line1, line2)

    def __del__(self):
        if self.show_progress:
            self.progress_dialog.close()


def log(msg):
    xbmc.log(u'[JemandoDownloader]: %s' % msg.encode('utf8', 'ignore'))


def _(string_id):
    if string_id in STRINGS:
        return addon.getLocalizedString(STRINGS[string_id])
    else:
        log('String is missing: %s' % string_id)
        return string_id
