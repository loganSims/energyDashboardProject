#!/usr/bin/python3

#this script defines functions for collectiong data 
#from the spread sheets


import xlrd

#finds the building row
def findBuildingUseRow(sheet, code):
	#iterate down the building Column
	building_row = 1
	num_rows = sheet.nrows - 1
	while building_row < num_rows:
		building_row += 1
		#building col is located at column 2(C in excel)
		building_value = sheet.cell_value(building_row, 2)
		if (str(building_value).strip() == code.strip()):
			return building_row


#finds the building row
def findBuildingCostRow(sheet, code):
	#iterate down the building Column
	building_row = 1
	foundFirst = False;
	num_rows = sheet.nrows - 1
	while building_row < num_rows:
		building_row += 1
		#finds the second listing of building which has price data
		building_value = sheet.cell_value(building_row, 2)
		if (str(building_value).strip() == code.strip()):
			if(foundFirst):
				return building_row
			else:
				foundFirst = True;

	#TODO note: This is not hit if code isnt in file!!!
	raise Exception("Building with code: " + code + " does not have data in this file.")

#finds the month column
def findMonthColumn(sheet, monthNum, datemode, year):
	mCol = -1
	num_cells = sheet.ncols - 1
	while mCol < num_cells:
		mCol += 1
		value = sheet.cell_value(1, mCol)

		#sheet uses excel number dates
		#look into xlrd.xldate_as_tuple for more info
		#date[0] holds year, date[1] holds month
		try:
			date = xlrd.xldate_as_tuple(value, datemode)
		except Exception as e: 
			#thrown if sheet does not use excel dates
			#filler value for x
			date = [-1, -1]
			pass

		if (date[1] == monthNum and date[0] == year):
			return mCol

#gets a utility measurement
def getMeasurement(sheet, mColumn, building_row):

	#try block in case cell is empty
	try:
		measurement = sheet.cell_value(building_row, mColumn)
		return int(measurement)
	except Exception as e:
		pass
	
	return 0
