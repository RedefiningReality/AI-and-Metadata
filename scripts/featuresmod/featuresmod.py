from os import path
from csv import reader

class CSVReader:
	def __init__(self, filename="features.csv"):
		self.update_csv(filename)
	
	def update_csv(self, filename="features.csv"):
		if not path.exists(filename):
			open(filename, mode='x')
		self.filename = filename
		self.table = []
		with open(filename, mode='r') as csv_file:
			for row in reader(csv_file):
				if len(row) > 0:
					self.table.append(row)
	
	""" To be implemented
	def import_csv(self, filename="features.csv"):
		if not path.exists(filename):
			open(filename, mode='x')
		self.filename = filename
		temp = []
		with open(filename, mode='r') as csv_file:
			for row in reader(csv_file):
				if len(row) > 0:
					temp.append(row)
		self.__merge__(temp)
	
	def __merge__(self, temp):
		for feature in temp[0][1:]:
			if feature not in self.table:
	"""
	
	def features(self, image):
		for row in self.table:
			if row[0] == image:
				result = []
				for i in range(1, len(row)):
					if row[i] == "Yes":
						result.append(self.table[0][i])
				return result
		else:
			return []
	
	def images(self, feature):
		for j in range(1, len(self.table[0])):
			if self.table[0][j] == feature:
				result = []
				for i in range(1, len(self.table)):
					if self.table[i][j] == "Yes":
						result.append(self.table[i][0])
				return result
		else:
			return []