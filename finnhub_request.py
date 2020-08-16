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

    if json == {}:
        return not_found_embed

    name = json2['name']
    
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
    
    embed.add_field(name = 'Current Price', value =f"{round(json['c'], 2)}", inline = False)
    embed.add_field(name = 'Open Price', value =f"{round(json['o'], 2)}", inline = False)
    embed.add_field(name = 'Daily High', value =f"{round(json['h'], 2)}", inline = False)
    embed.add_field(name = 'Daily Low', value =f"{round(json['l'], 2)}", inline = False)

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

    market_cap = '{:,.1f}'.format(json['marketCapitalization']) # formats large numbers with commas for readability
    out_shares = '{:,.0f}'.format(json['shareOutstanding'])

    description = ( f"{json['name']} is a {json['finnhubIndustry'].lower()} company based in {country_name} and listed on {exchange}."
                    f" {json['name']} has a market capitalization of {market_cap} million {json['currency']} with {out_shares} million outstanding shares." 
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
#TODO: react scroll
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
#TODO: react scroll
def get_news_sentiment(symbols): # done
    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = f"Media Sentiment Report"
    )
    
    for symbol in symbols:
        r = requests.get(f'https://finnhub.io/api/v1/news-sentiment?symbol={symbol.upper()}&token={API_KEY}')
        json = r.json()

        r2 = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}') # Get's company name. Makes two API calls, could be removed if needed
        json2 = r2.json()
        
        if json2 == {}:
            embed.add_field(name = f'{symbol.upper()} not found.', value = 'Sorry about that!')
            continue

        name = json2['name']
    
        change = '' # compares article count to average get right comparison word
        last_week = json['buzz']['articlesInLastWeek']
        weekly_average = json['buzz']['weeklyAverage']
        
        if last_week > weekly_average:
            change = 'MORE'
        elif last_week < weekly_average:
            change = 'FEWER'
        elif last_week == weekly_average:
            change = 'the same number of'

        bearbull = '' # compares bear to bull percent to find majority sentiment
        bear_per = json['sentiment']['bearishPercent']
        bull_per = json['sentiment']['bullishPercent']

        if bear_per > bull_per:
            bearbull = 'more BEARISH'
        elif bear_per < bull_per:
            bearbull = 'more BULLISH'
        elif bear_per == bull_per:
            bearbull = 'neither bearish nor bullish'

        if abs(bear_per - bull_per) < 0.05: # if percents are close add slightly
            bearbull = 'slightly ' + bearbull

        embed.add_field(name =  f'{symbol.upper()} ({name})', value = f'{name} had {change} articles in the news last week compaired to their weekly average. '
                                f'({last_week} articles last week vs. {weekly_average} on average.) \n\nOverall, the media seems to be {bearbull} on {name} ({round(bear_per, 2)}% of articles were bearish vs. {round(bull_per, 2)}% being bullish).'
                        )

    return embed

def get_recommendations(symbols): #done
    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = f"Analyst Recommendation Report"
    ) 

    for symbol in symbols:
        r = requests.get(f'https://finnhub.io/api/v1/stock/recommendation?symbol={symbol.upper()}&token={API_KEY}')
        json = r.json()

        r2 = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}') # Get's company name. Makes two API calls, could be removed if needed
        json2 = r2.json()
        
        if json2 == {}:
            embed.add_field(name = f'{symbol.upper()} not found.', value = 'Sorry about that!')
            continue

        name = json2['name'] #TODO: two weeks back

        strong_buy = 0
        buy = 0
        hold = 0
        sell = 0
        strong_sell = 0

        for i in range(14):
            strong_buy += json[i]['strongBuy']
            buy += json[i]['buy']
            hold += json[i]['hold']
            sell += json[i]['sell']
            strong_sell += json[i]['strongSell']
        
        total = strong_buy + buy + hold + sell + strong_sell 

        embed.add_field(name = f'{symbol.upper()} ({name})', value = f'Strong Buy: {round(strong_buy / total * 100, 1)}% \nBuy: {round(buy / total * 100, 1)}% \nHold: {round(hold / total * 100, 1)}% \nSell: {round(sell / total * 100, 1)}% \nStrong Sell: {round(strong_sell / total * 100, 1)}% \n\nTotal Opinions: {total}')
    
    return embed

def get_price_targets(symbols):

    return

def get_earnings(symbols):

    return

def get_covid(states):
    r = requests.get(f'https://finnhub.io/api/v1/covid19/us?token={API_KEY}')
    json = r.json()

    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = "State-by-State COVID-19 Data"
    ) 

    postals = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    for state in states:
        clean_state = ""

        if state.upper().strip() in postals.keys():
            clean_state = postals[state.upper().strip()]
        elif state.title().strip() in postals.values():
            clean_state = state.title().strip()
        else:
            embed.add_field(name = 'State not found.', value = 'Sorry about that!')
            continue

        value = "Couldn't find state in data. This is an issue."

        for i in range(len(json)): # must loop through the JSON response because the format provided is bad
            
            if str(json[i]['state']) == str(clean_state):
                value = 'Confirmed Cases: {0}\nConfirmed Deaths: {1}'.format(json[i]['case'], json[i]['death'])
                continue

        embed.add_field(name = f'{clean_state}', value = value)
    embed.set_footer(text = 'Data from the CDC as of {0}.'.format(json[0]['updated']))

    return embed


#Todo List
#TODO: crypto support
#TODO: technical indicator support
#TODO: add watchlists
#TODO: add charts
#TODO: add price alerts
#TODO: react based scrolling for news 