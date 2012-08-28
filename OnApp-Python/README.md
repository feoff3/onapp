OnApp-Python Library
====

This library was developed by Karl Kloppenborg with the contribution help of Daniel Tandowski
It is used as a wrapper API to implement OnApp control in a standard format for Python.

==

Note: Requires Python >= 2.6
Implementation example:

#!/usr/bin/python

## Import the required modules
from OnApp import OnAppBase, OnAppHyperVisors;

## Connect to OnApp
base = OnAppBase();
base.connectOnApp(“admin”, “password”, “IPADDRESS”, ‘80’);

## Now let’s instantiate the HV class
## Ensure you have the base class in there so you can make calls.
hvAPI = OnAppHyperVisors(base);

## Do a call
hvList = hvAPI. getListHyperVisors();

for hv in hvList:
                print hv[‘hypervisor’]; ##print all the info about the hv.
