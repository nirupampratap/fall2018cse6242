import requests
import sys
import time
import csv
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

#This is my APIKey
g_MyApiKey = "X1-ZWz18acdjsafij_8s1xw"
# This will work in the current scenario because it is a single thread. In multi-thread scenarios we will need a lock

def getZillowData(address="1600 Pennsylvania Avenue NW", zipcode = "20500"):

    global g_MyApiKey

    webResponse = ""

    zillowData = ZillowWrapper(g_MyApiKey)
    
    webResponse = zillowData.get_deep_search_results(address, zipcode)
    result = GetDeepSearchResults(webResponse)
        
    print(result.zestimate_percentile)

    return result

fullResult = getZillowData("251 10th St NW #153","30318")
