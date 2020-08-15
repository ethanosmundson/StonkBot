import requests
import shared
import math

RESOLUTIONS = ['1', '5', '15', '30', '60', 'D', 'W', 'M']
API_KEY = shared.config['finnhub']['token']

def get_quote(symbol): #TODO: add company name using Company Profile
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol.upper()}&token={API_KEY}')
    json = r.json()

    if json == {}:
        return "Stock symbol not found."
    else:
        message = f"```Price information for {symbol.upper()}: \n Current Price: {json['c']} \n Open Price: {json['o']} \n Daily High: {json['h']} \n Daily Low: {json['l']} \n```"
    
    return message

def get_financials(symbol):
    r = requests.get(f'https://finnhub.io/api/v1/stock/metric?symbol={symbol.upper()}&metric=all&token={API_KEY}')
    json = r.json()
    
    if json['metric'] == {}:
        return "Stock symbol not found."
    else:
        l1 = f"```Financials for {symbol.upper()}:\n  52 Week High: {json['metric']['52WeekHigh']} on {json['metric']['52WeekHighDate']}\n  52 Week Low: {json['metric']['52WeekLow']} on {json['metric']['52WeekLowDate']}\n\n"
        l2 = f"  Price to Book Quarterly: {json['metric']['pbQuarterly']}\n  Price to Book Annual: {json['metric']['pbAnnual']}\n\n  P/E: {json['metric']['peExclExtraTTM']}\n\n"
        l3 = f"  Normalized EPS Annual: {json['metric']['epsNormalizedAnnual']}\n  3-Year EPS Growth: {json['metric']['epsGrowth3Y']}\n  5-Year EPS Growth: {json['metric']['epsGrowth5Y']}\n\n  Quick Ratio Quarterly: {json['metric']['quickRatioQuarterly']}\n  Quick Ratio Annual: {json['metric']['quickRatioAnnual']}\n\n"
        l4 = f"  Return on Investment Annual: {json['metric']['roiAnnual']}\n  Return on Investment 5-Year: {json['metric']['roi5Y']}\n\n  Debt/Equity Annual: {json['metric']['totalDebt/totalEquityAnnual']}\n  Debt/Equity Quarterly: {json['metric']['totalDebt/totalEquityQuarterly']}```"

    return l1 + l2 + l3 + l4

def get_company_info(symbol):
    r = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol.upper()}&token={API_KEY}')
    json = r.json()
    
    if json == {}:
         return "Stock symbol not found."

    location = json['country']
    if location == 'US': # fixes awkward grammar
        location = 'the United States'

    message = f"{json['name']} is a {json['finnhubIndustry'].lower()} company based in {location}. {json['name']} has a market capitalization of {json['marketCapitalization']} million {json['currency']} with {math.trunc(json['shareOutstanding'])} outstanding shares. The company went public on {json['ipo']} and has the ticker symbol {json['ticker']}. More information can be found at {json['weburl']}."
    return message

def get_company_news(symbol):

    return

def get_market_headlines(symbol):

    return

def get_news_sentiment(symbol):

    return

def get_recommendations(symbol):

    return 

def get_price_targets(symbol):

    return

def get_earnings(symbol):

    return

def get_covid(symbol):

    return

#TODO: crypto support