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

PATH = 'content'
ARTICLE_URL = '{slug}.html'

STATIC_PATHS = ['extra', 'files', 'images']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
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
         ('Wireguard', 'https://wireguard.io/'),
         ('OWASP NZ', 'https://www.owasp.org/index.php/New_Zealand'),
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
