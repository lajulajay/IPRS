import tkMessageBox
import Tkinter as tk

class MedicalHistoryPage:
	"""Patient Medical History Page"""
	
	def __init__(self, pid, link, root):
		"""
		Retrieve essentials from calling page
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
		
		# Create blood pressure label widgets
		self.bloodpressure_label0 = tk.Label(self.frame, text='Blood Pressure (mmHg)')
		self.bloodpressure_label1 = tk.Label(self.frame, text='Systolic')
		self.bloodpressure_label2 = tk.Label(self.frame, text='Diastolic') 
		self.bloodpressure_label0.grid(row=2, column=1)
		self.bloodpressure_label1.grid(row=3, column=1)
		self.bloodpressure_label2.grid(row=4, column=1)
	
		# Create blood pressure entry widgets
		self.bloodpressure_entry1 = tk.Entry(self.frame)
		self.bloodpressure_entry2 = tk.Entry(self.frame)
		self.bloodpressure_entry1.grid(row=3, column=2, pady=1)
		self.bloodpressure_entry2.grid(row=4, column=2, pady=1)
		
		# Create current conditions label widget
		self.currentconditions_label = tk.Label(self.frame, text='Current Conditions')
		self.currentconditions_label.grid(row=5, column=1)
		
		# Create current conditions listbox widget (enable vertical scrolling)
		# Need exportselection=0 for multiple listboxes on same page to work
		self.currentconditions_listbox = tk.Listbox(self.frame, height=5, selectmode=tk.MULTIPLE, exportselection=0)
		self.currentconditions_listbox.grid(row=5, column=2, sticky=tk.N+tk.S, pady=1)
		self.currentconditions_scrollbar = tk.Scrollbar(self.frame)
		self.currentconditions_scrollbar.grid(row=5, column=3, sticky=tk.N+tk.S)
		for item in ['Autoimmune Disorders','Diabetes', 'Cortical Blindness', 'Convulsions', 'Edema', 
			'Headaches/Migranes', 'Hypertension', 'Hypomagnesia', 'Kidney Disease', 'Malnutrition', 
			'Proteinura']:
			self.currentconditions_listbox.insert(tk.END, item)
		self.currentconditions_listbox.configure(yscrollcommand=self.currentconditions_scrollbar.set)
		self.currentconditions_scrollbar.configure(command=self.currentconditions_listbox.yview)
		self.currentconditions_listbox.bind('<<ListboxSelect>>', self.activate_currentconditions)
		
		# Create previous conditions label widget
		self.previousconditions_label = tk.Label(self.frame, text='Previous Conditions')
		self.previousconditions_label.grid(row=6, column=1)
		
		# Create previous conditions listbox widget (enable vertical scrolling)
		# Need exportselection=0 for multiple listboxes on same page to work
		self.previousconditions_listbox = tk.Listbox(self.frame, height=5, selectmode=tk.MULTIPLE, exportselection=0)
		self.previousconditions_listbox.grid(row=6, column=2, sticky=tk.N+tk.S, pady=1)
		self.previousconditions_scrollbar = tk.Scrollbar(self.frame)
		self.previousconditions_scrollbar.grid(row=6, column=3, sticky=tk.N+tk.S)
		for item in ['Autoimmune Disorders','Diabetes', 'Cortical Blindness', 'Convulsions', 'Edema', 
			'Headaches/Migranes', 'Hypertension', 'Hypomagnesia', 'Kidney Disease', 'Malnutrition', 
			'Proteinura']:
			self.previousconditions_listbox.insert(tk.END, item)
		self.previousconditions_listbox.configure(yscrollcommand=self.previousconditions_scrollbar.set)
		self.previousconditions_scrollbar.configure(command=self.previousconditions_listbox.yview)
		self.previousconditions_listbox.bind('<<ListboxSelect>>', self.activate_previousconditions)
				
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
		self.triglycerides_value = tk.IntVar()
		self.triglycerides_radiobutton1 = tk.Radiobutton(self.frame, text='<150', variable=self.triglycerides_value, value=1)
		self.triglycerides_radiobutton2 = tk.Radiobutton(self.frame, text='150:200', variable=self.triglycerides_value, value=2)
		self.triglycerides_radiobutton3 = tk.Radiobutton(self.frame, text='>200', variable=self.triglycerides_value, value=3)
		self.triglycerides_radiobutton1.grid(row=9, column=2)
		self.triglycerides_radiobutton2.grid(row=9, column=3)
		self.triglycerides_radiobutton3.grid(row=9, column=4)
		
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
		import IdentificationPage, EclampsiaModel, RiskFactorsPage
		if page == 'Identification':
			IdentificationPage.IdentificationPage(self.pid, self.link, self.root)
		elif page == 'MainPage':
			EclampsiaModel.EclampsiaModel(self.root)
		elif page == 'RiskFactors':
			RiskFactorsPage.RiskFactorsPage(self.pid, self.link, self.root)
	
	def validate_bloodpressure_sys(self):
		""" 
		Validate systolic blood pressure entry.
		Set to default (-1) if invalid/missing.
		"""
		self.bloodpressure_sys_value = self.bloodpressure_entry1.get()
		if not self.bloodpressure_sys_value:
			tkMessageBox.showwarning(
				title='Missing Data',
				message='No entry for Systolic Blood Pressure')
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
			tkMessageBox.showwarning(
				title='Missing Data',
				message='No entry for Diastolic Blood Pressure')
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
		import EclampsiaUtility as util
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
		Set to default (empty) if no selection.
		"""
		try:
			self.currentconditions
		except AttributeError:
			self.currentconditions = ''
			
	def	activate_previousconditions(self, event):
		"""
		Activate previous conditions selection(s).
		"""
		import EclampsiaUtility as util
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
		Set to default (empty) if no selection.
		"""
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
			tkMessageBox.showwarning(
				title='Missing Data',
				message='No selection for Cholesterol')
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
			tkMessageBox.showwarning(
				title='Missing Data',
				message='No selection for Triglycerides')
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
		self.__write2db()
		return
	
	def __write2db(self):
		"""
		Write entries/selections to database.
		"""
		import sqlite3
		import EclampsiaUtility as util
		(self.conn, self.cursor) = util.open_db(self, link=self.link)
		# Entries (column, current value, default value, column type, full name)  
		entries = {'BloodPressure_Sys':(self.bloodpressure_sys, -1, 'INTEGER', 'Systolic Blood Pressure'),
					'BloodPressure_Dis':(self.bloodpressure_dis, -1, 'INTEGER', 'Diastolic Blood Pressure'),
					'CurrentConditions':(self.currentconditions, '', 'TEXT', 'Current Conditions'), 
					'PreviousConditions':(self.previousconditions, '', 'TEXT', 'Previous Conditions'),
					'Cholesterol':(self.cholesterol, '', 'TEXT', 'Cholesterol'),
					'Triglycerides':(self.triglycerides, '', 'TEXT', 'Triglycerides')}
		
		for key in entries:
			try:
				self.cursor.execute('''SELECT %s FROM Eclampsia WHERE PID=?''' % key, (self.pid,))
				query = self.cursor.fetchall()
				if query:
					if ((query[0][0] != entries[key][1]) & (entries[key][0] != query[0][0]) 
						& (entries[key][0] != entries[key][1]) & (query[0][0] != None)):
						# User is about to change an existing, non-default entry, confirm changes
						if tkMessageBox.askyesno(
								title='Database Overwrite Alert',
								message='%s already exists in database: \n\n Current Value: %s \n\n New Value: %s \n\n Overwrite?' 
								% (entries[key][3], query[0][0], entries[key][0])):
							self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][0], self.pid))
							self.conn.commit()
					else:
						self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][0], self.pid))
						self.conn.commit()
			except sqlite3.OperationalError:
				# Column does not exist in table, so add
				self.cursor.execute('''ALTER TABLE Eclampsia ADD COLUMN %s %s''' % (key, entries[key][2]))
				self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][0], self.pid))
				self.conn.commit()
		util.close_db(self, self.conn, self.cursor)
		
if __name__ == "__main__":
	MedicalHistoryPage(self.pid, self.link, self.root)
