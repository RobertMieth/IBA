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
	def __init__(self):
		self.sysJson = open("system\sysdata.json", 'r')
		self.sysData = json.load(self.sysJson)
		
		self.outDatenfelder = ('Bezeichner', 'Name', 'Messstelle', 'Steuerstelle', 'Komplex', 'Kunde', 'Datum', 'Uhrzeit', 'Umfang Messst.', 'Umfang SSt.', 'Installationspartner', 'PLZ', 'Ort', 'Straße', 'HNr', 'Anfahrtsinfo', 'Anlagentyp', 'Ansprechpartner vor Ort', 'Telefon 1 ASP', 'Telefon 2 ASP', 'Anprechpartner Vertraglich', 'Verteilnetzbetreiber', 'Kontakt VNB', 'Zählpunkt', 'PLZ Messstelle', 'Ort Messstelle', 'Straße Messstelle', 'HNr. Messstelle', 'Position Zähler', 'Gerätenummer', 'MSBA', 'Kontakt MSBA', 'Ausbau durch', 'Wandlerfaktor', 'Spannung ungewandelt', 'Spannung gewandelt', 'Strom ungewandelt', 'Strom gewandelt', 'Typenschlüssel', 'Nennspannung', 'Nennstrom', 'Genauigkeit', 'Leistungsbegrenzung', 'Hilfsspannung', 'Impulsausgang', 'Modem Typ', 'Modem Info', 'Technische Hinweise', 'PLZ Steuerstelle', 'Ort Steuerstelle', 'Straße Steuerstelle', 'HNr. Steuerstelle', 'Position Steuerung', 'Fernwirktechnik', 'Steuermodul', 'Sollwertgeber', 'Steuerung Infos')
		
	
	def write_planungsdaten2excel(self, dbData, planungData):
		outPath = "2016-03-23_Datenfelder_Installationsbeleg_ReleaseV2.0.xlsm"
		try:
			outWb = pxl.load_workbook(filename=outPath, keep_vba = True)
		except:
			print(outPath + " must be closed!")
			return
		outWs = outWb.get_sheet_by_name("Daten Installationsbelege Neu")
		outWs['B5'].value = ""
		
		outData = {}
		
		#Add planungsdaten
		for p in planungData:
			outData[('Bezeichner', p['Nummer MST/STST'])] = p['Nummer MST/STST']
			outData[('Datum', p['Nummer MST/STST'])] = p['Datum Installation']
			outData[('Uhrzeit', p['Nummer MST/STST'])] = p['Uhrzeit']
			outData[('Umfang Messst.', p['Nummer MST/STST'])] = p['Auftrag Messstelle']
			outData[('Umfang SSt.', p['Nummer MST/STST'])] = p['Auftrag Steuerstelle']	
			outData[('Installationspartner', p['Nummer MST/STST'])] = p['Termin angefragt bei']
			outData[('Ansprechpartner vor Ort', p['Nummer MST/STST'])] = str(p['Vorname']) + ' ' + str(p['Nachname'])
			outData[('Telefon 1 ASP', p['Nummer MST/STST'])] = p['Telefon']
			outData[('Telefon 2 ASP', p['Nummer MST/STST'])] = p['Mobil']
			outData[('Ausbau durch', p['Nummer MST/STST'])] = p['Ausbau Altzähler durch']
			outData[('Typenschlüssel', p['Nummer MST/STST'])] = p['Typenschlüssen (Anfang)']
			outData[('Nennspannung', p['Nummer MST/STST'])] = p['Spannung']
			outData[('Nennstrom', p['Nummer MST/STST'])] = p['Stromtyp']
			outData[('Genauigkeit', p['Nummer MST/STST'])] = p['Genauigkeitsklasse']
			outData[('Leistungsbegrenzung', p['Nummer MST/STST'])] = p['Leistungsbegrenzung']
			outData[('Hilfsspannung', p['Nummer MST/STST'])] = p['Hilfsspannung']
			outData[('Impulsausgang', p['Nummer MST/STST'])] = p['Impulsausgang']
			outData[('Modem Typ', p['Nummer MST/STST'])] = p['Bezeichnung']
			outData[('Modem Info', p['Nummer MST/STST'])] = p['Typenschlüssel']
			outData[('Technische Hinweise', p['Nummer MST/STST'])] = p['technische Hinweise Messstelle']
			outData[('Steuermodul', p['Nummer MST/STST'])] = p['Steuermodul']
			outData[('Sollwertgeber', p['Nummer MST/STST'])] = p['Sollwertgeber']
			outData[('Steuerung Infos', p['Nummer MST/STST'])] = p['technische Hinweise Steuerstelle']
			
			if p['Auftrag Messstelle'] != 0:
				outData[('Messstelle', p['Nummer MST/STST'])] = "X"
			else:
				outData[('Messstelle', p['Nummer MST/STST'])] = ""
				
			if p['Auftrag Steuerstelle'] != 0:
				outData[('Steuerstelle', p['Nummer MST/STST'])] = "X"
			else:
				outData[('Steuerstelle', p['Nummer MST/STST'])] = ""
		
		
		#Add dbDaten
		for lOuter in dbData:
			for lInner in lOuter:
				outData[('Name', lInner[1])] = lInner[0]
				#outData[('Messstelle', lInner[1])] = lInner[1]
				#outData[('Steuerstelle', lInner[1])] = lInner[2]
				outData[('Komplex', lInner[1])] = lInner[3]
				outData[('Kunde', lInner[1])] = lInner[4]
				outData[('PLZ', lInner[1])] = lInner[5]
				outData[('Ort', lInner[1])] = lInner[6]
				outData[('Straße', lInner[1])] = lInner[7]
				outData[('HNr', lInner[1])] = lInner[8]
				outData[('Anlagentyp', lInner[1])] = lInner[9]
				outData[('Anprechpartner Vertraglich', lInner[1])] = str(lInner[10]) + " " + str(lInner[11]) + " " + str(lInner[12])
				outData[('Verteilnetzbetreiber', lInner[1])] = lInner[13]
				if lInner[15] == 0:
					outData[('Zählpunkt', lInner[1])] = lInner[14]
				else: 
					outData[('Zählpunkt', lInner[1])] = lInner[15]
				outData[('PLZ Messstelle', lInner[1])] = lInner[5]
				outData[('Ort Messstelle', lInner[1])] = lInner[6]
				outData[('Straße Messstelle', lInner[1])] = lInner[7]
				outData[('HNr. Messstelle', lInner[1])] = lInner[8]
				outData[('Position Zähler', lInner[1])] = lInner[16]
				outData[('Gerätenummer', lInner[1])] = lInner[17]
				outData[('MSBA', lInner[1])] = lInner[18]
				outData[('Wandlerfaktor', lInner[1])] = lInner[19]
				outData[('Spannung ungewandelt', lInner[1])] = lInner[20]
				outData[('Spannung gewandelt', lInner[1])] = lInner[21]
				outData[('Strom ungewandelt', lInner[1])] = lInner[22]
				outData[('Strom gewandelt', lInner[1])] = lInner[23]
				outData[('PLZ Steuerstelle', lInner[1])] = lInner[5]
				outData[('Ort Steuerstelle', lInner[1])] = lInner[6]
				outData[('Straße Steuerstelle', lInner[1])] = lInner[7]
				outData[('HNr. Steuerstelle', lInner[1])] = lInner[8]
		
		#Add undefined
		for p in planungData:
			outData[('Anfahrtsinfo', p['Nummer MST/STST'])] = ""
			outData[('Kontakt VNB', p['Nummer MST/STST'])] = ""
			outData[('Kontakt MSBA', p['Nummer MST/STST'])] = ""
			outData[('Modem Info', p['Nummer MST/STST'])] = ""
			outData[('Position Steuerung', p['Nummer MST/STST'])] = ""
			outData[('Fernwirktechnik', p['Nummer MST/STST'])] = ""
		
		
		#Clear old Data
		clearRange = outWs['A5':'BJ300']
		for row in clearRange:
			for cell in row:
				cell.value = ""
		
		#Write new Data
		i_col = 1
		i_row = 5
		
		for p in planungData:
			for feld in self.outDatenfelder:
				value = outData[(feld, p['Nummer MST/STST'])]
				if value == 0:
					value = ""
				else:
					outWs.cell(row = i_row, column = i_col).value = value
				i_col += 1
			i_col = 1
			i_row +=1
			
		try:
			outWb.save(filename=outPath)
		except:
			print(outPath + " must be closed!")
			return
		
		print("Data sucessfully written to " + outPath)

		
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
	
	def get_db_data(self, ms_in):
		query = """SELECT 
					mst.name as name,
					mst.id as messstelle, 
					 sts.id as steuerstelle,
  					mst.komplex_id as komplex, 
  					k.kundennummer as kunde,
  					mst.anschrift_plz as mst_plz, 
  					mst.anschrift_stadt as mst_stadt, 
  					mst.anschrift_strasse as mst_strasse, 
  					mst.anschrift_hausnummer as mst_hausnummer, 
  					eva.technologie as anlagentyp,
  					p.anrede as k_anrede,
  					p.nachname as k_nachname,
  					p.vorname as k_vorname,
  					vnb.name as verteilnetzbetreiber,
  					m2k.zpn_kunde as zählpunkt_kunde,
  					m2vnb.zpn_wim as zählpunkt_wim,
  					mst.hinweise_zugang, 
  					mst.zaehler_vorher, 
  					mst.msb_vorher, 
  					mst.wandler_faktor, 
  					mst.spannung_ungewandelt, 
  					mst.spannung_gewandelt, 
  					mst.strom_ungewandelt,
  					mst.strom_gewandelt
				FROM 
  					dbfrontend_messstelle as mst
				LEFT JOIN dbfrontend_steuerstelle as sts ON mst.komplex_id = sts.komplex_id
				LEFT JOIN dbfrontend_messstelle2kunde as m2k ON mst.id = m2k.messstelle_id 
				LEFT JOIN dbfrontend_kunde as k ON m2k.kunde_id = k.kundennummer
				LEFT JOIN dbfrontend_person as p ON k.person_ptr_id = p.id 
				LEFT JOIN dbfrontend_eva as eva ON mst.id = eva.messstelle_id 
				LEFT JOIN dbfrontend_messstelle2vnb m2vnb ON mst.id = m2vnb.messstelle_id
				LEFT JOIN dbfrontend_vnb as vnb ON m2vnb.vnb_id = vnb.id
				WHERE
					mst.id = %s
				GROUP BY
					mst.id,
					sts.id,
					k.kundennummer,
					eva.technologie,
					p.anrede,
					p.nachname,
					p.vorname,
					vnb.name,
					m2k.zpn_kunde,
					m2vnb.zpn_wim
				ORDER BY
					mst.id,
					sts.id"""
	
		self.cursor.execute(query, [ms_in])
		return self.cursor.fetchall()
		
