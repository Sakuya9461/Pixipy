#-*- coding: utf-8 -*-
import requests
import collections
import re

SECURE_HOST = 'https://www.pixiv.net/'
HOST = 'http://www.pixiv.net/'
ERROR = '<span class="error">'
TOKKEN_PATTEN = '[0-9a-f]{32}'
R18 = 0
GROTESQUE = 1

class account(object):
	def __init__(self,name,pw):
		self.account = {"ID": name, "PW": pw}

	def login(self):
		self.session = requests.session()
		self.data = {"mode":"login", "pixiv_id":self.ID, "pass":self.PW}
		result = self.session.post(SECURE_HOST+'login.php',data=self.data)
		if ERROR in result.text:
			return "LOGIN ERROR"
		else:
			self.setuserinfo()
			return "LOGIN SUCCESS"

	def setuserinfo(self):
		result = self.session.get(HOST+'setting_user.php')
		enableOption = re.findall('name=\"[a-z_]+_[a-z]+\" value=\"[a-z0-9]+\" checked',result.text)

		if 'show' in enableOption[R18]:
			self.account.update({'R18':'show'})
		else:
			self.account.update({'R18':'hide'})

		if '2' in enableOption[GROTESQUE]:
			self.account.update({'GROTESQUE':'show'})
		else:
			self.account.update({'GROTESQUE':'hide'})
		return;

	def getuserinfo(self):
		ret = collections.OrderedDict()
		ret['ID'] = self.ID
		ret['R18'] = self.R18
		ret['GROTESQUE'] = self.GROTESQUE
		return ret;

	def updateuserinfo(self,data):
		result = self.session.get(HOST+'setting_user.php')
		tokken  = self.gettok(result.text.encode('utf-8'))
		data["mode"] = "mod"
		data["tt"] = tokken
		data["age_check"] = 1
		data["user_language"] = "ko"
		
		if data["user_x_restrict"] is "show":
			data["user_x_restrict"] = 2
		else:
			data["user_x_restrict"] = 1

		result = self.session.post(HOST+"setting_user.php",data=data)

	def gettok(self,result):
		tokken = re.search(TOKKEN_PATTEN,re.findall('name="tt" value=\"'+TOKKEN_PATTEN+'\"',result)[0])		
		return tokken.group()

	def __getattr__(self,attr):
		return self.account[attr]