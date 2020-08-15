import requests
import shared
import math
import pycountry as p
import time
import datetime
from datetime import date, timedelta
import discord

API_KEY = shared.config['finnhub']['token']

not_found_embed = discord.Embed( # default embed to be returned when symbol not found
    color = discord.Color.blurple(),
    title = "Stock symbol not found.")

def get_quote(symbol): # done
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol.upper()}&token={API_KEY}')
    json = r.json()

    r2 = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}') # Gets company name. Makes two API calls, could be removed if needed
    json2 = r2.json()

    name = json2['name']

    if json == {}:
        return not_found_embed
    
    if json['c'] > json['o']: # sets embed color based on price 
        price_color = discord.Color.green()
    elif json['c'] < json['o']:
        price_color = discord.Color.red()
    elif json['c'] == json['o']:
        price_color = discord.Color.light_grey()

    embed = discord.Embed(
        color = price_color,
        title = f"Price Information for {symbol.upper()} ({name})"
    )
    
    embed.add_field(name = 'Current Price', value =f"{json['c']}", inline = False)
    embed.add_field(name = 'Open Price', value =f"{json['o']}", inline = False)
    embed.add_field(name = 'Daily High', value =f"{json['h']}", inline = False)
    embed.add_field(name = 'Daily Low', value =f"{json['l']}", inline = False)
    
    return embed

def get_financials(symbol): # done
    r = requests.get(f'https://finnhub.io/api/v1/stock/metric?symbol={symbol.upper()}&metric=all&token={API_KEY}')
    json = r.json()
    
    if json['metric'] == {}:
        return not_found_embed
    
    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = f"Financials for {symbol.upper()}"
    )

    embed.add_field(name = '52 Week High', value =f"{json['metric']['52WeekHigh']} on {json['metric']['52WeekHighDate']}", inline = False)
    embed.add_field(name = '52 Week Low', value =f"{json['metric']['52WeekLow']} on {json['metric']['52WeekLowDate']}", inline = False)
    embed.add_field(name = 'Price to Book (Quarterly)', value =f"{json['metric']['pbQuarterly']}", inline = False)
    embed.add_field(name = 'Price to Book (Annual)', value =f"{json['metric']['pbAnnual']}", inline = False)
    embed.add_field(name = 'P/E', value =f"{json['metric']['peExclExtraTTM']}", inline = False)
    embed.add_field(name = 'Normalized EPS (Annual)', value =f"{json['metric']['epsNormalizedAnnual']}", inline = False)
    # commented are optional parameters
    # embed.add_field(name = '3-Year EPS Growth', value =f"{json['metric']['epsGrowth3Y']}", inline = False)
    # embed.add_field(name = '5-Year EPS Growth', value =f"{json['metric']['epsGrowth5Y']}", inline = False)
    # embed.add_field(name = 'Quick Ratio (Quarterly)', value =f"{json['metric']['quickRatioQuarterly']}", inline = False)
    embed.add_field(name = 'Quick Ratio (Annual)', value =f"{json['metric']['quickRatioAnnual']}", inline = False)
    embed.add_field(name = 'Return on Investment (Annual)', value =f"{json['metric']['roiAnnual']}", inline = False)
    # embed.add_field(name = 'Return on Investment (5-Year)', value =f"{json['metric']['roi5Y']}", inline = False)
    embed.add_field(name = 'Debt/Equity (Annual)', value =f"{json['metric']['totalDebt/totalEquityAnnual']}", inline = False)
    # embed.add_field(name = 'Debt/Equity (Quarterly)', value =f"{json['metric']['totalDebt/totalEquityQuarterly']}", inline = False)

    return embed

