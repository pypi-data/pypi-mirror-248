from MobileInventoryCLI.error.error import writeError,obj2dict

	
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from datetime import datetime,timedelta

class SelectList:
	def __str__(self):
		return 'SelectList'
	def __init__(self,engine,tbl,config,error_log):
		self.engine=engine
		self.tbl=tbl
		self.config=config
		self.error_log=error_log

		#self.displayListMenu()
		self.promptForAction()

	def promptForAction(self):
		while True:
			self.displayListMenu()
			action=input("what would you like to do?: ")
			if action.lower() in ["quit","6","q"]:
				exit("user quit")
			elif action.lower() in ["back","5","b"]:
				break
			else:
				try:
					try:
						value=int(action)
					except:
						value=action
					if value == 1 or action == "sl":
						self.search_lists()
					elif value == 3 or action == "sd":
						self.search_lists(isDeleted=1)
				except Exception as e:
					print(e)
					writeError(e,error_log=self.error_log)
	def getConfig(self,key=None):
		with self.config.open("r") as cfgfile:
			config=json.load(cfgfile)
			if key:
				return config.get(key)
			else:
				return config

	def search_lists(self,title=None,note=None,isDeleted=0):
		with Session(self.engine) as session:
			storageId=self.getConfig(key='storageId')
			query=session.query(self.tbl.List)
			if title:
				query=query.filter(self.tbl.List.Title==title)
			if note:
				query=query.filter(self.tbl.List.Note==note)
			query=query.filter(self.tbl.List.IsDeleted==isDeleted)
			query=query.filter(self.tbl.List.StorageId==storageId)
			results=query.all()
			data={}
			keys2Display=['ListId','Date','Title','Note','IsDeleted','UserId','StockChange','TypeId','StorageId','IsExported',]
			print(fg("light_green")+' '.join(keys2Display)+attr(0))
			for num,r in enumerate(results):
				data[num]=r
				asDict=obj2dict(r)
				print()
				for k in []:
					asDict.drop(k)
				ticks=asDict['Date']
				converted_ticks=datetime(1,1,1)+timedelta(microseconds=ticks/10)
				asDict['Date']=converted_ticks.ctime()
				
				try:
					line=[]
					for k in keys2Display:
						asDict[k]=asDict[k]
						if k in ["IsDeleted","IsExported"]:
							asDict[k]=bool(asDict[k])
						elif k == "StockChange":
							v=asDict[k]
							if v == 0:
								asDict[k]="NoChange"
							elif v == 1:
								asDict[k]="Incomming"
							elif v == 2:
								asDict[k]="Outgoing"
							elif v == 3:
								asDict[k]="Set"
						if asDict[k] == None:
							asDict[k]=''
						line.append("{}{}{}:{}'{}'{}\n".format(fg('light_green'),k,attr(0),fg('cyan'),asDict[k],attr(0)))
					l='----Entry {n0} Start----\n '+' '.join(line)+'----Entry {n1} Stop----'
					print(l.format(
						n1=str(fg("red")+str(num)+attr(0)),
						n0=str(fg("red")+str(num)+attr(0)),
					))
				except Exception as e:
					writeError(e,self.error_log)
				

	def displayListMenu(self):
		msg="""
		show Lists -> 1/sl
		goto List -> 2/gtl
		show deleted Lists -> 3/sd
		delete list -> 4/d/delete
		back -> 5/b/back
		quit -> 6/q/quit
		"""
		print(msg)
		return msg
