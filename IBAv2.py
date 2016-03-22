#Stoped 2016-02-16: load_data funktion, muss erkennen lernen ob ein Datum vorliegt, next: items in Listboy auswählen


import tkinter as tk
from PIL import Image, ImageTk

import openpyxl as pxl

import psycopg2

from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import argparse

import gspread
import json

from dateutil import parser
import datetime

#Object that can obtain and save data from google Spreadsheets
class GoogleGrabber():
	
	def __init__(self):
		self.cred_path = "system\iba_google_credential"
		self.client_secret = "system\client_secret.json"
		self.storage = Storage(self.cred_path)
		self.redirect_uri='urn:ietf:wg:oauth:2.0:oob'
		self.scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds'
		self.credentials = self.storage.get()
		
		self.sysJson = open("system\sysdata.json")
		self.sysData = json.load(self.sysJson)
		
		#Data Storage
		self.session_planungsdaten = []
		
	
	def get_planungsdaten(self):
		self.get_credentials()
		gSheet = self.sysData["planungSpread"]
		
		GSpread = gspread.authorize(self.credentials)
		act_sh = GSpread.open(gSheet)
		wks = act_sh.sheet1
		
		planungsdaten = wks.get_all_records(empty2zero=True, head=2)
		planungsdaten = self.clean_data(planungsdaten)
		
		self.session_planungsdaten = planungsdaten
		return planungsdaten
		
	def get_credentials(self):
		try:
			token = self.credentials.get_access_token
			if self.credentials.access_token_expired:
				self.credentials = self.obtain_new_credential()
		except:
			self.credentials = self.obtain_new_credential()
	
	def obtain_new_credential(self):
		parser = argparse.ArgumentParser(parents=[tools.argparser])
		flags = parser.parse_args()
		
		flow = flow_from_clientsecrets(self.client_secret, scope=self.scope, redirect_uri=self.redirect_uri)
		credentials = tools.run_flow(flow,self.storage,flags)
		
		self.storage.put(credentials)
		print('Obtained new Google Credential')
		
		return credentials    
		
	def clean_data(self, sheetData):
		#Entfernt HeaderZeilen und alle Einträge ohne geplantes Installationsdatum
		sheetData.pop(0)
		sheetData.pop(0)
		remove = []
		for s in sheetData:
			if s['Datum Installation']==0:
				remove.append(sheetData.index(s))
		
		for rem in sorted(remove, reverse=True):
			del sheetData[rem]
		
		return sheetData
		
#Read and write Data from Excel files
class ExcelHandler():
	#TODO
	def __init__(self):
		self.sysJson = open("system\sysdata.json", 'r')
		self.sysData = json.load(self.sysJson)
		
		self.get_data_paths()
		
	def get_data_paths(self):
		dataXl = pxl.load_workbook(filename = "system\was_liegt_wo.xlsx")
		dataWs = dataXl.get_sheet_by_name("Main")
		
		self.evaPath = dataWs['C3'].value
		self.mstPath = dataWs['D3'].value
		self.ststPath = dataWs['E3'].value
		self.komplexPath = dataWs['F3'].value
		self.vnbPath = dataWs['G3'].value
		
		ident = dataWs['A4:A60']
		
		#evaDict
		evaCol = dataWs['C4:C60']
		evaDict = self.range2dict(ident,evaCol)
		
		#mstDict
		mstCol = dataWs['D4:D60']
		mstDict = self.range2dict(ident,mstCol)
		
		#ststDict
		ststCol = dataWs['E4:E60']
		ststDict = self.range2dict(ident,ststCol)
		
		#komplexDict
		kompexCol = dataWs['F4:F60']
		komplexDict = self.range2dict(ident,kompexCol)
		
		#vnbDict
		vnbCol = dataWs['G4:G60']
		vnbDict = self.range2dict(ident,vnbCol)
		
		#isDbDict
		isDbCol = dataWs['H4:H60']
		isDbDict = self.range2dict(ident,isDbCol)

		
	def range2dict(self, range1, range2):
		range1List = []
		for r1 in range1:
			for cell in r1:
				range1List.append(cell.value)
				
		range2List = []
		for r2 in range2:
			for cell in r2:
				range2List.append(cell.value)
				
		return dict(zip(range1List,range2List))
	
		
		
	#def update_sysdata(self, param, new_value):
	#	self.sysData[param] = new_value
	#	with open("system\sysdata2.json", 'w') as f:
	#		json.dump(self.sysData, f)	

		
class DbHandler():

	def __init__(self):
		self.cursor = self.connect()

	def connect(self):
		conn_string = "host='localhost' port='5432' dbname='solandeo_operations' user='reader' password='Segoa5oopheleePhah1Aish' client_encoding='utf8'"
	
		print ("Connecting to database\n")
	
		conn = psycopg2.connect(conn_string)
	
		cursor = conn.cursor()
		print ("Connected to Database!\n")
	
		return cursor	

	def get_daten_mst(self, msliste_str):
		query = "select * from dbfrontend_messstelle as mst where mst.id in " + msliste_str
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def get_daten_technologie(self, msliste_str):
		query = "select mst.id, eva.technologie from dbfrontend_messstelle as mst, dbfrontend_eva as eva where mst.id = eva.messstelle_id and mst.id in " + msliste_str
		self.cursor.execute(query)
		return self.cursor.fetchall()
	
		
		
