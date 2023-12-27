import time
import configparser
from datetime import timedelta, date, datetime
from apixunit.apivalidation import *
from apixunit.plite import *
from apixunit.common import *
from apixunit.ghelper import get_nested_multiple_values
import random, json
import re

mypath = Path.cwd()  # .parent
config = configparser.ConfigParser()
config.read(mypath / "config.ini")
config.read(mypath / 'utils' / 'endpointapi.ini')


def pattern(extnurl, exValue):
    global rpurl
    pattern = r'\{[^{}]+\}'
    matching_variables = re.findall(pattern, extnurl)
    xid = []
    for variable in matching_variables:
        xid.append(variable)
    keys, values = xid, exValue
    replacements = dict(zip(keys, values))
    for pattern, replacement in replacements.items():
        rpurl = extnurl.replace(str(pattern), str(replacement))
        extnurl = rpurl
    return extnurl


def get_test_data(params, tdata, epoint):
    get_extracted_data = extractedValue(tdata, epoint)
    getPattern = pattern(extnurl=params, exValue=get_extracted_data)
    return getPattern


def saved_response_Data(start_time, vroles, callapis, tdata):
    global status_code

    try:
        status_code = callapis.status_code
        getalljson = json.loads(callapis.content)
        elapsed_time_secs = time.time() - start_time
        time_elapsed = timedelta(seconds=round(elapsed_time_secs))
        log.info(time_elapsed)
        if tdata != '!' and '!' not in tdata:
            if 'rMix' in tdata:
                dp_res_file = mypath / 'test_data' / 'json_data' / 'mixdata'
            else:
                dp_res_file = mypath / 'test_data' / 'json_data' / 'resdata'
            if 'vIdx' in tdata:
                vroles = 'vIdx.json'
            resp_file = dp_res_file / vroles
            dumpData(apiselect=resp_file, getalljson=getalljson)

            # Create Splited Tables with Index
            # dbname = str(vroles).split('.')[0]
            # cgetCreateTables(jsonDatax=getalljson, dbname=dbname, reqres='response')
            # time.sleep(1)
            # Create Splited Tables without Index
            # respdata(jsdata=getalljson, dbname=dbname)

        return status_code, getalljson
    except Exception as e:
        return status_code, 'httpstatus'


def saved_request_Data(payload, vroles, tdata):
    if tdata != '!' and '!' not in tdata:
        if payload != 'None' or payload == '!' and tdata != 'None':
            try:
                gettet = json.loads(payload)
            except Exception:
                gettet = payload
            dp_req_file = mypath / 'test_data' / 'json_data' / 'reqdata' / vroles
            dumpData(apiselect=dp_req_file, getalljson=gettet)

            # Create Splited Tables with Index
            # dbname = str(vroles).split('.')[0]
            # getCreateTables(jsonDatax=gettet, dbname=dbname, reqres='request')
            # time.sleep(1)
            # Create Splited Tables without Index
            # requdata(jsdata=gettet, dbname=dbname)


def get_file_headers(xendpoint, payload, headers):
    files = None
    if xendpoint.split(':')[1] == 'documents':
        headers.pop("Content-Type", None)
        files = payload
        payload = {}
    else:
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
    return files, payload, headers


def extractedValue(tdata, apipoint, ePoint=None, eValue=None, dictdata=None, gnx=0):
    global random_value, value
    getx, gnx, gxa = None, 0, None
    if ePoint is None and dictdata is None:
        if tdata != 'None' and tdata != '':
            eHome, ePoint, apxpoint, eValue = str(tdata).split('|')
            # print(eHome, ePoint, apxpoint, eValue)
            if eValue == '': eValue = None
            if eHome not in ['filterdata', 'mixdata'] and apxpoint == '':
                if ',' in apipoint:
                    xroles = apipoint
                else:
                    xroles = config.get('apiEndpoint', apipoint)
                xroles, cxUrl = xroles.split(',')
            elif eHome not in ['filterdata', 'mixdata'] and apxpoint != '':
                if ',' in apxpoint:
                    xroles = apxpoint
                else:
                    xroles = config.get('apiEndpoint', apxpoint)
                xroles, cxUrl = xroles.split(',')
            else:
                if 'mixdata' in eHome or eHome == 'mixdata':
                    xroles = apxpoint
                else:
                    xroles = apipoint
            vroles = str(xroles) + '.json'
            xrolesjson = mypath / 'test_data' / 'json_data' / eHome / vroles
            dictdata = data_required(xrolesjson)
    if dictdata:
        ePoint = get_nested_multiple_values(data=dictdata, keys=ePoint)
        getx = []
        for getresp in ePoint:
            if type(getresp) is str or type(getresp) is int:
                random_value = str(getresp)
                getx = random_value
                gxa = 'S1'
            elif eValue is None and type(getresp) == list:
                filtered_data = [x for x in getresp if x is not None]
                first_element = filtered_data[0]
                count = filtered_data.index(first_element) + 1
                if count > 0 and gnx == 0 and type(first_element) == list:
                    gnx = random.randint(0, len(first_element) - 1)
                    getx = first_element[gnx]
                else:
                    gnx = random.randint(0, len(filtered_data) - 1)
                    getx = filtered_data[gnx]
                gxa = 'S2'
            else:
                filtered_data = [x for x in getresp if x is not None]
                if filtered_data:
                    random_value = filtered_data
                    # getx.append(random_value)
                    getx = random_value
                    gxa = 'S3'
    return getx, gnx, gxa