#GUI App
class IbaTK(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background = "white")
		self.parent = parent
		self.version = "(C) Solandeo - Version 2016-02-16.2.0a"
		
		sysJson = open("system\sysdata.json",'r')
		self.sysData = json.load(sysJson)
		
		self.build()	
		
		self.dbColor('yellow')
		try: 
			self.db = DbHandler()
			self.dbColor('green')
		except: 
			self.dbColor('black')
		
		try:
			self.google = GoogleGrabber()
			self.googleColor('blue')
		except:
			self.googleColor('black')
			
		self.excel = ExcelHandler()
		
		
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
		self.rowconfigure(6, pad = 10)
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
		dataBox = tk.Listbox(self, height=26, width = 60, selectmode='extended', yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)
		dataBox.insert('end', "<<Noch keine Daten>>")
		dataBox.grid(column=1, row=5, columnspan=2)
		self.guiListe = dataBox #external Reference
		scrollY.config(command=dataBox.yview)
		scrollY.grid(column=3, row = 5)
		scrollX.config(command=dataBox.xview)
		scrollX.grid(column=2, row = 6)
		
		ind = tk.Frame(self, relief = 'sunken')
		ind.grid(row = 6, column = 1, columnspan = 4, sticky = 'W', padx=10)
		
		ind.columnconfigure(3, pad=10)
		ind.columnconfigure(6, pad=10)
		
		dbIndicatorF = tk.Frame(ind, border = 1, relief = 'sunken', width = 15, height = 15, bg='red')
		dbIndicatorF.grid(row = 0, column = 1, sticky='W')
		dbIndicatorT = tk.Label(ind, text="DB Verb.   ")
		dbIndicatorT.grid(row=0, column=2, sticky='W')
		self.dbFrame = dbIndicatorF #External reference
		
		googleIndicatorF = tk.Frame(ind, border = 1, relief = 'sunken', width = 15, height = 15, bg='red')
		googleIndicatorF.grid(row = 0, column = 4,sticky='W')
		googleIndicatorT = tk.Label(ind, text="Google Daten   ")
		googleIndicatorT.grid(row=0, column=5, sticky='W')
		self.googleFrame = googleIndicatorF #external reference
		
		excelIndicatorF = tk.Frame(ind, border = 1, relief = 'sunken', width = 15, height = 15, bg='red')
		excelIndicatorF.grid(row = 0, column = 7, sticky='W')
		excelIndicatorT = tk.Label(ind, text="Excel-Export")
		excelIndicatorT.grid(row=0, column=8,sticky='W')
		self.excelFrame = excelIndicatorF #external reference
		
		version =tk.Label(self, text=self.version, bg="white")
		version.grid(column= 1, row=7, pady=5)
		
	def dbColor(self, col):
		self.dbFrame.configure(bg=col)
		self.update()
	
	def googleColor(self, col):
		self.googleFrame.configure(bg=col)
		self.update()
		
	def excelColor(self, col):
		self.excelFrame.configure(bg=col)
		self.update()
		
	def load_data(self):
		#Loads Data of currently planned Installations
		
		self.googleColor('yellow')
		try:
			planungsdaten = self.google.get_planungsdaten()
		except:
			self.googleColor('black')
			return

		self.guiListe.delete(0,'end')
		for d in planungsdaten:
			addStr = str(d['Datum Installation']) + " - " + str(d['Nummer MST/STST']) + " - " + str(d['Name'])
			self.guiListe.insert('end', addStr)
		self.get_to_front()
		self.googleColor('green')
		
		
	def process_data(self):
		#Processes the gathered Data
		self.excelColor('yellow')
		auswahl = map(int, self.guiListe.curselection())
		planungsdaten = self.google.session_planungsdaten
		todoPlanung = []  
		for a in auswahl:
			todoPlanung.append(planungsdaten[a])
		msListe = []
		todoDbData = []
		for m in todoPlanung:
			todoDbData.append(self.db.get_db_data(m["Nummer MST/STST"]))
		try:
			self.excel.write_planungsdaten2excel(todoDbData, todoPlanung)
		except:
			self.excelColor('black')
			return
		self.excelColor('green')

		
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