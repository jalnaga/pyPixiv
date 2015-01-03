# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup

from Browser import PBR
from Browser import PIXIV_URL
from Browser import PIXIV_MYPAGE_URL
from Browser import PIXIV_WORK_URL
from Content import Content


class ContentsList(object):
	"""docstring for ContentsList"""
	def __init__(self, contentsListUrl = None):
		super(ContentsList, self).__init__()
		self.numTotal = 0
		self.contents = []
		self.htmls = []

	def appendContentPageHtml(self, contentPageUrl):
		self.htmls.append(PBR.open(contentPageUrl).read())
		
		nextPageLink = None
		for link in PBR.links():
			if ("class", "_button") in link.attrs and \
			("rel", "next") in link.attrs:
				nextPageLink = link
				break
		if nextPageLink != None:
			PBR.follow_link(url = nextPageLink.url)
			self.appendContentPageHtml(nextPageLink.url)

	def _setNumTotalContents(self):
		contentsListHtml = self.htmls[0]
		contentsListSoup = BeautifulSoup(contentsListHtml)
		self.numTotal = int(contentsListSoup.find("div", 
			{"id":"wrapper"}).find("span", {"class":"count-badge"}).text[:-1])

	def _genContentsFromHtml(self, inputHtml):
		pageSoup = BeautifulSoup(inputHtml)
		if self.numTotal != 0:
			contentsSoup = pageSoup.find("div", 
				{"class":"display_works linkStyleWorks "})
			contents = contentsSoup.findAll("li")

			for content in contents:
				contentUrl = content.find("a").get("href")
				contentUrl = PIXIV_URL + contentUrl
				appendContent = Content()
				appendContent.setUrl(contentUrl)

				contentThumnailUrl = content.find("img").get("src")
				appendContent.setThumnailUrl(contentThumnailUrl)

				self.contents.append(appendContent)
		else:
			self.numTotal = 0
			self.contents = []

	def genDetailInfo(self):
		self._setNumTotalContents()
		for html in self.htmls:
			self._genContentsFromHtml(html)

	def getContents(self):
		if self.numTotal == 0:
			self.genDetailInfo()
		return self.contents

	def getNumTotal(self):
		return self.numTotal

	def getContentByIndex(self, inputIndex):
		if self.numTotal != 0:
			if 0 <= inputIndex < self.numTotal:
				return self.contents[inputIndex]
			else:
				return None
		else:
			return None