""""
Use Finnhub.io candle data and format it for use
with QuickChart.io API. This will return an image.
"""
import requests
import shared
import datetime
from datetime import date, timedelta, datetime
import time
import math
import discord 
from quickchart import QuickChart




import yaml

with open ('config.yaml') as file: # loading config yaml file
    try:
        config = yaml.safe_load(file)
        for key, value in config.items():
            shared.config[key] = value
    except yaml.YAMLError as e: # yaml failed to load
        print(e)
        sys.exit(1)




invalid_embed = discord.Embed( # default embed to be returned when symbol not found
    color = discord.Color.blurple(),
    )
invalid_embed.add_field(name = 'No data for that timeframe.', value = 'Sorry about that!')
    
API_KEY = shared.config['finnhub']['token']
RES = ['1', '5', '15', '30', '60', 'D', 'W', 'M']

def add_dollar(value):
    return ('$' + str(value))

def get_chart(symbol, period):
    start = math.trunc(time.time())
    
    stop = 0.0
    resoultion = ''
    res_long = ''
    step = 60

    if period.upper().strip() == 'D':
        stop = math.trunc(time.time() - (86400 * 1))
        resolution = '1'
        res_long = 'Day'
        step = 60 * 1
    elif period.upper().strip() == 'W':
        stop = math.trunc(time.time() - (86400 * 7))
        resolution = '5'
        res_long = 'Week'
        step = 60 * 5 
    elif period.upper().strip() == 'M':
        stop = math.trunc(time.time() - (86400 * 30))
        resolution = '30'
        res_long = 'Month'
        step = 60 * 30
    elif period.upper().strip() == 'Y':
        stop = math.trunc(time.time() - (86400 * 365))
        resolution = 'D'
        res_long = 'Year'
        step = 60 * 1440
    else:
        print('Invalid period.')

    r = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol={symbol.upper()}&resolution={resolution}&from={stop}&to={start}&token={API_KEY}')
    json = r.json()

    if json == {'s': 'no_data'} or json['s'] == 'no_data':
        print('No data!')
        return invalid_embed

    r2 = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}') # Gets company name. Makes two API calls, could be removed if needed
    json2 = r2.json()

    name = json2['name']

    data = json['c']
    
    lables = [time.strftime('%b %d %H:%M',datetime.fromtimestamp(i).timetuple()) for i in json['t']] #TODO: format nicer
    # print(stop - start)
    # print(len(lables))
    # print(len(data))
    # print(lables)

    qc = QuickChart()
    qc.width = 700
    qc.height = 500
    qc.device_pixel_ratio = 1.0
    qc.background_color = '#ffffff'
    qc.config = {
        "type": "line",
        "data": {
            "labels": lables,
            "datasets": [{
                "data": data,
                "fill": "false",
                "spanGaps": "true",
                "pointRadius": 0,
                "pointBorderColor": '#000000',
                "showLine": "true",
                "borderWidth": 2.5,
                "borderColor": '#000000'
            }]
        },
        "options": {
            "title":{
                "display": "true",
                "text": f"{symbol.upper()} ({name}) {res_long} Price Chart",
                "fontSize": 16,
                "fontFamily": "Helvetica",
                "fontColor": '#000000'
            },
            "legend": {
                "display": 'false',
            },
            "scales": {
                "xAxes": [{
                    "scaleLabel":{
                        "display": 'true',
                        "labelString": 'Date'
                        },
                }],
                "yAxes": [{
                    "scaleLabel":{
                        "display": 'true',
                        "labelString": 'US Dollars'
                        },
                    "ticks": {
                        "suggestedMin": .95 * min(data), #TODO: more even 
                        "suggestedMax": 1.05 * max(data)
                    },
                }]
            }
        }
    }

    print(qc.get_short_url())

get_chart('lpcn', 'm')