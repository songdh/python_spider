#!/usr/local/bin/python3
#coding=utf-8

import urllib.request
import urllib.error
import re
import sys
import os

path = os.path.join(sys.path[0],'page')


def savePageToFile(page):
	#只是记录当前要查看页面的页码
	with open(path,'w') as fo:
		if fo:
			fo.write(str(page))
			fo.close()

def getPageInFile():
	#只是读取当前要查看页面的页码
	try:
		with open(path,'r') as fo:
			if fo:
				content = fo.read()
				return int(content)
			else:
				return 0
	except:
		return 0

def responseWithPage(page):
	url = "http://www.qiushibaike.com/hot/page/" + str(page)
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
	headers = {"User-Agent":user_agent}
	request = urllib.request.Request(url,headers=headers)

	try:
		response = urllib.request.urlopen(request)
	except urllib.error.HTTPError as e:
		print(e.code)
	except urllib.error.URLError as e:
		print(e.reason)
	else:
		pass

	return response


def printFormatResponse(response):
	content = response.read().decode('utf-8')
	parttern = r'<div class="author clearfix">.*?href=.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>(.*?)</div>.*?'
	match = re.compile(parttern,re.S)
	items = re.findall(match,content)
	
	for item in items:
		if len(item) >= 1:
			print('authen:' + item[0])

		if len(item) >= 2:
			article = item[1].replace('<br/>','\n')
			print(article)

		if len(item) >= 3:
			#取出字符串中的图片
			parttern = r'<div class="thumb">.*?<img src="(.*?)".*?/>.*?'
			match = re.compile(parttern,re.S)
			imageItems = re.findall(match,item[2])

			for img in imageItems:
				print('图片地址:' + img + '\n')
			
		print('\n')


if __name__=='__main__':
	argvs = sys.argv
	if len(argvs) >= 2:
		page = argvs[1]
		savePageToFile(page)
	else:
		page = getPageInFile()
		savePageToFile(page+1)

	page = getPageInFile()
	print("""
*************************************************
		第%d页
*************************************************
		""" % page)

	response = responseWithPage(page)
	printFormatResponse(response)


