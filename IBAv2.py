#Stoped 2016-02-16: load_data funktion, muss erkennen lernen ob ein Datum vorliegt, next: items in Listboy auswählen


import tkinter as tk
from PIL import Image, ImageTk

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
		sysJson = open("system\sysdata.json")
		self.sysData = json.load(sysJson)
	
	def get_planungsdaten(self):
		self.get_credentials()
		gSheet = self.sysData["planungSpread"]
		
		GSpread = gspread.authorize(self.credentials)
		act_sh = GSpread.open(gSheet)
		wks = act_sh.sheet1
		
		planungsdaten = wks.get_all_records(empty2zero=True, head=2)
		planungsdaten.pop(0)
		planungsdaten.pop(0)
		
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
  
		
#GUI App
class IbaTK(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background = "white")
		self.parent = parent
		self.version = "(C) Solandeo - Version 2016-02-16.2.0a"
		
		self.build()	
		
	def build(self):
	#Builds main Programmm Window
	
		self.parent.title("Solandeo - Installationsbelege Assistent")
		self.pack(fill='both', expand =False)
		
		#Menu Bar
		menubar = tk.Menu(self.parent)
		self.parent.config(menu=menubar)
		
		sysMenu = tk.Menu(self.parent)
		sysMenu.add_command(label="Dateipfade", command=self.find_path)
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
		google = GoogleGrabber()
		planungsdaten = google.get_planungsdaten()
		self.guiListe.delete(0,'end')
		for d in planungsdaten:
			if d['Datum Installation']!=0:
				if self.is_date(str(d['Datum Installation'])):
					addStr = str(d['Datum Installation']) + " - " + str(d['Nummer MST/STST']) + " - " + str(d['Name'])
					self.guiListe.insert('end', addStr)
		self.get_to_front()
		
	def is_date(self, dateStr):
		#TODO
		datum = parser.parse(dateStr, fuzzy=True)
		today = datetime.datetime.today()
		if today-datum == 0:
			ans = False
		else:
			ans = True
		
		return ans
		
	def process_data(self):
		#Processes the gathered Data
		print("TODO")
	
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