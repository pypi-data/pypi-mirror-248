import csv,json
def writeError(e,error_log):
	print(e)
	with error_log.open("a") as log:
		writer=csv.writer(log,delimiter=";")
		writer.writerow([str(e),])
		writer.writerow([repr(e),])
		
def obj2dict(obj):
	d={}
	for col in obj.__table__.columns:
		d[col.name]=getattr(obj,col.name)
	return d

def getConfig(self,key=None):
		with self.config.open("r") as cfgfile:
			config=json.load(cfgfile)
			if key:
				return config.get(key)
			else:
				return config