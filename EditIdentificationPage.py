import tkMessageBox
import Tkinter as tk
import datetime as dt
import EclampsiaUtility as util

class EditIdentificationPage:
	"""Patient Identification Page"""
	
	def __init__(self, pid, link='', root=None):
		"""
		Retrieve essentials from calling page.
		Create root (new Tkinter object) if necessary.
		Create frame (container for all widgets).
		Create widgets and apply them to frame via grid.
		"""
		# Retrieve essentials
		self.pid = pid
		self.link = link
		
		# Create root
		if root == None:
			self.root = tk.Tk()
		else:
			self.root = root
		self.root.title('Patient Identification Page')
		self.root.geometry('600x400+0+0')
		
		# Create frame
		self.frame = tk.Frame(self.root)
		self.frame.pack()
		
		# Create main page button widget
		self.mainpage_button = tk.Button(self.frame, text='<--Main', command=lambda x='MainPage': self.__nextpage(x))
		self.mainpage_button.grid(row=0, column=0)
		
		# Create medical history page button widget
		self.medicalhistory_button = tk.Button(self.frame, text='History-->', command=lambda x='MedicalHistory': self.__nextpage(x))
		self.medicalhistory_button.grid(row=0, column=3)
		
		# Create horizontal placeholder1 frame
		self.horizontal_placeholder1 = tk.Frame(self.frame, height=10)
		self.horizontal_placeholder1.grid(row=1, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)

		# Create vertical placeholder1 frame
		self.vertical_placeholder1 = tk.Frame(self.frame, width=10)
		self.vertical_placeholder1.grid(row=2, rowspan=8, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create vertical placeholder2 frame
		self.vertical_placeholder2 = tk.Frame(self.frame, width=25)
		self.vertical_placeholder2.grid(row=2, rowspan=8, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
	
		# Open database
		[self.conn, self.cursor] = util.open_db(self,link=self.link)
		
		# Create first name label widget
		self.firstname_label = tk.Label(self.frame, text='First Name *')
		self.firstname_label.grid(row=2, column=1)
	
		# Create first name entry widget
		self.firstname_value = tk.StringVar()
		self.firstname_entry = tk.Entry(self.frame, textvariable=self.firstname_value)
		self.firstname_entry.grid(row=2, column=2, pady=1)
		self.firstname_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'FirstName')
		self.firstname_value.set(self.firstname_dbvalue)
		
		# Create middle initial label widget
		self.middleinitial_label = tk.Label(self.frame, text='Middle Initial')
		self.middleinitial_label.grid(row=3, column=1)
		
		# Create middle initial entry widget
		self.middleinitial_value = tk.StringVar()
		self.middleinitial_entry = tk.Entry(self.frame, textvariable=self.middleinitial_value)
		self.middleinitial_entry.grid(row=3, column=2, pady=1)
		self.middleinitial_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'MiddleInitial', default='')
		self.middleinitial_value.set(self.middleinitial_dbvalue)
		
		# Create last name label widget
		self.lastname_label = tk.Label(self.frame, text='Last Name *')
		self.lastname_label.grid(row=4, column=1)
	
		# Create last name entry widget
		self.lastname_value = tk.StringVar()
		self.lastname_entry = tk.Entry(self.frame, textvariable=self.lastname_value)
		self.lastname_entry.grid(row=4, column=2, pady=1)
		self.lastname_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'LastName')
		self.lastname_value.set(self.lastname_dbvalue)
		
		# Create birth date label widget
		self.birthdate_label = tk.Label(self.frame, text='Birthdate *\n (MM/DD/YYYY)')
		self.birthdate_label.grid(row=5, column=1)
		
		# Create birth date entry widget
		self.birthdate_value = tk.StringVar()
		self.birthdate_entry = tk.Entry(self.frame, textvariable=self.birthdate_value)
		self.birthdate_entry.grid(row=5, column=2, pady=1)
		self.birthdate_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'BirthDate')
		self.birthdate_value.set(self.birthdate_dbvalue)
		self.age_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Age')
		
		# Create height label widget
		self.height_label = tk.Label(self.frame, text='Height (m)')
		self.height_label.grid(row=6, column=1)
	
		# Create height entry widget
		self.height_value = tk.DoubleVar()
		self.height_entry = tk.Entry(self.frame, textvariable=self.height_value)
		self.height_entry.grid(row=6, column=2, pady=1)
		self.height_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Height', default=-1.0)
		if self.height_dbvalue != 1.0:
			self.height_value.set(self.height_dbvalue)
		
		# Create weight label widget
		self.weight_label = tk.Label(self.frame, text='Weight (kg)')
		self.weight_label.grid(row=7, column=1)
	
		# Create weight entry widget
		self.weight_value = tk.DoubleVar()
		self.weight_entry = tk.Entry(self.frame, textvariable=self.weight_value)
		self.weight_entry.grid(row=7, column=2, pady=1)
		self.weight_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Weight', default=-1.0)
		if self.weight_dbvalue != -1.0:
			self.weight_value.set(self.weight_dbvalue)
			
		# Create race label widget
		self.race_label = tk.Label(self.frame, text='Race')
		self.race_label.grid(row=8, column=1)
		
		# Create race listbox widget
		self.race_listbox = tk.Listbox(self.frame, height=5, selectmode=tk.MULTIPLE)
		self.race_listbox.grid(row=8, column=2, pady=1)
		race_list = ['American Indian', 'Asian', 'Black', 'Pacific Islander', 'White']
		for item in race_list:
			self.race_listbox.insert(tk.END, item)
		self.race_dbvalue = util.retrieve_dbvalue(self, self.cursor, self.pid, 'Race', default='')
		if self.race_dbvalue:
			self.race_dbvalue = util.str2list(self, self.race_dbvalue)
			for item in self.race_dbvalue:
				index = race_list.index(item)
				self.race_listbox.selection_set(first=index)
		self.race_listbox.bind('<<ListboxSelect>>', self.activate_race)
		self.race_activate_status = 0
				
		# Create horizontal placeholder2 frame
		self.horizontal_placeholder2 = tk.Frame(self.frame, height=55)
		self.horizontal_placeholder2.grid(row=9, column=1, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
		
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
		import EclampsiaModel, EditMedicalHistoryPage
		if page == 'MainPage':
			EclampsiaModel.EclampsiaModel(self.root)
		elif page == 'MedicalHistory':
			EditMedicalHistoryPage.EditMedicalHistoryPage(self.pid, self.link, self.root)
	
	def validate_firstname(self):
		""" 
		Validate first name entry.
		Return status of 0 if invalid/missing, 1 if valid.
		"""
		self.firstname = self.firstname_value.get()
		self.validate_firstname_status = 1
		if not self.firstname:
			tkMessageBox.showerror(
				title='Missing Data',
				message='First Name required to proceed')
			self.validate_firstname_status = 0
		elif not self.firstname.isalpha():
			tkMessageBox.showerror(
				title='Invalid Data',
				message='First Name required to proceed')
			self.validate_firstname_status = 0
					
	def validate_lastname(self):
		""" 
		Validate last name entry.
		Return status of 0 if invalid/missing, 1 if valid.
		"""
		self.lastname = self.lastname_value.get()
		self.validate_lastname_status = 1
		if not self.lastname:
			tkMessageBox.showerror(
				title='Missing Data',
				message='Last Name required to proceed')
			self.validate_lastname_status = 0
		elif not self.lastname.isalpha():
			tkMessageBox.showerror(
				title='Invalid Data',
				message='Last Name required to proceed')
			self.validate_lastname_status = 1
			
	def validate_middleinitial(self):
		""" 
		Validate middle initial entry.
		Set to default (Null) if invalid/missing.
		"""
		self.middleinitial = self.middleinitial_value.get()
		if not self.middleinitial:
			self.middleinitial = ''
		elif not (self.middleinitial.isalpha() & len(self.middleinitial) == 1):
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting single letter for Middle Initial')
			self.middleinitial = ''
		
	def validate_birthdate(self):
		"""
		Validate birthdate entry.
		Calculate age from birthdate.
		Return status of 0 if invalid/missing, 1 if valid.
		"""
		self.birthdate = self.birthdate_value.get()
		if not self.birthdate:
			tkMessageBox.showerror(
				title='Missing Data',
				message='Birth Date required to proceed')
			self.validate_birthdate_status = 0
		else:
			try:
				self.birthdate_object = dt.datetime.strptime(self.birthdate, '%m/%d/%Y')
				self.validate_birthdate_status = 1
			except ValueError:
				tkMessageBox.showerror(
					title='Invalid Data',
					message='Birth Date (MM/DD/YYY) required to proceed')
				self.validate_birthdate_status = 0
		if self.validate_birthdate_status:
			self.calculate_age()
		
	def calculate_age(self):
		"""
		Calculate age.
		"""
		days_in_year = 365.25
		__birthdate = self.birthdate_object.date()
		self.age = int((dt.date.today() - __birthdate).days/days_in_year)
		
	def validate_height(self):
		""" 
		Validate height entry.
		Set to default (-1.0) if invalid/missing.
		"""
		try:	
			self.height = self.height_value.get()
			if self.height:
				if not (0.1 < self.height < 3.0):
					tkMessageBox.showwarning(
						title='Invalid Data',
						message='Expecting Height between 0 and 3.0')
					self.height = -1.0
		except ValueError:
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting Height between 0 and 3.0')
			self.height = -1.0
		
	def validate_weight(self):
		""" 
		Validate weight entry.
		Set to default (-1.0) if invalid/missing.
		"""
		try:
			self.weight = self.weight_value.get()
			if self.weight:
				if not (0 < self.weight < 300.0):
					tkMessageBox.showwarning(
						title='Invalid Weight',
						message='Expecting Weight between 0 and 300.0')
					self.weight = -1.0
		except ValueError:
			tkMessageBox.showwarning(
				title='Invalid Weight',
				message='Expecting Weight between 0 and 300.0')
			self.weight = -1.0
			
	def activate_race(self, event):
		""" 
		Activate race selection.
		"""
		self.race_activate_status = 1
		race_index = self.race_listbox.curselection()
		# Older versions of Tkinter return index as str vs int
		try:
			race_index = map(int, race_index)
		except ValueError:
			pass
		self.race = util.list2str(self, self.race_listbox, race_index)
			
	def validate_race(self):
		"""
		Validate race entry.
		Set to default (Null) if no selection.
		"""
		if self.race_activate_status:
			try:
				self.race
			except AttributeError:
				self.race = ''
		else:
			self.race = self.race_dbvalue
				
	def __save(self):
		""" 
		Validate widget entries/selections. 
		Write entries/selections to database.
		"""
		self.validate_firstname()
		self.validate_lastname()
		self.validate_birthdate()
		self.validate_middleinitial()
		self.validate_height()
		self.validate_weight()
		self.validate_race()
		self.__update_db()
		return
	
	def __update_db(self):
		"""
		Update database.
		"""
		import sqlite3
		# Entries (column, current value, new value) 
		entries = {'FirstName':(self.firstname_dbvalue, self.firstname),
					'MiddleInitial':(self.middleinitial_dbvalue,self.middleinitial),
					'LastName':(self.lastname_dbvalue, self.lastname), 
					'Birthdate':(self.birthdate_dbvalue, self.birthdate),
					'Age':(self.age_dbvalue, self.age),
					'Height':(self.height_dbvalue, self.height), 
					'Weight':(self.weight_dbvalue, self.weight),
					'Race':(self.race_dbvalue, self.race)}
		
		for key in entries:
			if (entries[key][0] != entries[key][1]):
				self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][1], self.pid))
				self.conn.commit()

if __name__ == "__main__":
	EditIdentificationPage()
