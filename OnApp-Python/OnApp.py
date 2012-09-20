"""
        OnApp Python Module
        @Author Karl Kloppenborg
        @Email: karl@crucialp.com
        @License GPL 3.0
        @Version 1.1
	@Contributed: Daniel Tandowski

    OnApp Python Module - Providing a Python Interface for OnApp
    Copyright (C) 2012  Karl Kloppenborg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#Import the basic required modules needed to run and request API

import base64, httplib, urllib, urllib2, json, random, string, time, uuid, logging, os, sys;

class OnAppBase:
        conn = False;
        basicAuth = "";
        def connectOnApp(self, username, password, hostname, port):
                self.basicAuth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '');
                self.conn = httplib.HTTPConnection(hostname, port);
                try:
                        logging.info("Connecting to HTTPConnection");
                        self.conn.connect();
                except:
                        logging.exception('Unable to run HTTPConnection Connect, unable to continue!');
                        sys.exit(1);

        def sendRequest(self, type, page, requestData=False):
                headers = {"Authorization": "Basic %s" % self.basicAuth, 'Accept': 'application/json', 'Content-type': 'application/json'};
                if requestData == False:
                        self.conn.request(type, page, None, headers);
                else:
                        self.conn.request(type, page, requestData, headers);
                return self.conn.getresponse();

        def getVersion(self):
                #Make Request to OnApp with Basic Auth
                response = self.sendRequest("GET", "/version.json");
                array = json.loads(response.read());
                if 'version' in array:
                        return array['version'];
                return False;

class OnAppDataStoreZones:
	baseObject = False;
	def __init__(self, baseObject):
		self.baseObject = baseObject;

	#
	# Get the list of data store zones, reference 10.1 - Page 95
	#	

	def getDataStoreZoneList(self):
		response = self.baseObject.sendRequest("GET", "/data_store_zones.json");
		data = json.loads(response.read());
		return data;

	#
	# Add a data store zone, reference 10.2 - Page 95
	#	

	def addDataStoreZone(self, label):
		request = {'pack': {'label': label}};
		request = json.dumps(request);
		response = self.baseObject.sendRequest("POST", "/data_store_zones.json", request);
		data = response.read();
		data = json.loads(data);
		if 'data_store_group' in data:
			return data['data_store_group'];
		else:
			return data;

	#
	# Get data store zone details, reference 10.3 - Page 96
	#						

	def getDataStoreZoneDetails(self, dszID):
		uriString = "/data_store_zones/%s.json" % (str(dszID));
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		if 'datastore_store_group' in data:
			return data['datastore_store_group'];
		else:
			return data;

	#
	# Edit a data store zone label, reference 10.4 - Page 96
	#

	def editDataStoreZone(self, dszID, dsLabel):
		uriString = "/data_store_zones/%d.json" % dszID;
		request = json.dumps(	{ "data_store_group": 
			{ "label": str(dsLabel) }
		}
		);
		response = self.baseObject.sendRequest("PUT", uriString, request);
		data = json.loads(response.read());
		if 'data_store_group' in data:
			return data['data_store_group'];
		else:
			return data;

	#
	# Delete a data store zone, reference 10.5 - Page 97
	#		

	def destroy(self, dszID):
		response = self.baseObject.sendRequest("DELETE", str('/data_store_zones/%s.json' %(dszID)));
		data = json.loads(response.read());
		##returns nothing###

	#
	# Get the list of data stores attached to a data store zone, reference 10.6 - Page 97
	#				

	def getListOfAttachedDataStores(self, dszID):
		uriString = "/data_store_zones/%d/data_stores.json" % dszID;
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		return data;

	#
	# Attach a data store to a data store zone,  reference 10.7 - Page 99
	#				

	def attachDataStoreToZone(self, dsID, dszID):
		postURL = "/data_store_zones/%d/data_stores/%d/attach.json" % (dszID, dsID);
		response = self.baseObject.sendRequest("POST", postURL);
		data = json.loads(response.read());

	#
	# Detach a data store to a data store zone,  reference 10.8 - Page 99
	#				

	def detachDataStoreFromZone(self, dszID, dsID):
		postURL = "/data_store_zones/%d/data_stores/%d/detach.json" % (dszID, dsID);
		response = self.baseObject.sendRequest("POST", postURL);
		data = json.loads(response.read());	

class OnAppDataStores:
	baseObject = False;
	def __init__(self, baseObject):
		self.baseObject = baseObject;

	#
	# Get the list of data stores,  reference 19.1 - Page 142
	#				

	def getDataStores(self):
		response = self.baseObject.sendRequest("GET", "/settings/data_stores.json");
		data = json.loads(response.read());
		return data;

	#
	# Get data store details,  reference 19.2 - Page 142
	#		

	def getDataStoreDetails(self, dsID):
		uriString = "/settings/data_stores/%s" % dsID;
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		return data;

	#
	# Add a new data store,  reference 19.3 - Page 143
	#		

	def addDataStore(self, label, dataStoreZoneID, ipAddress, dataStoreSize, enabled=True):
		request = {'data_store': {"label": label, "data_store_group": dataStoreZoneID, "ip": ipAddress, "enabled": enabled, "data_store_size": dataStoreSize}};
		request = json.dumps(request);
		response = self.baseObject.sendRequest("POST", "/settings/data_stores.json", request);
		data = json.loads(response.read());
		## Seems there is a bug in onapp and it doesnt apply the dataStoreZoneID, lets update datastore and apply it
		if 'data_store' in data:
			return data['data_store'];
		else:
			return data;

	#
	# Edit a data store,  reference 19.4 - Page 144
	#

	def editDataStore(self, dsID):
		uriString = "/data_stores/%d.json" % dsID;
		request = json.dumps(	{ "data_store_group": 
			{ "label": str(label) }
		}
		);
		response = self.baseObject.sendRequest("PUT", uriString, request);
		data = json.loads(response.read());
		if 'data_store_group' in data:
			return data['data_store_group'];
		else:
			return data;

	#
	# Delete a data store,  reference 19.5 - Page 145
	#

	def destroy(self, dsID):
		response = self.baseObject.sendRequest("DELETE", str('/settings/data_stores/%s.json' %(dsID)));
		data = json.loads(response.read());
		##returns nothing###	

class OnAppHypervisorZones:
        baseObject = False;
        def __init__(self, baseObject):
                self.baseObject = baseObject;

        def joinDataStore(self, dataStoreID, hyperVisorZoneID):
                ##Do the join.
                postURL = "/settings/hypervisor_zones/%s/data_store_joins.json" % (str(hyperVisorZoneID));
                request = json.dumps({'data_store_id': dataStoreID});
                response = self.baseObject.sendRequest("POST", postURL, request);
                data = json.loads(response.read());
                if 'data_store_join' in data:
                        return data['data_store_join'];
                else:
                        return data;

	#
	# Get the list of hypervisor zones, reference 12.1 - Page 104 
	#

        def getListOfHypervisorsInZone(self, hyperVisorZoneID):
                getURL = "/settings/hypervisor_zones/%s/hypervisors.json" % (str(hyperVisorZoneID));
                response = self.baseObject.sendRequest("GET", getURL);
                data = json.loads(response.read());
                return data;

	#
	# Add a hypervisor zone, reference 12.2 - Page 104 
	#

	def addHypervisorZone(self, label):
		request = {'pack': {'label': label}};
		request = json.dumps(request);
		response = self.baseObject.sendRequest("POST", "/hypervisor__zones.json", request);
		data = response.read();
		data = json.loads(data);
		if 'hypervisor_group' in data:
			return data['hypervisor_group'];
		else:
			return data;

	#
	# Get hypervisor zone details, reference 12.3 - Page 105 
	#

	def getHypervisorZoneDetails(self, hvzID):
		uriString = "/hypervisor_zones/%s.json" % (str(hyperVisorZoneID));
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		if 'hypervisor_group' in data:
			return data['hypervisor_group'];
		else:
			return data;

	#
	# Edit a hypervisor zone, reference 12.4 - Page 105 
	#

	def editHypervisorZone(self, hvzID, hvzLabel):
		uriString = "/hypervisor_zones/%d.json" % hvzID;
		request = json.dumps(	{ "hypervisor_zone_name": 
			{ "label": str(hvzLabel) }
		}
		);
		response = self.baseObject.sendRequest("PUT", uriString, request);
		data = json.loads(response.read());
		if 'hypervisor_zone_name' in data:
			return data['hypervisor_zone_name'];
		else:
			return data;

	#
	# Delete a hypervisor zone, reference 12.5 - Page 106 
	#

	def destroy(self, hvzID):
		response = self.baseObject.sendRequest("DELETE", str('/hypervisor_zones/%s.json' %(hvzID)));
		data = json.loads(response.read());
		##returns nothing###

	#
	# Get the list of hypervisors attached to hypervisor zone, reference 12.6 - Page 106 
	#

	def getListOfAttachedHypervisors(self, hvzID):
		uriString = "/data_store_zones/%d/hypervisors.json" % hvzID;
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		return data;


class OnAppHypervisors:
	baseObject = False;
	def __init__(self, baseObject):
			self.baseObject = baseObject;

	######## Hypervisor Methods ########
	#
	# Get the list of Hypervisors, reference 14.1 - Page 116
	#

	def getListHypervisors(self):
		uriString = "/settings/hypervisors.json";
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		return data;

	#
	# Get the list of unassigned hypervisors, reference 14.2 - Page 116
	#

	def getUnassignedHypervisors(self):
		response = self.baseObject.sendRequest("GET", "/hypervisors/not_grouped.json");
		data = json.loads(response.read());
		if 'hypervisors' in data:
			return data['hypervisors'];
		else:
			return data;

	#
	# Get hypervisor details, reference 14.3 - Page 118
	#

	def getHypervisorDetails(self, hvID):
		uriString = "/settings/hypervisors/%s.json" % (str(hvID));
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		if 'hypervisor' in data:
			return data['hypervisor'];
		else:
			return data;

	#
	# Add a new hypervisor, reference 14.4 - Page 120
	#

	def addHypervisor(self, ip_address, label, hypervisor_type, memory_overhead, enabled, hypervisor_group_id, disable_failover):
		request = json.dumps( 	{ "hypervisor": { 	
													"label": 				str(label),
													"enabled": 				str(enabled),
													"ip_address": 			str(ip_address),  
													"hypervisor_type": 		str(hypervisor_type),
													"memory_overhead": 		str(memory_overhead),
													"disable_failover": 	str(disable_failover),
													"hypervisor_group_id": 	str(hypervisor_group_id),
												} 
								} );
		response = self.baseObject.sendRequest("POST", "/settings/hypervisors.json", request);
		data = json.loads(response.read());
		if 'hypervisor' in data:
			return data['hypervisor'];
		else:
			return data;

	#
	# Edit a hypervisor, reference 14.5 - Page 120
	#

	def editHypervisor(self, hypervisor_id, ip_address, label, hypervisor_type, memory_overhead, enabled, hypervisor_group_id, disable_failover):
		uriString = "/settings/hypervisors/%d.json" % hypervisor_id;
		request = json.dumps( 	{ "hypervisor": { 	
													"label": 				str(label),
													"enabled": 				str(enabled),
													"ip_address": 			str(ip_address),  
													"hypervisor_type": 		str(hypervisor_type),
													"memory_overhead": 		str(memory_overhead),
													"disable_failover": 	str(disable_failover),
													"hypervisor_group_id": 	str(hypervisor_group_id),
												} 
								} );
		response = self.baseObject.sendRequest("PUT", uriString, request);
		data = json.loads(response.read());
		if 'hypervisor' in data:
			return data['hypervisor'];
		else:
			return data;

	#
	# Reboot a Hypervisor, reference 14.6 - Page 121
	# @note: Not implemented because current sendRequest wont handle none 200 request returns

	#def rebootHypervisor(self, hypervisor_id):

	#
	# Get the list of VM's running on the hypervisor, reference 14.7 - Page 122
	#

	def getListOfVMsRunning(self, hypervisor_id):
		uriString = "/hypervisors/%s/virtual_machines.json" % (str(hypervisor_id));
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		return data;

	#
	# Get the list of data store joins attached to the hypervisor, reference 14.8 - Page 122
	#

	def getJoinedDataStores(self, hypervisor_id):
		uriString "/settings/hypervisors/%d/data_store_joins.json" % hypervisor_id;
		response = self.baseObject.sendRequest("GET", uriString);
		data = json.loads(response.read());
		if 'data_store_joins' in data:
			return data['data_store_joins'];
		else:
			return data;

	#
	# Add a data store join to the hypervisor, reference 14.9 - Page 123
	#

	def joinDataStore(self, dataStoreID, hyperVisorID):
		postURL = "/settings/hypervisors/%s/data_store_joins.json" % (str(hyperVisorID));
		request = json.dumps({'data_store_id': dataStoreID});
		response = self.baseObject.sendRequest("POST", postURL, request);
		data = json.loads(response.read());
		if 'data_store_join' in data:
			return data['data_store_join'];
		else:
			return data;

	#
	# Remove a data store join from the hypervisor, reference 14.10 - Page 123
	#

	def removeDataStoreJoin(self, datastore_id, hypervisor_id):
		uriString = "/settings/hypervisors/%d/data_store_joins/%d" % (hypervisor_id, datastore_id);
		self.baseObject.sendRequest("DELETE", uriString);
		return True; ### It doesn't return anything anyways


class OnAppVirtualMachines:
	baseObject = False;
	def __init__(self, baseObject):
		self.baseObject = baseObject;

	def createVM(self, vmParams):
		request = json.dumps({"virtual_machine": vmParams});
		response = self.baseObject.sendRequest("POST", "/virtual_machines.json", request);
		data = json.loads(response.read());
		if 'virtual_machine' in data:
			return data['virtual_machine'];
		else:
			return data;

	def destroyVM(self, vmID):
		response = self.baseObject.sendRequest("DELETE", str("/virtual_machines/%s.json" % (vmID)));
		data = json.loads(response.read());
		### This method doesnt return anything

	def getListOfVirtualMachines(self):
		response = self.baseObject.sendRequest("GET", "/virtual_machines.json");
		data = json.loads(response.read());
		if 'virtual_machines' in data:
			return data['virtual_machines'];
		else:
			return data;

	def shutdownVM(self, vmID):
		uriString = "/virtual_machines/%s/shutdown.json" % (vmID);
		response = self.baseObject.sendRequest("POST", uriString);
		data = json.loads(response.read());

	def startupVM(self, vmID):
		uriString = "/virtual_machines/%s/startup.json" % (vmID);
		response = self.baseObject.sendRequest("POST", uriString);

	def migrate(self, vmID, destinationID, coldRollback):
		uriString = "/virtual_machines/%s/migrate.json" % (vmID);
		request = json.dumps({"virtual_machine": {"destination": str(destinationID), "cold_migrate_on_rollback": str(coldRollback)}});
		response = self.baseObject.sendRequest("POST", uriString, request);
		data = json.loads(response.read());
		if "virtual_machine" in data:
			return data['virtual_machine'];
		else:
			return data;


class OnAppTransactions:
        baseObject = False;
        def __init__(self, baseObject):
                self.baseObject = baseObject;

	#
	# Get the list of transactions,  reference 42.1 - Page 298
	#					
	def getTransactionList(self):
		response = self.baseObject.sendRequest("GET", "/transactions.json");
		data = json.loads(response.read());
		return data;				

	#
	# Get the list of a VMs transactions,  reference 42.2 - Page 299
	#	

        def getVirtualMachinesTransactions(self, virtualMachineID):
                uriString = "/virtual_machines/%s/transactions.json" % (virtualMachineID);
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                if 'transactions' in data:
                        return data['transactions'];
                else:
                        return data;

	#
	# Get a particular transactions details,  reference 42.3 - Page 300
	#	

        def getParticularTransaction(self, transactionID):
                uriString = "/transactions/%s.json" % (transactionID);
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                if 'transaction' in data:
                        return data['transaction'];
                else:
                        return data;

