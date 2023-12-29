import json
import random
import ijson
import re
import time
import ast
from functools import reduce
from cdxg.utils import genson
from cdxg.logging import log
from aapigtf.apivalid import Validations


def deep_get_imps(data, key: str):
    split_keys = re.split("[\\[\\]]", key)
    out_data = data
    for split_key in split_keys:
        if split_key == "":
            return out_data
        elif isinstance(out_data, dict):
            out_data = out_data.get(split_key)
        elif isinstance(out_data, list):
            try:
                sub = int(split_key)
            except ValueError:
                return None
            else:
                length = len(out_data)
                out_data = out_data[sub] if -length <= sub < length else None
        else:
            return None
    return out_data


def deep_get(dictionary, keys):
    return reduce(deep_get_imps, keys.split("."), dictionary)


def get_api_valid(data, textjson):
    getalx = 0
    spliterx = data
    getdat = spliterx.split('|')
    tjson = 0
    gdata = []
    for xna in getdat:
        gdata.clear()
        if tjson == 0:
            getalx = deep_get(textjson, xna)
            gdata.append(getalx)
        else:
            for xmac in range(0, tjson):
                getalx = deep_get(textjson[xmac], xna)
                gdata.append(getalx)
        getxx = []
        if type(getalx) != int and type(getalx) != dict and type(getalx) != bool and getalx is not None:
            for xlma in range(0, len(getalx)):
                getalxaa = getalx[xlma]
                getxx.append(getalxaa)
            tjson = len(getxx)
            textjson = getxx
    return gdata


def getexpectedresults(gxdata, expectedresults, txjson, gtypes):
    try:
        timeout_start = time.time()
        timeout = 1 * 10
        progress = None
        var_types, test_types, input_types = gtypes
        valid_data = get_api_valid(data=gxdata, textjson=txjson)
        print(valid_data)
        xvalid = valid_data
        schemavalid_all = genson(valid_data)
        while progress is None:
            delta = time.time() - timeout_start
            for xvalid in valid_data:
                schemavalid_indv = genson(xvalid)
                if str(test_types) == 'Json':
                    expectedresults = ast.literal_eval(str(expectedresults))
                    # json.dumps(json.loads(expectedresults), separators=(',', ':'))
                if input_types == 'Data':
                    if str(expectedresults) in str(xvalid):
                        progress = 'set1'
                        break
                    elif str(expectedresults) == str(xvalid):
                        progress = 'set2'
                        break
                    else:
                        progress = None
                elif input_types == 'Schema':
                    if str(expectedresults) == str(schemavalid_indv):
                        progress = 'set1'
                        break
                    elif str(expectedresults) == str(schemavalid_all):
                        progress = 'set2'
                        break
                    else:
                        progress = None
                elif input_types == 'List':
                    progress = 'set3'
                    xvalid = valid_data
                else:
                    if str(expectedresults) not in str(xvalid) or str(expectedresults) != str(xvalid):
                        progress = 'set3'
                        break
                    # elif str(expectedresults) != str(xvalid):
                    #    progress = 'set2'
                    #    break
                    else:
                        progress = None
            if delta >= timeout:
                break
        if progress == 'set1' or progress == 'set2':
            return expectedresults
        elif progress == 'set3':
            return xvalid
        else:
            return 'Expected results given is not Matched :' + str(valid_data)
    except Exception as e:
        return 'Error [No Match]: ' + str(e)


def get_expected_results(gxdata, expectedresults, txjson, gtypes):
    gettextan = str(expectedresults).split('*')
    gtxtna = []
    for expectedresults in gettextan:
        expected_results = getexpectedresults(gxdata=gxdata, expectedresults=expectedresults, txjson=txjson,
                                              gtypes=gtypes)
        gtxtna.append(expected_results)
    return gtxtna


def show_indices(obj, indices):
    for k, v in obj.items() if isinstance(obj, dict) else enumerate(obj):
        if isinstance(v, (dict, list)):
            yield from show_indices(v, indices + [k])
        else:
            yield indices + [k], v


def get_json_details(obj, indices, jsonxx, gdex):
    getxn = []
    for keys, v in show_indices(obj, indices):
        obj = jsonxx
        if len(keys) == len(gdex):
            for key in range(0, len(keys)):
                if type(gdex[key]) == int and type(keys[key]) == int:
                    gdexm = keys[key]
                    obj = obj[gdexm]
                else:
                    gdexm = gdex[key]
                    obj = obj[gdexm]
            getxn.append(obj)
    return getxn


