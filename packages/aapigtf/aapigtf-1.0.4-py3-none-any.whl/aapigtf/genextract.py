from datetime import timedelta, date, datetime
from aapigtf.dataextract import get_defined_data
from aapigtf.common import getTypesplit, data_required, dumpData, id_generator
from aapigtf.ghelper import update_values_by_keys
import json
from pathlib import Path

mypath = Path.cwd()


def get_vehicle_dict(xType, roles, tdata, apipoint, get_data=None, gtd=None):
    try:
        dpfile = None
        dfile = str(roles) + '.json'
        if xType == '!' or '!' in xType:
            dpfile = mypath / 'test_data' / 'json_data' / 'reqdata' / dfile
            if tdata != 'None' and '|' not in tdata and '!' not in tdata:
                if '**' in tdata:
                    tdata = str(tdata).replace('**', '_' + str(id_generator(5)) + '_' + dateformat()[0])
                tdata = eval(tdata)
                gettetx = update_values_by_keys(dictionary=data_required(datafile=dpfile), key_value_pairs=tdata)
                gettet = json.dumps(gettetx)
            else:
                gettet = json.dumps(data_required(datafile=dpfile))
                if xType.startswith('@!'):
                    xType = xType.replace('@!', '@')
                    get_data = data_required(datafile=dpfile)
                    gettet = get_defined_data(apipoint=apipoint, ddata=xType)
                    gettet = getTypesplit(xType=gettet, get_data=get_data, gtd=gtd, tdata=tdata)
        else:
            if get_data:
                get_data = get_data
            if xType == '@':
                gettet = json.dumps(dict(get_data))
                dpfile = mypath / 'test_data' / 'json_data' / 'reqdata' / dfile
                dumpData(apiselect=dpfile, getalljson=dict(get_data))
            elif xType.startswith('!'):
                if '**' in tdata:
                    tdata = str(tdata).replace('**', '_' + str(id_generator(5)) + '_' + dateformat()[0])
                tdatax = get_defined_data(apipoint=apipoint, ddata=tdata)
                tdatax = eval(tdatax)
                dictdata = str(xType).split('!')[1:]
                gettetx = update_values_by_keys(dictionary=json.loads(dictdata[0]), key_value_pairs=tdatax)
                gettet = json.dumps(gettetx)
            else:
                gettet = get_defined_data(apipoint=apipoint, ddata=xType)
                gettet = getTypesplit(xType=gettet, get_data=get_data, gtd=gtd, tdata=tdata)
        return gettet
    except Exception as e:
        return xType


def dateformat(sdate=None, edate=None):
    end_date_string = None
    today = date.today()
    date_string = today.strftime('%Y-%m-%d')
    if sdate:
        start_date = datetime.strptime(date_string, "%Y-%m-%d")  # convert string to datetime object
        start_date = start_date - timedelta(days=sdate)  # add 30 days
        date_string = start_date.strftime("%Y-%m-%d")  # convert datetime object to string in desired format

    if edate:
        start_date = datetime.strptime(date_string, "%Y-%m-%d")  # convert string to datetime object
        end_date = start_date + timedelta(days=edate)  # add 30 days
        end_date_string = end_date.strftime("%Y-%m-%d")  # convert datetime object to string in desired format
    return date_string, end_date_string


def unixtimedate(dformat):
    # Your input date in string format
    date_string = str(dformat)
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    # Get the Unix timestamp (seconds since January 1, 1970)
    unix_timestamp = date_object.timestamp()
    # Print the Unix timestamp
    return int(unix_timestamp)