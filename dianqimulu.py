import requests
import re
from bs4 import BeautifulSoup
aimUrl1="https://tieba.baidu.com/p/5856228534?see_lz=1&pn=1"
aimUrl2="https://tieba.baidu.com/p/5856228534?see_lz=1&pn=2"
aimUrl3="https://tieba.baidu.com/p/5856228534?see_lz=1&pn=3"
aimfile="二十世纪电气目录.txt"
def changeBrToReturn(tag):
	tag=str(tag)
	tag=tag.replace("<br/>","\n")
	try:
		soup=BeautifulSoup(tag,"html.parser")
	except Exception as e:
		print(tag[0:100]+'---提取失败')
	else:
		pass
	finally:
		pass
	#print(tag)
	return soup

#获取页面
def getHtmlContent(url):
	#get方法请求到页面
	res=requests.get(url)
	#print(res.text[0:1000])
	#返回页面内容
	return res.text
#把小说内容存入文本
def makeHtmlContentToText(text):
	#制作soup
	soup=BeautifulSoup(text,"html.parser")
	#查找所有id是postcontent开头的盒子
	posts=soup.find_all('div',attrs={'id':re.compile('post_content_*')})
	changeBrToReturn(posts[3])
	#print(text)
	#小说内容
	outText=""
	#对所有楼主发表的文章进行文本提取和把<br>标签换成换行符
	for post in posts:
		post=changeBrToReturn(post)
		#print(post)
		#执行替换
		strtemp=post.text
		#加入文本
		outText+=strtemp
	#print(outText)
	return outText

if "__main__"==__name__:
	print("Hello PY!")
	content1=getHtmlContent(aimUrl1)
	text1=makeHtmlContentToText(content1)
	content2=getHtmlContent(aimUrl2)
	text2=makeHtmlContentToText(content2)
	content3=getHtmlContent(aimUrl3)
	text3=makeHtmlContentToText(content3)
	#print(text1+text2+text3)
	f=open(aimfile,"a+",encoding='utf-8')
	f.write(text1+text2+text3)
	f.close()
