#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eric Light'
SITENAME = u'Such geek. Wow.'
SITESUBTITLE = u'An eclectic collection of technical learnings and assorted challenges, for... reasons.'
SITETITLE = u'Making things work'
SITEURL = 'https://www.ericlight.com'
SITELOGO = 'https://www.ericlight.com/profile.png'
THEME = u'/home/eric/Pelican/ericlight.com/Flex'

MAIN_MENU = True

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS=['sitemap']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

PATH = 'content'
ARTICLE_URL = '{slug}.html'

STATIC_PATHS = ['extra', 'files', 'images']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/cv.pdf': {'path': 'cv/EricLight.pdf'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
    'extra/security.txt': {'path': '.well-known/security.txt'},
    'extra/profile.png': {'path': 'profile.png'}
}

TIMEZONE = 'Pacific/Auckland'

SUMMARY_MAX_LENGTH = 90
DEFAULT_DATE = 'fs'
DEFAULT_LANG = 'en'

DISABLE_URL_HASH = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# Blogroll
LINKS = (
         ('InfoSecNZ', 'https://github.com/binarymist/InfoSecNZ/'),
         ('WireGuard', 'https://www.wireguard.com/'),
         ('OWASP NZ', 'https://owasp.org/www-chapter-new-zealand/'),
         ('NZ Python Users Group', 'https://python.nz'),
         ('RingZer0 Team CTF', 'https://ringzer0team.com'),
         )

# Social widget
SOCIAL = (
         ('linkedin', 'https://linkedin.com/in/ericdlight'),
         ('github', 'https://github.com/rhyven'),
         ('twitter', 'https://twitter.com/rhyvenNZ'),
         )


MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)



DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

GOOGLE_ANALYTICS = 'UA-23358170-1'
GOOGLE_TAG_MANAGER = 'GTM-NNM4P6R'
