#!/usr/bin/python
##########################
# Base Code: Allen Suner #
# Date: 05/26/2014       #
########################################################
# Edits: Logan Sims                                    #
# 2015                                                 #
#                                                      #
# This script collects usage data for a given building.#
# It compiles data for two years as a total and        #
# on a month to month basis. It also collects          #
# the data for the pie chart on each dashboard         #
#                                                      #
########################################################

#imports
import cgi, cgitb
from glob import glob
import xlrd
import json
from datetime import date
import calendar


#import our own scripts
from speadsheetAccessFunctions import findMonthColumn, findBuildingUseRow, getMeasurement
from buildings import BuildingNames

#python object that will be translated into a JSON string
class BuildingUtilData:

	#JSON fields
	name = ""
	code = ""
	utility = None
	unit = None
	months = None
	pretotal = 0.0
	posttotal = 0.0
	#holds grand total usage for all tracked buildings besides selected
	#used to compare with selected building
	preGrandTotal = 0.00
	postGrandTotal = 0.00
	
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
def build(building, code, util, year):

	months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

	#get book and worksheet for util
	if (util == 'electric'):
		#attempt to handle file name changes (go glob!)
		bookname = glob('Energy*')[0]	
		book = xlrd.open_workbook(bookname)
		sheet = book.sheet_by_name('BldgEnergyCost')
		building.unit = 'kWh'	

	if (util == 'steam'):
		#attempt to handle file name changes
		bookname = glob('Gas*')[0]
		book = xlrd.open_workbook(bookname)
		sheet = book.sheet_by_name('SteamEnergyPerBldg')
		building.unit = 'Mbtu'	


	preyear = year - 1
	curyear = year

	building.currYear = curyear
	building.prevYear = preyear

	building_row = None	


	#TODO add function find building column?

	#gets building row
	building.name = BuildingNames[code]

	building_row = findBuildingUseRow(sheet, building.name)

	for i in range(0, 12):

		#gets month col for preyear
		mColumn = findMonthColumn(sheet, months[i], book.datemode, preyear)
		#set month data in utilpre of data to measurement
		building.months[i]['pre'] = getMeasurement(sheet, mColumn, building_row)
		#gets month col for curyear
		mColumn = findMonthColumn(sheet, months[i], book.datemode, curyear)
		#set month data in utilcur of data to measurement
		building.months[i]['post'] = getMeasurement(sheet, mColumn, building_row)

		if ((building.months[i]['post'] != 0) and (building.months[i]['pre'] != 0)):
			building.pretotal = building.pretotal + building.months[i]['pre']	
			building.posttotal = building.posttotal + building.months[i]['post']


	#collect grand total from other buildings (DOES NOT INCLUDE SELECTED BUILDING)
	for key in BuildingNames:
		if (key != code):
			row = findBuildingUseRow(sheet, BuildingNames[key])
			for i in range(0, 12):
				mColumn = findMonthColumn(sheet, months[i], book.datemode, preyear)
				building.preGrandTotal = building.preGrandTotal + getMeasurement(sheet, mColumn, row)
				mColumn = findMonthColumn(sheet, months[i], book.datemode, curyear)
				building.postGrandTotal = building.postGrandTotal + getMeasurement(sheet, mColumn, row)


#main 
cgitb.enable()
print "Content-Type: application/json"
print
form = cgi.FieldStorage()
code = form.getvalue("code")
util = form.getvalue("util")
year = int(form.getvalue("year"))
#DEBUG VALUES
#code = "aOM" #test value
#util = 'steam' #test value
#year = 2013 #test value

building = BuildingUtilData(code, util)
build(building, code, util, year)

print json.dumps(building.__dict__, indent = 4)
