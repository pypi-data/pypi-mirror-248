from sqlalchemy import create_engine
from pathlib import Path
import sqlite3
import pandas as pd
import ast

mypath = Path.cwd()


def createSQL(dfx, rindex, dbname):
    engine = create_engine('sqlite:///' + str(dbname) + '.db', echo=False)
    dfx.to_sql(rindex, con=engine, if_exists='replace')


def flatten_nested_json_df(df):
    df = df.reset_index()
    # search for columns to explode/flatten
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    # print(f"lists: {list_columns}, dicts: {dict_columns}")
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            # print(f"flattening: {col}")
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)  # inplace

        for col in list_columns:
            # print(f"exploding: {col}")
            # explode lists vertically, adding new columns
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()
    return df


def passValues_index(rIndex, jsdondx, gettype=list):
    if gettype == list:
        df = pd.DataFrame(jsdondx, index=[rIndex]).explode('data')
    else:
        df = pd.DataFrame(jsdondx, index=[rIndex])
    geetdf = flatten_nested_json_df(df)
    return geetdf


def engConnect(rindex, getdata, dbname, where=None):
    global value
    id_value, name_value = None, None
    cnx = sqlite3.connect(mypath / 'test_data' / 'db_data' / dbname)
    cursor = cnx.cursor()
    if where:
        cursor.execute('SELECT "' + str(getdata) + '" FROM ' + str(rindex) + ' WHERE ' + str(where))
    else:
        cursor.execute('SELECT "' + str(getdata) + '" FROM ' + rindex)
    rows = cursor.fetchall()
    for row in rows:
        if type(row[0]) == float or type(row[0]) == int or type(row[0]) == str:
            value = row[0]
        else:
            list_object = ast.literal_eval(row[0])
            # Check if the list_object is a list
            if isinstance(list_object, list):
                # Access the dictionary inside the list
                dict_object = list_object[0]
                # Check if the dict_object is a dictionary
                if isinstance(dict_object, dict):
                    # Access the values inside the dictionary
                    keys = dict_object.keys()
                    values = dict_object.values()
                    value=[]
                    for key, value in zip(keys, values):
                        print(f"Key1: {key}, Value1: {value}")
                        value.append(value)
            else:
                if isinstance(list_object, dict):
                    # Access the values inside the dictionary
                    keys = list_object.keys()
                    values = list_object.values()
                    value = []
                    for key, value in zip(keys, values):
                        print(f"Key2: {key}, Value2: {value}")
                        value.append(value)
    return value


def createTables(jsonf, apiePoint, dbname):
    gettype = None
    dbname = mypath / 'test_data' / 'db_data' / dbname
    df_3 = pd.DataFrame(jsonf)
    gIndex = df_3.index.values
    print('**********SQLite DB Index***********')
    print(dbname, apiePoint, gIndex)
    print('***********************************')
    for xindex in gIndex:
        try:
            if jsonf['data'][xindex]:
                gettype = type(jsonf['data'][xindex])
            else:
                gettype = type(jsonf[xindex])
        except Exception as e:
            print(str(e))
        get_df = passValues_index(rIndex=xindex, jsdondx=jsonf, gettype=gettype)
        deleteTables(apiePoint + '_' + str(xindex), dbname)
        createSQL(get_df, apiePoint + '_' + str(xindex), dbname)


def deleteTables(tabname, dbname):
    try:
        dbname = str(dbname) + '.db'
        cnx = sqlite3.connect(mypath / 'test_data' / 'db_data' / dbname)
        cnx.execute("PRAGMA foreign_keys = ON;")
        cursor = cnx.cursor()
        getx = cursor.execute("DROP TABLE IF EXISTS " + str(tabname))
        # print(getx)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        raise e


def getCreateTables(jsonDatax, dbname, reqres):
    global apipoint
    if '_' in dbname:
        xpoint = str(dbname).split('_')
        if len(xpoint) > 2:
            abx = []
            for lex in range(0, 2):
                abx.append(xpoint[lex])
            apipoint = '_'.join(abx)
        else:
            apipoint = str(reqres)+'_'+str(xpoint[0])

    if 'data' in jsonDatax:
        jsonDatax = jsonDatax
    else:
        jsonDatax = {"data": jsonDatax}
    createTables(jsonDatax, apipoint, dbname=dbname)


def respdata(jsdata, dbname):
    global apipoint
    if '_' in dbname:
        xpoint = str(dbname).split('_')
        if len(xpoint) > 2:
            abx = []
            for lex in range(0, 2):
                abx.append(xpoint[lex])
            apipoint = '_'.join(abx)
        else:
            apipoint = 'response_'+str(xpoint[0])
    dbname = str(dbname)+'.db'
    conn = sqlite3.connect(mypath / 'test_data' / 'db_data' / dbname)
    json_data = jsdata
    # Extract the required data from the JSON
    data = json_data
    # Normalize the JSON data
    df = pd.json_normalize(data)
    df = df.astype(str)
    df.to_sql(apipoint, conn, if_exists='replace', index=False)
    conn.close()


def requdata(jsdata, dbname):
    global apipoint
    if '_' in dbname:
        xpoint = str(dbname).split('_')
        if len(xpoint) > 2:
            abx = []
            for lex in range(0, 2):
                abx.append(xpoint[lex])
            apipoint = '_'.join(abx)
        else:
            apipoint = 'request_'+str(xpoint[0])
    dbname = str(dbname) + '.db'
    conn = sqlite3.connect(mypath / 'test_data' / 'db_data' / dbname)
    json_data = jsdata
    # Convert attributeValues list to a JSON string
    # json_data["attributeValues"] = json.dumps(json_data["attributeValues"])
    df = pd.DataFrame.from_dict(json_data, orient='index').T
    df = df.astype(str)
    df.to_sql(apipoint, conn, if_exists='replace', index=False)
    conn.close()
