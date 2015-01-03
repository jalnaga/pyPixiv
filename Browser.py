# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cookielib

import mechanize


PIXIV_URL = "http://www.pixiv.net"
"""
전역 변수.

Pixiv의 웹페이지 루트 주소.
"""

PIXIV_MYPAGE_URL = PIXIV_URL + "/mypage.php"
"""
전역 변수.

Pixiv에 로그인 후 보게 되는 최초의 개인 웹페이지 주소.
"""

PIXIV_WORK_URL = PIXIV_URL + "/member_illust.php?mode=medium&illust_id="
"""
전역 변수.

작업물 ID를 제외한 절대 웹주소.
"""

_USER_AGENT = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')]
_CJ = cookielib.LWPCookieJar()

PBR = mechanize.Browser()
"""
전역 변수.

Mechanize 가상 브라우저.

.. note:: PBR은 Pixiv BRowser의 줄임말.
"""
PBR.set_cookiejar(_CJ)
PBR.set_handle_equiv(True)
PBR.set_handle_gzip(False)
PBR.set_handle_redirect(True)
PBR.set_handle_referer(True)
PBR.set_handle_robots(False)
PBR.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
PBR.addheaders = _USER_AGENT