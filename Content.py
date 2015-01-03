# -*- coding: utf-8 -*-
"""
.. moduleauthor:: 김동석 <jalnagakds@gmail.com>

설명
-----------------------------------

작업물 모듈 입니다. 픽시브의 작업물에 관한 정보를 담고 있는 
:class:`pypixiv.Content` 클래스 하나로 구성되어 있습니다.

작업 내역
------------------------------------

* [2014/09/06] -- 최초 사용 가능 버전 완성. 문서화를 위한 DocString 작업

-------------------------------------
"""

from __future__ import unicode_literals

import os
import re
import datetime

from bs4 import BeautifulSoup

from Browser import PBR
from Browser import PIXIV_URL
from Browser import PIXIV_MYPAGE_URL
from Browser import PIXIV_WORK_URL

# ==============================================================================
class Content(object):
	"""
	픽시브의 작업물 ID나 작업물의 웹페이지 주소, BeautifulSoup 객체로부터 
	작업물의 정보를 생성하고 관리합니다.

	.. warning::
		* 처음 객체가 생성되면 아무런 정보도 갖고 있지 않습니다.
		* :func:`setUrl` 이나 :func:`setID` 로 기본 정보를 할당 한 후
		  :func:`genDetailInfo` 를 실행해야 제대로 사용 할 수 있습니다.
	"""
	def __init__(self):
		super(Content, self).__init__()
		self.url = ""
		self.thumbnailUrl = ""
		self.artistName = ""
		self.artistID = ""
		self.id = ""
		self.title = ""
		self.dateTime = None
		self.type = ""
		self.viewCount = 0
		self.scoreCount = 0
		self.width = 0
		self.height = 0
		self.imgUrl = ""

	# --------------------------------------------------------------------------
	def _genIDFromUrl(self, inputUrl):
		"""
		Private function for generating content ID from content url.

		:param inputUrl: Content url.
		:type inputUrl: str.
		"""
		self.id = inputUrl.split("id=")[-1]

	# --------------------------------------------------------------------------
	def _genTitleFromSoup(self, inputSoup):
		"""
		Private function for  generating content title from BeautifulSoup 
		object.

		:param inputSoup: BeautifulSoup object. It must be created from Content
		page html.
		:type inputSoup: BeautifulSoup.
		"""
		self.title = inputSoup.find("h1", {"class":"title"}).text

	# --------------------------------------------------------------------------
	def _genScoreFromSoup(self, inputSoup):
		"""
		Private function for generating content Score from BeautifulSoup object.

		Score is some kind of calculated point from view count and favorite 
		count. Score is most useful variable for  judging value of content.

		:param inputSoup: BeautifulSoup object. It must be created from Content
		page html.
		:type inputSoup: BeautifulSoup.
		"""
		scoreSoup = inputSoup.find("section", {"class":"score"})
		self.viewCount = int(scoreSoup.find("dd", {"class":"view-count"}).text)
		self.scoreCount = int(scoreSoup.find("dd", 
			{"class":"score-count"}).text)

	# --------------------------------------------------------------------------
	def _genMetaDataFromSoup(self, inputSoup):
		"""
		Private function for generating content type from BeautifulSoup object.

		Content type is used to select dowloading function.

		:param inputSoup: BeautifulSoup object. It must be created from Content
		page html.
		:type inputSoup: BeautifulSoup.

		.. warning:: This function supports only two types - Illust and Comic. 
		It doesn't support **Animation** type. Every animation type contents are 
		treated as **Comic**.
		"""
		metaSoup = inputSoup.find("ul", {"class":"meta"})
		metaDatas = metaSoup.findAll("li")
		
		# generating numbers from date text.
		dateTimeTuple = re.findall(r"\d+", metaDatas[0].string)
		self.dateTime = datetime.datetime(
			year = int(dateTimeTuple[0]), 
			month = int(dateTimeTuple[1]), 
			day = int(dateTimeTuple[2]), 
			hour = int(dateTimeTuple[3]), 
			minute = int(dateTimeTuple[4]))
		
		# generating nubers from resolution text.
		resolution = re.findall(r"\d+", metaDatas[1].string)
		
		if len(resolution) == 2:
			self.type = "Illust"
			self.width = int(resolution[0])
			self.height = int(resolution[1])
		else:
			self.type = "Comic"

	# --------------------------------------------------------------------------
	def _genArtistFromSoup(self, inputSoup):
		"""
		Private function for generating basic information of content's artist
		from BeautifulSoup object.

		:param inputSoup: BeautifulSoup object. It must be created from Content
		page html.
		:type inputSoup: BeautifulSoup.
		"""
		artistSoup = inputSoup.find("a", {"class":"user-link"})
		self.artistName = artistSoup.find("h1").text
		self.artistID = artistSoup.get("href").split("id=")[-1]

	# --------------------------------------------------------------------------
	def _genContentInfoFromSoup(self, inputSoup):
		"""
		Private function for filling up every info of content.

		:param inputSoup: BeautifulSoup object. It must be created from Content
		page html.
		:type inputSoup: BeautifulSoup.
		"""
		self._genArtistFromSoup(inputSoup)

		contentInfoSoup = inputSoup.find("section", 
			{"class":"work-info"})
		self._genScoreFromSoup(contentInfoSoup)
		self._genTitleFromSoup(contentInfoSoup)
		self._genMetaDataFromSoup(contentInfoSoup)

	# --------------------------------------------------------------------------
	def _genImgUrlFromSoup(self, inputSoup):
		"""
		Private function for generating real content url which is used to 
		download.

		:param inputSoup: BeautifulSoup object. It must be created from Content
		page html.
		:type inputSoup: BeautifulSoup.
		"""
		contentDisplaySoup = inputSoup.find("div", {"class":"works_display"})
		self.imgUrl = contentDisplaySoup.find("a").get("href")
		self.imgUrl = PIXIV_URL + "/" + self.imgUrl

	# --------------------------------------------------------------------------
	def setUrl(self, inputUrl):
		"""
		작업물의 웹페이지 주소를 할당.

		:param inputUrl: 작업물의 웹페이지 주소.
		:type inputUrl: str.
		"""
		self.url = inputUrl

	# --------------------------------------------------------------------------
	def setID(self, inputID):
		"""
		작업물의 ID를 할당.

		:param inputID: 작업물의 ID. 작업물 웹페이지 주소의 "id="이후의 숫자.
		:type inputUrl: str.
		"""
		self.id = inputID
		self.url = PIXIV_WORK_URL + inputID

	# --------------------------------------------------------------------------
	def setThumnailUrl(self, inputUrl):
		"""
		작업물의 미리보기 이미지 주소를 할당.
		"""
		self.thumbnailUrl = inputUrl

	# --------------------------------------------------------------------------
	def hasUrl(self):
		"""
		작업물 웹페이지의 절대 주소가 존재하는지 확인하는 함수.

		:returns: *bool.*
		"""
		if self.url != "" and self.url != None:
			return True
		else:
			return False

	# --------------------------------------------------------------------------
	def genDetailInfo(self):
		"""
		작업물의 모든 정보를 생성해서 객체를 사용 할 수 있도록 하는 함수.

		.. warning::
			* :func:`setUrl` 이나 :func:`setID` 로 기본 정보를 할당 한 후
			  :func:`genDetailInfo` 를 실행해야 제대로 사용 할 수 있습니다.

		:returns: *bool.*
		"""
		if self.hasUrl():
			self._genIDFromUrl(self.url)
			contentHtml = PBR.open(self.url).read()
			contentSoup = BeautifulSoup(contentHtml)
			self._genContentInfoFromSoup(contentSoup)
			self._genImgUrlFromSoup(contentSoup)
			return True
		else:
			return False

	# --------------------------------------------------------------------------
	def getTitle(self):
		"""
		작업물의 제목을 반환.

		:returns: *str.*
		"""
		return self.title

	# --------------------------------------------------------------------------
	def getDate(self):
		"""
		작업물의 업로드 날짜를 반환.

		:returns: *datetime.*
		"""
		return self.dateTime

	# --------------------------------------------------------------------------
	def getViewCount(self):
		"""
		작업물의 조회수를 반환.

		:returns: *int.*
		"""
		return self.viewCount

	# --------------------------------------------------------------------------
	def getScoreCount(self):
		"""
		작업물의 총점을 반환.

		:returns: *str.*

		.. note:: 
			* 총점은 Pixiv가 자체적인 알고리즘을 기반으로 작업물의 조회수와 
			  평가횟수를 통해 작업물의 가치나 선호도를 평가한 것.
			* 이것이 높을 수록 작업물의 가치가 높다.
		"""
		return self.scoreCount

	# --------------------------------------------------------------------------
	def getType(self):
		"""
		작업물의 형태를 반환.

		:returns: *str.* ::
			
			"Illust" -- 일러스트나 애니메이션
			"Comic" -- 만화

		.. note:: 새로 추가된 형태인 애니메이션 타입의 작업물들은 아직 지원 하지
				  않습니다.
		"""
		return self.type

	# --------------------------------------------------------------------------
	def getThumnailUrl(self):
		"""
		작업물의 미리보기 이미지 웹주소를 반환.

		:returns: *str.*
		"""
		return self.thumbnailUrl

	# --------------------------------------------------------------------------
	def getImgUrl(self):
		"""
		작업물의 실제 이미지 웹주소를 반환.

		.. warning:: 작업물의 웹페이지 주소가 아님! 크게 보기를 위한 웹주소.

		:returns: *str.*
		"""
		return self.imgUrl

	# --------------------------------------------------------------------------
	def getUrl(self):
		"""
		작업물의 웹페이지 주소를 반환.

		:returs: *str.*
		"""
		return self.url

	# --------------------------------------------------------------------------
	def getArtistName(self):
		"""
		작업물을 작업한 아티스트의 이름을 반환.

		.. note:: 업데이트 예정

		:returns: *str.*
		"""
		return self.artistName

	# --------------------------------------------------------------------------
	def getArtistID(self):
		"""
		작업물을 작업한 아티스트의 ID를 반환.

		.. note:: 업데이트 예정

		:returns: *str.*
		"""
		return self.artistID

	def isIllust(self):
		"""
		작업물이 일러스트인지 확인하는 함수.

		:returns: *bool.*
		"""
		if self.type == "Illust":
			return True
		else:
			return False

	def isComic(self):
		"""
		작업물이 만화인지 확인하는 함수.

		:returns: *bool.*
		"""
		if self.type == "Comic":
			return True
		else:
			return False

	def _setSaveImgFileName(self, imgUrl, args):
		extension = imgUrl.split(".")[-1]
		extension = "." + extension
		illustFileName = ""

		for fileName in args:
			illustFileName += fileName + "_"
		illustFileName = illustFileName[:-1]

		return (illustFileName + extension)

	def _saveImg(self, imgUrl, savePath, saveName):
		finalImg = PBR.open(imgUrl)
		finalImgFileName = os.path.join(savePath, saveName)
		f = open(finalImgFileName, "wb")
		f.write(finalImg.read())
		f.close()
		PBR.back()

	def _downIllust(self, savePath, saveNameArgs):
		PBR.addheaders = [("Referer", self.url)]
		
		try:
			response = PBR.open(self.imgUrl)
		except:
			print ("Fail to download {0}").format(self.title)
			return False
		
		illustHtml = response.read()
		illustSoup = BeautifulSoup(illustHtml)
		downIllustUrl = illustSoup.find("img")["src"]

		illustFileName = self._setSaveImgFileName(downIllustUrl, 
			saveNameArgs)
		self._saveImg(downIllustUrl, savePath, illustFileName)

	def _downComic(self, savePath, saveNameArgs):
		PBR.open(self.imgUrl)
		links = [l for l in PBR.links(
				url_regex = "^/member_illust\.php\?mode=manga_big&illust_id=")]
		
		comicPageNum = 0
		for imgLink in links:
			PBR.addheaders = [("Referer", self.imgUrl)]
			finalImgHtml = PBR.follow_link(imgLink).read()
			finalImgSoup = BeautifulSoup(finalImgHtml)
			finalImgUrl = finalImgSoup.find("img")["src"]
			
			newSaveNameArgs = list(saveNameArgs)
			newSaveNameArgs.append(str(comicPageNum))
			finalImgFileName = self._setSaveImgFileName(finalImgUrl, 
				newSaveNameArgs)
			self._saveImg(finalImgUrl, savePath, finalImgFileName)
			comicPageNum += 1

	def download(self, savePath, *saveNameArgs):
		"""
		작업물을 지정한 경로에 지정된 이름으로 저장하는 함수.

		:param savePath: 작업물이 저장될 폴더의 경로
		:type savePath: str.
		:param *saveNameArgs: Arguments 파라미터. 작업물의 이름을 구성하는 
		 요소를 *str.* 형으로 여러개 입력. ::

			Content.download('/Users/kimdongseok/Desktop', 'morry', '구려')

		"""
		if self.isIllust():
			self._downIllust(savePath, saveNameArgs)
		elif self.isComic():
			self._downComic(savePath, saveNameArgs)