def get_x_results(textjson, expectedresults, gdetails='data-serviceDetails-0-roleDetails-0-name'):
    try:
        gdetx1 = gdetails.split('-')
        lxnn = [int(v) if v.lstrip('-').isnumeric() else v for v in gdetx1]
        gdetx = lxnn
        spliterx = get_json_details(textjson, [], textjson, gdetx)
        print(spliterx)
        return list(set(spliterx))
    except KeyError:
        return 'Key_Not_Found:' + str(expectedresults)
    except Exception as e:
        return str(e)


def jsonbreak(gdetails='data-userInfo-domain-0-code|data-userInfo-domain-0-current'):
    gsplit = gdetails.split('|')
    getan = []
    for xsplit in gsplit:
        gdetx1 = xsplit.split('-')
        lxnn = [int(v) if v.lstrip('-').isnumeric() else v for v in gdetx1]
        getan.append(lxnn)
    return getan


def get_multiple_results(textjson, expected='MAX|True', gdetails='data-userInfo-domain-0-code'):
    try:
        getsplit = jsonbreak(gdetails)
        getan = []
        for xsplit in getsplit:
            spliterx = get_json_details(textjson, [], textjson, xsplit)
            for xam in list(set(spliterx)):
                exsplit = expected.split('*')
                for esplit in exsplit:
                    if str(xam) == str(esplit):
                        getan.append(xam)
        return list(set(getan))
    except KeyError:
        return 'Key_Not_Found:' + str(expected)
    except Exception as e:
        return str(e)


def get_json_string_results(gdetails, textjson):
    # data = ijson.parse(json.dumps(textjson, indent=4))
    # for prefix, event, value in data:
    #    print('prefix=', prefix, 'event=', event, 'value=', value)
    objects = ijson.items(json.dumps(textjson, indent=4), gdetails)
    columns = list(objects)
    return columns


def get_multiple_results_list(txjson, expectedresults, gxdata, testtypes):
    # try:
    getresultsxx = get_json_string_results(gxdata, txjson)
    getresults = ast.literal_eval(str(getresultsxx))
    if testtypes == 'Json':
        print(expectedresults)
        expectedresults = json.loads(expectedresults)
        print(expectedresults)
    exresults = ast.literal_eval(str(expectedresults))
    print(exresults)
    if not getresults:
        getxln = 'Invalid'
    else:
        if getresults == exresults:
            getxln = 'Valid'
            # print('PASS : Actual equals expected')
        else:
            gbn = None
            eResults = exresults
            getxln = []
            for gres in getresults:
                # print(gres)
                for i in range(0, len(eResults)):
                    if eResults[i] == gres:
                        # print(gres, eResults[i])
                        gbn = 'Valid'
                        break
                    elif eResults[i] == gres[i]:
                        # print(gres[i], eResults[i])
                        gbn = 'Valid'
                        break
                    else:
                        gbn = 'Invalid'
                getxln.append(gbn)
    print(getxln)
    if 'Invalid' in list(set(getxln)) or getxln == 'Invalid':
        return 'Invalid'
    else:
        return 'Valid'


# except Exception as e:
#    return str(e)


