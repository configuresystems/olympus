#!/usr/bin/python
import simplejson as json
import pycurl, urllib, sys
import subprocess
import memcache

mc = memcache.Client(['localhost:11211'], debug=0)
alertEmails = ['stephenc@hhs1.com']
restUrlBase = 'https://ruby-ds-east.vpn'
response = ''

def getResponse(respPart):
    global response
    if respPart != None:
        response = response + respPart

def sendAlertEmail(subject, bodyTxt, fromAddr='sfRestBridge@hhs1.com'):
    for toAddress in alertEmails:
        echoSP = subprocess.Popen(['/bin/echo', bodyTxt], stdout=subprocess.PIPE)
        subprocess.Popen(["/bin/mail", "-s", subject, toAddress, "--", "-r", fromAddr], stdin=echoSP.stdout, stdout=subprocess.PIPE)

def hl7Update(bed, msgType, facility, theSex, oldBed='', id='', pdata=''):   #names of http params matter as SF tries to deserialize into local vars passed to the context function
    try:
        tenant = getCachedHL7ToTenantMap()[facility]['tenant']
        if (pdata != '') :
            extra_parms = json.loads(pdata) #load up JSON compliant string as python dictionary
            named_parms = {'bedname': bed, 'frombed': oldBed, 'action': msgType, 'id': id, 'sex': theSex}
            all_parms = dict( named_parms.items() + extra_parms.items())
            httpParams = json.dumps(all_parms)
        else:
            httpParams = json.dumps({'bedname': bed, 'frombed': oldBed, 'action': msgType, 'id': id, 'sex': theSex})
#        print httpParams
        return json.loads(restPost('/api/' + tenant + '/hl7/' + facility + '/' + msgType, httpParams))
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def ivrUpdate(pin, bed, state, facility):
    try:
        tenant = getCachedIVRToTenantMap()[facility]['tenant']
        httpParams = json.dumps({'bedname': bed, 'ivrid': pin, 'action': state})
#        print httpParams
        return json.loads(restPost('/api/' + tenant + '/ivr/' + facility + '/'+ state, httpParams))
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def txIvrUpdate(facility, campus, pin, state, job='', jsonMethodParams=''):
    try:
        tenant = getCachedIVRToTenantMap()[facility]['tenant']
        if jsonMethodParams != '':
            httpParams = json.dumps({'params': jsonMethodParams})
            return json.loads(restPost('/api/' + tenant + '/' + facility + '/' + campus + '/transporter/' + pin + '/' + state + '/' + job, httpParams))
        else:
            return json.loads(restPost('/api/' + tenant  + '/' + facility + '/' + campus + '/transporter/' + pin + '/' + state + '/' + job))
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def txMessage(facility, campus, sender, jsonMethodParams):
    try:
        tenant = getCachedIVRToTenantMap()[facility]['tenant']
        httpParams = json.dumps({'params': jsonMethodParams})
        return json.loads(restPost('/api/' + tenant  + '/' + facility + '/' + campus +  '/transporter/' + sender + '/tx_message', httpParams))
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def listBedNumbers(tenant):
    try:
        beds = restPost('/api/' + tenant + '/bwintlist/getFacilityBedNumbers')
        return json.loads(beds)
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def listIds(tenant):
    try:
        ids = restPost('/api/' + tenant + '/bwintlist/getFacilityIvrIds')
        return json.loads(ids)
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def listTenants():
    try:
        tenants = restPost('/api/getTenants')
        return json.loads(tenants)
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def getCachedTenantList():
    cachedList = mc.get("fmbCache:tenantList")
    if cachedList == None:
        ###Cached tenant list not available, fetching from DS and cacheing for future use...###
        tenants = listTenants()
        mc.set("fmbCache:tenantList", tenants, 3600)
        return tenants
    else:
        ###Cached tenant list found, returning it.###
        return cachedList

def getCachedIVRToTenantMap():
    cachedMap = mc.get("fmbCache:ivrToTenantMap")
    if cachedMap == None:
        ###Cached map not available, fetching from DS and cacheing for future use...###
        ivrToTenantMap = getIVRToTenantMap()
        mc.set("fmbCache:ivrToTenantMap", ivrToTenantMap, 3600)
        return ivrToTenantMap
    else:
        ###Cached map found, returning it.###
        return cachedMap

def getCachedHL7ToTenantMap():
    cachedMap = mc.get("fmbCache:hl7ToTenantMap")
    if cachedMap == None:
        ###Cached map not available, fetching from DS and cacheing for future use...###
        hl7ToTenantMap = getHL7ToTenantMap()
        mc.set("fmbCache:hl7ToTenantMap", hl7ToTenantMap, 3600)
        return hl7ToTenantMap
    else:
        ###Cached map found, returning it.###
        return cachedMap

def getIVRToTenantMap():
    try:
        tenants = restGet('/api/all_tenants_ivrs')
        return json.loads(tenants)
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def getHL7ToTenantMap():
    try:
        tenants = restGet('/api/all_tenants_hl7s')
        return json.loads(tenants)
    except Exception, err:
        sys.stderr.write('ERROR: ' + str(err) + '\n')

def getPrimaryIVRId(ivrNum):
    primaryIVR = getCachedIVRToTenantMap()[ivrNum]['primaryIVR']
    if primaryIVR == None:
        return ivrNum
    else:
        return primaryIVR


def restPost(restResource, params=''):   #pycurl seems to have a bug that requires postfields (params) to be present even if just an empty string...
    global response
    curl = pycurl.Curl()
    curl.setopt(curl.URL, restUrlBase + restResource)
    curl.setopt(curl.POST, 1)
    curl.setopt(curl.CONNECTTIMEOUT, 10)
    curl.setopt(curl.TIMEOUT, 30)
    curl.setopt(curl.SSL_VERIFYHOST, 0)
#    curl.setopt(curl.VERBOSE, 1)
    curl.setopt(curl.HTTPHEADER, ['Content-Type: application/json'])
    curl.setopt(curl.POSTFIELDS, params)
    curl.setopt(curl.WRITEFUNCTION, getResponse)
    curl.perform()
    curl.close()

    resp = response
    response = ''
    return resp


def restGet(restResource):   #pycurl seems to have a bug that requires postfields (params) to be present even if just an empty string...
    global response
    curl = pycurl.Curl()
    curl.setopt(curl.URL, restUrlBase + restResource)
#    curl.setopt(curl.POST, 1)
    curl.setopt(curl.CONNECTTIMEOUT, 10)
    curl.setopt(curl.TIMEOUT, 30)
    curl.setopt(curl.SSL_VERIFYHOST, 0)
#    curl.setopt(curl.VERBOSE, 1)
    curl.setopt(curl.HTTPHEADER, ['Content-Type: application/json'])
#    curl.setopt(curl.POSTFIELDS, params)
    curl.setopt(curl.WRITEFUNCTION, getResponse)
    curl.perform()
    curl.close()

    resp = response
    response = ''
    return resp


