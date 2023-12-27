from apixunit.api import apicall
from apixunit.results_validate import Results
from apixunit.common import Create_New_Report, getepoint
from configparser import ConfigParser
from pathlib import Path

mypath = Path.cwd()
config = ConfigParser()


class apiSteps:

    def execute_steps(self, getall, reportpath, xHeaders):
        try:
            testcase, xendpoint, xmethod, payload, params, testdata, exresults, scvarib, ctype, results, sprints, \
                exestp = getall
            incidentids = ''
            config.read(mypath / 'utils' / 'endpointapi.ini')
            if '/' in xendpoint:
                xpoint = str(xendpoint).split('/')
                rolepoint = getepoint(xpoint)  # xpoint[len(xpoint)-1]
            else:
                rolepoint = xendpoint
            roles = config.get('apiEndpoint', rolepoint)
            if ',' in roles:
                roles, cxUrl = roles.split(',')
            else:
                cxUrl = None
            if '**' in xendpoint:
                xpoint = str(xendpoint).split('**')
                xendpoint = xpoint[0]
            gettypes = str(ctype).split('|')
            var_types, test_types, input_types = gettypes
            statuscode, getrespn, xendpoint, payload, exresults, params, elapsed_time, alljson = \
                apicall().apicall(testcase, xendpoint, xmethod, payload, params, testdata, xHeaders, exresults, scvarib,
                                  gettypes, reportpath, roles, sprints, incidentids, cxUrl)
            # print(statuscode, getrespn, xendpoint, payload, exresults, params)
            if getrespn is not None and getrespn != 'Skipped' and exestp is not None:
                case = 'Positive'
                Results().resultsvalidations(testcase=testcase, getresults=getrespn, test_types=test_types,
                                             var_types=var_types, input_types=input_types, exresults=exresults,
                                             case=case, results=results, xlcreate=reportpath, tepoint=xendpoint,
                                             tpload=payload, tparams=params, comments=scvarib, roles=roles,
                                             httpcodes=statuscode, timeelapsed=elapsed_time, sprints=sprints,
                                             incidentids=incidentids, alljson=alljson)
        except Exception as e:
            raise e