# -*- coding: utf-8 -*-

import sys
import re
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import CommonFunctions as common

try:
	import json
except:
	import simplejson as json

from categories import categories, menus

feeds_prefix = 'http://hd-feeds.herokuapp.com'
direct_prefix = 'http://fshare.herokuapp.com'

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

def add_cat(category, main_category):
    url = build_url({'mode': 'category', 'category': main_category + ',' + category['code']})
    li = xbmcgui.ListItem(category['title'], iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
def add_page(page, category):
    url = build_url({'mode': 'category', 'category': category, 'page': page})
    li = xbmcgui.ListItem('Trang ' + page, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

def add_search_page(page, query):
    url = build_url({'mode': 'search', 'query': query, 'page': page})
    li = xbmcgui.ListItem('Trang ' + page, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
mode = args.get('mode', None)

if mode is None:
    for menu in menus:
        add_menu(menu)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'search':
    query = args.get('query', '')
    if not query:
        query = common.getUserInput('Search', '')
    else:
        query = query[0]
    page = args.get('page', '1')[0]
    items = json.load(urllib.urlopen(feeds_prefix + '/search/' + query + '/' + page))
    for item in items['content']:
        url = build_url({'mode': 'item', 'id': item['_id']})
        li = xbmcgui.ListItem(item['title'], iconImage=item['thumbnail'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    
    pages = pagination(items['total'], page)
    for p in sorted(pages):
        if p != int(page):
            add_search_page(str(p), query)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'menu':
    main_category = args.get('category', 'phim-le')[0]
    for category in categories[main_category]:
        add_cat(category, main_category)
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
    
    pages = pagination(items['total'], page)
    for p in sorted(pages):
        if p != int(page):
            add_page(str(p), category)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'item':
    id = args.get('id')[0]
    item = json.load(urllib.urlopen(feeds_prefix + '/id/' + id))
    for link in item['links']:
        url = url = build_url({'mode': 'play', 'id': re.search('\/file\/(\w+)', link['link']).group(1)})
        li = xbmcgui.ListItem(link['filename'], iconImage="DefaultVideo.png", thumbnailImage=item['thumbnail'])
        # li.setInfo(type="Video", infoLabels={ "Title": item['title'], "Plot": description, "Duration": duration})
        li.setInfo('video', { 'title': item['title'] })
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play':
    url = urllib.urlopen(direct_prefix + '/file/' + args.get('id')[0]).geturl()
    item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)