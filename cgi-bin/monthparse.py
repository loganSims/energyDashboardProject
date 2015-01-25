#!/usr/bin/python3
##########################
# Base Code: Allen Suner #
# Date: 05/26/2014       #
##########################
# Edits: Logan Sims  #
# 2015               #
######################

#imports
import cgi, cgitb
import xlrd
import json
from datetime import date
import calendar

#python object that will be translated into a JSON string
class BuildingUtilData:

	#JSON fields
	name = ""
	code = ""
	utility = None
	unit = None
	data = None

	def __init__(self, code, util):
		self.code = code
		self.utility = util
		utilpre = {
			1 : None,
			2 : None,
			3 : None,
			4 : None,
			5 : None,
			6 : None,
			7 : None,
			8 : None,
			9 : None,
			10 : None,
			11 : None,
			12 : None
		}
		utilcurr = {
			1 : None,
			2 : None,
			3 : None,
			4 : None,
			5 : None,
			6 : None,
			7 : None,
			8 : None,
			9 : None,
			10 : None,
			11 : None,
			12 : None
		}

		self.data = [utilpre, utilcurr]


#building a JSON string from the two letter building code
def build(building, book, code, util):

	#two different sets of month for diff excel sheets	
	monthsStrs = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	
	#worksheets
	if (util == 'elec'):
		currElectric = book.sheet_by_name('FY2014 GEFdash Elec kWh')
		prevElectric = book.sheet_by_name('FY2013 GEFdash Elec kWh')
		sheet = {
			0: currElectric,
			1: prevElectric
		}
	elif (util == 'steam'):
		currSteam = book.sheet_by_name('FY2014 GEFdash Steam THERMS')
		prevSteam = book.sheet_by_name('FY2013 GEFdash Steam THERMS')
		sheet = {
			0: currSteam, 
			1: prevSteam
		}
	elif (util == 'water'):
		currWater = book.sheet_by_name('FY2014 GEFdash Water CCF')
		prevWater = book.sheet_by_name('FY2013 GEFdash Water CCF')
		sheet = {
			0: currWater, 
			1: prevWater
		}
	elif (util == 'refu'):
		currRefuse = book.sheet_by_name('FY2014 GEFdash Refuse Yds')
		prevRefuse = book.sheet_by_name('FY2013 GEFdash Refuse Yds')
		sheet = {
			0: currRefuse, 
			1: prevRefuse
		}
	

   #TODO get year from sheet?
	building.currYear = date.today().year
	building.prevYear = building.currYear - 1

	building_row = None
	try:
		for sh in sheet:
			#find the header
			header_row, building_col = findHeaderCol(sheet[sh], code)
			building_row = findBuildingRow(sheet[sh], code, header_row, building_col)

         #last year's sheet
			if sh == 1:
				print("processing last years sheet\n")
				for i in range(0, 12):
					mColumn = findMonthColumn(sheet[sh], header_row, months[i], monthsStrs[i], book.datemode)
					#set month data in utilpre of data to measurement
					building.data[0][months[i]] = getMeasurement(sheet[sh], mColumn, building_row)
		   #current years sheet
			else:
				print("processing current years sheet\n")
				for i in range(0, 12):
					mColumn = findMonthColumn(sheet[sh], header_row, months[i], monthsStrs[i], book.datemode)
					#set utilcur of data at month months[i] to measurement
					building.data[1][months[i]] = getMeasurement(sheet[sh], mColumn, building_row)

			building.name = getBuildingName(sheet[sh], building_row)

	except Exception as e:
		pass


#finds the header row
def findHeaderCol(sheet, code):
	num_rows = sheet.nrows - 1
	num_cells = sheet.ncols - 1
	header_row = -1
	while header_row < num_rows:
		header_row += 1
		header_cell = -1
		while header_cell < num_cells:
			header_cell += 1
			value = sheet.cell_value(header_row, header_cell)
			value = ' '.join(str(value).split())
			if (value == 'BLDG ID' or value == 'Loc ID'):
				return header_row, header_cell

#finds the building row
def findBuildingRow(sheet, code, header_row, building_col):
	#iterate down the BLDG ID Column
	building_row = header_row
	num_rows = sheet.nrows - 1
	while building_row < num_rows:
		building_row += 1
		building_value = sheet.cell_value(building_row, building_col)
		if (building_value == code):
			return building_row

	raise Exception("Building with code: " + code + " does not have data in this file.")

#finds the month column
def findMonthColumn(sheet, header_row, monthNum, monthStr, datemode):
	mCol = -1
	num_cells = sheet.ncols - 1
	while mCol < num_cells:
		mCol += 1
		value = sheet.cell_value(header_row, mCol)

		#if sheet uses string dates
		if (value == monthStr):
			return mCol

		#if sheet uses excel number dates
		#look into xlrd.xldate_as_tuple for more info
		try:
			x = xlrd.xldate_as_tuple(value, datemode)
		except Exception as e:
			#filler value for x
			x = [-1, -1]
			pass

		if (x[1] == monthNum):
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

#gets the building name on a sheet given an specific row
def getBuildingName(sheet, building_row):
	name = str(sheet.cell_value(building_row, 0))
	name = name.strip()
	return name

#main 
#cgitb.enable()
print("Content-Type: application/json")
print("")
form = cgi.FieldStorage()
code = form.getvalue("code")
util = form.getvalue("util")
code = "OM" #test value
util = "water" #test value
building = BuildingUtilData(code, util)
book = xlrd.open_workbook('file.xlsx')
build(building, book, code, util)

print(json.dumps(building.__dict__, indent = 4))
