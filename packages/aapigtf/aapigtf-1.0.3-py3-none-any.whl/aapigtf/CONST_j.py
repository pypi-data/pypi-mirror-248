import json


class CONST:
    try:
        json_file = open('Env.json')
        json_data = json.load(json_file)
        EXCELPATH = json_data['EXCELPATH']
        URL = json_data['URL']
        CHROMEDRIVERPATH = json_data['CHROMEDRIVERPATH']
        IEDRIVERPATH = json_data['IEDRIVERPATH']
        TESTREPORTPATH = json_data['TESTREPORTPATH']
    except Exception as msg:
        print(msg)


