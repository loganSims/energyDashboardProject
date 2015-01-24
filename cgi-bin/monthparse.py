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
			'type': self.utility,
			'unit': self.unit,
			'Jan': None,
			'Feb': None,
			'Mar': None,
			'Apr': None,
			'May': None,
			'Jun': None,
			'Jul': None,
			'Aug': None,
			'Sep': None,
			'Oct': None,
			'Nov': None,
			'Dec': None
		}
		utilcurr = {
			'type': self.utility,
			'unit': self.unit,
			'Jan': None,
			'Feb': None,
			'Mar': None,
			'Apr': None,
			'May': None,
			'Jun': None,
			'Jul': None,
			'Aug': None,
			'Sep': None,
			'Oct': None,
			'Nov': None,
			'Dec': None
		}

		self.data = [utilpre, utilcurr]


#building a JSON string from the two letter building code
def build(building, book, code, util):

	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Oct", "Nov", "Dec"]
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

			mColumn = findUtilityColumn(sheet[sh], header_row)
          
         #last years sheet
			if sh == 0:
				#TODO GET MONTH NOT YEAR
				for month in months:
		      

					
					
					prevM = getMeasurement(1, sheet, mColumn, building_row)
					utility = building.utilities[utilCount]
					utility['prevMeasurement'] = prevM


		   #current years sheet
			else:

				#TODO GET MONTH NOT YEAR
				currM = getMeasurement(0, sheet, mColumn, building_row)
				utility = building.utilities[utilCount]
				utility['currMeasurement'] = currM

			building.name = getBuildingName(sheets[sh], building_row)

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

#finds the utility column
def findUtilityColumn(sheet, header_row):
	mCol = -1
	num_cells = sheet.ncols - 1
	while mCol < num_cells:
		mCol += 1
		value = sheet.cell_value(header_row, mCol)
		if (str(value).startswith('GraphYTD')):
			return mCol

#gets a utility measurement
def getMeasurement(year, sheets, mColumn, building_row):
	measurement = sheets[year].cell_value(building_row, mColumn)
	return int(measurement)

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
code = "OM" #test value
util = "elec" #test value
building = BuildingUtilData(code, util)
book = xlrd.open_workbook('file.xlsx')
build(building, book, code, util)

print(json.dumps(building.__dict__, indent = 4))
