import requests
import socket
import json

# auth details for PRTG API calls
myuser = ''
mypassword = ''

def delete_prtg_probe(prestage_data_id):
	print "Deleting option", prestage_data_id
	prestage_data_id = prestage_data_id - 1
	#convert prtg object id passed into the fucntion to str for the url
	PRTGObjID = str(probe_prestage_data[prestage_data_id]['PRTGObjID'])
	probename = str(probe_prestage_data[prestage_data_id]['ProbeName'])
	confirm_choice_msg = "Are you sure you want to delete probe " + PRTGObjID +": "+ probename +"? This is PERMANANT! \n(Y/N): "
	confirm_choice = raw_input(confirm_choice_msg)
	api_call = 'https://prtg.cc.lan/api/deleteobject.htm?id=' + PRTGObjID + '&approve=1&&username=' + myuser + '&password=' + mypassword
	
	#make request
	if confirm_choice.lower() == "y":
		r=requests.get(api_call, verify=False)
		print "HTTPS Status Code: ", r.status_code
		print "ProbeID",PRTGObjID,"deleted"
	else:
		print "Aborting..."
		exit()
	return
  
#user input of probe name to delete
probe_to_search_for = raw_input("Probe Name: ")
#convert to lowercase
probe_to_search_for = probe_to_search_for.lower()
#Get a list of all probes in PRTG group ID 1 and return their name and object ID
#send request to prtg api, verify needed to ignore https cert warnings
r = requests.get('https://prtg.cc.lan/api/table.json?id=1&count=5000&content=probes&output=json&columns=objid,name&&username=' + myuser + '&password=' + mypassword, verify=False)
print "HTTPS Status Code: ", r.status_code
#The server returns a json array of probes
result_json = r.json()
#load the actual probe object data from the json into variable called probe
probes = result_json["probes"]
# create list to hold dictionaries of all found interfaces with names and prtg object IDs
probe_prestage_data = []
#create counter and set to 0, this forms the basis of the menu system
result_counter = 0

#loop through all returned probes
for probe in probes:
	probename = probe["name"]
	probeid = probe["objid"]
	#search for user entry against probe names converted to lower case
	if probe_to_search_for in probename.lower():
		# print probeid,":",probename
		result_counter = result_counter + 1
		#add info to new dictionary in prestage list
		probe_prestage_data.append({'OptionID' : result_counter, 'PRTGObjID' : probeid, 'ProbeName' : probename})
		
#sort the prestage list by option id
probe_prestage_data = sorted(probe_prestage_data, key=lambda k: k ['OptionID'])

print "Found", len(probe_prestage_data), "matches for", probe_to_search_for, "\n"
for entry in  probe_prestage_data:
	print "Option:", entry['OptionID']
	print "PRTG ObjectID:", entry['PRTGObjID']
	print "Probe Name:", entry['ProbeName']
	print "--------------------------"
#user input section for choosing which probes to delete
counter = 1
#infinite loop so user can delete multiple probes
while 1:
	print "Select probe to delete.  Type the option number, or 'all' to delete all probes.  Ctrl+C to cancel"	
	selected_ID = raw_input("probe to delete: ")
	#if user types all then delete all probes by setting a counter and looping through until the counter = the lenght of the list
	if selected_ID == "all":
		while counter < len(probe_prestage_data) + 1:
			delete_prtg_probe(counter)
			counter = counter + 1
		print "All probes deleted, exiting...."
		exit()
			
	else:
		selected_ID = int(selected_ID)
		delete_prtg_probe(selected_ID)
