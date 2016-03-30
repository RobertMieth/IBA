class ibaTK(tk.Frame):
	
	def __init__(self, parent):
		tk.frame.__init__(self, parent, background = "white")
		self.parent = parent
		self.build()
		
	def build(self):
	
		self.parent.title = ("Solandeo - Installationsbelege Assistent")
		self.pack(fill='both', expand =True)
		
		
