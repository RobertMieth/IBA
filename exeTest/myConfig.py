import json

def get(param):
	sysJson = open("system\sysdata.json")
	sysData = json.load(sysJson)
	try:
		return sysData[param]
	except:
		return
		
def update(param, new_value):
		pfad = "system\sysdata.json"
		sysJson = open(pfad)
		sysData = json.load(sysJson)
		sysData[param] = new_value
		with open(pfad, 'w') as f:
			json.dump(sysData, f)