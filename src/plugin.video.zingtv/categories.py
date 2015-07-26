# -*- coding: utf-8 -*-
api_prefix = 'http://api.tv.zing.vn/2.0/'
thumb_prefix = 'http://image.mp3.zdn.vn/'
thumb_ep_prefix = thumb_prefix + 'tv_media_210_120/'
program_url = api_prefix + 'program/list?list_type=new&api_key=8344bd6d1cadff9678e609fa4c909251&genre_id=%(genre_id)s&page=%(page)s&count=10'
program_info_url = api_prefix + 'program/info?api_key=8344bd6d1cadff9678e609fa4c909251&program_id=%(program_id)s'
series_url = api_prefix + 'tv/series/medias?api_key=8344bd6d1cadff9678e609fa4c909251&series_id=%(series_id)s&page=%(page)s&count=10'
media_url = api_prefix + 'tv/media/info?api_key=8344bd6d1cadff9678e609fa4c909251&media_id=%(media_id)s'
playable_url = 'http://%(url)s'
menus = [
    {
        'title': 'TV Show',
        'mode': 'genre',
        'genre':  '78'
    },
    {
        'title': 'Phim Truyền Hình',
        'mode': 'genre',
        'genre':  '82'
    },
    {
        'title': 'Hoạt Hình',
        'mode': 'genre',
        'genre':  '83'
    },
    {
        'title': 'Giáo Dục',
        'mode': 'genre',
        'genre':  '87'
    },
    {
        'title': 'Âm Nhạc',
        'mode': 'genre',
        'genre':  '92'
    },
    {
        'title': 'Tin Tức - Sự Kiện',
        'mode': 'genre',
        'genre':  '79'
    },
    {
        'title': 'Thể Thao',
        'mode': 'genre',
        'genre':  '81'
    },
    {
        'title': 'Quảng Cáo ',
        'mode': 'genre',
        'genre':  '93'
    }
]
