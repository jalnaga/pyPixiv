# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup

from Browser import PBR
from Browser import PIXIV_URL
from Browser import PIXIV_MYPAGE_URL
from Browser import PIXIV_WORK_URL
from Artist import Artist


class Bookmark(object):
	"""Class for managing Bookmark."""
	def __init__(self):
		super(Bookmark, self).__init__()
		self.htmls = []
		self.artists = []
		self.numTotalArtists = 0

	def appendBookmarkPageHtml(self, bookmarkPageUrl):
		self.htmls.append(PBR.open(bookmarkPageUrl).read())
		
		nextPageLink = None
		for link in PBR.links():
			if ("class", "button") in link.attrs and \
			("rel", "next") in link.attrs:
				nextPageLink = link
				break
		if nextPageLink != None:
			PBR.follow_link(url = nextPageLink.url)
			self.appendBookmarkPageHtml(nextPageLink.url)

	def _setTotalArtistsNumberFromHtml(self, inputHtml):
		pageSoup = BeautifulSoup(inputHtml)
		self.numTotalArtists = int(pageSoup.find("div", {"class":"info"}).find(
			"span", {"class":"count"}).text)

	def _setArtistsFromHtml(self, inputHtml):
		pageSoup = BeautifulSoup(inputHtml)
		if self.numTotalArtists != 0:
			artistsSoup = pageSoup.find("div", {"class":"members"})
			artists = artistsSoup.findAll("li")

			for artist in artists:
				artistSoup = artist.find("div", 
					{"class":"userdata"}).find("a")
				appendArtist = Artist(artistSoup = artistSoup)
				self.artists.append(appendArtist)
		else:
			self.artists = []
			self.numTotalArtists = 0

	def hasHtmls(self):
		if len(self.htmls) > 0:
			return True
		else:
			return False

	def hasArtists(self):
		if self.hasHtmls():
			if self.numTotalArtists == 0:
				return False
			else:
				return True
		else:
			return False

	def genDetailInfo(self):
		self._setTotalArtistsNumberFromHtml(self.htmls[0])
		for html in self.htmls:
			self._setArtistsFromHtml(html)

	def getArtists(self):
		return self.artists

	def getArtistsUrls(self):
		returnUrls = []
		for artist in self.artists:
			returnUrls.append(artist.getUrl())
		return returnUrls

	def getArtistsNames(self):
		returnNames = []
		for artist in self.artists:
			returnNames.append(artist.getName())
		return returnNames

	def getArtistsIDs(self):
		returnIDs = []
		for artist in self.artists:
			returnIDs.append(artist.getID())
		return returnIDs

	def getNumTotalArtists(self):
		return self.numTotalArtists