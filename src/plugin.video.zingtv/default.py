# -*- coding: utf-8 -*-

import sys
import re
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import math

try:
	import json
except:
	import simplejson as json

from categories import thumb_prefix, thumb_ep_prefix, program_url, program_info_url, series_url, media_url, playable_url, menus

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def pagination(n, page):
    # Build set of pages to display
    if n <= 5:
        return set(range(1, n + 1))
    else:
        return (set(range(1, 2))
                 | set(range(max(1, int(page) - 2), min(int(page) + 3, n + 1)))
                 | set(range(n - 2, n + 1)))

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def add_menu(menu):
    url = build_url(menu)
    li = xbmcgui.ListItem(menu['title'], iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

def add_genre_page(page, genre):
    url = build_url({'mode': 'genre', 'genre': genre, 'page': page})
    li = xbmcgui.ListItem('Trang ' + page, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

def add_series_page(page, series):
    url = build_url({'mode': 'series', 'series': series, 'page': page})
    li = xbmcgui.ListItem('Trang ' + page, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

mode = args.get('mode', None)

if mode is None:
    for menu in menus:
        add_menu(menu)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'genre':
    genre = args.get('genre', '78')[0]
    page = args.get('page', '1')[0]
    items = json.load(urllib.urlopen(program_url % { 'genre_id': genre, 'page': page } ))
    for item in items['response']:
        program = json.load(urllib.urlopen(program_info_url % { 'program_id': item['id'] } ))
        url = build_url({'mode': 'series', 'series': program['response']['series'][0]['id']})
        li = xbmcgui.ListItem(item['name'], iconImage=thumb_prefix + item['thumbnail'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    
    pages = pagination(int(math.ceil(float(items['total'])/10)), page)
    for p in sorted(pages):
        if p != int(page):
            add_genre_page(str(p), genre)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'series':
    series = args.get('series')[0]
    page = args.get('page', '1')[0]
    items = json.load(urllib.urlopen(series_url % { 'series_id': series, 'page': page } ))
    for item in items['response']:
        url = build_url({'mode': 'play', 'id': item['id']})
        li = xbmcgui.ListItem(item['title'], iconImage=thumb_ep_prefix + item['thumbnail'])
        li.setInfo('video', { 'title': item['title'] })
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    
    pages = pagination(int(math.ceil(float(items['total'])/10)), page)
    for p in sorted(pages):
        if p != int(page):
            add_series_page(str(p), series)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play':
    id = args.get('id')[0]
    item = json.load(urllib.urlopen(media_url % { 'media_id': id }))
    if 'other_url' in item['response']:
        if 'Video1080' in item['response']['other_url']:
            url = urllib.urlopen(playable_url % { 'url': item['response']['other_url']['Video1080'] }).geturl()
        elif 'Video720' in item['response']['other_url']:
            url = urllib.urlopen(playable_url % { 'url': item['response']['other_url']['Video720'] }).geturl()
        elif 'Video480' in item['response']['other_url']:
            url = urllib.urlopen(playable_url % { 'url': item['response']['other_url']['Video480'] }).geturl()
        else:
            url = urllib.urlopen(playable_url % { 'url': item['response']['file_url'] }).geturl()
    item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
