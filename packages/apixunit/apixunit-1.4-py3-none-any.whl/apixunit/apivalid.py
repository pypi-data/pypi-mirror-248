import json
import ijson
import datetime
import math
from pathlib import Path
from datetime import timedelta

mypath = Path.cwd()  # .parent
effective_date = datetime.datetime.strftime(datetime.datetime.now(), '%d %b %Y')
expiry_date = (datetime.datetime.now() + timedelta(days=30)).strftime('%d %b %Y')


class Validations:

    def get_vehicle_attribute_details(self, statuscode, expectedresults, data_response, gxdata):
        print(expectedresults, gxdata, data_response)
        try:
            if not statuscode == 500:
                if data_response == 'httpstatus':
                    return str(statuscode)
                else:
                    if type(data_response['data']) == list:
                        datapack = self.get_json_string_results('data.item.' + str(gxdata), data_response)
                        if 'asc' in expectedresults:
                            getresp = self.is_ascending(aList=datapack, atype=gxdata)
                        elif 'desc' in expectedresults:
                            getresp = self.is_descending(dList=datapack, dtype=gxdata)
                        else:
                            getresp = datapack
                        return getresp
                    else:
                        return data_response
            else:
                return data_response['error']
        except Exception:
            if data_response['metadata']:
                messageResponse = self.get_json_string_results('metadata.message', data_response)
                if messageResponse:
                    messageResponse = messageResponse[0]
                else:
                    messageResponse = None
                errorResponse = self.get_json_string_results('metadata.errors', data_response)
                if errorResponse:
                    errorR = errorResponse[0]
                    errorResponse = []
                    for eresp in errorR:
                        if 'field' not in eresp:
                            errorResponse.append(eresp['description'])
                            errorResponse.append(eresp['screen'])
                        elif 'screen' not in eresp:
                            errorResponse.append(eresp['field'])
                            errorResponse.append(eresp['description'])
                        else:
                            if 'screen' and 'field' in eresp:
                                errorResponse.append(eresp['field'])
                                errorResponse.append(eresp['description'])
                                errorResponse.append(eresp['screen'])
                            else:
                                errorResponse.append(eresp['description'])
                else:
                    errorResponse = data_response
                return messageResponse if messageResponse is not None else errorResponse
            else:
                return data_response

    def get_json_string_results(self, gdetails, textjson):
        objects = ijson.items(json.dumps(textjson, indent=4), gdetails)
        columns = list(objects)
        return columns

    def resp_validations(self, id, data_response):
        idx, name, status, compType = None, None, None, None
        for xrespid in sorted(id):
            for yrespid in range(len(data_response['data'])):
                if data_response['data'][yrespid]['id'] == xrespid:
                    idx = data_response['data'][yrespid]['id']
                    name = data_response['data'][yrespid]['name']
                    status = data_response['data'][yrespid]['status']
                    compType = data_response['data'][yrespid]['componentType']
                    break
        return idx, name, status, compType

    @staticmethod
    def is_descending(dList, dtype):
        is_descending = True
        for i in range(1, len(dList)):
            if isinstance(dList[i], str) and isinstance(dList[i - 1], str):
                if dList[i].lower() > dList[i - 1].lower():
                    is_descending = False
                    break
            elif isinstance(dList[i], int) and isinstance(dList[i - 1], int):
                if dList[i] > dList[i - 1]:
                    is_descending = False
                    break
            else:
                raise TypeError("Mixed list contains both strings and integers.")

        if is_descending:
            return dtype + ',desc'
        else:
            return dtype + ',desc is not in descending order'

    @staticmethod
    def is_ascending(aList, atype):
        is_ascending = True
        for i in range(1, len(aList)):
            if isinstance(aList[i], str) and isinstance(aList[i - 1], str):
                if aList[i].lower() < aList[i - 1].lower():
                    is_ascending = False
                    break
            elif isinstance(aList[i], int) and isinstance(aList[i - 1], int):
                if aList[i] < aList[i - 1]:
                    is_ascending = False
                    break
            else:
                raise TypeError("Mixed list contains both strings and integers.")
        if is_ascending:
            return atype + ',asc'
        else:
            return atype + ',asc is not in ascending order'

    def getpageElements(self, data_response):
        page = self.get_json_string_results('metadata.page', data_response)
        size = self.get_json_string_results('metadata.size', data_response)
        total_page = self.get_json_string_results('metadata.totalPage', data_response)
        total_elements = self.get_json_string_results('metadata.totalElements', data_response)
        get_total_page = total_elements[0] / size[0]
        rounded_x = math.ceil(get_total_page / 1) * 1
        if rounded_x == total_page[0]:
            return 'Total page elements are valid'
        else:
            return 'Total page elements are invalid'
