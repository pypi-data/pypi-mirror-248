#summarize_list.py
import os,json,base64,string
from MobileInventoryCLI.error.error import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from colored import Fore,Back,Style
from datetime import datetime

class SummarizeList:
	def __str__(self):
		return "SummarizeList (Better for ScreenShots)"


	def listById(self):
		while True:
			try:
				listid_user=input("ListId/q/b: ")
				if listid_user.lower() in ['q','quit']:
					exit("user quit!")
				elif listid_user.lower() in ['b','back']:
					break
				else:
					listid_user=int(round(float(listid_user),0))
					with Session(self.engine) as session:
						ListName=session.query(self.tbl.List.Title).filter(self.tbl.List.ListId==listid_user).first()
						if ListName:
							query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid_user)
							items=query.all()
							h="{start}Name{end}|{start}Qty{end}|{start}bCode{end}|{start}SKU{end}|{start}iPrice{end}|{start}i/Ttl{end}".format(start=Fore.yellow,end=Style.reset)
							br=str('-'*20)
							print(br)
							print(ListName.Title)
							print(br)
							
							print(h)
							print(br)
							end=' -({}/{})-'
							for num,r in enumerate(items):
								line=[]
								line.append(r.ItemName)
								line.append(r.Quantity)
								line.append(r.ItemBarcode)
								line.append(r.ItemCode)
								line.append(r.ItemPrice)
								line.append(end.format(str(num+1),str(len(items))))
								line=[str(i) for i in line]
								if num % 2 == 0:
									print(Fore.cyan+'|'.join(line)+Style.reset)
								else:
									print(Fore.light_green+'|'.join(line)+Style.reset)
							print(br)
							
						else:
							raise Exception("No Such List! {}".format(listid))
				break
			except Exception as e:
				writeError(e,self.error_log)

	def searchAndSelect(self):
		menu=["Search and Select Menu",]

	def __init__(self,engine,config,tbl,error_log):
		self.error_log=error_log
		self.tbl=tbl
		self.config=config
		self.engine=engine

		self.cfg=getConfig(self)
		cmdlist={
		'1':{
			'names':['1','quit','q','exit'],
			'exec':lambda :exit("user quit")
			},
		'2':{
			'names':['2','back','b','prev'],
			'exec':False,
			},
		'3':{
			'names':['ListById','lbid','3'],
			'exec':lambda self=self:self.listById(),
			},
		'4':{
			'names':['searchselect','ss','4','search-select'],
			'exec':lambda self=self:self.searchAndSelect(),
			}
		}
		while True:
			for k in cmdlist:
				print(k,cmdlist[k]['names'])
			cmd=input("Do what? ")
			for k in cmdlist:
				if cmd.lower() in cmdlist[k]['names']:
					if k == '2':
						return
					else:
						cmdlist[k]['exec']()