def get_multiple_results_string(txjson, expectedresults, gxdata, gtypes):
    global getexpected, getsplit
    vartypes, testtypes, inputtypes = gtypes
    try:
        if '\xa0' in expectedresults:
            expectedresults = expectedresults.replace('\xa0', ' ')
            log.info('Removed backspaces : ' + str(expectedresults))

        if inputtypes == 'List':
            print(txjson, expectedresults, gxdata)
            datax = get_multiple_results_list(txjson, expectedresults, gxdata, testtypes)
            log.info(datax)
        else:
            getan, xtn, getsplit = [], None, None
            getspliter = gxdata.split('|')
            for xlen in range(0, len(getspliter)):
                getsplit = get_json_string_results(getspliter[xlen], txjson)
                log.info(getsplit)
                log.info(expectedresults)
                if testtypes == 'Json':
                    expectedresults = json.loads(expectedresults)
                else:
                    if not getsplit:
                        getan = 'Invalid'
                        break
                    else:
                        if len(getspliter) == 1:
                            try:
                                getexpected = ast.literal_eval(str(expectedresults))
                            except Exception as e:
                                getexpected = expectedresults
                            if getsplit == getexpected:
                                getan = 'Valid'
                            elif getexpected in getsplit:
                                getan = 'Valid'
                            else:
                                if '*' not in getexpected:
                                    gtnx = []
                                    for xan in getsplit:
                                        if xan in getexpected and xan != '':
                                            xtn = 'Valid'
                                            gtnx.append(xtn)
                                        else:
                                            xtn = 'Invalid'
                                            gtnx.append(xtn)
                                    if 'Valid' in gtnx:
                                        getan.append('Valid')
                                    else:
                                        getan.append('Invalid')
                                else:
                                    getexpected = str(getexpected).split('*')
                                    for est in range(0, len(getexpected)):
                                        if str(getexpected[est]) in getsplit:
                                            xtn = 'Valid'
                                            getan.append(xtn)
                                        else:
                                            xtn = 'Invalid'
                                            getan.append(xtn)
                        else:
                            exsplit = str(expectedresults).split('*')
                            try:
                                getexpected = ast.literal_eval(str(exsplit[xlen]))
                            except Exception as e:
                                getexpected = exsplit[xlen]
                            if getsplit == getexpected:
                                xtn = 'Valid'
                            elif getexpected in getsplit:
                                xtn = 'Valid'
                            else:
                                for xsplit in getsplit:
                                    if str(xsplit) == str(exsplit[xlen]):
                                        xtn = 'Valid'
                                        break
                                    elif str(exsplit[xlen]) in str(xsplit):
                                        xtn = 'Valid'
                                        break
                                    else:
                                        xtn = 'Invalid'
                            getan.append(xtn)
            if getsplit == [] or getsplit is None:
                datax = 'Invalid'
            else:
                datax = list(set(getan))
        if inputtypes is not None:
            if 'Valid' in datax and 'Invalid' in datax or 'Invalid' in datax:
                return 'No Match Found'
            else:
                return 'Match Found'
    except Exception as e:
        if str(e) == "argument of type 'int' is not iterable":
            num = []
            if type(getexpected) == list:
                for number in getexpected:
                    number_str = str(number)
                    print(number_str)
                    if int(number_str) in getsplit:
                        num.append('Valid')
                    else: num.append('Invalid')
            else:
                if getexpected in getsplit:
                    num.append('Valid')
                else:
                    num.append('Invalid')
            if 'Valid' in num and 'Invalid' in num or 'Invalid' in num:
                return 'No Match Found'
            else:
                return 'Match Found'
        else:
            return str(e)


def specific_key(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    # return values
    to_return = []
    for val in values:
        if type(val) == list:
            for item in val:
                to_return.append(item)
        else:
            to_return.append(val)
    return to_return


def get_specific_keys(gxdata, expectedresults, txjson, gtypes):
    gettextan = str(gxdata).split('*')
    gtxtna = []
    for gxdtn in gettextan:
        expected_results = getexpectedresults(gxdata=gxdtn, expectedresults=expectedresults, txjson=txjson,
                                              gtypes=gtypes)
        gtxtna.append(expected_results)
    return gtxtna


def paramReplace(xparams, strjson):
    string = None
    pairs = xparams.split('&')
    for pair in pairs:
        variable, value = pair.split('=')
        replacements = get_json_string_results(value, strjson)
        replacements = random.choice(replacements)
        string = xparams.replace(pair, f"{variable}={replacements}")
    return string


def api_valid(gxdata, expectedresults, txjson, gtypes, var_types, statuscode=None):
    if var_types == 'ST1':
        getresults = get_expected_results(gxdata=gxdata, expectedresults=expectedresults, txjson=txjson,
                                          gtypes=gtypes)
    elif var_types == 'ST3':
        getresults = get_multiple_results(textjson=txjson, expected=expectedresults, gdetails=gxdata)
    elif var_types == 'ST4':
        getresults = get_multiple_results_string(gxdata=gxdata, expectedresults=expectedresults, txjson=txjson,
                                                 gtypes=gtypes)
    elif var_types == 'ST5':
        getresults = Validations().get_vehicle_attribute_details(statuscode=statuscode, expectedresults=expectedresults,
                                                                 data_response=txjson, gxdata=gxdata)
    else:
        # getresults = get_results(textjson=txjson, expectedresults=expectedresults, gdetails=gxdata)
        getresults = Validations().getpageElements(data_response=txjson)
    return getresults
