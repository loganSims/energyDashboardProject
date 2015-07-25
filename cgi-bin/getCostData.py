#!/usr/bin/python
##########################
# Base Code: Allen Suner #
# Date: 05/26/2014       #
#############################
# Edits: Logan Sims         #
# 2015                      #
#                           #
# refer to getUsageData.py, #
# acts the same but gets    #
# cost data                 #
#                           # 
#############################

#imports
import cgi, cgitb
from glob import glob
import xlrd
import json
from datetime import date
import calendar

#import our own scripts
from speadsheetAccessFunctions import findMonthColumn, findBuildingCostRow, getMeasurement
from buildings import BuildingNames

#python object that will be translated into a JSON string
class BuildingUtilCostData:

	#JSON fields
	name = ""
	code = ""
	utility = None
	months = None
	pretotal = 0
	posttotal = 0

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

	if (util == 'steam'):
		#attempt to handle file name changes
		bookname = glob('Gas*')[0]
		book = xlrd.open_workbook(bookname)
		sheet = book.sheet_by_name('SteamEnergyPerBldg')


	building.unit = 'Dollars'	
	
	preyear = year - 1
	curyear = year

	building.currYear = curyear
	building.prevYear = preyear

	building_row = None	


	#TODO figure out why this breaks when we remove this try block...
	try:

		#TODO add function find building column?

		#gets building row
		building.name = BuildingNames[code]
		building_row = findBuildingCostRow(sheet, building.name)

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

			if ((building.months[i]['post'] != 0) and (building.months[i]['pre'] != 0)):
				building.pretotal = building.pretotal + building.months[i]['pre']	
				building.posttotal = building.posttotal + building.months[i]['post']

	except Exception as e:
		pass




#main 
cgitb.enable()
print "Content-Type: application/json"
print
form = cgi.FieldStorage()
code = form.getvalue("code")
util = form.getvalue("util")
year = int(form.getvalue("year"))

#code = "OM" #test value
#util = 'elec' #test value
#year = 2014 #test value

building = BuildingUtilCostData(code, util)
build(building, code, util, year)

print json.dumps(building.__dict__, indent = 4)
