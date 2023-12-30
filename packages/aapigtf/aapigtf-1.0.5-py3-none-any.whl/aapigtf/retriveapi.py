import cdxg
import json
import urllib3
from aapigtf.common import getbaseUrl, dumpData, data_required, getepoint
from aapigtf.apivalid import Validations
from aapigtf.dataextract import get_defined_data
from configparser import ConfigParser
from pathlib import Path

urllib3.disable_warnings()
config = ConfigParser()
mypath = Path.cwd()


class retrivalData(cdxg.TestCase):

    def getRetrieve(self, apixGet, vResjson, burl, xHeaders, extn=None, mix=None):
        for aget in apixGet:
            if extn:
                config.read(mypath / 'utils' / 'endpointapi.ini')
                aget = config.get("pdefinedget", aget)
                aget, cxUrl = aget.split(',')
                config.read(mypath / 'config.ini')
                base_Url = config.get("bURL", 'burl')
                burl = getbaseUrl(ddata=base_Url, urlString=cxUrl)
            params = None
            vResjson = vResjson
            gtx = aget.split('?')
            if '?' in aget:
                apiend, params = gtx
                if '/' in apiend:
                    # ftx, aid = apiend.split('/')
                    # gtname = ftx
                    ftx = apiend.split('/')
                    if len(ftx) == 2:
                        ftx, aid = apiend.split('/')
                        if str(aid).isdigit():
                            gtname = ftx
                        else:
                            gtname = aid
                    else:
                        if str(ftx[len(ftx) - 1]).isdigit():
                            gtname = str(ftx[len(ftx) - 2])
                        else:
                            gtname = str(ftx[len(ftx) - 1])
                else:
                    gtname = apiend
            else:
                apiend = gtx[0]
                gtname = apiend

            if '/' in apiend:
                gtname = getepoint(apiend.split('/'))
                # print(gtname)
            # apiendpoint = burl + '/api/v1.0/' + apiend
            apiendpoint = burl + apiend
            data_response = self.get(apiendpoint, data={}, params=params, verify=False, headers=xHeaders)
            getalljson = json.loads(data_response.content)
            # print(getalljson)
            dfile = str(gtname) + '.json'
            if mix:
                dpfile = mypath / 'test_data' / 'json_data' / 'mixdata' / dfile
            else:
                dpfile = mypath / 'test_data' / 'json_data' / 'filterdata' / dfile
            dumpData(dpfile, getalljson=getalljson)

    def getindvmethod(self, apiendpoint, xHeaders, params=None, methd=None):
        # print(apiendpoint)
        if methd:
            data_response = self.post(apiendpoint, data={}, params=params, verify=False, headers=xHeaders)
        else:
            data_response = self.get(apiendpoint, data={}, params=params, verify=False, headers=xHeaders)
        getalljson = json.loads(data_response.content)
        return getalljson

    def get_mix_data(self, roles, burl, xHeaders, apiept=None, param=None, tdata=None, xtjson=None):
        global apixGet, jplen, jpathxx, gname, exext
        config.read(mypath / 'utils' / 'endpointapi.ini')
        vResjson = mypath / 'test_data' / 'json_data'
        methdx, epoint = str(apiept).split(':')
        if '|' in tdata:
            if '!' in tdata:
                tdata = tdata[1:]
            mixer, jpath, jparam, actn = str(tdata).split('|')
            # print(mixer, jpath, jparam, actn)
            if xtjson is not None and jparam == 'response':
                dfile = str(jpath) + '.json'
                dpfile = mypath / 'test_data' / 'json_data' / mixer / dfile
                dumpData(dpfile, getalljson=xtjson)
                exext = 'NY'
            else:
                apixGet = []
                gname = []
                if ',' in jparam:
                    jplen = str(jparam).split(',')
                    if ',' in jpath:
                        jpathxx = str(jpath).split(',')
                    for jpn in range(0, len(jplen)):
                        if jpath == '':
                            if jplen[jpn].startswith('/') or '/' in jplen[jpn]:
                                jparamLen = str(jplen[jpn]).replace('*', '|')
                                apixGet.append(get_defined_data(apipoint=epoint, ddata=jparamLen))
                            else:
                                if '*' in jplen[jpn]:
                                    jparamLen = str(jplen[jpn]).replace('*', '|')
                                    apixGet.append(get_defined_data(apipoint=epoint, ddata=jparamLen))
                                else:
                                    apixGet.append(epoint + '?' + jplen[jpn])
                            gname.append(epoint)
                        else:
                            jpathx = jpathxx[jpn]
                            if '_' in jpathxx[jpn]:
                                jpath = jpathxx[jpn].split('_')
                                jpathx = jpath[0]

                            if jplen[jpn].startswith('/') or '/' in jplen[jpn]:
                                jparamLen = str(jplen[jpn]).replace('*', '|')
                                apixGet.append(get_defined_data(apipoint=jpathx, ddata=jparamLen))
                            else:
                                if '*' in jplen[jpn]:
                                    jparamLen = str(jplen[jpn]).replace('*', '|')
                                    apixGet.append(get_defined_data(apipoint=epoint, ddata=jparamLen))
                                else:
                                    apixGet.append(jpathx + '?' + jplen[jpn])
                            gname.append(jpathxx[jpn])
                    exext = 'YY'
                else:
                    if jpath == '':
                        jpath = epoint

                    if jparam.startswith('/') or '/' in jparam:
                        jparamLen = str(jparam).replace('*', '|')
                        apixGet.append(get_defined_data(apipoint=jpath, ddata=jparamLen))
                        gname.append(jpath)
                        exext = 'YY'
                    else:
                        if '_' in jpath:
                            gname.append(jpath)
                            exext = 'YY'
                        else:
                            apixGet = [jpath + '?' + jparam]
                            exext = 'NN'

                        if '*' in jparam:
                            jparamLen = str(jparam).replace('*', '|')
                            apixGet.append(get_defined_data(apipoint=jpath, ddata=jparamLen))
        else:
            exext = 'NN'
            if methdx == 'GET':
                apixGet = [epoint + '?' + param]

        if exext == 'NN':
            self.getRetrieve(apixGet, vResjson, burl, xHeaders, mix='Y')
        elif exext == 'YY':
            for yrx in range(0, len(apixGet)):
                # print(apixGet[yrx])
                apiend, params = apixGet[yrx], None
                if '?' in apixGet[yrx]:
                    apiend, params = apixGet[yrx].split('?')
                apiendpoint = burl + apiend
                data_response = self.get(apiendpoint, data={}, params=params, verify=False, headers=xHeaders)
                getalljson = json.loads(data_response.content)
                # print(getalljson)
                dfile = str(gname[yrx]) + '.json'
                dpfile = mypath / 'test_data' / 'json_data' / 'mixdata' / dfile
                dumpData(dpfile, getalljson=getalljson)
        else:
            pass

    def get_data_filter(self, datax=None):
        global x, grx
        config.read(mypath / 'utils' / 'endpointapi.ini')
        if datax:
            getspt = datax.split('|')
            if getspt[0] == 'resdata':
                roles, rolepath = config.get('apiEndpoint', getspt[2]).split(',')
            else:
                roles = str(getspt[2])
            roles = str(roles) + '.json'
            getpth = mypath / 'test_data' / 'json_data' / str(getspt[0]) / roles
            getxr = data_required(datafile=getpth)
            getidx = get_defined_data(apipoint=getspt[2], ddata='{' + datax + '}')
            getjsn = getxr['data']
            if type(getjsn) == list:
                for x in getjsn:
                    if x['id'] == int(getidx):
                        grx = '{' + datax.replace('data.', '') + '}'
                        break
            else:
                grx = '{' + datax + '}'
                x = getjsn
            vroles = getspt[2] + '_mr.json'
            dp_req_file = mypath / 'test_data' / 'json_data' / 'mixdata' / vroles
            dumpData(apiselect=dp_req_file, getalljson=x)
            # return x