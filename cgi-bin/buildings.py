#These are the buildings currently being tracked. 
#When new building is added it must be added here
#for the parsers to get the information from the
#spread sheets

#NOTE: each building code starts with either
#'r', 'a', or 's'. this represents which
#type of building it is.
# r = res hall
# a = academic
# s = student building
#this is important for the summaryData.py parser

BuildingNames = {
	#res halls
	"rBT":"BUCHANAN TOWERS - ORIGINAL",
	"rEN":"EDENS HALL NORTH",
	"rEH":"EDENS HALL",
	"rFT":"FAIRHAVEN TOWERS",
	"rHL":"HIGHLAND I & II",
	"rHI":"HIGGINSON",
	"rMA":"MATHES",
	"rNA":"NASH",
	"rRA":"RDG ALPHA",
	"rRB":"RDG BETA",
	"rRD":"RDG DELTA",
	"rRG":"RDG GAMMA",
	"rRK":"RDG KAPPA",
	"rRO":"RDG OMEGA",
	"rRS":"RDG SIGMA",

	#academic buildings
	"aAI":"ACADEMIC INSTRUCTION CENTER",
	"aAH":"ARNTZEN HALL",
	"aBI":"BIOLOGY",
	"aBH":"BOND HALL",
	"aCS":"CAMPUS SERVICES",
	"aCF":"COMMUNICATIONS FACILITY",
	"aCB":"CHEMISTRY",
	"aCH":"COLLEGE HALL",
	"aCO":"COMMISSARY",
	"aET":"ENGINEERING TECHNOLOGY",
	"aES":"ENVIRONMENTAL STUDIES", 
	"aFH":"FAIRHAVEN ACADEMIC",
	"aFI":"FINE ARTS",
	"aFR":"FRASER HALL",
	"aHA":"HAGGARD HALL",
	"aHU":"HUMANITIES",
	"aMH":"MILLER HALL",
	"aOM":"OLD MAIN",
	"aPH":"PARKS HALL",
	"aPA":"PERFORMING ARTS",
	"aSM":"SMATE",
	"aWL":"WILSON LIBRARY",

	#student buildings
	"sAF":"ARNTZEN FOOD FACILITY",
	"sBS":"BOOKSTORE",
	"sCG":"CARVER GYMNASIUM",
	"sFC":"FAIRHAVEN COMMONS",
   "sRC":"RIDGEWAY COMMONS",
	"sSR":"STUDENT RECREATION",
	"sVC":"VIKING COMMONS",
	#"sMC":"MILLER HALL COFFEE SHOP", TODO no steam data
	"sVU":"VIKING UNION"

	}