#GUI App
class IbaTK(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background = "white")
		self.parent = parent
		self.version = "(C) Solandeo - Version 2016-02-16.2.0a"
		
		sysJson = open("system\sysdata.json",'r')
		self.sysData = json.load(sysJson)
		
		self.google = GoogleGrabber()
		self.excel = ExcelHandler()
		self.db = DbHandler()
		
		self.build()	
		
	def build(self):
	#Builds main Programmm Window
	
		self.parent.title("Solandeo - Installationsbelege Assistent")
		self.pack(fill='both', expand =False)
		
		#Menu Bar
		menubar = tk.Menu(self.parent)
		self.parent.config(menu=menubar)
		
		sysMenu = tk.Menu(self.parent)
		sysMenu.add_command(label="Einstellungen", command=self.find_path)
		menubar.add_cascade(label="System", menu=sysMenu)
		
		helpMenu = tk.Menu(self.parent)
		helpMenu.add_command(label="Hilfe", command=self.help_me)
		menubar.add_cascade(label="Hilfe", menu=helpMenu)
		
		#Rest of Layout
		self.rowconfigure(1, pad = 5)
		self.rowconfigure(2, pad = 10)
		self.rowconfigure(4, pad = 10)
		self.columnconfigure(1, pad = 10)
		self.columnconfigure(2, pad = 10)
		
		logo = Image.open("gui\solandeo_logo.png")
		logoObj = ImageTk.PhotoImage(logo)
		logoLabel = tk.Label(self, image=logoObj, bg="white")
		logoLabel.image = logoObj # to keep a reference
		logoLabel.grid(sticky='NW', column=1, row=1, padx = 3)
		
		text1 = tk.Label(self, text="Assistent zur Erstellung von\n Installationsbelegen", bg="white")
		text1.grid(sticky='NE', column=2, row=1, padx = 3)
		
		text2 = tk.Label(self, text="Derzeit geplante Installationen:", bg="white")
		text2.grid(sticky='W', column=1, row=4, pady = 5)
		
		loadBtn = tk.Button(self, text="Installationsdaten laden", command=self.load_data, height=2, width=25)
		loadBtn.grid(column=1, row=3)
		
		processBtn = tk.Button(self, text="Daten verarbeiten", command=self.process_data, height=2, width=25)
		processBtn.grid(column=2, row=3, columnspan=2)
		
		scrollY = tk.Scrollbar(self, orient='vertical')
		scrollX = tk.Scrollbar(self, orient='horizontal')
		dataBox = tk.Listbox(self, height=27, width = 60, selectmode='extended', yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)
		dataBox.insert('end', "<<Noch keine Daten>>")
		dataBox.grid(column=1, row=5, columnspan=2)
		self.guiListe = dataBox #external Reference
		scrollY.config(command=dataBox.yview)
		scrollY.grid(column=3, row = 5)
		scrollX.config(command=dataBox.xview)
		scrollX.grid(column=2, row = 6)
		
		version =tk.Label(self, text=self.version, bg="white")
		version.grid(column= 1, row=6, pady=5)
		
	
	def load_data(self):
		#Loads Data of currently planned Installations
		planungsdaten = self.google.get_planungsdaten()
		self.guiListe.delete(0,'end')
		for d in planungsdaten:
			addStr = str(d['Datum Installation']) + " - " + str(d['Nummer MST/STST']) + " - " + str(d['Name'])
			self.guiListe.insert('end', addStr)
		self.get_to_front()
		
		
	def process_data(self):
		#Processes the gathered Data
		auswahl = map(int, self.guiListe.curselection())
		planungsdaten = self.google.session_planungsdaten
		todoPlanung = []  
		for a in auswahl:
			todoPlanung.append(planungsdaten[a])
		msListe = []
		for m in todoPlanung:
			msListe.append(m["Nummer MST/STST"])
		msString = "(" + str(msListe).strip('[]') + ")"
		todoMessstelle = self.db.get_daten_mst(msString)
		todoTechnologie = self.db.get_daten_technologie(msString)
		print(todoTechnologie)
		
		
	def find_path(self):
		#Dialog zur Einstellung der Excel Dateien
		print("TODO")
		
		
	def help_me(self):
		#Kurzes Hilfemenue
		print("TODO")
		
	def get_to_front(self):
		self.parent.attributes('-topmost', 1)
		self.parent.attributes('-topmost', 1)

		
def main():
	
	#Build Gui Root
	tkRoot = tk.Tk()
	tkRoot.geometry("440x600+300+300")
	tkRoot.resizable(width=False, height=False)
	ibaIns = IbaTK(tkRoot)
	
	#Run Gui 
	tkRoot.mainloop()
	
	
if __name__ == "__main__":
	main()