#!/usr/bin/python3
#######################
# Author: Allen Suner #
# Date: 05/26/2014    #
#######################

#imports
import cgi, cgitb
import xlrd
import json
from datetime import date
import calendar

#print "Content-Type: application/json"


#python object that will be
#translated into a JSON string
class Building:

	#JSON fields
	name = ""
	code = ""
	currYear = 0
	prevYear = 0
	utilities = None
	currCo2 = 0
	prevCo2 = 0
	co2unit = "" #TODO - ASK GREG Co2 units

	def __init__(self, code):
		self.code = code

		electric = {
			'type': "electric",
			'unit': "kWh",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		steam = {
			'type': "steam",
			'unit': "thm",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		water = {
			'type': "water",
			'unit': "CCF",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		refuse = {
			'type': "refuse",
			'unit': "yds",
			'prevMeasurement': None,
			'currMeasurement': None
		}

		self.co2unit = "lbs"
		self.utilities = [electric, steam, water, refuse]


#building a JSON string from the
#two letter building code
def build(building, book, code):

	#worksheets
	currElectric = book.sheet_by_name('FY2014 GEFdash Elec kWh')
	prevElectric = book.sheet_by_name('FY2013 GEFdash Elec kWh')
	sheet_electric = {
		0: currElectric,
		1: prevElectric
	}

	currSteam = book.sheet_by_name('FY2014 GEFdash Steam THERMS')
	prevSteam = book.sheet_by_name('FY2013 GEFdash Steam THERMS')
	sheet_steam = {
	 	0: currSteam, 
	 	1: prevSteam
	 }

	currWater = book.sheet_by_name('FY2014 GEFdash Water CCF')
	prevWater = book.sheet_by_name('FY2013 GEFdash Water CCF')
	sheet_water = {
		0: currWater, 
		1: prevWater
	}

	currRefuse = book.sheet_by_name('FY2014 GEFdash Refuse Yds')
	prevRefuse = book.sheet_by_name('FY2013 GEFdash Refuse Yds')
	sheet_refuse = {
		0: currRefuse, 
		1: prevRefuse
	}

	building.currYear = date.today().year
	building.prevYear = building.currYear - 1

	#TODO add sheet_refuse once we figure out how to parse it!
	util_sheets = [sheet_electric, sheet_steam, sheet_water]

	utilCount = -1

	for util in util_sheets:

		utilCount += 1
		sheets = util
		building_row = None
		try:
			for sh in sheets:
				#find the header
				header_row, building_col = findHeaderRow(sheets[sh], code)
				building_row = findBuildingRow(sheets[sh], code, header_row, building_col)

				mColumn = findUtilityColumn(sheets[sh], header_row)
				cColumn = findCo2Column(sheets[sh], header_row)

				if sh == 0:
					prevM = getMeasurement(1, sheets, mColumn, building_row)
					utility = building.utilities[utilCount]
					utility['prevMeasurement'] = prevM
					if (utilCount == 0):
						data = getCo2Data(1, sheets, cColumn, building_row)
						building.prevCo2 = data
				else:
					currM = getMeasurement(0, sheets, mColumn, building_row)
					utility = building.utilities[utilCount]
					utility['currMeasurement'] = currM
					if (utilCount == 0):
						data = getCo2Data(0, sheets, cColumn, building_row)
						building.currCo2 = data

				building.name = getBuildingName(sheets[sh], building_row)

		except Exception as e:
			pass

#	if (building_row == None):
#		raise Exception("Building with code: " + str(code) + " does not exist in worksheets.")

#finds the header row
def findHeaderRow(sheet, code):
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

#finds the Co2 column
def findCo2Column(sheet, header_row):
	cCol = -1
	num_cells = sheet.ncols -1
	while cCol < num_cells:
		cCol += 1
		value = sheet.cell_value(header_row, cCol)
		value = ' '.join(str(value).split())
		if (str(value) == 'YTD CO2 SUM'):
			return cCol

#gets a utility measurement
def getMeasurement(year, sheets, mColumn, building_row):
	measurement = sheets[year].cell_value(building_row, mColumn)
	return int(measurement)

#gets a Co2 measurment
def getCo2Data(year, sheets, cColumn, building_row):
	measurement = sheets[year].cell_value(building_row, cColumn)
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
building = Building(code)
book = xlrd.open_workbook('file.xlsx')
build(building, book, code)
	#JSONString = json.dumps(building.__dict__, indent = 4)
	#return JSONString
print(json.dumps(building.__dict__, indent = 4))
