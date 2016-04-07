#-*- coding: utf-8 -*-

import json
import requests
import os
import re
import time

HOST="http://www.pixiv.net/"
def jsonparse(data):
    js = json.loads(data)
    return js

def Download(data,account):
	now =time.localtime()
	timestamp = str(now.tm_year)+"_"+str(now.tm_mon)+"_"+str(now.tm_mday)
	URL ="member_illust.php?mode=medium&illust_id="+str(data['illust_id'])
	DIR='./DOWN/'+timestamp+"/"
	if not os.path.exists(DIR):
		os.makedirs(DIR)

	s = account.session
	r = s.get(HOST+URL)
	URL = re.findall("member_illust.php\?mode=[a-z]+&amp;illust_id="+str(data['illust_id']),r.text.encode('utf-8'))[-2].replace("&amp;","&")
	Referer = HOST+URL
	if not os.path.exists(DIR+str(data['illust_id'])):
		os.mkdir(DIR+str(data['illust_id']))
	DIR += str(data['illust_id'])+"/"

	if data['illust_page_count'] != '1':
		if not os.path.exists(DIR+"MANGA"+str(data['illust_upload_timestamp'])):
			os.mkdir(DIR+"MANGA"+str(data['illust_upload_timestamp']))
		DIR += "MANGA"+str(data['illust_upload_timestamp'])+"/"
		r = s.get(HOST+URL)
		lists = re.findall("member_illust.php\?mode=[a-z_]+&amp;illust_id="+str(data['illust_id'])+"&amp;page=[0-9]+",r.text)

		for i in lists:
			r = s.get(HOST+i)
			pic = "http://"+re.findall('i[0-9]+\.pixiv\.net/[a-zA-Z0-9/\._\-]+',r.text)[0]
			ext = pic.split('.')[-1]
			r= s.get(pic,headers={'referer':Referer})
			filename = str(DIR+"MANGA_"+str(data['illust_upload_timestamp'])+"_"+i.split('=')[-1]+"."+ext).encode('ascii','ignore')
			picDown(r,filename)
	else:
		r = s.get(Referer)
		picpage = HOST+re.findall("member_illust.php\?mode=[a-z_]+&amp;illust_id="+str(data['illust_id']),r.text)[0]
		r = s.get(picpage)
		pic = "http://"+re.findall('i[0-9]+\.pixiv\.net/img-original[a-zA-Z0-9/\._\-]+',r.text)
		if len(pic) >0 :
			pic = pic[0]
		else:
			return;
		r = s.get(pic,headers={'referer':Referer})
		filename = str(DIR+pic.split('/')[-1]).encode('ascii','ignore')
		picDown(r,filename)

def picDown(r,filename):
	if r.status_code == 200:
	    with open(filename, 'wb') as f:
	        for chunk in r.iter_content(1024):
	            f.write(chunk)    