def get_company_info(symbol): # done
    r = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}')
    json = r.json()
    
    print(json)

    if json == {}:
        return not_found_embed

    country_code = json['country']
    country = p.countries.get(alpha_2 = country_code)
    country_name = country.name

    if country_name == 'United States': # fixes awkward grammar, may need to add more countries
        country_name = 'the United States'

    exchange = json['exchange'].title()
    
    if exchange == 'New York Stock Exchange, Inc.': # may need to add other exchanges here
        exchange = 'the New York Stock Exchange'
    elif exchange == 'Nasdaq Nms - Global Market':
        exchange = 'the Nasdaq'

    time_obj = time.strptime(json['ipo'], '%Y-%m-%d') # convert YYY-MM-DD to nicer format
    day = time.strftime('%B %d, %Y', time_obj)

    embed = discord.Embed(
        color = discord.Color.blurple(),
    )

    description = ( f"{json['name']} is a {json['finnhubIndustry'].lower()} company based in {country_name} and is listed on {exchange}."
                    f" {json['name']} has a market capitalization of {round(json['marketCapitalization'] ,1)} million {json['currency']} with {math.trunc(json['shareOutstanding'])} million outstanding shares." 
                    f" The company went public on {day} and has the ticker symbol {json['ticker']}. More information can be found at {json['weburl']}.")
    
    embed.add_field(name = f"{json['name']} ({json['ticker']})", value = description)
                
    return embed

def get_company_news(symbol): # done
    today = date.today()
    start_date = str(today.strftime("%Y-%m-%d"))
    end_date = str((today - timedelta(days = 1)).strftime("%Y-%m-%d")) # this is messy

    r = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={symbol.upper()}&from={end_date}&to={start_date}&token={API_KEY}')
    json = r.json()

    if json == []:
        return not_found_embed

    if len(json) < 3:
        length = len(json)
    else:
        length = 3

    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = "{0} News for {1}".format(symbol.upper(), date.fromtimestamp(json[0]['datetime']).strftime("%A, %B %d, %Y"))
    )
    
    for i in range(length):
        embed.add_field(name = json[i]['headline'], value = json[i]['summary'] + '\n' + json[i]['url'] + '\n', inline=False)
    
    return embed

def get_market_headlines(): # done
    r = requests.get(f'https://finnhub.io/api/v1/news?category=general&token={API_KEY}')
    json = r.json()

    if len(json) < 3:
        length = len(json)
    else:
        length = 3

    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = "Top Market News for {0}".format(date.fromtimestamp(json[0]['datetime']).strftime("%A, %B %d, %Y"))
    )

    for i in range(length):
        embed.add_field(name = json[i]['headline'], value = json[i]['summary'] + '\n' + json[i]['url'] + '\n', inline=False)
    
    return embed

def get_news_sentiment(*symbols):
    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = f"Media Sentiment Report"
    )
    
    for symbol in symbols):
        print(symbol)
        r = requests.get(f'https://finnhub.io/api/v1/news-sentiment?symbol={symbol.upper()}&token={API_KEY}')
        json = r.json()

        r2 = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}') # Get's company name. Makes two API calls, could be removed if needed
        json2 = r2.json()

        name = json2['name']
    
        change = '' # compares article count to average get right comparison word
        last_week = json['buzz']['articlesInLastWeek']
        weekly_average = json['buzz']['weeklyAverage']
        
        if last_week > weekly_average:
            change = 'more'
        elif last_week < weekly_average:
            change = 'fewer'
        elif last_week == weekly_average:
            change = 'the same number of'

        bearbull = '' # compares bear to bull percent to find majority sentiment
        bear_per = json['sentiment']['bearishPercent']
        bull_per = json['sentiment']['bullishPercent']

        if bear_per > bull_per:
            bearbull = 'more bearish'
        elif bear_per < bull_per:
            bearbull = 'more bearish'
        elif bear_per == bull_per:
            bearbull = 'neither bearish nor bullish'

        if math.abs(bear_per - bull_per) < 0.05: # if percents are close add slightly
            bearbull = 'slightly ' + bearbull

        embed.add_field(name = f'{symbol.upper()} ({name})', value = f'{name} had {change} articles in the news last week compaired to their weekly average.'
                             f'({last_week} articles last week vs. an average of {weekly_average}.) Overall, the media seems to be {bearbull} on {name} ({bear_per}% of articles were bearish vs. {bull_per} being bullish).'
                        )

    return embed

def get_recommendations(symbol):

    return 

def get_price_targets(symbol):

    return

def get_earnings(symbol):

    return

def get_covid(symbol):

    return

#TODO: crypto support