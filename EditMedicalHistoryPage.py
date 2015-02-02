import tkMessageBox
import Tkinter as tk
import EclampsiaUtility as util

class EditMedicalHistoryPage:
	"""Patient Medical History Page"""
	
	def __init__(self, pid, link, root):
		"""
		Retrieve essentials from calling page.
		Initialize root (new Tkinter object).
		Create frame (container for all widgets).
		Create widgets and apply them to frame via grid.
		"""
		# Retrieve essentials
		self.pid = pid
		self.link = link
		
		# Initialize root
		self.root = root
		self.root.title('Patient Medical History Page')
		
		# Create frame
		self.frame = tk.Frame(self.root)
		self.frame.pack()
		
		# Create identification page button widget
		self.identification_button = tk.Button(self.frame, text='<--ID', command=lambda x='Identification': self.__nextpage(x))
		self.identification_button.grid(row=0, column=0)
		
		# Create main page button widget
		self.mainpage_button = tk.Button(self.frame, text='Main', command=lambda x='MainPage': self.__nextpage(x))
		self.mainpage_button.grid(row=0, column=2)
		
		# Create risk factors page button widget
		self.riskfactors_button = tk.Button(self.frame, text='Risk-->', command=lambda x='RiskFactors': self.__nextpage(x))
		self.riskfactors_button.grid(row=0, column=4)
		
		# Create horizontal placeholder1 frame
		self.horizontal_placeholder1 = tk.Frame(self.frame, height=10)
		self.horizontal_placeholder1.grid(row=1, column=0, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create vertical placeholder frame
		self.vertical_placeholder = tk.Frame(self.frame, width=10)
		self.vertical_placeholder.grid(row=2, rowspan=10, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Open db
		(self.conn, self.cursor) = util.open_db(self, link=self.link)
		
		# Create blood pressure label widgets
		self.bloodpressure_label0 = tk.Label(self.frame, text='Blood Pressure (mmHg)')
		self.bloodpressure_label1 = tk.Label(self.frame, text='Systolic')
		self.bloodpressure_label2 = tk.Label(self.frame, text='Diastolic') 
		self.bloodpressure_label0.grid(row=2, column=1)
		self.bloodpressure_label1.grid(row=3, column=1)
		self.bloodpressure_label2.grid(row=4, column=1)
	
		# Create blood pressure entry widgets
		self.bloodpressure_value1 = tk.IntVar()
		self.bloodpressure_value2 = tk.IntVar()
		self.bloodpressure_entry1 = tk.Entry(self.frame, textvariable=self.bloodpressure_value1)
		self.bloodpressure_entry2 = tk.Entry(self.frame, textvariable=self.bloodpressure_value2)
		self.bloodpressure_entry1.grid(row=3, column=2, pady=1)
		self.bloodpressure_entry2.grid(row=4, column=2, pady=1)
		self.bloodpressure_dbvalue1 = util.retrieve_dbvalue(self, self.cursor, self.pid, 'BloodPressure_Sys', default=-1)
		self.bloodpressure_dbvalue2 = util.retrieve_dbvalue(self, self.cursor, self.pid, 'BloodPressure_Dis', default=-1)
		if (self.bloodpressure_dbvalue1 != -1) & (self.bloodpressure_dbvalue1 != None):
			self.bloodpressure_value1.set(self.bloodpressure_dbvalue1)
		if (self.bloodpressure_dbvalue2 != -1) & (self.bloodpressure_dbvalue2 != None) :
			self.bloodpressure_value2.set(self.bloodpressure_dbvalue2)
		
		# Create current conditions label widget
		self.currentconditions_label = tk.Label(self.frame, text='Current Conditions')
		self.currentconditions_label.grid(row=5, column=1)
		
		# Create current conditions listbox widget (enable vertical scrolling)
		# Need exportselection=0 for multiple listboxes on same page to work
		self.currentconditions_listbox = tk.Listbox(self.frame, height=5, selectmode=tk.MULTIPLE, exportselection=0)
		self.currentconditions_listbox.grid(row=5, column=2, sticky=tk.N+tk.S, pady=1)
		self.currentconditions_scrollbar = tk.Scrollbar(self.frame)
		self.currentconditions_scrollbar.grid(row=5, column=3, sticky=tk.N+tk.S)
		currentconditions_list = ['Autoimmune Disorders','Diabetes', 'Cortical Blindness', 'Convulsions', 'Edema', 
			'Headaches/Migranes', 'Hypertension', 'Hypomagnesia', 'Kidney Disease', 'Malnutrition', 'Proteinura']
		for item in currentconditions_list:
			self.currentconditions_listbox.insert(tk.END, item)
		self.currentconditions_listbox.configure(yscrollcommand=self.currentconditions_scrollbar.set)
		self.currentconditions_scrollbar.configure(command=self.currentconditions_listbox.yview)
		self.currentconditions_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'CurrentConditions', default='')
		if self.currentconditions_dbvalue:
			self.currentconditions_dbvalue = util.str2list(self, self.currentconditions_dbvalue)
			for item in self.currentconditions_dbvalue:
				index = currentconditions_list.index(item)
				self.currentconditions_listbox.selection_set(first=index)
		self.currentconditions_listbox.bind('<<ListboxSelect>>', self.activate_currentconditions)
		self.activate_currentconditions_status = 0
		
		# Create previous conditions label widget
		self.previousconditions_label = tk.Label(self.frame, text='Previous Conditions')
		self.previousconditions_label.grid(row=6, column=1)
		
		# Create previous conditions listbox widget (enable vertical scrolling)
		# Need exportselection=0 for multiple listboxes on same page to work
		self.previousconditions_listbox = tk.Listbox(self.frame, height=5, selectmode=tk.MULTIPLE, exportselection=0)
		self.previousconditions_listbox.grid(row=6, column=2, sticky=tk.N+tk.S, pady=1)
		self.previousconditions_scrollbar = tk.Scrollbar(self.frame)
		self.previousconditions_scrollbar.grid(row=6, column=3, sticky=tk.N+tk.S)
		previousconditions_list = ['Autoimmune Disorders','Diabetes', 'Cortical Blindness', 'Convulsions', 'Edema', 
			'Headaches/Migranes', 'Hypertension', 'Hypomagnesia', 'Kidney Disease', 'Malnutrition', 'Proteinura']
		for item in previousconditions_list:
			self.previousconditions_listbox.insert(tk.END, item)
		self.previousconditions_listbox.configure(yscrollcommand=self.previousconditions_scrollbar.set)
		self.previousconditions_scrollbar.configure(command=self.previousconditions_listbox.yview)
		self.previousconditions_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'PreviousConditions', default='')
		if self.previousconditions_dbvalue:
			self.previousconditions_dbvalue = util.str2list(self, self.previousconditions_dbvalue)
			for item in self.previousconditions_dbvalue:
				index = previousconditions_list.index(item)
				self.previousconditions_listbox.selection_set(first=index)
		self.previousconditions_listbox.bind('<<ListboxSelect>>', self.activate_previousconditions)
		self.activate_previousconditions_status = 0
				
		# Create lab tests label widgets			
		self.labtests_label = tk.Label(self.frame, text='Lab Tests')
		self.labtests_label.grid(row=7, column=1)
		self.cholesterol_label = tk.Label(self.frame, text='Cholesterol (mg/dL)')
		self.cholesterol_label.grid(row=8, column=1)
		self.triglycerides_label = tk.Label(self.frame, text='Triglycerides (mg/dL)')
		self.triglycerides_label.grid(row=9, column=1)
		
		# Create lab tests radiobutton widgets
		self.cholesterol_value = tk.IntVar()
		self.cholesterol_radiobutton1 = tk.Radiobutton(self.frame, text='<200', variable=self.cholesterol_value, value=1)
		self.cholesterol_radiobutton2 = tk.Radiobutton(self.frame, text='200:300', variable=self.cholesterol_value, value=2)
		self.cholesterol_radiobutton3 = tk.Radiobutton(self.frame, text='>300', variable=self.cholesterol_value, value=3)
		self.cholesterol_radiobutton1.grid(row=8, column=2) 
		self.cholesterol_radiobutton2.grid(row=8, column=3)
		self.cholesterol_radiobutton3.grid(row=8, column=4)
		self.cholesterol_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Cholesterol', default='')
		if self.cholesterol_dbvalue:
			if self.cholesterol_dbvalue == '<200':
				self.cholesterol_radiobutton1.select()
			elif self.cholesterol_dbvalue == '200:300':
				self.cholesterol_radiobutton2.select()
			elif self.cholesterol_dbvalue == '>300':
				self.cholesterol_radiobutton3.select()
		
		self.triglycerides_value = tk.IntVar()
		self.triglycerides_radiobutton1 = tk.Radiobutton(self.frame, text='<150', variable=self.triglycerides_value, value=1)
		self.triglycerides_radiobutton2 = tk.Radiobutton(self.frame, text='150:200', variable=self.triglycerides_value, value=2)
		self.triglycerides_radiobutton3 = tk.Radiobutton(self.frame, text='>200', variable=self.triglycerides_value, value=3)
		self.triglycerides_radiobutton1.grid(row=9, column=2)
		self.triglycerides_radiobutton2.grid(row=9, column=3)
		self.triglycerides_radiobutton3.grid(row=9, column=4)
		self.triglycerides_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Triglycerides', default='')
		if self.triglycerides_dbvalue:
			if self.triglycerides_dbvalue == '<150':
				self.triglycerides_radiobutton1.select()
			elif self.triglycerides_dbvalue == '150:200':
				self.triglycerides_radiobutton2.select()
			elif self.triglycerides_dbvalue == '>200':
				self.triglycerides_radiobutton3.select()

		# Create horizontal placeholder2 frame
		self.horizontal_placeholder2 = tk.Frame(self.frame, height=5)
		self.horizontal_placeholder2.grid(row=10, column=0, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create save button widget
		self.save_button = tk.Button(self.frame, text='Save', command=self.__save)
		self.save_button.grid(row=11, column=2)
		
		# Invoke main loop
		self.root.mainloop()
	
	def __nextpage(self, page):
		"""
		Close current page.
		Call new page.
		"""	
		self.frame.destroy()
		util.close_db(self, self.conn, self.cursor)
		import EditIdentificationPage, EclampsiaModel, EditRiskFactorsPage
		if page == 'Identification':
			EditIdentificationPage.EditIdentificationPage(self.pid, self.link, self.root)
		elif page == 'MainPage':
			EclampsiaModel.EclampsiaModel(self.root)
		elif page == 'RiskFactors':
			EditRiskFactorsPage.EditRiskFactorsPage(self.pid, self.link, self.root)
	
	def validate_bloodpressure_sys(self):
		""" 
		Validate systolic blood pressure entry.
		Set to default (-1) if invalid/missing.
		"""
		self.bloodpressure_sys_value = self.bloodpressure_entry1.get()
		if not self.bloodpressure_sys_value:
			self.bloodpressure_sys = -1
		elif not self.bloodpressure_sys_value.isdigit():
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting numeric Systolic Blood Pressure between 50 and 230')
			self.bloodpressure_sys = -1
		elif not (50 < int(self.bloodpressure_sys_value) < 230):
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting Systolic Blood Pressure between 50 and 230')
			self.bloodpressure_sys = -1
		else:
			self.bloodpressure_sys = int(self.bloodpressure_sys_value)
		
			
	def validate_bloodpressure_dis(self):
		""" 
		Validate diastolic blood pressure entry.
		Set to default (-1) if invalid/missing.
		"""
		self.bloodpressure_dis_value = self.bloodpressure_entry2.get()
		if not self.bloodpressure_dis_value:
			self.bloodpressure_dis = -1
		elif not self.bloodpressure_dis_value.isdigit():
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting numeric Diastolic Blood Pressure between 0 and 140')
			self.bloodpressure_dis = -1
		elif not (0 < int(self.bloodpressure_dis_value) < 140):
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting Diastolic Blood Pressure between 0 and 140')
			self.bloodpressure_dis = -1
		else:
			self.bloodpressure_dis = int(self.bloodpressure_dis_value)
						
	def activate_currentconditions(self, event):
		"""
		Activate current condition selection(s).
		"""
		self.activate_currentconditions_status = 1
		currentconditions_index = self.currentconditions_listbox.curselection()
		# Older versions of Tkinter return index as str vs int
		try:
			currentconditions_index = map(int, currentconditions_index)
		except ValueError:
			pass
		self.currentconditions = util.list2str(self, self.currentconditions_listbox, currentconditions_index)
	
	def validate_currentconditions(self):
		"""
		Validate current conditions selection(s).
		Set to default (empty) if user activates listbox without selection(s).
		"""
		if not self.activate_currentconditions_status:
			self.currentconditions = self.currentconditions_dbvalue
		else:	
			try:
				self.currentconditions
			except AttributeError:
				self.currentconditions = ''
			
	def	activate_previousconditions(self, event):
		"""
		Activate previous conditions selection(s).
		"""
		self.activate_previousconditions_status = 1
		previousconditions_index = self.previousconditions_listbox.curselection()
		# Older versions of Tkinter return index as str vs int
		try:
			previousconditions_index = map(int, previousconditions_index)
		except ValueError:
			pass
		self.previousconditions = util.list2str(self, self.previousconditions_listbox, previousconditions_index)
		
	def validate_previousconditions(self):
		"""
		Validate previous conditions selection(s).
		Set to default (empty) if user activates listbox without selection(s).
		"""
		if not self.activate_previousconditions_status:
			self.previousconditions = self.previousconditions_dbvalue
		else:
			try:
				self.previousconditions
			except AttributeError:
				self.previousconditions = ''
			
	def validate_cholesterol(self):
		"""
		Validate cholesterol selection.
		Set to default (empty) if no selection.
		"""
		cholesterol_choice = self.cholesterol_value.get()
		if cholesterol_choice:
			cholesterol_choices = {1:'<200', 2:'200:300', 3:'>300'}
			self.cholesterol = cholesterol_choices[cholesterol_choice]
		else:
			self.cholesterol = ''
	
	def validate_triglycerides(self):	
		"""
		Validate triglycerides selection.
		Set to default (empty) if no selection.
		"""
		triglycerides_choice = self.triglycerides_value.get()
		if triglycerides_choice:
			triglycerides_choices = {1:'<150', 2:'150:200', 3:'>200'}
			self.triglycerides = triglycerides_choices[triglycerides_choice]
		else:
			self.triglycerides = ''		
			
	def __save(self):
		""" 
		Validate widget entries/selections. 
		Write entries/selections to database.
		"""
		self.validate_bloodpressure_sys()
		self.validate_bloodpressure_dis()
		self.validate_currentconditions()
		self.validate_previousconditions()
		self.validate_cholesterol()
		self.validate_triglycerides()
		self.__update_db()
		return
	
	def __update_db(self):
		"""
		Write entries/selections to database.
		"""
		import sqlite3
		# Entries (column, current value, new value, column type, full name)  
		entries = {'BloodPressure_Sys':(self.bloodpressure_dbvalue1, self.bloodpressure_sys),
					'BloodPressure_Dis':(self.bloodpressure_dbvalue2, self.bloodpressure_dis),
					'CurrentConditions':(self.currentconditions_dbvalue, self.currentconditions), 
					'PreviousConditions':(self.previousconditions_dbvalue, self.previousconditions),
					'Cholesterol':(self.cholesterol_dbvalue, self.cholesterol),
					'Triglycerides':(self.triglycerides_dbvalue, self.triglycerides)}
		
		for key in entries:
			if (entries[key][0] != entries[key][1]):
				self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][1], self.pid))
				self.conn.commit()

if __name__ == "__main__":
	EditMedicalHistoryPage(self.pid, self.link, self.root)
