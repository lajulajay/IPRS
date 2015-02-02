import os.path, sqlite3
"""
Utility methods for EclampsiaModel
"""

def open_db(self, link=None):
	"""
	Open database.
	"""
	if link == None:
		link = str(os.path.expanduser('~')+'/iprs.db')
	conn = sqlite3.connect(link)
	conn.text_factory = str
	cursor = conn.cursor()
	return (conn, cursor)

def close_db(self, conn, cursor):
	"""
	Close database.
	"""
	cursor.close()
	conn.close()

def retrieve_dbvalue(self, cursor, pid, column, default=''):
	"""
	Retrieve value stored in database.
	Return default if no value in database.
	"""
	cursor.execute('''SELECT %s FROM Eclampsia WHERE PID=?''' % column, (self.pid,))
	query = cursor.fetchall()
	if query:
		return query[0][0]
	else:
		return default

def str2list(self, input_string):
	"""
	Convert string to list.
	"""
	output_string = input_string.strip(', ')
	output_string = output_string.split(', ')
	return output_string
	
def list2str(self, input_listbox, input_index):
	"""
	Convert list to string for easy db storage.
	"""
	input_list = list()
	for item in input_index[:]:
		input_list.append(input_listbox.get(item))
	output_str = str()
	if input_list:
		for item in input_list:
			output_str += item + ', '
	return output_str
