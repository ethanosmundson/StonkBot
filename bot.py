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

    print(shared.config)

import finnhub_request as fr

load_dotenv() # not sure what this does
TOKEN = os.getenv('DISCORD TOKEN')

description = 'StonkBot - A Python Discord bot providing stock prices, financials, and alerts.\nCreated by Ethan Osmundson.\nhttps://github.com/ethanosmundson/StonkBot'
bot = commands.Bot(command_prefix = '$', description = description)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

@bot.command(name ='help')
async def help_command(ctx):
    """A help message"""
    author = ctx.message.author
    
    embed = discord.Embed(
        color = discord.Color.blurple(),
        title = 'StonkBot Help'
    )

    
    embed.add_field(name = f'$info <symbol>', value = 'Company information such as sector, headquarters, and more', inline = False)
    embed.add_field(name = f'$companynews <symbol>', value = 'Recent news on a company', inline = False)
    embed.add_field(name = f'$covid <state>', value = 'COVID-19 data per US state', inline = False)
    embed.add_field(name = f'$earnings <symbol>', value = 'Recient earnings data on a company', inline = False)
    embed.add_field(name = f'$fin <symbol>', value = 'Financial data incuding margin, P/E ratio, and more', inline = False)
    embed.add_field(name = f'$headlines <symbol>', value = 'Top market headlines', inline = False)
    embed.add_field(name = f'$help', value = 'Sends this help message', inline = False)
    embed.add_field(name = f'$pricetarget <symbol>', value = 'Price target consensus on a company', inline = False)
    embed.add_field(name = f'$quote <symbol>', value = 'Daily price information on the stock', inline = False)
    embed.add_field(name = f'$recommends <symbol>', value = 'Analyst recommendations on a company', inline = False)
    embed.add_field(name = f'$sentiment <symbol>', value = 'Overall news sentiment for a company', inline = False)
    embed.set_thumbnail(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQDEylpvECg3TgpRV-zuhYzR3zLzfUNh1PaMQ&usqp=CAU')
    embed.set_author(name = 'Created by Ethan Osmundson')
    embed.set_footer(text = 'DISCLAIMER: Financial data provided is not guaranteed to be accurate. The developer of this bot assumes no responsibility for financial loss.')


    await ctx.send('Check your DMs!')
    channel = await author.create_dm()
    await channel.send(embed=embed)

@bot.command(name ='quote')
async def quote_command(ctx, symbol): #TODO: allow multiple stocks
    """24h stock quote for symbol"""
    response = fr.get_quote(symbol)
    await ctx.send(response)

@bot.command(name ='fin')
async def fin_command(ctx, symbol):
    """Financial data incuding margin, P/E ratio, and more"""
    response = fr.get_financials(symbol)
    await ctx.send(response)

@bot.command(name ='info')
async def info_command(ctx, symbol):
    """Company information such as sector, headquarters, and more"""
    response = fr.get_company_info(symbol)
    await ctx.send(response)

@bot.command(name = "companynews")
async def companynews_command(ctx, symbol):
    """Recent news on company"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    
@bot.command(name ='headlines')
async def headlines_command(ctx, symbol):
    """Top market headlines"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    
@bot.command(name ='sentiment')
async def sentiment_command(ctx, symbol):
    """Overall news sentiment for a company"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    
@bot.command(name ='recommends')
async def recommends_command(ctx, symbol):
    """Analyst recommendations on a company"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    
@bot.command(name ='pricetarget')
async def price_target_command(ctx, symbol):
    """Price target consensus on a company"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    
@bot.command(name ='earnings')
async def earnings_command(ctx, symbol):
    """Recient earnings data on a company"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    
@bot.command(name ='covid')
async def covid_command(ctx, symbol):
    """Per state COVID-19 data"""
    response = 'My creator has not yet implemented this function!'
    await ctx.send(response)
    

bot.run(shared.config['discord']['token'])

#TODO: watchlists
#TODO: price alerts