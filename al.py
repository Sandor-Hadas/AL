import os
import sys
import json
import csv
import xmltodict # pip install xmltodict
import pprint


# Print a simple help
def help():
	print("Python example converter for AL\n")
	print("Usage:")
	print("al.py --in <input file name> --out <output name> --print <txt|html>")
	print("Valid file formats/extensions: .json, .csv, .xml (input/output), .html (only output)")
	print("One input file is required, one output and one print target is handled per run, latest if multiple are defined.")
	print("Printing is directed to stdout (python errors may appear on stderr)\n")


# Get file extensions for a file name
# Html is output format only
def getExt(filename, acceptHtml = 0):
	splitted = filename.split(".")
	if len(splitted) < 2:
		print("Could not find extension for file name: ", filename)
		return ""

	extension = splitted[len(splitted) - 1]
	if (extension.lower() == "json" or extension.lower() == "csv" or extension.lower() == "xml"):
		return extension
	if (extension.lower() == "html" and acceptHtml > 0):
		return extension

	print("Invalid extension for for file: " + filename)
	return ""


# Check file size for know output lengths
def checkFileSize(stringdata, filename):
	if os.stat(filename).st_size != len(stringdata):
		print("File write probably failed to file " + filename + " as dump text size and file size differs")
	else:
		print("File writing to " + filename + " looks to be OK")


# Load a json file from disk
def loadJson(filename):
	data = None

	print("Loading json file: " + filename)
	with open(filename) as json_file:
		data = json.load(json_file)

	return data


# Save json file to disk
def saveJson(data, filename):
	dump = json.dumps(data, indent=4)

	savefile = open(filename, "w")
	savefile.write(dump)
	savefile.close()

	checkFileSize(dump, filename)


# Load a csv file, comma separator is assumed
def loadCsv(filename):
	data = {}
	loadstring = ""

	with open(filename, mode='r') as csvfile:
		csvdata = csv.DictReader(csvfile)

		for rows in csvdata:
			if (len(loadstring) > 0):
				loadstring += ","
			else:
				loadstring = "{ 'people': ["
			loadstring += str(rows)

	loadstring += " ] }"
	loadstring = loadstring.replace("\'", "\"")

	data = json.loads(loadstring)

	return data


# Save csv with comma separator
def saveCsv(data, filename):
	filecsv = open(filename, "w")
	filecsv.write("name,street,city,region,zip,country,phone\n")
	for p in data['people']:
		filecsv.write("\"" + p['name'] + "\",")
		filecsv.write("\"" + p['street'] + "\",")
		filecsv.write("\"" + p['city'] + "\",")
		filecsv.write("\"" + p['region'] + "\",")
		filecsv.write("\"" + p['zip'] + "\",")
		filecsv.write("\"" + p['country'] + "\",")
		filecsv.write("\"" + p['phone'] + "\"\n")	
	print("Written " + str(filecsv.tell()) + " bytes to file " + filename + " during CSV export")
	filecsv.close

 
# Load xml file from disk
def loadXml(filename):
	with open(filename, 'r') as xmlFile:
		xmlContent = xmlFile.read()

	with open(filename, 'r') as fd:
		data = xmltodict.parse(fd.read())

	data = data['data']

	pp = pprint.PrettyPrinter(indent=4)
	loadthis = pp.pformat(json.dumps(data))

	return data


# Save xml file from memory
def saveXml(data, filename):
	savedata = {}
	savedata['data'] = data

	with open(filename, "w") as outfile:
		outfile.write(xmltodict.unparse(savedata))
		print("Written " + str(outfile.tell()) + " bytes to file " + filename + " during xml export")


# Print memory data to the screen
def printTxt(data):
	print("\nPrinting data to text format:")
	for p in data['people']:
		print('Name: ' + p['name'])
		print('Address:')
		print(' street: ' + p['street'])
		print(' city: ' + p['city'])
		print(' region: ' + p['region'])
		print(' zip: ' + p['zip'])
		print(' country: ' + p['country'])
		print('Phone number: ' + p['phone'])
		print('')


