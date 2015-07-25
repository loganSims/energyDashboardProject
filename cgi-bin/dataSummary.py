#!/usr/bin/python
######################
# Author: Logan Sims #
# 2015               #
######################
#
#This parser gets the data for the
#Summary homepage. It collects electric and stea
#usage for the current year for each catagory of
#building on campus. The 3 are res halls, student buildings,
#and academic buildings. 
#
#IMPORTANT: it converts kwh to Mbtu

import cgi, cgitb
from glob import glob
import xlrd
import json
from datetime import date
import calendar

#import our own scripts
from speadsheetAccessFunctions import findMonthColumn, findBuildingUseRow, findBuildingCostRow, getMeasurement
from buildings import BuildingNames

#python object that will be translated into a JSON string
class SummaryData:

	ResElectricUse = 0
	ResSteamUse = 0
	ResElectricCost = 0
	ResSteamCost = 0

	StuElectricUse = 0
	StuSteamUse = 0
	StuElectricCost = 0
	StuSteamCost = 0

	AcaElectricUse = 0
	AcaSteamUse = 0
	AcaElectricCost = 0
	AcaSteamCost = 0

#building a JSON string from the two letter building code
def build(summary, year):

	#get spreadsheets
	#attempt to handle file name changes (go glob!)
	bookname = glob('Energy*')[0]	
	elecBook = xlrd.open_workbook(bookname)
	elecSheet = elecBook.sheet_by_name('BldgEnergyCost')
	
	#attempt to handle file name changes
	bookname = glob('Gas*')[0]
	steamBook = xlrd.open_workbook(bookname)
	steamSheet = steamBook.sheet_by_name('SteamEnergyPerBldg')

	for code in BuildingNames:

		#get use rows of building in both spread sheets
		steam_use_row = findBuildingUseRow(steamSheet, BuildingNames[code])
		elec_use_row = findBuildingUseRow(elecSheet, BuildingNames[code])

		#get cost rows of building in both spread sheets
		steam_cost_row = findBuildingCostRow(steamSheet, BuildingNames[code])
		elec_cost_row = findBuildingCostRow(elecSheet, BuildingNames[code])


		for i in range(1, 13):

			#gets month col for electric
			mColumnElec = findMonthColumn(elecSheet, i, elecBook.datemode, year)
			#gets month col for steam
			mColumnSteam = findMonthColumn(steamSheet, i, steamBook.datemode, year)

			if code.startswith('r'):		
				summary.ResElectricUse += getMeasurement(elecSheet, mColumnElec, elec_use_row)
				summary.ResSteamUse += getMeasurement(steamSheet, mColumnSteam, steam_use_row)

				summary.ResElectricCost += getMeasurement(elecSheet, mColumnElec, elec_cost_row)
				summary.ResSteamCost += getMeasurement(steamSheet, mColumnSteam, steam_cost_row)
	
			elif code.startswith('s'):		
				summary.StuElectricUse += getMeasurement(elecSheet, mColumnElec, elec_use_row)
				summary.StuSteamUse += getMeasurement(steamSheet, mColumnSteam, steam_use_row)

				summary.StuElectricCost += getMeasurement(elecSheet, mColumnElec, elec_cost_row)
				summary.StuSteamCost += getMeasurement(steamSheet, mColumnSteam, steam_cost_row)

			elif code.startswith('a'):
				summary.AcaElectricUse += getMeasurement(elecSheet, mColumnElec, elec_use_row)
				summary.AcaSteamUse += getMeasurement(steamSheet, mColumnSteam, steam_use_row)

				summary.AcaElectricCost += getMeasurement(elecSheet, mColumnElec, elec_cost_row)
				summary.AcaSteamCost += getMeasurement(steamSheet, mColumnSteam, steam_cost_row)


	#convert kwh to btu: 1 kwh = 3,413 btu
        # 1 kwh = 0.003413 million btus
	summary.ResElectricUse = summary.ResElectricUse * 0.003413
	summary.StuElectricUse = summary.StuElectricUse * 0.003413
	summary.AcaElectricUse = summary.AcaElectricUse * 0.003413



#main 
cgitb.enable()
print "Content-Type: application/json"
print
form = cgi.FieldStorage()
year = int(form.getvalue("year"))
#year = 2015
summary = SummaryData()
build(summary, year)

print json.dumps(summary.__dict__, indent = 4)
