from MobileInventoryCLI.error.error import writeError,obj2dict

	
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from datetime import datetime

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
			if action.lower() in ["quit","6"]:
				exit("user quit")
			elif action.lower() in ["back","5"]:
				break
			else:
				try:
					value=int(action)
					if value == 1:
						self.search_lists()
				except Exception as e:
					print(e)
					writeError(e,error_log=self.error_log)

	def search_lists(self,title=None,note=None,isDeleted=0):
		with Session(self.engine) as session:
			query=session.query(self.tbl.List)
			if title:
				query=query.filter(self.tbl.List.Title==title)
			if note:
				query=query.filter(self.tbl.List.Note==note)
			query=query.filter(self.tbl.List.IsDeleted==isDeleted)
			results=query.all()
			data={}
			for num,r in enumerate(results):
				data[num]=r
				asDict=obj2dict(r)
				for k in []:
					asDict.drop(k)
				ticks=asDict['Date']
				print(num,asDict)

	def displayListMenu(self):
		msg="""
		show Lists -> 1
		
		goto List -> 2
		show deleted Lists -> 3
		delete list -> 4
		back -> 5
		quit -> 6
		"""
		print(msg)
		return msg
