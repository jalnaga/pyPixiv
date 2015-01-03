# pyPixiv

파이썬을 사용해 픽시브에서 이미지를 긁어오는 모듈 입니다. 자신이 팔로잉 하는 아티스트 목록을 통해, 각 아티스트의 작품들을 가져 옵니다.

## 사용법

```
from pypixiv import Pixiv

def main():
	pixiv = Pixiv()
	pixiv.login(loginPass = "픽시브 패워드", loginID = "픽시브 아이디")
	testWork = pixiv.getWorkByUrl("http://www.pixiv.net/member_illust.php?mode=medium&illust_id=44777994")
	testWork.genDetailInfo()
	print testWork.getTitle()
	print testWork.getScoreCount()
	print testWork.getDate()
	print testWork.getArtistName()
	print testWork.getArtistID()


if __name__ == '__main__':
	main()
```