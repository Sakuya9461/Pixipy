#-*- coding: utf-8 -*-
import requests
import re
import util
import collections
import sys

RANK="http://www.pixiv.net/ranking.php"
class Search(object):
	def __init__(self, arg):
		self.Funclist = {"Ranking":self.Ranking}
		self.ret = self.Funclist[arg['menu']](arg)

	def Ranking(self,arg):
		session = requests.session()
		ret = collections.OrderedDict()
		for p in range(1,(arg['max']/50)+1):
			result = session.get(RANK+"?p="+str(p)+"&format=json&mode="+arg['mode'])
			data = util.jsonparse(result.text)
			for i in data['contents']:
				ret[str(i['rank'])] = {"rank":str(i['rank']),
								'date' : str(i['date'].encode('utf-8').replace('\xe5\xb9\xb4',"-").replace('\xe6\x9c\x88',"-").replace('\xe6\x97\xa5'," ")),
								'illust_upload_timestamp' : str(i['illust_upload_timestamp']),
								'illust_id' : (i['illust_id']) ,
								'illust_type' : str(i['illust_type']),
								'view_count' : str(i['view_count']),
								'width' : str(i['width']), 
								'height' : str(i['height']), 
								'illust_page_count' : str(i['illust_page_count']), 
								'total_score' : str(i['total_score']), 
								'illust_content_type' : str(i['illust_content_type'])}
		ret['mode']=arg['mode']
		return ret;
	def __getattr__(self,attr):
		return self.ret
