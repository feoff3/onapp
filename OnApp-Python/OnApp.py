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


        def getDataStoreZoneList(self):
                response = self.baseObject.sendRequest("GET", "/data_store_zones.json");
                data = json.loads(response.read());
                return data;

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
        def destroy(self, dsZID):
                response = self.baseObject.sendRequest("DELETE", str('/data_store_zones/%s.json' %(dsZID)));
                data = json.loads(response.read());
                ##returns nothing###


class OnAppDataStores:
        baseObject = False;
        def __init__(self, baseObject):
                self.baseObject = baseObject;

        def getDataStores(self):
                response = self.baseObject.sendRequest("GET", "/settings/data_stores.json");
                data = json.loads(response.read());
                return data;
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

        def destroy(self, dsID):
                response = self.baseObject.sendRequest("DELETE", str('/settings/data_stores/%s.json' %(dsID)));
                data = json.loads(response.read());
                ##returns nothing###

class OnAppHyperVisorZones:
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
        def getListOfHyperVisorsInZone(self, hyperVisorZoneID):
                getURL = "/settings/hypervisor_zones/%s/hypervisors.json" % (str(hyperVisorZoneID));
                response = self.baseObject.sendRequest("GET", getURL);
                data = json.loads(response.read());
                return  data;

class OnAppHyperVisors:
        baseObject = False;
        def __init__(self, baseObject):
                self.baseObject = baseObject;
				
		######## HyperVisor Methods ########
		
		#
		# Get the list of Hypervisors, reference 14.1 - Page 116
		#
		def getHyperVisorDetails(self, hvID):
                uriString = "/settings/hypervisors/%s.json" % (str(hvID));
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                if 'hypervisor' in data:
                        return data['hypervisor'];
                else:
                        return data;
		
		#
		# Get the list of unassigned hypervisors
		#
		def getUnassignedHyperVisors(self):
			response = self.baseObject.sendRequest("GET", "/hypervisors/not_grouped.json");
			data = json.loads(response.read());
			if 'hypervisors' in data:
					return data['hypervisors'];
			else:
					return data;

        def joinDataStore(self, dataStoreID, hyperVisorID):
                postURL = "/settings/hypervisors/%s/data_store_joins.json" % (str(hyperVisorID));
                request = json.dumps({'data_store_id': dataStoreID});
                response = self.baseObject.sendRequest("POST", postURL, request);
                data = json.loads(response.read());
                if 'data_store_join' in data:
                        return data['data_store_join'];
                else:
                        return data;
        def getListOfVMsRunning(self, hvID):
                uriString = "/hypervisors/%s/virtual_machines.json" % (str(hvID));
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                return data;

        def getListHyperVisors(self):
                uriString = "/settings/hypervisors.json";
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                return data;

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

        def getVirtualMachinesTransactions(self, virtualMachineID):
                uriString = "/virtual_machines/%s/transactions.json" % (virtualMachineID);
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                if 'transactions' in data:
                        return data['transactions'];
                else:
                        return data;

        def getParticularTransaction(self, transactionID):
                uriString = "/transactions/%s.json" % (transactionID);
                response = self.baseObject.sendRequest("GET", uriString);
                data = json.loads(response.read());
                if 'transaction' in data:
                        return data['transaction'];
                else:
                        return data;