# -*- coding: utf-8 -*-
'''
.. moduleauthor:: 김동석 <jalnagakds@gmail.com>

설명
--------------------------------------------

아티스트 모듈 입니다. 픽시브의 아티스트에 관한 정보를 담고 있는 
:class:`pypixiv.Artist` 클래스 하나로 구성되어 있습니다.

작업 내역
--------------------------------------------

* [2014/09/06] - 최초 사용 가능 버전 완성. 문서화를 위한 DocString 작업

--------------------------------------------
'''

from __future__ import unicode_literals

from bs4 import BeautifulSoup

from Browser import PBR
from Browser import PIXIV_URL
from Browser import PIXIV_MYPAGE_URL
from Browser import PIXIV_WORK_URL
from ContentsList import ContentsList


class Artist(object):
	"""
	아티스트의 ID나 북마크 페이지로부터 생성된 BeautifulSoup 객체로부터 아티스트
	정보를 생성하고 관리합니다.

	.. warning::
		* 처음 객체를 생성할때 아티스트 ID나 BeautifulSoup 객체를 반드시 입력해
		  야 합니다.
		* 객체가 생성 되었어도 세부 정보는 갖고 있지 않습니다. 반드시 
		  :func:`genDetailInfo()` 로 세부 정보를 생성 해야 제대로 사용 할 수 
		  있습니다.

	:param artistID: 아티스트 ID. 아티스트 웹페이지 주소의 'id=' 이후의 숫자.
	:type artistID: str.
	:param artistSoup: 북마크로부터 클래스를 생성하기 위한 파라미터.
	:type artistSoup: BeautifulSoup.

	"""
	def __init__(self, artistID = None, artistSoup = None):
		super(Artist, self).__init__()
		self.id = ""
		self.name = ""
		self.url = ""
		self.comment = ""
		self.profileImgUrl = ""
		self.smallProfileImgUrl = ""
		self.worksUrl = ""
		self.worksList = ContentsList()
		self.works = []
		
		if artistSoup != None:
			self.id = artistSoup["data-user_id"]
			self.name = artistSoup["data-user_name"]
			self.smallProfileImgUrl = artistSoup["data-profile_img"]
			self._genUrlFromID(self.id)
		elif artistID != None:
			self._genUrlFromID(artistID)

	def _genUrlFromID(self, inputID):
		self.id = inputID
		self.url = PIXIV_URL + "/member.php?id=" + self.id
		self.worksUrl = PIXIV_URL + "/member_illust.php?id=" + self.id
			
	def _genSmallProfileImgUrlFromOri(self, inputUrl):
		returnUrl = inputUrl
		splitUrl = returnUrl.split("/")
		imgFullFileName = splitUrl[-1]
		newImgFullFileName = ("mobile/" + imgFullFileName[:-4] + "_80" 
			+ imgFullFileName[-4:])
		
		self.smallProfileImgUrl = \
			returnUrl.replace(imgFullFileName, newImgFullFileName)

	def _genProfileImgUrlFromSoup(self, inputSoup):
		artistIDSoup = inputSoup.find("div", {"class":"_unit profile-unit"})
		self.profileImgUrl = artistIDSoup.find("img")["src"]
		self.smallProfileImgUrl = \
			self._genSmallProfileImgUrlFromOri(self.profileImgUrl)

	def _genNameFromSoup(self, inputSoup):
		artistIDSoup = inputSoup.find("div", {"class":"_unit profile-unit"})
		self.name = artistIDSoup.find("h1", {"class":"user"}).text

	def _genCommentFromSoup(self, inputSoup):
		commentSoup = inputSoup.find("tr", {"class":"profile-comment"})\
			.find("td", {"class":"td2"})
		self.comment = ""
		for content in commentSoup.contents:
			if content.name == "br":
				self.comment += "\n"
			else:
				self.comment += content.string

	def genDetailInfo(self):
		'''
		아티스트 세부 정보를 생성해 주는 함수.

		:returns: *bool* -- 성공하면 True, 실패시 False
		'''
		if self.hasID():
			artistHtml = PBR.open(self.url).read()
			artistSoup = BeautifulSoup(artistHtml)
			self._genProfileImgUrlFromSoup(artistSoup)
			self._genNameFromSoup(artistSoup)
			self._genCommentFromSoup(artistSoup)
			return True
		else:
			return False

	def hasID(self):
		'''
		아티스트가 ID를 갖고 있는지 테스트.

		:returns: *bool.*
		'''
		if self.id != "" and self.id != None:
			return True
		else:
			return False

	def getID(self):
		'''
		아티스트의 ID를 반환.

		:returns: *str, None.* -- ID가 없으면 None을 반환.
		'''
		if self.hasID():
			return self.id
		else:
			return None

	def getName(self):
		'''
		아티스트의 이름을 반환.

		:returns: *str, None* -- 이름이 없으면 None을 반환.
		'''
		if self.hasID():
			return self.name
		else:
			return None

	def getProfileImgUrl(self):
		'''
		170 * 170 크기의 프로필 이미지 주소를 반환.

		:returns: *str, None.* -- 이미지 주소가 없으면 None을 반환.
		'''
		if self.hasID():
			return self.profileImgUrl
		else:
			return None

	def getSmallProfileImgUrl(self):
		'''
		80 * 80 크기의 프로필 이미지 주소를 반환.

		:returns: *str, None.* -- 이미지 주소가 없으면 None을 반환.
		'''
		if self.hasID():
			return self.smallProfileImgUrl
		else:
			return None

	def getUrl(self):
		'''
		아티스트의 웹페이지 주소를 반환.

		:returns: *str, None.* -- 웹페이지 주소가 없으면 None을 반환.
		'''
		if self.hasID():
			return self.url
		else:
			return None

	def getComment(self):
		'''
		아티스트가 자신의 프로필에 써놓은 코멘트를 반환.

		.. note:: 코멘트는 무조건 문자열로 전환하여 가져옴.

		:returns: *str, None.* -- 코멘트가 없으면 None을 반환.
		'''
		if self.hasID():
			return self.comment
		else:
			return None

	def getWorks(self):
		'''
		아티스트의 작업물들을 :class:`pypixiv.Content` 형 List로 반환.

		:returns: *List, None.* -- 작업물이 없으면 None을
		          반환
		'''
		if self.hasID():
			if self.worksList.getNumTotal() == 0:
				self.worksList.appendContentPageHtml(self.worksUrl)
				self.worksList.genDetailInfo()
				self.works = self.worksList.getContents()
			return self.works
		else:
			return None
