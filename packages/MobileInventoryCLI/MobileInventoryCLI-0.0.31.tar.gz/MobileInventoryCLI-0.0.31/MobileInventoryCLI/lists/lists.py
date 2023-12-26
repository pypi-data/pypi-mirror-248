from MobileInventoryCLI.error.error import writeError,obj2dict

	
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from datetime import datetime,timedelta


class GotoLists:
	def __str__(self):
		return "GotoLists/gtl/2"

	def __init__(self,config,engine,tbl,error_log):
		self.tbl=tbl
		self.error_log=error_log
		self.config=config
		self.engine=engine
		self.cfg=self.getConfig()
		self.promptForAction()

	def displayListItemMenu(self):
		msg="""
		{row1}strings with a return line that do not start with '#' 
		symbol and will search barcode|code|itemid and use 
		the first located item, and will be treated as entries
			-if this is not correct please see below[r2u]{end}

		{row0}"+[num]" will search for an entry, if there is none, 
			make one, and increment its quantity by the number 
			provided after the plus[r2u]{end}

		{row1}"-[num]" will search for an entry, if there is none, 
			make one, and decrement its quantity by the number 
			provided after the minus[r2u]{end}

		{row0}"#quit" "#q" "#6" will exit the application [r2u]{end}

		{row1}"#deleteItem [ListItemId]" or "#deleteItem" "#di [ListItemId]" or "#di"  
		will search for item identified by ListItemId provided 
		immediately after cmd, or the immediate last ListItemId 
		entered if none is provided. [r2u]{end}

		{row0}"#back" "#b" "#5" will go back a menu [r2u]{end}

		{row1}"#search" "#s" will search for codes using code|barcode|itemid|name|note
		 and display them with a prompt to select code for use{end}-

		{row0}"#barcode []" will only search barcode field{end}-

		{row1}"#itemCode [] will only search code field{end}-

		{row0}#itemid []" will only search itemid field{end}-

		{row1}"#?" will display THIS [r2u]{end}

		{row0}"#showBarcode" [barcode] displays item by barcode in List[r2u]{end}
		{row1}'cyan colored items existed in list{end}
		{row0}'green' colored items were just created in list{end}
		"""
		msg=msg.format(row0=fg("red"),row1=fg("green"),end=attr(0))
		print(msg)
		return msg

	def searchAndCreate(self,itemcode,listid,icr=None,dcr=None,mode="insert"):
		with Session(self.engine) as session:
			query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid)
			result=query.filter(or_(self.tbl.ListItem.ListItemId==itemcode,self.tbl.ListItem.ItemCode==itemcode,self.tbl.ListItem.ItemBarcode==itemcode))					
			r=result.first()
			if r:
				if icr:
					r.Quantity+=icr
				elif dcr:
					r.Quantity+=dcr
				else:
					r.Quantity+=1
				session.commit()
				session.flush()
				session.refresh(r)
				d=obj2dict(r)
				self.printListItem(r,created=False)
				
			else:
				resultSub=session.query(self.tbl.Item).filter(self.tbl.Item.StorageId==self.cfg.get('storageId'))
				resultSub=resultSub.filter(or_(self.tbl.Item.ItemId.icontains(itemcode),self.tbl.Item.Code.icontains(itemcode),self.tbl.Item.Barcode.icontains(itemcode)))
				rSub=resultSub.first()
				print(rSub)
				if rSub != None:
					newLI=self.tbl.ListItem()
					for field in rSub.__table__.columns:
						try:
							f="Item{}".format(field.name)
							v=getattr(rSub,field.name)
							setattr(newLI,f,v)
						except Exception as e:
							"#ignore"
							writeError(e,self.error_log)
					setattr(newLI,"ListId",listid)
					setattr(newLI,"ItemId",rSub.ItemId)
					setattr(newLI,"Quantity",1)

					session.add(newLI)
					session.commit()
					session.flush()
					session.refresh(newLI)
					#d=obj2dict(newLI)
					#d=obj2dict(r)
					
				
					cf=session.query(self.tbl.ItemCustomField).filter(self.tbl.ItemCustomField.ItemId==rSub.ItemId).all()
					for c in cf:
						nlcf=self.tbl.ListItemCustomField()
						
						nlcf.ListItemId=newLI.ListItemId
						nlcf.Value=c.Value
						nlcf.CustomFieldId=c.CustomFieldId

						session.add(nlcf)
						session.commit()
					self.printListItem(newLI,created=True)
				#make new ListItem with Corresponding fields and custom fields
				pass
	def printListItem(self,listItem,created=True,printCF=False):
		d=obj2dict(listItem)
		for k in d.keys():
			if k == "ListItemId":
				print(attr(5)+k+attr(0)+":"+fg("red")+str(d[k])+attr(0))
			elif k == "Quantity":
				print(attr(5)+k+attr(0)+":"+fg("yellow")+str(d[k])+attr(0))
			else:
				if created:
					print(k+":"+fg("green")+str(d[k])+attr(0))
				else:
					print(k+":"+fg("cyan")+str(d[k])+attr(0))
		if printCF:
			with Session(self.engine) as session:
				if isinstance(listItem,self.tbl.ListItem):
					cf=session.query(self.tbl.ListItemCustomField).filter(self.tbl.ListItemCustomField.ListItemId==listItem.ListItemId).all()
				elif isinstance(listItem,self.tbl.Item):
					cf=session.query(self.tbl.ItemCustomField).filter(self.tbl.ItemCustomField.ItemId==listItem.ItemId).all()
				else:
					raise Exception(listItem)
				
				for num,c1 in enumerate(cf):
					print("---CF {}---".format(num))
					cfname=session.query(self.tbl.CustomField).filter(self.tbl.CustomField.CustomFieldId==c1.CustomFieldId).first()	
					if cfname:
						for col in c1.__table__.columns:
							if col.name == "Value":
								print("{f}Name{e}: {v}".format(f=fg("blue"),e=attr(0),v=cfname.Name))
								print("{f}Type{e}: {v}".format(f=fg("blue"),e=attr(0),v=cfname.Type))
								print("{f}Value{e}: {v}".format(f=fg("blue"),e=attr(0),v=c1.Value))
							else:
								print("{s}{f}{e}: {v}".format(e=attr(0),s=fg("green"),f=col,v=getattr(c1,col.name)))
					print("---CF {}---".format(num))

	def searchAndDelete(self,code):
		try:
			with Session(self.engine) as session:
				query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListItemId==int(code)).delete()
				session.commit()
				print(query)
		except Exception as e:
			writeError(e,self.error_log)

	def showList(self,listid):
		try:
			with Session(self.engine) as session:
				query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ListId==listid).all()
				for num,row in enumerate(query):
					print("=======Entry {}/{} Start=========".format(num,len(query)))
					if num % 2 == 0:

						self.printListItem(row,created=False,printCF=True)
					else:
						self.printListItem(row,created=True,printCF=True)
					print("=======Entry {}/{} End=========".format(num,len(query)))
		except Exception as e:
			writeError(e,self.error_log)

	def checkList(self,listid):
		with Session(self.engine) as session:
			try:
				listExists=session.query(self.tbl.List).filter(self.tbl.List.ListId==listid).first()
				if listExists:
					return True
				else:
					return False

			except Exception as e:
				writeError(e,self.error_log)
	def showListItemBarcode(self,code,returnable=False):
		with Session(self.engine) as session:
			query=session.query(self.tbl.ListItem).filter(self.tbl.ListItem.ItemBarcode==code)
			result=query.first()
			if result:
				if returnable:
					return obj2dict(result)
				else:
					if input("print custom fields? [y/N]").lower() in ['y','yes']:
						self.printListItem(result,printCF=True)
					else:
						self.printListItem(result,created=True,printCF=False)

	def promptForAction(self):
		listid=None
		listTitle=None
		while True:
			listid=input("listid/#q/#b: ")
			if listid.lower() in ["#q","#quit"]:
				exit("user quit!")
			elif listid.lower() in ["#b","#back"]:
				return
			try:
				listid=int(listid)
				if self.checkList(listid):
					break
				else:
					print("that list does not exist!")
			except Exception as e:
				writeError(e,self.error_log)
		while True:
			action=input("code/#[cmd]/#quit/#back/#show/#?: ")
			if action.lower() in ["#quit","#6","#q"]:
				exit("user quit")
			elif action.lower() in ["#back","#5","#b"]:
				break
			elif action.lower() == "#?":
				self.displayListItemMenu()
			elif action.split(' ')[0] in ["#deleteItem","#di"]:
				code=''
				if len(action.split(" ")) > 1:
					code=action.split(" ")[-1]
				else:
					code=input("ListItemId to delete: ")
				self.searchAndDelete(code)
			elif action.lower() == "#show":
				self.showList(listid)
			elif action.split(" ")[0] == "#showBarcode":
				if len(action.split(" ")) > 1:
					self.showListItemBarcode(action.split(" ")[-1])
				else:
					p=input("itembarcode: ")
					if p.lower() in ["#q","#quit"]:
						exit("user quit!")
					elif p.lower() in ["#b",'#back']:
						break
					else:
						self.showListItemBarcode(p)
			else:
				try:
					if action.startswith("+"):
						try:
							icr=float(action[1:])
						except Exception as e:
							icr=1
						code=input("code/q/skip: ")
						self.searchAndCreate(code,listid,icr=icr)
					if action.startswith("-"):
						try:
							dcr=-float(action[1:])
						except Exception as e:
							dcr=-1
						code=input("code/q/skip: ")
						self.searchAndCreate(code,listid,dcr=dcr)
					else:
						code=action
						self.searchAndCreate(code,listid)

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
					elif value == 2 or action == "gtl":
						GotoLists(self.config,self.engine,self.tbl,self.error_log)
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
