import tkMessageBox	
import Tkinter as tk
from ttk import *
import datetime as dt

class EclampsiaModel:
	"""Main Page"""
	
	def __init__(self, root=None):
		"""
		Create root (new Tkinter object).
		Create frame (container for all widgets).
		Create widgets and apply them to frame via grid.
		"""
		# Create root
		if root == None:
			self.root = tk.Tk()
		else:
			self.root = root
		self.root.title('Eclampsia Model')
		self.root.geometry('600x400+0+0')
		
		# Create frame
		self.frame = tk.Frame(self.root)
		self.frame.pack()
			
		# Create horizontal placeholder1 frame 
		self.horizontal_placeholder1 = tk.Frame(self.frame, height=50)
		self.horizontal_placeholder1.grid(row=0, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create new patient button widget
		self.newpatient_button = tk.Button(self.frame, text='New Patient', command=lambda x='NewPatient': self.__nextpage(x))
		self.newpatient_button.grid(row=1, column=0)
		
		# Create view/edit patient button widget
		self.editpatient_button = tk.Button(self.frame, text='View/Edit Patient', command=lambda x='EditPatient': self.__nextpage(x))
		self.editpatient_button.grid(row=1, column=1)
		
		# Create view database button widget
		self.allpatients_button = tk.Button(self.frame, text='All Patients', command=lambda x='AllPatients': self.__nextpage(x))
		self.allpatients_button.grid(row=1, column=2)
		
		# Create horizontal placeholder2 frame 
		self.horizontal_placeholder2 = tk.Frame(self.frame, height=10)
		self.horizontal_placeholder2.grid(row=2, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create first name label widget
		self.firstname_label = tk.Label(self.frame, text='First Name')
		self.firstname_label.grid(row=3, column=1)
	
		# Create first name entry widget
		self.firstname_entry = tk.Entry(self.frame)
		self.firstname_entry.grid(row=4, column=1)
		
		# Create last name label widget
		self.lastname_label = tk.Label(self.frame, text='Last Name')
		self.lastname_label.grid(row=5, column=1)
	
		# Create last name entry widget
		self.lastname_entry = tk.Entry(self.frame)
		self.lastname_entry.grid(row=6, column=1)
		
		# Create birth date label widget
		self.birthdate_label = tk.Label(self.frame, text='Birthdate (MM/DD/YYYY)')
		self.birthdate_label.grid(row=7, column=1)
		
		# Create birth date entry widget
		self.birthdate_entry = tk.Entry(self.frame)
		self.birthdate_entry.grid(row=8, column=1)
		
		# Create horizontal placeholder3 frame 
		self.horizontal_placeholder3 = tk.Frame(self.frame, height=10)
		self.horizontal_placeholder3.grid(row=9, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create OR label widget
		self.or_label = tk.Label(self.frame, text='OR')
		self.or_label.grid(row=10, column=1)
		
		# Create horizontal placeholder4 frame 
		self.horizontal_placeholder4 = tk.Frame(self.frame, height=10)
		self.horizontal_placeholder4.grid(row=11, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create pid label widget
		self.pid_label = tk.Label(self.frame, text='Patient ID')
		self.pid_label.grid(row=12, column=1)
		
		# Create pid entry widget
		self.pid_entry = tk.Entry(self.frame)
		self.pid_entry.grid(row=13, column=1)
		
		# Set link
		import os.path
		self.link = str(os.path.expanduser('~')+'/iprs.db')
		
		# Invoke main loop
		self.root.mainloop()
	
	def __nextpage(self, page):
		""" 
		Close current page. Call new page.
		"""
		import IdentificationPage, EditIdentificationPage, DisplayDatabasePage
		if page == 'NewPatient':
			self.frame.destroy()
			IdentificationPage.IdentificationPage(root=self.root)
		elif page == 'EditPatient':
			self.retrieve_pid()
			if self.pid_status:
				self.frame.destroy()
				EditIdentificationPage.EditIdentificationPage(self.pid, link=self.link, root=self.root)
		else:
			DisplayDatabasePage.DisplayDatabasePage(self.link)
			
	def retrieve_pid(self):
		"""
		Retrieve PID.
		"""
		self.validate_firstname()
		self.validate_lastname()
		self.validate_birthdate()
		self.validate_pid()
		self.pid_status = 0
		
		if self.validate_firstname_status & self.validate_lastname_status & self.validate_birthdate_status:
			self.search_database('FLB')
		elif self.validate_pid_status:
			self.search_database('PID')
		else:
			tkMessageBox.showerror(
				title='Missing/Invalid Patient Data', 
				message='Must provide: \n\n First Name \n Last Name \n Birth Date (MM/DD/YYYY) \n\n OR \n\n Patient ID') 
		
	def search_database(self, method):
		"""
		Search database for specified patient.
		FLB: use First name, Last name, Birth date.
		PID: use Patient ID.
		"""
		import sqlite3
		try: 
			db_handle = open(self.link, 'r')
			db_handle.close()
			try:
				self.__conn = sqlite3.connect(self.link)
				self.__conn.text_factory = str
				self.__cursor = self.__conn.cursor()
				table_query = self.__cursor.execute('''SELECT * FROM sqlite_master WHERE type="table" AND name="Eclampsia"''')
				if not table_query:
					tkMessageBox.showerror(title='Database Error', message='Eclampsia table does not exist in database')
				else:
					if method == 'FLB':
						self.__cursor.execute('''SELECT PID FROM Eclampsia WHERE FirstName=? AND LastName=? AND Birthdate=?''', 
						(self.firstname, self.lastname, self.birthdate))
						pid_query = self.__cursor.fetchall()
						if pid_query:
							if len(pid_query) == 1:
								self.pid = pid_query[0][0]
								self.pid_status = 1
							elif len(pid_query) > 1:
								tkMessageBox.showerror(
									title='Database Duplicate Error', 
									message='Multiple entries detected for: \n\n First Name: %s \n Last Name: %s \n Birth Date: %s' 
									% (self.firstname, self.lastname, self.birthdate))
						else:
							tkMessageBox.showerror(
								title='Database Match Error', 
								message='No match in database for: \n\n First Name: %s \n Last Name: %s \n Birth Date: %s' 
								% (self.firstname, self.lastname, self.birthdate)) 
					elif method == 'PID':
						self.__cursor.execute('''SELECT * FROM Eclampsia WHERE PID=?''', (self.pid_value,))
						patient_query = self.__cursor.fetchall()
						if patient_query:
							self.pid = self.pid_value
							self.pid_status = 1
						else:
							tkMessageBox.showerror(
								title='Database Match Error', 
								message='No match in database for PID=%s' % self.pid_value)
			except sqlite3.OperationalError:
				pass
		except IOError: 
			tkMessageBox.showerror(title='Database Error', message='Database does not exist')
	
	def validate_firstname(self):
		""" 
		Validate first name entry.
		Return status of 0 if invalid, 1 if valid.
		"""
		self.firstname = self.firstname_entry.get()
		self.validate_firstname_status = 0
		if self.firstname:
			if self.firstname.isalpha():
				self.validate_firstname_status = 1
					
	def validate_lastname(self):
		""" 
		Validate last name entry.
		Return status of 0 if invalid, 1 if valid.
		"""
		self.lastname = self.lastname_entry.get()
		self.validate_lastname_status = 0
		if self.lastname:
			if self.lastname.isalpha():
				self.validate_lastname_status = 1
		
	def validate_birthdate(self):
		"""
		Validate birthdate entry.
		Return status of 0 if invalid, 1 if valid.
		"""
		self.birthdate = self.birthdate_entry.get()
		self.validate_birthdate_status = 0
		if self.birthdate:
			try:
				self.birthdate_object = dt.strptime(self.birthdate, '%m/%d/%Y')
				self.validate_birthdate_status = 1
			except ValueError:
				pass
				
	def validate_pid(self):
		""" 
		Validate pid entry.
		Return status of 0 if invalid, 1 if valid.
		"""
		self.pid_value = self.pid_entry.get()
		self.validate_pid_status = 0
		if self.pid_value:
			if self.pid_value.isdigit():
				if self.pid_value > 0:
					self.validate_pid_status = 1
					self.pid_value = int(self.pid_value)

if __name__ == "__main__":
	EclampsiaModel()
		
