# -*- coding: utf-8 -*-

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin

try:
	import json
except:
	import simplejson as json

from categories import categories

feeds_prefix = 'http://hd-feeds.herokuapp.com'
direct_prefix = 'http://fshare.herokuapp.com'

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def add_cat(category):
    url = build_url({'mode': 'category', 'category': category['code']})
    li = xbmcgui.ListItem(category['title'], iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

def add_page(page, category):
    url = build_url({'mode': 'category', 'category': category, 'page': page})
    li = xbmcgui.ListItem('Trang ' + page, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
mode = args.get('mode', None)

if mode is None:
    for category in categories:
        add_cat(category)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'category':
    category = args.get('category', 'phim-le')[0]
    page = args.get('page', '1')[0]
    items = json.load(urllib.urlopen(feeds_prefix + '/category/' + category + '/' + page))
    for item in items['content']:
        url = build_url({'mode': 'item', 'id': item['_id']})
        li = xbmcgui.ListItem(item['title'], iconImage=item['thumbnail'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    # Build set of pages to display
    n = items['total']
    pages = (set(range(1, 2))
             | set(range(max(1, int(page) - 2), min(int(page) + 3, n + 1)))
             | set(range(n - 2, n + 1)))
    for p in sorted(pages):
        if p != int(page):
            add_page(str(p), category)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'item':
    id = args.get('id')[0]
    item = json.load(urllib.urlopen(feeds_prefix + '/id/' + id))
    for link in item['links']:
        direct_url = direct_prefix + link['link'][link['link'].index('/file/'):]
        li = xbmcgui.ListItem(link['filename'], iconImage=item['thumbnail'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=direct_url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
