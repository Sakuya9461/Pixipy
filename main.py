#-*- coding: utf-8 -*-
from account import *
import search
import os
import time
import util
import sys

def clear():
	if os.name is 'nt':
		os.system('cls')
	else:
		os.system('clear')
		
def ModifySetting(account):
	info = account.getuserinfo()
	data = {"x_restrict" : info['R18'], "user_x_restrict" : info['GROTESQUE']}
	while True:
		clear()
		print "+==============================================================+"
		print "|%-30s : %-29s|" %(" 1. R18 Tag Search" ,data['x_restrict'])
		print "|%-30s : %-29s|" %(" 2. Groteqsue Tag Search" ,data['user_x_restrict'])
		print "|%-62s|" %" 3. Save and back to main"
		print "+==============================================================+"
		menu  = raw_input(">> ").strip()
		if menu is "1":
			if data["x_restrict"] is "show":
				data["x_restrict"] = "hide"
				data["user_x_restrict"] = "hide"
			else:
				data["x_restrict"] = "show"

		elif menu is "2":
			if data["user_x_restrict"] is "show":
				data["user_x_restrict"] = "hide"
			else:
				data["x_restrict"] = "show"
				data["user_x_restrict"] = "show"
		elif menu is "3":
			account.updateuserinfo(data)
			break;

	pass

def Selectpic(data,account):
	print "+------+-----------+----------+-------+---------------+--------------------+"
	print "| %-4s |   %-5s   |   %-4s   | %-5s |     %-7s   | %11s%7s |"%("RANK","SCORE", "TYPE", "PAGES","VIEWS","DATE"," ")
	print "+------+-----------+----------+-------+---------------+--------------------+"
	for i in range(1,len(data)):
		illust_type = 'ILLUST'
		try:
			if '1' in data[str(i)]['illust_type']:
				illust_type = ' MANGA'
			print "| %-4s |   %-5s   |  %-6s  | %-5s |     %-7s   | %11s%2s|"%(data[str(i)]['rank'],data[str(i)]['total_score'], illust_type, data[str(i)]['illust_page_count'],data[str(i)]['view_count'],data[str(i)]['date']," ")
		except:
			continue		
	print "+------+-----------+----------+-------+---------------+--------------------+"
	print "PS. 0 is download all."
	print "PS2. q is return to menu."
	while True:
		menu = raw_input("Input download number >>").strip()
		if menu =='q':
			break;
		elif menu != "0":
			util.Download(data[str(menu)],account)
		elif menu == "0":
			for i in range(1,len(data)):
				try:
					sys.stdout.write("\r%4d / %4d is now downloading.." %(i,len(data)))
					util.Download(data[str(i)],account)
				except:
					continue
		else:
			continue

def Ranked(account):
	menuArr = {"1" : "Daily", "2" : "Weekly", "3" : "Monthly", "4" : "Rookie", "5" : "Original"}
	Data ={"menu" : "Ranking", "mode" : None, "max" : 100}
	while True:
		clear()
		print "+==============================================================+"
		print "|%-62s|" %(" 1. Daily")
		print "|%-62s|" %(" 2. Weekly")
		print "|%-62s|" %(" 3. Monthly")
		print "|%-62s|" %(" 4. Rookie")
		print "|%-62s|" %(" 5. Original")
		print "|%-15s : %-44s|" %(" 6. MAX COUNT", str(Data['max']))
		print "+==============================================================+"
		menu = raw_input(">> ").strip()
		if menu is not "6":
			Data["mode"] = menuArr[menu]
			s = search.Search(Data)
			Selectpic(s.result,account)
			return;
		else:
			tmp = int(raw_input("Max Count >> ").strip())
			if tmp > 1000:
				print "Too Big.."
				time.sleep(2)
				continue;
			Data['max'] = tmp

def Search(account):
	data = {"word" : ""}
	print "+==============================================================+"
	print "|%-30s : %-29s|" %(" 1. TAG" ,data['word'])
	print "|%-30s : %-29s|" %(" 2. R18" ,data['user_x_restrict'])
	print "|%-62s|" %" 3. Save and back to main"
	print "+==============================================================+"
	pass

def Showlists(account):
	print "show"
	pass

def Exit(account):
	exit(1)
	pass

def showmenu(data):
 	print "+==============================================================+"
	print "| ID : %-56s|" %data['ID']
	print "| R18 : %-55s|" %data['R18']
	print "| GRO : %-55s|" %data['GROTESQUE']
	print "+==============================================================+"
	print "|%-62s|" %" 1. Modify settings (R18, GRO)"
	print "|%-62s|" %" 2. Search"
	print "|%-62s|" %" 3. Ranked Images"
	print "|%-62s|" %" 4. Show download lists"
	print "|%-62s|" %" 5. Exit"
	print "+==============================================================+"
	return

if __name__ == "__main__":
	clear()
	banner = """ .----------------. .----------------. .----------------. .----------------. .----------------. 
| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |
| |   ______     | | |     _____    | | |  ____  ____  | | |     _____    | | | ____   ____  | |
| |  |_   __ \   | | |    |_   _|   | | | |_  _||_  _| | | |    |_   _|   | | ||_  _| |_  _| | |
| |    | |__) |  | | |      | |     | | |   \ \  / /   | | |      | |     | | |  \ \   / /   | |
| |    |  ___/   | | |      | |     | | |    > `' <    | | |      | |     | | |   \ \ / /    | |
| |   _| |_      | | |     _| |_    | | |  _/ /'`\ \_  | | |     _| |_    | | |    \ ' /     | |
| |  |_____|     | | |    |_____|   | | | |____||____| | | |    |_____|   | | |     \_/      | |
| |              | | |              | | |              | | |              | | |              | |
| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |
 '----------------' '----------------' '----------------' '----------------' '----------------' """
	menufunc = {"1": ModifySetting, "2": Search, "3":Ranked, "4": Showlists, "5":Exit }
	acc = account("id","pw")
	if 'ERROR' in acc.login():
		print "ID or PW is invalid. Try again."
	        exit(1)
	else:
		while True:
			clear()
			print banner;
			showmenu(acc.getuserinfo())
			menu = raw_input(">> ").strip()
			if menu is not '':
				clear()
				menufunc[menu](acc)