# Create html data for printing / saving
def createHtmlString(data):
	hypst = "<!DOCTYPE html><html lang=\"en-US\"><head><title>AL data converter example program</title><meta charset=\"utf-8\"><style>"
	hypst += "table, th, td { border: 1px solid black; }"
	hypst += "</style></head><body>"
	hypst += "<table style=\"width:100%\">"
	hypst += "<tr><th id=\"name\" rowspan=\"2\">Name</th><th id=\"address\" colspan=\"5\" colspan=\"1\">Address</th><th id=\"phone\" rowspan=\"2\">Phone</th></tr>"
	hypst += "<tr><th id=\"street\">Street</th><th id=\"city\">City</th><th id=\"region\">Region</th><th id=\"zip\">Zip</th><th id=\"country\">Country</th></tr>"
	for p in data['people']:
		hypst += "<tr>"
		hypst += "<td headers=\"name\">" + p['name'] + "</td>"
		hypst += "<td headers=\"street\">" + p['street'] + "</td>"
		hypst += "<td headers=\"city\">" + p['city'] + "</td>"
		hypst += "<td headers=\"region\">" + p['region'] + "</td>"
		hypst += "<td headers=\"zip\">" + p['zip'] + "</td>"
		hypst += "<td headers=\"country\">" + p['country'] + "</td>"
		hypst += "<td headers=\"phone\">" + p['phone'] + "</td>"
		hypst += "</tr>"
	hypst += "</table>"
	hypst += "</head></html>"
	return hypst


# Print html file to the screen
def printHtml(data):
	print("\nPrinting data to html format:")
	print(createHtmlString(data))


# Save html data to a file
def saveHtml(data, filename):
	dump = createHtmlString(data)

        savefile = open(filename, "w")
        savefile.write(dump)
        savefile.close()

        checkFileSize(dump, filename)


# main

# Check arguments
if len(sys.argv) < 3:
	help()
	print("Invalid number of arguments used when invoking program.")
	exit(-1)

if len(sys.argv) % 2 == 0:
	help
	print("This program accepts parameters with values only, so all parameters must have a value paired.")
	exit(-2)

# Argument derived data
inFileName = ""
inFileExt = ""
outFileName = ""
outFileExt = ""
printFormat = ""

counter = 1

while counter + 2 <= len(sys.argv):
	if sys.argv[counter] == "--in":
		inFileExt = getExt(sys.argv[counter + 1])
		if (len(inFileExt) > 0):
			inFileName = sys.argv[counter + 1]
	elif sys.argv[counter] == "--out":
		outFileExt = getExt(sys.argv[counter + 1], 1)
		if (len(outFileExt) > 0):
			outFileName = sys.argv[counter + 1]
	elif sys.argv[counter] == "--print":
		printFormat = sys.argv[counter + 1]
		if (printFormat != "txt" and printFormat != "html"):
			print("Invalid printformat found: " + printFormat + ". It is ignored")
			printFormat = ""
	counter += 2

if len(inFileName) == 0:
	help()
	print("There is no valid inFileName. The script will not run, input file is required.")
	exit(-3)

print("Arguments read, running with the following parameters:")
print("Input file: " + inFileName)
print("Output file: " + outFileName)
print("Printing to screen as: " + printFormat)
print("\n")

# Sanity check, there must be at least one input file
if not os.path.isfile(inFileName):
	print("File " + inFileName + " is not found.")
	exit(-4)

# in one of the supported formats
if inFileExt.lower() == "json":
	data = loadJson(inFileName)
elif inFileExt.lower() == "csv":
	data = loadCsv(inFileName)
elif inFileExt.lower() == "xml":
	data = loadXml(inFileName)

if data is None:
	exit(-5)

# File output
if outFileExt.lower() == "json":
	saveJson(data, outFileName)
elif outFileExt.lower() == "csv":
	saveCsv(data, outFileName)
elif outFileExt.lower() == "xml":
	saveXml(data, outFileName)
elif outFileExt.lower() == "html":
	saveHtml(data, outFileName)
elif len(outFileName) > 0:
	print("Invalid output file format: " + outFileName)

# Console output
if printFormat == "txt":
	printTxt(data)
elif printFormat == "html":
	printHtml(data)
elif len(printFormat) > 0:
	print("Invalid print format: " + printFormat)

