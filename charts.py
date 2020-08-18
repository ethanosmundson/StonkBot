import requests
import shared
import datetime
from datetime import date, timedelta, datetime
import time
import math
import discord 
from quickchart import QuickChart
    
API_KEY = shared.config['finnhub']['token']

def get_chart(symbol, duration):
    """Fetches Finnhub candle data and creates a chart using QuickChart.io API"""
    start = math.trunc(time.time())
    
    stop = 0.0
    resoultion = ''
    res_long = ''
    step = 60

    if duration.lower().strip() == 'd': # sets some variables to be used later based on chart duration
        stop = math.trunc(time.time() - (86400 * 1))
        resolution = '1'
        res_long = 'Day'
        step = 60 * 1
    elif duration.lower().strip() == 'w':
        stop = math.trunc(time.time() - (86400 * 7))
        resolution = '5'
        res_long = 'Week'
        step = 60 * 5 
    elif duration.lower().strip() == 'm':
        stop = math.trunc(time.time() - (86400 * 30))
        resolution = '30'
        res_long = 'Month'
        step = 60 * 30
    elif duration.lower().strip() == 'y':
        stop = math.trunc(time.time() - (86400 * 365))
        resolution = 'D'
        res_long = 'Year'
        step = 60 * 1440
    else:
        return 'invalid_duration'

    r = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={symbol.upper()}&resolution={resolution}&from={stop-86400}&to={start-86400}&token={API_KEY}')
    json = r.json()

    # print(json) FIX THIS
    # print(datetime.datetime.today().weekday())
    #Test this over a weekend

    if json == {'s': 'no_data'} or json['s'] == 'no_data':
        if datetime.datetime.today().weekday() >= 5:
            return 'invalid_weekend'
        else:
            return 'invalid_symbol'


    r2 = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}') # Gets company name. Makes two API calls, could be removed if needed
    json2 = r2.json()

    name = json2['name']

    data = json['c'] # stock price (close) data 
    
    lables = [time.strftime('%b %d %H:%M', datetime.fromtimestamp(i).timetuple()) for i in json['t']] # lables for x axis

    qc = QuickChart() 
    qc.width = 700
    qc.height = 500
    qc.device_pixel_ratio = 1.0
    qc.background_color = '#ffffff'
    qc.config = { # configuration data for chart formatting. See https://www.chartjs.org/.
        "type": "line",
        "data": {
            "labels": lables,
            "datasets": [{
                "data": data,
                "fill": "false",
                "spanGaps": True,
                "pointRadius": 0,
                "showLine": True,
                "borderWidth": 2.5,
                "borderColor": "#000000"
            }]
        },
        "options": {
            "title":{
                "display": True,
                "text": f"{symbol.upper()} ({name}) {res_long} Price Chart",
                "fontSize": 18,
                "fontFamily": "Helvetica",
                "fontColor": "#000000"
            },
            "legend": {
                "display": False,
            },
            "scales": {
                "xAxes": [{
                    "scaleLabel":{
                        "display": True,
                        "labelString": "Date"
                        },
                }],
                "yAxes": [{
                    "scaleLabel":{
                        "display": True,
                        "labelString": "US Dollars"
                        },
                    "ticks": {
                        "suggestedMin": .95 * min(data),
                        "suggestedMax": 1.05 * max(data)
                    },
                }]
            }
        }
    }

    return qc.get_short_url()
