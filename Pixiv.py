# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup

from Browser import PBR
from Browser import PIXIV_URL
from Browser import PIXIV_MYPAGE_URL
from Browser import PIXIV_WORK_URL
from Bookmark import Bookmark
from Artist import Artist
from Content import Content


class Pixiv(object):
	"""Main Class. Get boo"""
	def __init__(self, userID = "", userPassword = ""):
		super(Pixiv, self).__init__()
		self.userID = userID
		self.userPassword = userPassword
		self.loginStatus = False
		self.openBookmark = Bookmark()
		self.hiddenBookmark = Bookmark()

		# Trying login if has ID and Password.
		if self.userID != "" and self.userPassword != "":
			self.goHome()
			self.login(self.userID, self.userPassword)

	def goHome(self):
		# Mechanize goes to Pixiv root page.
		PBR.open(PIXIV_URL)

	def goMyPage(self):
		# Mechanize goes to User page of Pixiv.
		PBR.open(PIXIV_MYPAGE_URL)

	def goOpenBookmarkPage(self):
		self.goMyPage()
		PBR.follow_link(url = "/bookmark.php?type=user")

	def goHiddenBookmarkPage(self):
		# Go to hidden bookmark page through open bookmark page. There are no 
		# direct link to go to hidden bookmark page.
		self.goMyPage()
		PBR.follow_link(url = "/bookmark.php?type=user")
		PBR.follow_link(url = "bookmark.php?type=user&rest=hide")

	def _getLoginFormNum(self):
		# Return form number for login.
		formNum = 0
		for f in PBR.forms():
			for control in f.controls:
				if control.name == "pixiv_id":
					return formNum
			formNum += 1
		return False

	def _checkFirstLogin(self):
		if PBR.geturl() == PIXIV_MYPAGE_URL:
			self.loginStatus = True
		else:
			self.goHome()
			self.userID = ""
			self.userPass = ""
			self.loginStatus = False
		return self.loginStatus

	def login(self, loginID = "", loginPass = ""):
		self.goHome()
		formNum = self._getLoginFormNum()

		if formNum:
			self.userID = loginID
			self.userPassword = loginPass
			PBR.select_form(nr = formNum)
			PBR["pixiv_id"] = self.userID
			PBR["pass"] = self.userPassword
			PBR.submit()
			return self._checkFirstLogin()
		else:
			return False

	def didLogin(self):
		return self.loginStatus

	def getOpenBookmark(self):
		if self.didLogin():
			if not self.openBookmark.hasHtmls():
				self.goOpenBookmarkPage()
				self.openBookmark.appendBookmarkPageHtml(bookmarkPageUrl = 
					PBR.geturl())
			return self.openBookmark
		else:
			return None

	def getHiddenBookmark(self):
		if self.didLogin():
			if not self.hiddenBookmark.hasHtmls():
				self.goHiddenBookmarkPage()
				self.hiddenBookmark.appendBookmarkPageHtml(bookmarkPageUrl = 
					PBR.geturl())
			return self.hiddenBookmark
		else:
			return None

	def getArtistByID(self, inputID):
		returnArtist = Artist(artistID = inputID)
		resultHtml = PBR.open(returnArtist.getUrl()).read()
		resultSoup = BeautifulSoup(resultHtml)
		if not resultSoup.find("span", {"class":"error"}):
			returnArtist.genDetailInfo()
			return returnArtist
		else:
			return None

	def getWorkByUrl(self, inputUrl):
		returnWork = Content()
		returnWork.setUrl(inputUrl)
		return returnWork

	def getWorkByID(self, inputID):
		returnWork = Content()
		returnWork.setID(inputID)
		return returnWork