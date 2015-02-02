import tkMessageBox
import Tkinter as tk
import EclampsiaUtility as util

class EditRiskFactorsPage:
	"""Patient Risk Factors Page"""
	
	def __init__(self, pid, link, root):
		"""
		Retrieve essentials from calling page.
		Initialize root (new Tkinter object).
		Create frame (container for all widgets).
		Create widgets and apply them to frame via grid.
		"""
		# Retrieve essentials from last page
		self.pid = pid
		self.link = link
		
		# Initialize root
		self.root = root
		self.root.title('Patient Risk Factors Page')
		
		# Create frame
		self.frame = tk.Frame(self.root)
		self.frame.pack()

		# Create medical history page button widget
		self.medicalhistory_button = tk.Button(self.frame, text='<--History', command=lambda x='MedicalHistory': self.__nextpage(x))
		self.medicalhistory_button.grid(row=0, column=0)
		
		# Create main page button widget
		self.mainpage_button = tk.Button(self.frame, text='Main', command=lambda x='MainPage': self.__nextpage(x))
		self.mainpage_button.grid(row=0, column=2)
		
		# Create recommendations page button widget
		self.recommendation_button = tk.Button(self.frame, text="Recs'-->", command=lambda x='Recommendations': self.__nextpage(x))
		self.recommendation_button.grid(row=0, column=4)
		
		# Create horizontal placeholder1 frame
		self.horizontal_placeholder1 = tk.Frame(self.frame, height=25)
		self.horizontal_placeholder1.grid(row=1, column=0, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create vertical placeholder frame
		self.vertical_placeholder = tk.Frame(self.frame, width=10)
		self.vertical_placeholder.grid(row=2, rowspan=6, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Open db
		(self.conn, self.cursor) = util.open_db(self, link=self.link)
		
		# Create pregnancy history label widget
		self.pregnancyhistory_label = tk.Label(self.frame, text='Pregnancy History')
		self.pregnancyhistory_label.grid(row=2, column=1)
		
		# Create pregrnancy history radiobutton widget
		self.pregnancyhistory_value = tk.IntVar()
		self.pregnancyhistory_radiobutton1 = tk.Radiobutton(self.frame, text='1st', variable=self.pregnancyhistory_value, value=1)
		self.pregnancyhistory_radiobutton2 = tk.Radiobutton(self.frame, text='Other', variable=self.pregnancyhistory_value, value=2)
		self.pregnancyhistory_radiobutton1.grid(row=2, column=2) 
		self.pregnancyhistory_radiobutton2.grid(row=2, column=3)
		self.pregnancyhistory_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'PregnancyHistory', default='')
		if self.pregnancyhistory_dbvalue:
			if self.pregnancyhistory_dbvalue == '1st':
				self.pregnancyhistory_radiobutton1.select()
			elif self.pregnancyhistory_dbvalue == 'Other':
				self.pregnancyhistory_radiobutton2.select()
		
		# Create children expected label widget
		self.childrenexpected_label = tk.Label(self.frame, text='Children Expected')
		self.childrenexpected_label.grid(row=3, column=1)
		
		# Create children expected radiobutton widget
		self.childrenexpected_value = tk.IntVar()
		self.childrenexpected_radiobutton1 = tk.Radiobutton(self.frame, text='1', variable=self.childrenexpected_value, value=1)
		self.childrenexpected_radiobutton2 = tk.Radiobutton(self.frame, text='>1', variable=self.childrenexpected_value, value=2)
		self.childrenexpected_radiobutton1.grid(row=3, column=2) 
		self.childrenexpected_radiobutton2.grid(row=3, column=3)
		self.childrenexpected_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'ChildrenExpected', default='')
		if self.childrenexpected_dbvalue:
			if self.childrenexpected_dbvalue == '1':
				self.childrenexpected_radiobutton1.select()
			elif self.childrenexpected_dbvalue == '>1':
				self.childrenexpected_radiobutton2.select()
		
		# Create trimester label widget
		self.trimester_label = tk.Label(self.frame, text='Trimester')
		self.trimester_label.grid(row=4, column=1)
		
		# Create trimester radiobutton widget 
		self.trimester_value = tk.IntVar()
		self.trimester_radiobutton1 = tk.Radiobutton(self.frame, text='1st', variable=self.trimester_value, value=1)
		self.trimester_radiobutton2 = tk.Radiobutton(self.frame, text='2nd', variable=self.trimester_value, value=2)
		self.trimester_radiobutton3 = tk.Radiobutton(self.frame, text='3rd', variable=self.trimester_value, value=3)
		self.trimester_radiobutton1.grid(row=4, column=2) 
		self.trimester_radiobutton2.grid(row=4, column=3)
		self.trimester_radiobutton3.grid(row=4, column=4)
		self.trimester_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Trimester', default='')
		if self.trimester_dbvalue:
			if self.trimester_dbvalue == '1st':
				self.trimester_radiobutton1.select()
			elif self.trimester_dbvalue == '2nd':
				self.trimester_radiobutton2.select()
			elif self.trimester_dbvalue == '3rd':
				self.trimester_radiobutton3.select()

		# Create pregnancy interval radiobutton label
		self.pregnancyinterval_label = tk.Label(self.frame, text='Pregnancy Interval \n(since last)')
		self.pregnancyinterval_label.grid(row=5, column=1)
		
		# Create pregnancy interval radiobutton widget
		self.pregnancyinterval_value = tk.IntVar()
		self.pregnancyinterval_radiobutton1 = tk.Radiobutton(self.frame, text='<10 yrs', variable=self.pregnancyinterval_value, value=1)
		self.pregnancyinterval_radiobutton2 = tk.Radiobutton(self.frame, text='>10 yrs', variable=self.pregnancyinterval_value, value=2)
		self.pregnancyinterval_radiobutton3 = tk.Radiobutton(self.frame, text='N/A', variable=self.pregnancyinterval_value, value=3)
		self.pregnancyinterval_radiobutton1.grid(row=5, column=2) 
		self.pregnancyinterval_radiobutton2.grid(row=5, column=3)
		self.pregnancyinterval_radiobutton3.grid(row=5, column=4)
		self.pregnancyinterval_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'PregnancyInterval', default='')
		if self.pregnancyinterval_dbvalue:
			if self.pregnancyinterval_dbvalue == '<10 yrs':
				self.pregnancyinterval_radiobutton1.select()
			elif self.pregnancyinterval_dbvalue == '>10 yrs':
				self.pregnancyinterval_radiobutton2.select()
			elif self.pregnancyinterval_dbvalue == 'N/A':
				self.pregnancyinterval_radiobutton3.select()
		
		# Create paternity change label widget
		self.paternitychange_label = tk.Label(self.frame, text='Paternity Change? \n(since last)')
		self.paternitychange_label.grid(row=6, column=1)
		
		# Create paternity change radiobutton widget 
		self.paternitychange_value = tk.IntVar()
		self.paternitychange_radiobutton1 = tk.Radiobutton(self.frame, text='Yes', variable=self.paternitychange_value, value=1)
		self.paternitychange_radiobutton2 = tk.Radiobutton(self.frame, text='No', variable=self.paternitychange_value, value=2)
		self.paternitychange_radiobutton3 = tk.Radiobutton(self.frame, text='N/A', variable=self.paternitychange_value, value=3)
		self.paternitychange_radiobutton1.grid(row=6, column=2) 
		self.paternitychange_radiobutton2.grid(row=6, column=3)
		self.paternitychange_radiobutton3.grid(row=6, column=4)
		self.paternitychange_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'PaternityChange', default='')
		if self.paternitychange_dbvalue:
			if self.paternitychange_dbvalue == 'Yes':
				self.paternitychange_radiobutton1.select()
			elif self.paternitychange_dbvalue == 'No':
				self.paternitychange_radiobutton2.select()
			elif self.paternitychange_dbvalue == 'N/A':
				self.paternitychange_radiobutton3.select()
		
		# Create IVF radiobutton label
		self.invitro_label = tk.Label(self.frame, text='IVF?')
		self.invitro_label.grid(row=7, column=1)
		
		# Create IVF radiobutton widget
		self.invitro_value = tk.IntVar()
		self.invitro_radiobutton1 = tk.Radiobutton(self.frame, text='Yes', variable=self.invitro_value, value=1)
		self.invitro_radiobutton2 = tk.Radiobutton(self.frame, text='No', variable=self.invitro_value, value=2)
		self.invitro_radiobutton1.grid(row=7, column=2) 
		self.invitro_radiobutton2.grid(row=7, column=3)
		self.invitro_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'InVitro', default='')
		if self.invitro_dbvalue:
			if self.invitro_dbvalue == 'Yes':
				self.invitro_radiobutton1.select()
			elif self.invitro_dbvalue == 'No':
				self.invitro_radiobutton2.select()
		
		# Create family history label widget
		self.familyhistory_label = tk.Label(self.frame, text='Family History')
		self.familyhistory_label.grid(row=8, column=1)
		
		# Create family history listbox widget
		self.familyhistory_listbox = tk.Listbox(self.frame, width=10, height=5, selectmode=tk.MULTIPLE)
		self.familyhistory_listbox.grid(row=8, column=2, pady=1)
		familyhistory_list = ['Self', 'Parent', 'Sibling', 'Cousin', 'Other']
		for item in familyhistory_list:
			self.familyhistory_listbox.insert(tk.END, item)
		self.familyhistory_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'FamilyHistory', default='')
		if self.familyhistory_dbvalue:
			self.familyhistory_dbvalue = util.str2list(self, self.familyhistory_dbvalue)
			for item in self.familyhistory_dbvalue:
				index = familyhistory_list.index(item)
				self.familyhistory_listbox.selection_set(first=index)
		self.familyhistory_listbox.bind('<<ListboxSelect>>', self.activate_familyhistory)
		self.activate_familyhistory_status = 0
				
		# Create horizontal placeholder2 frame
		self.horizontal_placeholder2 = tk.Frame(self.frame, height=55)
		self.horizontal_placeholder2.grid(row=9, column=0, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create save button widget
		self.save_button = tk.Button(self.frame, text='Save', command=self.__save)
		self.save_button.grid(row=10, column=2)
		
		# Invoke main loop
		self.root.mainloop()
	
	def __nextpage(self, page):
		"""
		Close current page.
		Call new page.
		"""	
		self.frame.destroy()
		util.close_db(self, self.conn, self.cursor)
		import EditMedicalHistoryPage, EclampsiaModel, RecommendationsPage
		if page == 'MedicalHistory':
			EditMedicalHistoryPage.EditMedicalHistoryPage(self.pid, self.link, self.root)
		elif page == 'MainPage':
			EclampsiaModel.EclampsiaModel(self.root)
		elif page == 'Recommendations':
			RecommendationsPage.RecommendationsPage(self.pid, self.link, self.root)
	
	def validate_pregnancyhistory(self):
		"""
		Validate family history selection.
		Set to default (empty) if no selection.
		"""
		pregnancyhistory_choice = self.pregnancyhistory_value.get()
		if pregnancyhistory_choice:
			pregnancyhistory_choices = {1:'1st', 2:'Other'}
			self.pregnancyhistory = pregnancyhistory_choices[pregnancyhistory_choice]
		else:
			self.pregnancyhistory = ''
	
	def validate_childrenexpected(self):
		"""
		Validate children expected selection.
		Set to default (empty) if no selection.
		"""
		childrenexpected_choice = self.childrenexpected_value.get()
		if childrenexpected_choice:
			childrenexpected_choices = {1:'1', 2:'>1'}
			self.childrenexpected = childrenexpected_choices[childrenexpected_choice]
		else:
			self.childrenexpected = ''
	
	def validate_trimester(self):
		"""
		Validate trimester selection.
		Set to default (empty) if no selection.
		"""
		trimester_choice = self.trimester_value.get()
		if trimester_choice:
			trimester_choices = {1:'1st', 2:'2nd', 3:'3rd'}
			self.trimester = trimester_choices[trimester_choice]
		else:
			self.trimester = ''
	
	def validate_pregnancyinterval(self):
		"""
		Validate pregnancy interval selection.
		Set to default (empty) if no selection.
		"""
		pregnancyinterval_choice = self.pregnancyinterval_value.get()
		if pregnancyinterval_choice:
			pregnancyinterval_choices = {1:'>10 yrs', 2:'<10 yrs', 3:'N/A'}
			self.pregnancyinterval = pregnancyinterval_choices[pregnancyinterval_choice]
		else:
			self.pregnancyinterval = ''
			
	def validate_paternitychange(self):
		"""
		Validate paternity change  selection.
		Set to default (empty) if no selection.
		"""
		paternitychange_choice = self.paternitychange_value.get()
		if paternitychange_choice:
			paternitychange_choices = {1:'Yes', 2:'No', 3:'N/A'}
			self.paternitychange = paternitychange_choices[paternitychange_choice]
		else:
			self.paternitychange = ''
			
	def validate_invitro(self):
		"""
		Validate in vitro selection.
		Set to default (empty) if no selection.
		"""
		invitro_choice = self.invitro_value.get()
		if invitro_choice:
			invitro_choices = {1:'Yes', 2:'No'}
			self.invitro = invitro_choices[invitro_choice]
		else:
			self.invitro = ''
	
	def activate_familyhistory(self, event):
		"""
		Activate family history selection(s).
		"""
		self.activate_familyhistory_status = 1
		familyhistory_index = self.familyhistory_listbox.curselection()
		# Older versions of Tkinter return index as str vs int
		try:
			familyhistory_index = map(int, familyhistory_index)
		except ValueError:
			pass
		self.familyhistory = util.list2str(self, self.familyhistory_listbox, familyhistory_index)
				
	def validate_familyhistory(self):
		"""
		Validate current conditions selection(s).
		Set to default (empty) if user activates listbox with no selection(s).
		"""
		if not self.activate_familyhistory_status:
			self.familyhistory = self.familyhistory_dbvalue
		else:
			try:
				self.familyhistory
			except AttributeError:
				self.familyhistory = ''		
	
	def __save(self):
		""" 
		Validate widget entries/selections. 
		Write entries/selections to database.
		Return unique db patient identifier (pid) to pass to other pages (frames).
		"""
		self.validate_pregnancyhistory()
		self.validate_childrenexpected()
		self.validate_trimester()
		self.validate_pregnancyinterval()
		self.validate_paternitychange()
		self.validate_invitro()
		self.validate_familyhistory()
		self.__update_db()
		return
	
	def __update_db(self):
		"""
		Write entries/selections to database.
		"""
		import sqlite3
		# Entries (column, current value, new value, column type, full name) 
		entries = {'PregnancyHistory':(self.pregnancyhistory_dbvalue, self.pregnancyhistory),
					'ChildrenExpected':(self.childrenexpected_dbvalue, self.childrenexpected),
					'Trimester':(self.trimester_dbvalue, self.trimester),
					'PregnancyInterval':(self.pregnancyinterval_dbvalue, self.pregnancyinterval),
					'PaternityChange':(self.paternitychange_dbvalue, self.paternitychange),
					'InVitro':(self.invitro_dbvalue, self.invitro), 
					'FamilyHistory':(self.familyhistory_dbvalue, self.familyhistory)}
		
		for key in entries:
			if (entries[key][0] != entries[key][1]):
				self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][1], self.pid))
				self.conn.commit()

if __name__ == "__main__":
	EditRiskFactorsPage(self.pid, self.link)
