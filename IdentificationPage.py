import tkMessageBox
import Tkinter as tk
import datetime as dt

class IdentificationPage:
	"""Patient Identification Page"""
	
	def __init__(self, pid=-1, link='', root=None):
		"""
		Retrieve essentials from calling page.
		Create root (new Tkinter object) if necessary.
		Create frame (container for all widgets).
		Create widgets and apply them to frame via grid.
		"""
		# Retrieve essentials from last page
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
	
		# Create first name label widget
		self.firstname_label = tk.Label(self.frame, text='First Name *')
		self.firstname_label.grid(row=2, column=1)
	
		# Create first name entry widget
		self.firstname_entry = tk.Entry(self.frame)
		self.firstname_entry.grid(row=2, column=2, pady=1)
		
		# Create middle initial label widget
		self.middleinitial_label = tk.Label(self.frame, text='Middle Initial')
		self.middleinitial_label.grid(row=3, column=1)
		
		# Create middle initial entry widget
		self.middleinitial_entry = tk.Entry(self.frame)
		self.middleinitial_entry.grid(row=3, column=2, pady=1)
		
		# Create last name label widget
		self.lastname_label = tk.Label(self.frame, text='Last Name *')
		self.lastname_label.grid(row=4, column=1)
	
		# Create last name entry widget
		self.lastname_entry = tk.Entry(self.frame)
		self.lastname_entry.grid(row=4, column=2, pady=1)
		
		# Create birth date label widget
		self.birthdate_label = tk.Label(self.frame, text='Birthdate *\n (MM/DD/YYYY)')
		self.birthdate_label.grid(row=5, column=1)
		
		# Create birth date entry widget
		self.birthdate_entry = tk.Entry(self.frame)
		self.birthdate_entry.grid(row=5, column=2, pady=1)
		
		# Create height label widget
		self.height_label = tk.Label(self.frame, text='Height (m)')
		self.height_label.grid(row=6, column=1)
	
		# Create height entry widget
		self.height_entry = tk.Entry(self.frame)
		self.height_entry.grid(row=6, column=2, pady=1)
		
		# Create weight label widget
		self.weight_label = tk.Label(self.frame, text='Weight (kg)')
		self.weight_label.grid(row=7, column=1)
	
		# Create weight entry widget
		self.weight_entry = tk.Entry(self.frame)
		self.weight_entry.grid(row=7, column=2, pady=1)
			
		# Create race label widget
		self.race_label = tk.Label(self.frame, text='Race')
		self.race_label.grid(row=8, column=1)
		
		# Create race listbox widget
		self.race_listbox = tk.Listbox(self.frame, height=5, selectmode=tk.MULTIPLE)
		self.race_listbox.grid(row=8, column=2, pady=1)
		for item in ['American Indian', 'Asian', 'Black', 'Pacific Islander', 'White']:
			self.race_listbox.insert(tk.END, item)
		self.race_listbox.bind('<<ListboxSelect>>', self.activate_race)
				
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
		import EclampsiaModel, MedicalHistoryPage
		if page == 'MainPage':
			EclampsiaModel.EclampsiaModel(self.root)
		elif page == 'MedicalHistory':
			MedicalHistoryPage.MedicalHistoryPage(self.pid, self.link, self.root)
	
	def validate_firstname(self):
		""" 
		Validate first name entry.
		Return status of 0 if invalid/missing, 1 if valid.
		"""
		self.firstname = self.firstname_entry.get()
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
		self.lastname = self.lastname_entry.get()
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
		Set to default (empty) if invalid/missing.
		"""
		self.middleinitial = self.middleinitial_entry.get()
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
		self.birthdate = self.birthdate_entry.get()
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
			self.height = self.height_entry.get()
			if not self.height:
				tkMessageBox.showwarning(
					title='Missing Data',
					message='No entry for Height')
				self.height = -1.0
			elif not (0.1 < float(self.height) < 3.0):
				tkMessageBox.showwarning(
					title='Invalid Data',
					message='Expecting Height between 0 and 3.0')
				self.height = -1.0
			else:
				self.height = float(self.height)
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
			self.weight = self.weight_entry.get()
			if not self.weight:
				tkMessageBox.showwarning(
					title='Missing Data',
					message='No entry for Weight')
				self.weight = -1.0
			elif not (0 < float(self.weight) < 300.0):
				tkMessageBox.showwarning(
					title='Invalid Data',
					message='Expecting Weight between 0 and 300.0')
				self.weight = -1.0
			else:
				self.weight = float(self.weight)
		except ValueError:
			tkMessageBox.showwarning(
				title='Invalid Data',
				message='Expecting Weight between 0 and 300.0')
			self.weight = -1.0
			
	def activate_race(self, event):
		""" 
		Activate race selection.
		"""
		import EclampsiaUtility as util
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
		Set to default (empty) if no selection.
		"""
		try:
			self.race
		except AttributeError:
			tkMessageBox.showwarning(
				title='Missing Data',
				message='No selection for Race')
			self.race = ''
				
	def __save(self):
		""" 
		Validate widget entries/selections. 
		Write entries/selections to database.
		"""
		self.validate_firstname()
		self.validate_lastname()
		self.validate_birthdate()
		if (self.validate_firstname_status & self.validate_lastname_status & self.validate_birthdate_status):
			self.validate_middleinitial()
			self.validate_height()
			self.validate_weight()
			self.validate_race()
			self.setup_db()
			self.__write2db()
		return
	
	def setup_db(self):
		"""
		Create database if necessary.
		Write exit status (0: failure, 1: success)
		"""
		import os.path
		self.db_status = 0
		if not self.link:
			self.link = str(os.path.expanduser('~')+'/iprs.db')
		try:
			db_handle = open(self.link, 'r+')
			self.db_status = 1
			db_handle.close()
		except IOError:
			tkMessageBox.showwarning(
				title='Database Error',
				message='Database does not exist. \n Will attempt to create.')
			try:
				db_handle = open(self.link,'w')
				self.db_status = 1
				db_handle.close()
			except IOError:
				tkMessageBox.showerror(
					title='Database Error',
					message='Unable to create database')
		except OperationalError:
			tkMessageBox.showerror(
				title='Database Error',
				message='Unable to access database')
	
	def __write2db(self):
		"""
		Write entries to database.
		"""
		import sqlite3
		import EclampsiaUtility as util
		if self.db_status:
			# Database exists so open
			(self.conn, self.cursor) = util.open_db(self, link=self.link)
			self.cursor.execute('''SELECT * FROM sqlite_master WHERE type="table" AND name="Eclampsia"''')
			table_query = self.cursor.fetchall()
			if not table_query:
				# Table does not exist so create
				self.cursor.execute('''CREATE TABLE Eclampsia(PID INTEGER PRIMARY KEY, 
				FirstName TEXT, MiddleInitial TEXT, LastName TEXT, Birthdate TEXT, 
				Age INTEGER, Height FLOAT, Weight FLOAT, Race TEXT)''')
				self.cursor.execute('''INSERT into Eclampsia 
				(FirstName, MiddleInitial, LastName, BirthDate, Age, Height, Weight, Race) 
				VALUES(?,?,?,?,?,?,?,?)''', (self.firstname, self.middleinitial, self.lastname, 
				self.birthdate, self.age, self.height, self.weight, self.race))
				self.conn.commit()
				self.pid = self.cursor.lastrowid
			else:
				self.cursor.execute('''SELECT PID FROM Eclampsia WHERE FirstName=? AND LastName=? AND Birthdate=?''', 
				(self.firstname, self.lastname, self.birthdate))
				pid_query = self.cursor.fetchall()
				if pid_query:
					if len(pid_query) == 1:
						# Located PID based on mandatory entries
						self.pid = pid_query[0][0]
						self.__update_db()
					elif len(pid_query) > 1:
						# Mandatory entries map to multiple PIDs; warn user and exit
						tkMessageBox.showerror(
							title='Database Duplicate Error',
							message='Multiple entries detected for: \n\n%s \n%s \n%s' 
							% (self.firstname, self.lastname, self.birthdate))
				else:
					self.cursor.execute('''INSERT into Eclampsia 
					(FirstName, MiddleInitial, LastName, BirthDate, Age, Height, Weight, Race) 
					VALUES(?,?,?,?,?,?,?,?)''', (self.firstname, self.middleinitial, self.lastname, 
					self.birthdate, self.age, self.height, self.weight, self.race))
					self.conn.commit()
					self.pid = self.cursor.lastrowid
			util.close_db(self, self.conn, self.cursor)
		else:
			tkMessageBox.showerror(title='Database Error', message='Database does not exist. Aborting write')
							
	def __update_db(self):
		"""
		Update database.
		"""
		import sqlite3
		# Entries (column, current value, default value, full name) 
		entries = {'FirstName':(self.firstname, self.firstname, 'First Name'),
					'MiddleInitial':(self.middleinitial, '', 'Middle Initial'),
					'LastName':(self.lastname, self.lastname, 'Last Name'), 
					'Birthdate':(self.birthdate, self.birthdate, 'Birth Date'),
					'Age':(self.age, self.age, 'Age'),
					'Height':(self.height, -1.0, 'Height'), 
					'Weight':(self.weight, -1.0, 'Weight'),
					'Race':(self.race, '', 'Race')}
		
		for key in entries:
			self.cursor.execute('''SELECT %s FROM Eclampsia WHERE PID=?''' % key, (self.pid,))
			query = self.cursor.fetchall()
			if ((query[0][0] != entries[key][1]) & (entries[key][0] != query[0][0]) 
				& (entries[key][0] != entries[key][1]) & (query[0][0] != None)):
				# User is about to change an existing, non-default entry, confirm changes
				if tkMessageBox.askyesno(
						title='Database Overwrite Alert',
						message='%s already exists in database: \n\n Current Value: %s \n\n New Value: %s \n\n Overwrite?' 
						% (entries[key][2], query[0][0], entries[key][0])): 
					self.cursor.execute('''UPDATE Eclampsia SET %s=? WHERE PID=?''' % key, (entries[key][0], self.pid))
					self.conn.commit()
							
if __name__ == "__main__":
	IdentificationPage()
