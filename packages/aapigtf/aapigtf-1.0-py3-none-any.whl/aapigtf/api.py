import cdxg
import time
from apixunit.apivalidation import api_valid
from apixunit.genextract import get_vehicle_dict
from apixunit.retriveapi import retrivalData
from datetime import timedelta
from cdxg.logging import log
from cdxg import Cdxg
import traceback, json
from apixunit.dataextract import get_defined_data, get_entries, get_base_Url, saved_request_Data, \
    saved_response_Data, get_file_headers, get_test_data, get_data_expected
from apixunit.common import getcURL, get_results


class apicall(cdxg.TestCase):

    def apicall(self, testcase, apiendpoint, xmethod, payload, params, tdata, headers, exresults, schemavar, gtypes,
                xlcreate, roles, sprints, incidentids, cxUrl):
        global getalljson, gettet, sparams, callapis, getendpoint
        var_types, test_types, input_types = gtypes
        status_code = 000
        apiendpoint, xendpoint = get_entries(apiendpoint)
        getpointapi = apiendpoint
        xendpoint = xmethod + ':' + xendpoint
        base_Url = f'{Cdxg.base_url}'  # config.get('bURL', burl) #
        self.baseUrl = get_base_Url(ddata=base_Url, urlString=cxUrl)
        apiendpoint = self.baseUrl + apiendpoint
        print('###################---API[' + str(xendpoint) + ']---############################')
        vroles = str(roles) + '.json'
        retData = retrivalData()
        try:
            if 'mixdata' in tdata and '*X' not in tdata:
                # log.info('*****MixData*****')
                retData.get_mix_data(roles, self.baseUrl, headers, apiept=xendpoint, param=params, tdata=tdata)

            if tdata.startswith('^'):
                # log.info('***Generated data in mixed folder***')
                retData.get_data_filter(datax=str(tdata).split('^')[1])
                apiendpoint = get_entries(apiendpoint)[0]

            if tdata != 'None' and '@' in tdata:
                tdatax = str(tdata).split('@')[1:][0]
                params = get_test_data(params=params, tdata=tdatax, epoint=str(xendpoint).split(':')[1])

            params = get_defined_data(apipoint=str(xendpoint).split(':')[1], ddata=params)
            if params != 'None' and params.startswith('/') and params is not None:
                if '*' in params:
                    sparams, params = str(params).split('*')
                else:
                    sparams = params
                apiendpoint = apiendpoint + sparams
                xendpoint = xendpoint + sparams
            start_time = time.time()
            if xmethod == 'GET':
                callapis = self.get(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'POST':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                files, payload, headers = get_file_headers(xendpoint, payload, headers)
                start_time = time.time()
                callapis = self.post(apiendpoint, data=payload, params=params, verify=False, headers=headers,
                                     files=files)

            if xmethod == 'PUT':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                start_time = time.time()
                callapis = self.put(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'PATCH':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                start_time = time.time()
                callapis = self.patch(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'DELETE':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                start_time = time.time()
                callapis = self.delete(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if 'documents' in xendpoint:
                log.info(getcURL(xmethod, apiendpoint, payload, params))
            else:
                log.info(self.curl())
            end_time = time.time() - start_time
            etime = timedelta(seconds=end_time).total_seconds()
            elapsed_time = averagebuy = "{0:.2f}".format(float(etime))
            log.info(elapsed_time)
            status_code, getalljson = saved_response_Data(start_time, vroles, callapis, tdata)
            saved_request_Data(payload, vroles, tdata)
            try:
                gettet = json.loads(payload)
            except Exception as e:
                gettet = payload

            if '/' in xendpoint:
                xpoint = str(xendpoint).split('/')
                xendpoint = xpoint[0]
            exresults = get_data_expected(exresults, str(xendpoint).split(':')[1])

            kwords = ['mixdata', 'resdata', 'reqdata']
            kfound = any(keyword in tdata for keyword in kwords)
            if kfound and '*X' in tdata:
                # log.info('*****Stored as response data to re-use*****')
                retData.get_mix_data(roles, self.baseUrl, headers, apiept=xendpoint, param=params, tdata=tdata,
                                     xtjson=getalljson)

            getresults = api_valid(gxdata=schemavar, expectedresults=exresults, txjson=getalljson,
                                   gtypes=gtypes, var_types=var_types, statuscode=status_code)
            getendpoint = str(xendpoint).split(':')[0] + ':' + getpointapi
            return status_code, getresults, getendpoint, payload, exresults, params, elapsed_time, getalljson
        except Exception as e:
            time_elapsed = 0.00  # timedelta(seconds=round(elapsed_time_secs))
            getendpoint = str(xendpoint).split(':')[0] + ':' + getpointapi
            get_results(xlcreate, roles, testcase, getendpoint, payload, params, exresults, 'ScriptError:' + str(e),
                        results='FAILED', fontx='FC2C03', httpcodes=status_code,
                        elapsed_secs=time_elapsed, comments=schemavar, sprints=sprints, incidentids=incidentids,
                        alljson=traceback.print_exc())