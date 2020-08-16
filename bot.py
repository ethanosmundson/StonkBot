import os
import discord
from dotenv import load_dotenv
import yaml
import shared
from discord.ext import commands

with open ('config.yaml') as file: # loading config yaml file
    try:
        config = yaml.safe_load(file)
        for key, value in config.items():
            shared.config[key] = value
    except yaml.YAMLError as e: # yaml failed to load
        print(e)
        sys.exit(1)

    # print(shared.config)

import finnhub_request as fr

description = 'StonkBot - A Python Discord bot providing stock prices, financials, (soon) alerts, and watchlists. Market data from Finnhub.io.\nCreated by Ethan Osmundson using Discord.py.\nhttps://github.com/ethanosmundson/StonkBot'
bot = commands.Bot(command_prefix = '$', description = description)
bot.remove_command('help') # allows help command to be overwritten

@bot.event
async def on_ready():
    activity = discord.Game(name="$help for commands", type = 3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user.name}!')

@bot.event # will this ever print a message?
async def on_disconnect():
    print(f'{bot.user.name} has disconnected!')

@bot.command(name ='help')
async def help_command(ctx, command=None):
    """A help message"""
    author = ctx.message.author
    
    if command != None:
        embed = discord.Embed(
            color = discord.Color.blurple(),
            title = 'StonkBot Help'
        )

        if command == 'conews':
            embed.add_field(name = 'Company News Command', value = '$conews <symbol>\n\n This command will provide you with the top three news headlines related to the company you enter. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'covid' or command == '$covid':
            embed.add_field(name = 'COVID-19 Command', value = '$covid <state> <...> \n\n This command will provide state-by-state COVID-19 data. Note that the data is only avaliable for US states (not including the District of Columbia) and a maximum of six states may be queried at a time. Enter the postal code or full name of a US state in place of <state>.')
        elif command == 'earn' or command == '$earn':
            embed.add_field(name = 'Earnings Command', value = '$earn <symbol> <...> \n\n This command will provide the last four quarters of earnings data on the companies request. A maximum of three companies are allowed. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'fin' or command == '$fin':
            embed.add_field(name = 'Financials Command', value = '$fin <symbol> <...> \n\n This command will provide the following financial data: 52-Week High, 52-Week Low, Price to Book (Quarterly and Annual), P/E, Normalized EPS (Annual), Quick Ratio (Annual), RoI (annual), Debt/Equity (Annual). A maximum of three companies are allowed. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'news' or command == '$news':
            embed.add_field(name = 'News Command', value = '$news \n\n This command will provide three top market-related news stories for the day.')
        elif command == 'help' or command == '$help':
            embed.add_field(name = 'Help Command', value = 'This is getting confusing.')
        elif command == 'info' or command == '$info':
            embed.add_field(name = 'Company Information Command', value = '$info <symbol> \n\n This command will provide a brief description including information on sector, location, market cap, outstanding shares, IPO date, ticker symbol, and website. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'target' or command == '$target':
            embed.add_field(name = 'Price Target Command', value = '%target <symbol> <...> \n\n This command will provide price target consensus data on a maximum of three companies. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'quote' or command == '$quote':
            embed.add_field(name = 'Quote Command', value = '$quote <symbol> <...> \n\n This command will provide a price quote on a stock including current price, open price, daily high, and daily low. A maximum of three companies are allowed. Note that the left bar of the response is either green or red based on the price change from open. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'rec' or command == '$rec':
            embed.add_field(name = 'Recommendations Command', value = '$rec <symbol> <...> \n\n This command will provide aggregate analyst recommendation data from the last two weeks on a stock. A maximum of three companies are allowed. Enter a stock ticker symbol in place of <symbol>.')
        elif command == 'sent' or command == '$sent':
            embed.add_field(name = 'Media Sentiment Command', value = '$sent <symbol> <...> \n\n This command will provide overall media sentiment data based on article frequencies and sentiment. A maximum of three companies are allowed. Enter a stock ticker symbol in place of <symbol>.')
        else:
            embed.add_field(name = 'Unknown Command', value = f"I don't recognise that command ({command}). Try again?")
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/743997950648385598/744332473860620468/avatar.jpg')
        embed.set_footer(text = 'DISCLAIMER: Financial data provided is not guaranteed to be accurate. The developer of this bot assumes no responsibility for financial loss. Market data from Finnhub.io.')

        await ctx.send('Check your DMs!')
        channel = await author.create_dm()
        await channel.send(embed=embed)

    elif command == None:
        embed = discord.Embed(
            color = discord.Color.blurple(),
            title = 'StonkBot Help \nUse $help <command> for more info on a specific command!',
        )

        embed.add_field(name = f'$conews <symbol>', value = "Today's news on a company", inline = False)
        embed.add_field(name =f'$covid <state> <...>', value = 'COVID-19 data per US state on up to six states', inline = False)
        embed.add_field(name = f'$earn <symbol> <...>', value = 'Recient earnings data on a company on up to three companies', inline = False)
        embed.add_field(name = f'$fin <symbol> <...>', value = 'Financial data incuding margins, P/E ratio, and more on up to three companies', inline = False)
        embed.add_field(name = f'$news', value = "Today's top three news headlines", inline = False)
        embed.add_field(name = f'$help <command>', value = 'Sends this help message or specific information on a command', inline = False)
        embed.add_field(name = f'$info <symbol>', value = 'Company information such as sector, headquarters, market cap, and more', inline = False)
        embed.add_field(name = f'$target <symbol> <...>', value = 'Price target consensus on up to three companies', inline = False)
        embed.add_field(name = f'$quote <symbol> <...>', value = 'Daily price information on up to three companies', inline = False)
        embed.add_field(name = f'$rec <symbol> <...>', value = 'Analyst recommendations on up to three companies', inline = False)
        embed.add_field(name = f'$sent <symbol> <...>', value = 'Overall media sentiment for up to three companies', inline = False)
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/743997950648385598/744332473860620468/avatar.jpg')
        embed.set_footer(text = 'DISCLAIMER: Financial data provided is not guaranteed to be accurate. The developer of this bot assumes no responsibility for financial loss. Market data from Finnhub.io.')

        await ctx.send('Check your DMs!')
        channel = await author.create_dm()
        await channel.send(embed=embed)

@bot.command(name ='quote')
async def quote_command(ctx, *symbols): 
    """Stock quote for up to three symbols"""
    if len(symbols) > 3:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many stocks.', value = 'Please enter a maximum of three symbols.')
        await ctx.send(embed = embed)
    else:
        for symbol in symbols: 
            embed = fr.get_quote(symbol)
            await ctx.send(embed = embed)

@bot.command(name ='fin')
async def fin_command(ctx, *symbols):
    """Financial data incuding margin, P/E ratio, and more"""
    if len(symbols) > 3:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many stocks.', value = 'Please enter a maximum of three symbols.')
        await ctx.send(embed = embed)
    else:
        for symbol in symbols:
            embed = fr.get_financials(symbol)
            await ctx.send(embed = embed)

@bot.command(name ='info') 
async def info_command(ctx, symbol):
    """Company information such as sector, headquarters, and more"""
    embed = fr.get_company_info(symbol)
    await ctx.send(embed = embed)

@bot.command(name = 'conews') 
async def companynews_command(ctx, symbol):
    """Today's news on company"""
    embed = fr.get_company_news(symbol)
    await ctx.send(embed = embed)
    
@bot.command(name ='news')
async def headlines_command(ctx):
    """Top market headlines"""
    embed = fr.get_market_headlines()
    await ctx.send(embed = embed)
    
@bot.command(name ='sent')
async def sentiment_command(ctx, *symbols):
    """Overall news sentiment for a company"""
    if len(symbols) > 3:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many stocks.', value = 'Please enter a maximum of three symbols.')
        await ctx.send(embed = embed)
    else:
        embed = fr.get_news_sentiment(symbols)
        await ctx.send(embed = embed)
    
@bot.command(name ='rec')
async def recommends_command(ctx, *symbols):
    """Analyst recommendations on a company"""
    if len(symbols) > 3:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many stocks.', value = 'Please enter a maximum of three symbols.')
        await ctx.send(embed = embed)
    else:
        embed = fr.get_recommendations(symbols)
        await ctx.send(embed = embed)
    
@bot.command(name ='target')
async def price_target_command(ctx, *symbols):
    """Price target consensus on a company"""
    if len(symbols) > 3:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many stocks.', value = 'Please enter a maximum of three symbols.')
        await ctx.send(embed = embed)
    else:
        for symbol in symbols:
            embed = fr.get_price_targets(symbol)
            await ctx.send(embed = embed)
    
@bot.command(name ='earn')
async def earnings_command(ctx, *symbols):
    """Recient earnings data on a company"""
    if len(symbols) > 3:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many stocks.', value = 'Please enter a maximum of three symbols.')
        await ctx.send(embed = embed)
    else:
        for symbol in symbols:
            embed = fr.get_earnings(symbol)
            await ctx.send(embed = embed)
        
@bot.command(name ='covid')
async def covid_command(ctx, *states):
    """Per state COVID-19 data"""
    if len(states) > 6:
        embed = discord.Embed(
        color = discord.Color.blurple(),
        )
        embed.add_field(name = 'Too many states.', value = 'Please enter a maximum of six states.')
        await ctx.send(embed = embed)
    else:
        embed = fr.get_covid(states)
        await ctx.send(embed = embed)
    

bot.run(shared.config['discord']['token'])
