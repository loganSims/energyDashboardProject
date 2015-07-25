#!/usr/bin/python

######################
# Author: Logan Sims #
# 2015               #
######################

#imports
import cgi, cgitb
import json
from xml.dom import minidom


#python object that will be translated into a JSON string
class Desc:

	#JSON fields
	buildingInfo = ""
	utilInfo = ""

def buildDesc(desc, code, util):

	xmldoc = minidom.parse('infoText.xml')
	buildText = xmldoc.getElementsByTagName(code)
	utilText = xmldoc.getElementsByTagName(util)

	desc.buildingInfo = buildText[0].childNodes[0].nodeValue
	desc.utilInfo = utilText[0].childNodes[0].nodeValue


#main 
cgitb.enable()
print "Content-Type: application/json"
print
form = cgi.FieldStorage()
code = form.getvalue("code")
util = form.getvalue("util")
#DEBUG VALUES
#code = "OM" #test value
#util = 'steam' #test value

desc = Desc()
buildDesc(desc, code, util)

print json.dumps(desc.__dict__, indent = 4)
