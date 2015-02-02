import tkMessageBox	
import Tkinter as tk

class DisplayDatabasePage:
	"""Display Database Contents"""
	
	def __init__(self, link):
		"""
		Retrieve db contents.
		Display db contents.
		"""
		
		# Retrieve essential details from calling page
		self.link = link
		
		# Create root
		self.root = tk.Tk()
		self.root.title('Database: All Patients')
		self.root.geometry('1000x500+0+0')
		
		# Create canvas
		self.canvas = tk.Canvas(self.root)
		
		# Create/Pack scrollbars
		self.yscrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
		self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
		self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
		
		# Pack canvas
		self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		
		# Attach canvas to scrollbars
		self.canvas.configure(xscrollcommand=self.xscrollbar.set)
		self.canvas.configure(yscrollcommand=self.yscrollbar.set)
		
		# Create frame inside canvas
		self.frame = tk.Frame(self.canvas)
		self.canvas.create_window((0,0), window=self.frame, anchor=tk.NW)
		self.frame.bind('<Configure>', self.set_scrollregion)
		
		# Display db contents
		self.print_dbcontents()
		
		# Invoke main loop
		self.root.mainloop()
	
	def set_scrollregion(self, event):
		"""
		Set scroll region within canvas.
		"""
		self.canvas.configure(scrollregion=self.canvas.bbox('all'))
	
	def print_dbcontents(self):
		"""
		Output db contents.
		"""
		import sqlite3
		import EclampsiaUtility as util
		(self.conn, self.cursor) = util.open_db(self, link=self.link)
		count_query = self.cursor.execute('''SELECT COUNT(PID) FROM Eclampsia''')
		count = count_query.fetchall()
		if count:
			# Get total number of records in db
			dbnrows = count[0][0]
			content_query = self.cursor.execute('''SELECT * FROM Eclampsia''')
			# Get db column names
			dbcolumn_names = [tuple[0] for tuple in content_query.description]
			# Format db column names
			dbcolumn_names = self.format_columns(dbcolumn_names)
			# Output table title (db column names)
			for name in dbcolumn_names:
					self.label = tk.Label(self.frame, text=name)
					self.label.grid(row=0, column=dbcolumn_names.index(name))
			# Output cosmetic divider line
			self.label_line = tk.Label(self.frame, text=('+'*200))
			self.label_line.grid(row=1, column=0, columnspan=len(dbcolumn_names))
			contents = content_query.fetchall()
			# Output db contents (all records)
			for dbrow in range(dbnrows):
				for dbcol in range(len(contents[dbrow])):
					if type(contents[dbrow][dbcol]) is str:
						entry = self.format_contents(contents[dbrow][dbcol])
						self.entry_label = tk.Label(self.frame, text=entry)
					else:
						self.entry_label = tk.Label(self.frame, text=contents[dbrow][dbcol])
					self.entry_label.grid(row=dbrow+2, column=dbcol)
		else:
			tkMessageBox.showerror(
				title='Database Error',
				message='Database is empty')
		util.close_db(self, self.conn, self.cursor)
	
	def format_contents(self, contents):
		"""
		Format db strings: 
			Strip trailing ','
			Replace other occurences of ',' with '\n'
		"""
		if ',' in contents:
			stripped_contents = contents.strip(', ')
			formatted_contents = stripped_contents.replace(',', ' \n ')
		else:
			formatted_contents = contents
		return formatted_contents
	
	def format_columns(self, column_names):
		"""
		Format db column names: 
			Insert new line ('\n') between concanated strings.
		"""
		if len(column_names):
			try:
				column_names[column_names.index('FirstName')] = 'First \n Name'
			except ValueError:
				pass
			try:
				column_names[column_names.index('LastName')] = 'Last \n Name'
			except ValueError:
				pass
			try:
				column_names[column_names.index('MiddleInitial')] = 'Middle \n Initial'
			except ValueError:
				pass
			try:
				column_names[column_names.index('BloodPressure_Sys')] = 'Blood \n Pressure \n (Systolic)'
			except ValueError:
				pass
			try:
				column_names[column_names.index('BloodPressure_Dis')] = 'Blood \n Pressure \n (Diastolic)'
			except ValueError:
				pass
			try:
				column_names[column_names.index('CurrentConditions')] = 'Current \n Conditions'
			except ValueError:
				pass
			try:
				column_names[column_names.index('PreviousConditions')] = 'Previous \n Conditions'
			except ValueError:
				pass
			try:
				column_names[column_names.index('PregnancyHistory')] = 'Pregnancy \n History'
			except ValueError:
				pass
			try:
				column_names[column_names.index('ChildrenExpected')] = 'Children \n Expected'
			except ValueError:
				pass
			try:
				column_names[column_names.index('PregnancyInterval')] = 'Pregnancy \n Interval'
			except ValueError:
				pass
			try:
				column_names[column_names.index('PaternityChange')] = 'Paternity \n Change'
			except ValueError:
				pass
			try:
				column_names[column_names.index('FamilyHistory')] = 'Family \n History'
			except ValueError:
				pass
		return column_names

if __name__ == "__main__":
	DisplayDatabasePage(self.link)
