import sys
import csv
import webbrowser
from xml.dom.minidom import parse
from difflib import SequenceMatcher

##########################################
##          MDT Driver Reporter         ##
##          Author: Jason Walsh         ##
##                                      ##
##########################################

def load_xml():
	global xmlDrivers 
	xmlDrivers = parse('Drivers.xml')
	global xmlDriverGroups
	xmlDriverGroups = parse('DriverGroups.xml')

def write_to_file(s0,s1): # filename, content
	with open(s0,'w') as the_file:
		the_file.write(s1)
	the_file.close;
	
def get_html_header():
	head=''
	head+='<!DOCTYPE html><html><head>\n'
	head+='<script src="sorttable.js"></script>\n'
	head+='<style>body{background-color: #F2F2F2;}table, td, th {border: 1px solid black;border-collapse: collapse;background-color: #D9D9D9;}td.offline{background-color: rgb(130, 206, 184);}'
	head+='th{background-color: #C9C9C9;border: 1px solid black;border-collapse: collapse;}#results{border: solid;text-align: center;} h1{text-align: center;} p{text-align: center; font-weight: 900;}'
	head+='</style>\n</head>\n<body>\n'
	return head
	
def get_table_header():
	tabHead=''
	tabHead+="<h1>Driver Report</h1><p>Source: Drivers.xml, DriverGroups.xml</p></br>"
	tabHead+='<table class="sortable" style="width:100%">'
	tabHead+='<tr><th>Name</th><th>GUID</th><th>HID</th><th>Version</th><th>Class</th><th>Platform</th><th>OS Version</th><th>Last Updated</th><th>Groups</th></tr>'
	return tabHead
	
def get_table_end():
	return '</table>'
	
def get_table_row(s0):
	row=''
	for el in s0:
		row+="<td valign='top'>"
		row+=str(el)
		row+="</td>"
	row+="</tr>"
	return row
		
def xml_pull_tag(s0,s1):
	list = s0.getElementsByTagName(s1)
	combine = ''
	if list.length > 0:
		for el in list:
			if el.hasChildNodes():
				if is_empty(el.childNodes[0].nodeValue) == False:
					if is_empty(combine) == False:
						combine+=','
					combine+=el.childNodes[0].nodeValue
	return combine
	
def is_empty(s0):
	empty = True
	if s0 != "" and s0 != " ":
		empty = False
	return empty
	
def main():

	print('')
	print('MDT Driver Reporter v2.0')
	print('________________________________________________')
	print("Working...")
	
	load_xml()
	writeString=""
	writeString+=get_html_header()
	writeString+=get_table_header()
	
	#tally info
	numberOfDrivers=0;
	numberOfGroups=0;
	
	#current hardware variable to ensure no duplicate groups are displayed
	selectedHardware = ""
	
	#get the drivers
	drivers = xmlDrivers.getElementsByTagName('driver')
	progressTotal = drivers.length;
	
	for el in drivers:
		numberOfDrivers+=1
	
		name = xml_pull_tag(el,"Name")
		guid = el.attributes['guid'].value
		hid	= xml_pull_tag(el,'PNPId')
		ver		= xml_pull_tag(el,'Version')
		clas	= xml_pull_tag(el,'Class')
		plat	= xml_pull_tag(el,'Platform')	
		os		= xml_pull_tag(el,'OSVersion')
		lastMod	= xml_pull_tag(el,'LastModifiedTime')
		infLoc	= xml_pull_tag(el,'Source')
		

		#search for instances of the GUID
		driverGroups = xmlDriverGroups.getElementsByTagName('group')
		hardwareList=''
		if numberOfGroups > 0:
			numberOfGroups=0;
		for el1 in driverGroups:
			numberOfGroups+=1;		
			guidList = xml_pull_tag(el1,'Member').split(',')
			for el2 in guidList:
				if str(el2) == guid:
									
					#get the hardware name:
					hardwareName = xml_pull_tag(el1,'Name')
					temp = []
					temp = hardwareName.split(',')
					for el3 in temp:
						hardwareList+= str(el3)+'</br></br>'		


		#print the info
		infoList = []
		infoList.append(name)
		infoList.append(guid)
		infoList.append(hid)
		infoList.append(ver)
		infoList.append(clas)
		infoList.append(plat)
		infoList.append(os)
		infoList.append(lastMod)
		infoList.append(hardwareList)
		writeString += get_table_row(infoList)
		
	writeString+= get_table_end()
	writeString+="</br><b>Total Drivers: "+str(numberOfDrivers)+"</br>Total Groups: "+str(numberOfGroups)+"</b></br>"
	write_to_file("DriverReport.html",writeString)
	
	print("Complete!")
	
if __name__ == "__main__":
	main()