def get_data_expected(ddata, apipoint):
    # Use regular expressions to find the string inside the braces
    try:
        if '$' in ddata:
            xid = []
            match = re.findall(r'\$(.*?)\$', ddata)
            gnx = 0
            for variable in match:
                if '|' in variable:
                    dfile, dxt, appoint, gtxa = variable.split('|')
                    if appoint != apipoint and appoint is not None:
                        apipoint = appoint
                    else:
                        apipoint = apipoint
                exresults, gnx, gxa = extractedValue(tdata=variable, apipoint=apipoint, gnx=gnx)
                xid.append(exresults)
                gnx = gnx
            keys, values = xid, match
            for pattern, replacements in zip(values, keys):
                rpurl = ddata.replace('$' + pattern + '$', str(replacements))
                ddata = rpurl
            return ddata
        else:
            if '{}' in ddata:
                return ddata
            else:
                match = re.search(r'{(.*?)}', ddata)
                # pattern = r'\{[^{}]+\}'
                # matching_variables = re.findall(pattern, ddata)
                if match:
                    # Extract the string inside the braces
                    extracted_string = match.group(1)
                    if '|' in extracted_string:
                        dfile, dxt, appoint, gtxa = extracted_string.split('|')
                        if appoint != apipoint and appoint is not None:
                            apipoint = appoint
                        else:
                            apipoint = apipoint
                        # print(dfile,dxt, apipoint, gtxa)
                    # exresults = get_nested_value(data=payload, keys=extracted_string)
                    exresults, gnx, gxa = extractedValue(tdata=extracted_string, apipoint=apipoint)
                    # replaced_string = re.sub(r'{(.*?)}', extracted_string, exresults)
                    replaced_string = ddata.replace(str('{' + extracted_string + '}'), str(exresults))
                    return replaced_string
                else:
                    return ddata
    except Exception as e:
        return str(e)


def get_defined_data(apipoint, ddata):
    # Use regular expressions to find the string inside the braces
    try:
        global dResults, extnurl, gtxa
        if '$' in ddata:
            xid = []
            match = re.findall(r'\$(.*?)\$', ddata)
            gnx = 0
            for variable in match:
                if '|' in variable:
                    dfile, dxt, appoint, gtxa = variable.split('|')
                    if appoint != apipoint and appoint is not None:
                        apipoint = appoint
                    else:
                        apipoint = apipoint
                exresults, gnx, gxa = extractedValue(tdata=variable, apipoint=apipoint, gnx=gnx)
                xid.append(exresults)
                gnx = gnx
            keys, values = xid, match
            for pattern, replacements in zip(values, keys):
                rpurl = ddata.replace('$' + pattern + '$', str(replacements))
                ddata = rpurl
            return ddata
        else:
            match = re.search(r'{(.*?)}', ddata)
            if match:
                extracted_string = match.group(1)
                if '|' in extracted_string:
                    dfile, dxt, appoint, gtxa = extracted_string.split('|')
                    if appoint != apipoint and appoint is not None:
                        apipoint = appoint
                    else:
                        apipoint = apipoint
                    # print(dfile,dxt, apipoint, gtxa)
                exresults, gnx, gxa = extractedValue(tdata=extracted_string, apipoint=apipoint)
                # print(exresults, gnx, gxa)
                if gxa in ['S1', 'S2']:
                    dResults = exresults
                else:
                    if type(exresults) == list:
                        if gtxa == '*':
                            dResults = ','.join(str(item) for item in exresults)
                        else:
                            splgtxa = gtxa.split('*')
                            if splgtxa[1].isdigit():
                                itemsx = random.sample(exresults, int(splgtxa[1]))
                                dResults = ','.join(str(item) for item in itemsx)
                            else:
                                splgtxa = gtxa.split('**')
                                if splgtxa[1].isdigit():
                                    dResults = random.sample(exresults, int(splgtxa[1]))
                                else:
                                    dResults = exresults
                replaced_string = ddata.replace('{' + extracted_string + '}', str(dResults))
                return replaced_string
            else:
                return ddata
    except Exception as e:
        return ddata


def get_entries(apiendpoint):
    if '/' in apiendpoint:
        apoint = str(apiendpoint).split('/')
        apiendpoint = get_defined_data(apipoint=getepoint(apoint), ddata=apiendpoint)
        return apiendpoint, getepoint(apoint)  # apoint[len(apoint) - 1]
    else:
        return apiendpoint, apiendpoint


def getDataSql(sQLx, dbname):
    # Get results using Sqlite3
    sqlx, tbname, query = str(sQLx).split('|')
    global apipoint
    if '_' in dbname:
        xpoint = str(dbname).split('_')
        if len(xpoint) > 2:
            abx = []
            for lex in range(0, 2):
                abx.append(xpoint[lex])
            apipoint = '_'.join(abx)
        else:
            apipoint = str(xpoint[0])
    tbname = apipoint + '_' + tbname
    getresult = engConnect(rindex=tbname, getdata=query, dbname=str(dbname) + '.db')
    return getresult


def get_base_Url(ddata, urlString):
    if urlString:
        match = re.search(r'{(.*?)}', ddata)
        if match:
            extracted_string = match.group(1)
            replaced_string = ddata.replace(str('{' + extracted_string + '}'), str(urlString))
            return replaced_string
    else:
        return ddata