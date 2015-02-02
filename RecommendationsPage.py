import tkMessageBox
import Tkinter as tk

class RecommendationsPage:
	"""Recommendations Page"""
	
	def __init__(self, pid, link, root):
		"""
		Initialize root (new Tkinter object).
		Create frame (container for all widgets).
		Create widgets and apply them to frame via grid.
		"""
		# Initialize root
		self.root = root
		self.root.title('Patient Recommendations Page')
		
		# Create frame
		self.frame = tk.Frame(self.root)
		self.frame.pack()
	
		# Create risk factors page button widget
		self.riskfactors_button = tk.Button(self.frame, text='<--Risk', command=lambda x='RiskFactors': self.__nextpage(x))
		self.riskfactors_button.grid(row=0, column=0)
		
		# Create main page button widget
		self.mainpage_button = tk.Button(self.frame, text='Main', command=lambda x='MainPage': self.__nextpage(x))
		self.mainpage_button.grid(row=0, column=1)
		
		# Create recommendations button widget
		self.recommendations_button = tk.Button(self.frame, text='Show', command=self.display_all)
		self.recommendations_button.grid(row=0, column=2)
		
		# Create horizontal placeholder frame
		self.horizontal_placeholder = tk.Frame(self.frame, height=10)
		self.horizontal_placeholder.grid(row=1, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
		
		# Create text widget
		self.textbox = tk.Text(self.frame, width=60, height=20)
		self.textbox.grid(row=2, column=1, sticky=tk.E+tk.W)
		self.textbox.tag_config('underline', underline=1)
		
		# Retrieve essentials from last page 
		self.pid = pid
		self.link = link
		
		# Invoke main loop
		self.root.mainloop()
	
	def __nextpage(self, page):
		"""
		Close current page.
		Call new page.
		"""	
		self.frame.destroy()
		import RiskFactorsPage, EclampsiaModel
		if page == 'RiskFactors':
			RiskFactorsPage.RiskFactorsPage(self.pid, self.link, self.root)
		elif page == 'MainPage':
			EclampsiaModel.EclampsiaModel(root=self.root)

	def __retrieve_records(self):
		"""
		Retrieve entries/selections from database.
		"""
		import sqlite3
		import EclampsiaUtility as util
		(self.conn, self.cursor) = util.open_db(self, link=self.link)
		self.entries = {'FirstName':'',
					'MiddleInitial':'',
					'LastName':'',
					'Age':-1,
					'Height':-1.0,
					'Weight':-1.0,
					'Race':'',
					'BloodPressure_Sys':-1,
					'BloodPressure_Dis':-1,
					'CurrentConditions':'', 
					'PreviousConditions':'',
					'Cholesterol':'',
					'Triglycerides':'',
					'PregnancyHistory':'',
					'ChildrenExpected':'',
					'Trimester':'',
					'PregnancyInterval':'',
					'PaternityChange':'',
					'InVitro':'', 
					'FamilyHistory':''}
		
		# Retrieve db entries
		for key in self.entries:
			try:
				self.cursor.execute('''SELECT %s FROM Eclampsia WHERE PID=?''' % key, (self.pid,))
				query = self.cursor.fetchall()
				if query:
					self.entries[key] = query[0][0]
			except sqlite3.OperationalError:
				tkMessageBox.showwarning(
					title='Database Retrieval Error',
					message='Unable to retrieve entry for %s from database: will omit from algorithm' % key,)
		
		util.close_db(self, self.conn, self.cursor)
	
	def get_riskscore(self):
		"""
		Compute risk score.
		"""
		self.__retrieve_records()
		self.risk_weights = list()
					
		# Age: risk is 1.5x for Age<20 | Age>40
		self.age_flag = 0
		if self.entries['Age'] != -1:
			if (self.entries['Age'] < 20) | (self.entries['Age'] > 40):
				self.risk_weights.append(1.5)
				self.age_flag = 1
			else:
				self.risk_weights.append(1.0)
			
		# BMI: risk is 2x for BMI>35
		self.bmi_flag = 0
		if (self.entries['Height'] != -1) & (self.entries['Weight'] != -1):
			self.bmi = self.entries['Weight']/(self.entries['Height']*self.entries['Height'])
			if self.bmi > 35:
				self.risk_weights.append(2.0)
				self.bmi_flag = 1
			else:
				self.risk_weights.append(1.0)
			
		# Race: risk is 2x for Black
		self.race_flag = 0
		if self.entries['Race']:
			if 'Black' in self.entries['Race']:
				self.risk_weights.append(2.0)
				self.race_flag = 1
			else:
				self.risk_weights.append(1.0)
				
		# Bloodpressure:
		self.bloodpressure_flag = 0
		if (self.entries['BloodPressure_Sys'] != -1) & (self.entries['BloodPressure_Dis'] != -1):
			if (self.entries['BloodPressure_Sys'] > 140) & (self.entries['BloodPressure_Dis'] > 90):
				self.bloodpressure_flag = 1
				
		# Conditions: 
		self.current_autoimmunedisorders_flag = 0;	self.previous_autoimmunedisorders_flag = 0
		self.current_diabetes_flag = 0;				self.previous_diabetes_flag = 0
		self.current_corticalblindess_flag = 0;		self.previous_corticalblindess_flag = 0
		self.current_convulsions_flag = 0;			self.previous_convulsions_flag = 0
		self.current_edema_flag = 0;				self.previous_edema_flag = 0
		self.current_headachesmigranes_flag = 0;	self.previous_headachesmigranes_flag = 0
		self.current_hypertension_flag = 0;			self.previous_hypertension_flag = 0
		self.current_hypomagnesia_flag = 0;			self.previous_hypomagnesia_flag = 0
		self.current_kidneydisease_flag = 0;		self.previous_kidneydisease_flag = 0
		self.current_malnutrition_flag = 0;			self.previous_malnutrition_flag = 0
		self.current_proteinura_flag = 0;			self.previous_proteinura_flag = 0
		
		self.currentconditions_flag = 0
		if self.entries['CurrentConditions']:
			if 'Autoimmune Disorders' in self.entries['CurrentConditions']:
				self.current_autoimmunedisorders_flag = 1
			if 'Diabetes' in self.entries['CurrentConditions']:
				self.current_diabetes_flag = 1
			if 'Cortical Blindness' in self.entries['CurrentConditions']:
				self.current_corticalblindess_flag = 1
			if 'Convulsions' in self.entries['CurrentConditions']:	
				self.current_convulsions_flag = 1
			if 'Edema' in self.entries['CurrentConditions']:
				self.current_edema_flag = 1
			if 'Headaches/Migranes' in self.entries['CurrentConditions']:	
				self.current_headachesmigranes_flag = 1
			if 'Hypertension' in self.entries['CurrentConditions']:	
				current_hypertension_flag = 1
			if 'Hypomagnesia' in self.entries['CurrentConditions']:	
				self.current_hypomagnesia_flag = 1
			if 'Kidney Disease' in self.entries['CurrentConditions']:	
				self.current_kidneydisease_flag = 1
			if 'Malnutrition' in self.entries['CurrentConditions']:	
				self.current_malnutrition_flag = 1
			if 'Proteinura' in self.entries['CurrentConditions']:	
				self.current_proteinura_flag = 1
			self.currentconditions_flag = 1
		self.previousconditions_flag = 0
		if self.entries['PreviousConditions']:
			if 'Autoimmune Disorders' in self.entries['PreviousConditions']:
				self.previous_autoimmunedisorders_flag = 1
			if 'Diabetes' in self.entries['PreviousConditions']:
				self.previous_diabetes_flag = 1
			if 'Cortical Blindness' in self.entries['PreviousConditions']:
				self.previous_corticalblindess_flag = 1
			if 'Convulsions' in self.entries['PreviousConditions']:	
				self.previous_convulsions_flag = 1
			if 'Edema' in self.entries['PreviousConditions']:
				self.previous_edema_flag = 1
			if 'Headaches/Migranes' in self.entries['PreviousConditions']:	
				self.previous_headachesmigranes_flag = 1
			if 'Hypertension' in self.entries['PreviousConditions']:	
				self.previous_hypertension_flag = 1
			if 'Hypomagnesia' in self.entries['PreviousConditions']:	
				self.previous_hypomagnesia_flag = 1
			if 'Kidney Disease' in self.entries['PreviousConditions']:	
				self.previous_kidneydisease_flag = 1
			if 'Malnutrition' in self.entries['PreviousConditions']:	
				self.previous_malnutrition_flag = 1
			if 'Proteinura' in self.entries['PreviousConditions']:	
				self.previous_proteinura_flag = 1
			self.previousconditions_flag = 1
				
		# Conditions: Autoimmune Disorders; risk is 5x for autoimmune disorders (verify)
		if self.current_autoimmunedisorders_flag | self.previous_autoimmunedisorders_flag:
			self.risk_weights.append(5.0)
		
		# Conditions: Diabetes; risk is 2x for diabetes (verify)
		if self.current_diabetes_flag | self.previous_diabetes_flag:
			self.risk_weights.append(2.0)
			
		# Conditions: Hypomagnesia; risk is 2x for hypomagnesia (verify)
		if self.current_hypomagnesia_flag | self.previous_hypomagnesia_flag:
			self.risk_weights.append(2.0)
			
		# Conditions: Kidney; risk is 2x for kidney (verify)
		if self.current_kidneydisease_flag | self.previous_kidneydisease_flag:
			self.risk_weights.append(2.0)
			
		# Conditions: Malnutrition; risk is 2x for malnutrition (verify)
		if self.current_malnutrition_flag | self.previous_malnutrition_flag:
			self.risk_weights.append(2.0)
			
		# Cholesterol: risk is 2x for high cholesterol (verify)
		self.cholesterol_flag = 0
		if self.entries['Cholesterol']:
			if self.entries['Cholesterol'] == '>300':
				self.risk_weights.append(2.0)
				self.cholesterol_flag = 1
			else:
				self.risk_weights.append(1.0)
		
		# Triglycerides: risk is 2x for high triglycerides (verify)
		self.triglycerides_flag = 0
		if self.entries['Triglycerides']:
			if self.entries['Triglycerides'] == '>200':
				self.risk_weights.append(2.0)
				self.triglycerides_flag = 1
			else:
				self.risk_weights.append(1.0)
		
		# PregnancyHistory: risk is 2x for 1st pregnancy
		self.pregnancyhistory_flag = 0
		if self.entries['PregnancyHistory']:
			if self.entries['PregnancyHistory'] == '1st':
				self.risk_weights.append(2.0)
				self.pregnancyhistory_flag = 1
			else:
				self.risk_weights.append(1.0)
		
		# ChildrenExpected: risk is 2.5x for multiple gestation
		self.childrenexpcted_flag = 0
		if self.entries['ChildrenExpected']:
			if self.entries['ChildrenExpected'] == '>1':
				self.risk_weights.append(2.5)
				self.childrenexpected_flag = 1 
			else:
				self.risk_weights.append(1.0)
		
		# Trimester: risk is 80%x for 3rd trimester
		self.trimester_flag = 0
		if self.entries['Trimester']:
			if self.entries['Trimester'] == '3rd':
				self.risk_weights.append(1.8)
				self.trimester_flag = 1 
			else:
				self.risk_weights.append(1.0) 
		
		# PregnancyInterval: risk is 2x for interval >10 yrs
		self.pregnancyinterval_flag = 0
		if self.entries['PregnancyInterval']:
			if self.entries['PregnancyInterval'] == '>10 yrs':
				self.risk_weights.append(2.0)
				self.pregnancyinterval_flag = 1
			else:
				self.risk_weights.append(1.0)
			
		# PaternityChange: risk is 30% greater for change in paternity
		self.paternitychange_flag = 0
		if self.entries['PaternityChange']:
			if self.entries['PaternityChange'] == 'Yes':
				self.risk_weights.append(1.3)
				self.paternitychange_flag = 1
			else:
				self.risk_weights.append(1.0)
				
		# InVitro: risk is 40% greater for invitro fertilization
		self.invitro_flag = 0
		if self.entries['InVitro']:
			if self.entries['InVitro'] == 'Yes':
				self.risk_weights.append(1.4)
				self.invitro_flag = 1
			else:
				self.risk_weights.append(1.0)
		
		# FamilyHistory: risk is 7x for self; 40%x for parent; 20%x for sibling
		# Assign self risk if: 
		#	self entry or combo (edema, hypertension, proteinura) or combo (convulsions, cortical blindness, headaches/migranes)
		self.selffamilyhistory_flag = 0; self.parentfamilyhistory_flag = 0; self.siblingfamilyhistory_flag = 0
		if self.entries['FamilyHistory']:
			if (('Self' in self.entries['FamilyHistory']) | 
				(self.previous_edema_flag & self.previous_hypertension_flag & self.previous_proteinura_flag) | 
				(self.previous_convulsions_flag & self.previous_corticalblindess_flag & self.previous_headachesmigranes_flag)):
				self.risk_weights.append(7.0)
				self.selffamilyhistory_flag = 1
			if 'Parent' in self.entries['FamilyHistory']:
				self.risk_weights.append(1.4)
				self.parentfamilyhistory_flag = 1
			if 'Sibling' in self.entries['FamilyHistory']:
				self.risk_weights.append(1.2)
				self.siblingfamilyhistory_flag = 1
				
		self.risk_score = self.calc_arithmetic_mean(self.risk_weights)
	
	def calc_arithmetic_mean(self, risk_weights):
		"""
		Compute arithmetic mean.
		"""
		__risk_score = float(sum(risk_weights))/len(risk_weights) if len(risk_weights) > 0 else 0
		return __risk_score
		
	def get_riskprofile(self):
		"""
		Assign risk profile.
		"""
		self.get_riskscore()
		if self.risk_score < 1.5:
			self.risk_profile = 'LOW'
		elif (self.risk_score > 1.5) & (self.risk_score < 2.5):
			self.risk_profile = 'MODERATE'
		else:
			self.risk_profile = 'HIGH'
					
	def display_all(self):
		"""
		Display risk profile/recommendations.
		"""
		self.get_riskprofile()
		
		# Risks
		self.textbox.insert('2.0', 'RISK PROFILE \n', 'underline')
		self.textbox.insert(tk.END, '\n')
		self.textbox.insert(tk.END, 'Risk for %s %s %s is %s: \n' 
		% (self.entries['FirstName'], self.entries['MiddleInitial'], self.entries['LastName'], self.risk_profile))
		self.textbox.insert(tk.END, '\n')
		if self.age_flag:
			self.textbox.insert(tk.END, ' - Age is %d: risk is 1.5x for age <20 or >40 \n' % self.entries['Age'])
		if self.bmi_flag:
			self.textbox.insert(tk.END, ' - BMI is %d: risk is 2x for BMI >35 \n' % self.bmi)
		if self.race_flag:
			self.textbox.insert(tk.END, ' - Race includes Black: risk is 2x for African descent \n')
		if self.previousconditions_flag:
			self.textbox.insert(tk.END, ' - Self history of %s \n' % self.entries['PreviousConditions'].strip(', '))
		if self.cholesterol_flag:
			self.textbox.insert(tk.END, ' - Cholesterol is %s mg/dL: risk is 2x \n' 
			% self.entries['Cholesterol'])
		if self.triglycerides_flag:
			self.textbox.insert(tk.END, ' - Triglycerides are %s mg/dL: risk is 2x \n' 
			% self.entries['Triglycerides'])
		if self.pregnancyhistory_flag:
			self.textbox.insert(tk.END, ' - 1st pregnancy: risk is 2x for 1st issue \n')
		if self.childrenexpcted_flag:
			self.textbox.insert(tk.END, ' - Expecting multiple children: risk is 2.5x for multiple gestation \n')
		if self.trimester_flag:
			self.textbox.insert(tk.END, ' - 3rd Trimester: risk is 80% greater in 3rd trimester \n')
		if self.pregnancyinterval_flag:
			self.textbox.insert(tk.END, ' - Pregnancy interval >10 yrs: risk is 2x \n')
		if self.paternitychange_flag:
			self.textbox.insert(tk.END, ' - Paternity change since last issue: risk is 30% greater \n')
		if self.invitro_flag:
			self.textbox.insert(tk.END, ' - IVF: risk is 40% greater \n')
		if self.selffamilyhistory_flag:
			self.textbox.insert(tk.END, ' - Self history of pre-clampsia/eclampsia: risk is 7x \n')
		if self.parentfamilyhistory_flag:
			self.textbox.insert(tk.END, ' - Parent history of pre-eclampsia/eclampsia: risk is 40% greater \n')
		if self.siblingfamilyhistory_flag:
			self.textbox.insert(tk.END, ' - Sibling history of pre-eclampsia/eclampsia: risk is 20% greater \n')
		
		# Recommendations
		# Short-term
		self.textbox.insert(tk.END, '\n')
		self.textbox.insert(tk.END, 'RECOMMENDATIONS \n', 'underline')
		self.textbox.insert(tk.END, '\n')
		if self.bloodpressure_flag:
			self.textbox.insert(tk.END, ' - High Blood Pressure (%s/%s mmHg), recommend medical attention \n'
			% (self.bloodpressure_sys, self.bloodpressure_dis))
		if self.current_edema_flag & self.current_hypertension_flag & self.current_proteinura_flag:
			self.textbox.insert(tk.END, ' - Pre-eclampsia symptoms: recommend immediate medical attention \n')
		if self.current_convulsions_flag & self.current_corticalblindess_flag:
			self.textbox.insert(tk.END, ' - Eclampsia symptoms: recommend immediate medical attention')
		# Long-term
		if self.bmi_flag:
			self.textbox.insert(tk.END, ' - High BMI: recommend lifestyle change \n')
		if self.cholesterol_flag:
			self.textbox.insert(tk.END, ' - High Cholesterol: recommend lifestyle change \n')
		if self.triglycerides_flag:
			self.textbox.insert(tk.END, ' - High Triglycerides: recommend lifestyle change \n')
			
		self.textbox.config(state=tk.DISABLED)
							
if __name__ == "__main__":
	RecommendationsPage(self.pid, self.link, self.root)
		
