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
from glob import glob
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
	months = None

	def __init__(self, code, util):
		self.code = code
		self.utility = util

		jan = { 'name' : 'jan', 'pre' : None, 'post' : None }
		feb = { 'name' : 'feb', 'pre' : None, 'post' : None }
		mar = { 'name' : 'mar', 'pre' : None, 'post' : None }
		apr = { 'name' : 'apr', 'pre' : None, 'post' : None }
		may = { 'name' : 'may', 'pre' : None, 'post' : None }
		jun = { 'name' : 'jun', 'pre' : None, 'post' : None }
		jul = { 'name' : 'jul', 'pre' : None, 'post' : None }
		aug = { 'name' : 'aug', 'pre' : None, 'post' : None }
		sep = { 'name' : 'sep', 'pre' : None, 'post' : None }
		oct = { 'name' : 'oct', 'pre' : None, 'post' : None }
		nov = { 'name' : 'nov', 'pre' : None, 'post' : None }
		dec = { 'name' : 'dec', 'pre' : None, 'post' : None }
		self.months = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]


#building a JSON string from the two letter building code
def build(building, code, util):

	months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

	
	BuildingNames = {
                       "OM": "OLD MAIN" ,
                       "BH": "BOND HALL",
                       "AI": "ACADEMIC INSTRUCTION CTR",
                       "CF": "COMMUNICATIONS",
                       "BI": "BIOLOGY BUILDING",
                       "AH": "ARNTZEN",
                       "MH": "MILLER HALL"
			}

	#get book and worksheet for util
	if (util == 'elec'):
		#attempt to handle file name changes (go glob!)
		bookname = glob('Energy*')[0]	
		book = xlrd.open_workbook(bookname)
		sheet = book.sheet_by_name('BldgEnergyCost')
		building.unit = 'kWh'	

	if (util == 'steam'):
		#attempt to handle file name changes
		bookname = glob('Gas*')[0]
		book = xlrd.open_workbook(bookname)
		sheet = book.sheet_by_name('PoundsSteamPerBldg')
		building.unit = 'lbs'	





	#TODO find place to get year!!!! maybe URL?
	preyear = 2013
	curyear = 2014

	building.currYear = curyear
	building.prevYear = preyear

	building_row = None	

	try:

			#TODO add function find building column?

			#gets building row
			building.name = BuildingNames[code]
			building_row = findBuildingRow(sheet, building.name)

			#print("processing sheet\n")
			for i in range(0, 12):

				#gets month col for preyear
				mColumn = findMonthColumn(sheet, months[i], book.datemode, preyear)
				#set month data in utilpre of data to measurement
				building.months[i]['pre'] = getMeasurement(sheet, mColumn, building_row)

				#gets month col for curyear
				mColumn = findMonthColumn(sheet, months[i], book.datemode, curyear)
				#set month data in utilcur of data to measurement
				building.months[i]['post'] = getMeasurement(sheet, mColumn, building_row)


			building.name = getBuildingName(sheet[sh], building_row)

	except Exception as e:
		pass



#finds the building row
def findBuildingRow(sheet, code):
	#iterate down the building Column
	building_row = 1
	num_rows = sheet.nrows - 1
	while building_row < num_rows:
		building_row += 1
		#building col is located at column 2(C in excel)
		building_value = sheet.cell_value(building_row, 2)
		if (str(building_value).startswith(code)):
			return building_row

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

#gets the building name on a sheet given an specific row
def getBuildingName(sheet, building_row):
	name = str(sheet.cell_value(building_row, 0))
	name = name.strip()
	return name

#main 
cgitb.enable()
print("Content-Type: application/json")
print("")
form = cgi.FieldStorage()
code = form.getvalue("code")
util = form.getvalue("util")

#code = "OM" #test value
#util = 'elec' #test value

building = BuildingUtilData(code, util)
build(building, code, util)

print(json.dumps(building.__dict__, indent = 4))
