import requests
import sys
import time
import csv
from datetime import datetime

g_URL = 'https://search.onboard-apis.com'

#This is my APIKey
g_MyApiKey = "fe61702bb2e95e80b4e0b45f3e8d2e8f"
g_BusCatDict = {'hospitality':'HOSPITALITY', 'shopping': 'SHOPPING', 'restaurant': 'EATING - DRINKING'}
g_PropTypeDict = {0:'APARTMENT', 1: 'COMMERCIAL (NEC)', 3: 'COMMERCIAL BUILDING', 4: 'CONDOMINIUM', 5:'STORES & OFFICES', 6:'STORES & RESIDENTIAL'}
# This will work in the current scenario because it is a single thread. In multi-thread scenarios we will need a lock

def getPOIByGeo(postalCodeKey = '10005', searchDistance = '5', recLim = '20', sortBy = 'NAME'):

    global g_URL
    global g_MyApiKey

    urlExtension = "/poisearch/v2.0.0/poi/geography?"
    webResponse = ""
    resultsJson = []
    headers = {'ApiKey': g_MyApiKey, 'accept': 'application/json'}

    webResponse = requests.get(g_URL + urlExtension + 'PostalCodeKey=' + postalCodeKey + '&SearchDistance=' + searchDistance + '&RecordLimit=' + recLim + '&Sort=' + sortBy + '&BusinessCategory=' + g_BusCatDict['restaurant'], timeout=10, headers = headers)

    resultsJson = webResponse.json()["response"]

    return resultsJson

def getRestaurantAddress(resultsJson = []):
    for items in resultsJson['result']['package']['item']:
        print(items['name'])

def getPropInZip(postalCode = '82009', pageNum = 1, pageSize = 50, maxRec = 200):

    global g_URL
    global g_MyApiKey
    global g_PropTypeDict

    totalRec = 0
    totalProc = 0
    fullResults = []

    urlExtension = "/propertyapi/v1.0.0/property/address?"
    webResponse = ""
    headers = {'apikey': g_MyApiKey, 'accept': 'application/json'}
    
    while (totalProc < maxRec):
        print("Loop ",pageNum, postalCode)
        processedResults = []
        propResultsJson = {}

##        webResponse = requests.get(g_URL + urlExtension + 'postalcode=' + postalCode + '&propertytype=' + g_PropTypeDict[5] + '&page=' + str(pageNum) + '&pagesize=' + str(pageSize), timeout=10, headers = headers)
        webResponse = requests.get(g_URL + urlExtension + 'postalcode=' + postalCode + '&page=' + str(pageNum) + '&pagesize=' + str(pageSize), timeout=10, headers = headers)

        if(webResponse.status_code == 200):
            status = webResponse.json()['status']
            propResultsJson = webResponse.json()['property']
            totalProc += status['pagesize']
            if(status['total'] <= maxRec): maxRec = status['total']

            processedResults = getAtomIdsFromPropList(propResultsJson)
            fullResults.append(processedResults)
            pageNum += 1
        else:
            totalProc = maxRec+1


    return fullResults

def getSaleInfoByProp(attomid = '184713191'):

    global g_URL
    global g_MyApiKey
    global g_PropTypeDict

    urlExtension = "/propertyapi/v1.0.0/property/basicprofile?"
    webResponse = ""
    headers = {'apikey': g_MyApiKey, 'accept': 'application/json'}
    saleRetInfo = {}
    
    webResponse = requests.get(g_URL + urlExtension + 'attomid=' + str(attomid) , timeout=10, headers = headers)

    bldgInfo = webResponse.json()['property'][0]['building']
    saleInfo = webResponse.json()['property'][0]['sale']

    saleRetInfo['amt'] = saleInfo['saleAmountData']['saleAmt']
##    saleRetInfo['transyr'] = datetime.strptime(saleInfo['saleAmountData']['saleRecDate'], "%Y-%m-%d")
##    if any('saleSearchDate' in key for key in saleInfo):
##        saleRetInfo['transyr'] = saleInfo['saleSearchDate']
    if('saleSearchDate' in saleInfo.keys()):
        saleRetInfo['transyr'] = datetime.strptime(saleInfo['saleSearchDate'], '%Y-%m-%d').year
    else:
        saleRetInfo['transyr'] = -1
    saleRetInfo['sft'] = bldgInfo['size']['grossSize']

    return saleRetInfo

def getAtomIdsFromPropList(resultsJson = {}):

    propResList = []

    for props in resultsJson:
        propResult = {}
        saleInfo = {}

        propResult['attomid'] = props['identifier']['attomId']
        propResult['addressline'] = props['address']['oneLine']
        saleInfo = getSaleInfoByProp(propResult['attomid'])
        propResult['salevalue'] = saleInfo['amt']
        propResult['sft'] = saleInfo['sft']
        propResult['year'] = saleInfo['transyr']
        propResList.append(propResult)

    return propResList

def saveToFile(inputList={}, filePath = "./", fileName="prop_details.csv"):

    if not inputList:
        return
    else:
        with open(filePath + fileName, mode='w') as propDetailsFile:
            propFileWriter = csv.writer(propDetailsFile, dialect='excel')

            propFileWriter.writerow(inputList)

#        for listItem in inputList:
            #Items of interest to us are movie-id and movie-name
            #propFileWriter.writerow([str(listItem['attomid']), listItem['year'], listItem['sft'], listItem['salevalue'], listItem['addressline']])
#            propFileWriter.writerow(Lis)

    return


# Main function

finalProcList = []
presentRow = 0

with open('zipcodes.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fullList = []
        fullList = getPropInZip(postalCode=str(row['Zipcode']),pageSize=100,maxRec=500)
        finalProcList.append(fullList)
#        presentRow += 1
#        if(presentRow >=3): break

saveToFile(finalProcList)
