#!/usr/bin/env python

#TODO fix bug where program goes ahead

import os

import discord
from dotenv import load_dotenv, find_dotenv
import time

from videomaker import main

from discord.ext import commands

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASEDIR, 'token.env'))


TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="!")

global index, rundict

index = 0
rundict = {}


def checkLimits(value, low, high, correcttype):
    if value == None:
        return True
    elif type(value) != correcttype:
        return False
    elif value < low or value > high:
        return False
    else:
        return True

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("BOT is in " + str(guild_count))

@bot.command(brief="Plays a video url in ascii", description="Usage: !ascii Youtube_Link. Options: image=number(0 or 1, 1 enables image mode which spams but allows for higher res ascii), width=number(between 5 and 44, default is 44), height=number(between 5 and 22, default is 22), frameskip=number(between 0 and 90, dictates how many frames to skip when playing, defaults to 5), mapping=number(1 to 3, select mapping technique(average,min-max,luminosity), defaults to 3), charset=number(1 or 2, 1 is more characters 2 is less characters, default is 2). Any incorrect commands entered will be replaced with defaults.")
async def ascii(ctx, link, *args):
    print("starting command ascii")

    await ctx.send("```Starting the bot...```")

    global index, rundict
    index = index + 1
    origin = ctx.channel.id
    rundict.update({origin:index})
    print(rundict)


    running = True
    print("index = " + str(index))

    options = {"VideoLink":link}

    for x in args:
        if '=' in x:
            x = x.strip(",")
            temp = x.split("=")
            try:
                options.update({temp[0]: int(temp[1])})
            except:
                pass
#its getting correct arguments but it incorrectly gets fixed
    if checkLimits(options.get('image'), 0, 1, int) == False:
        options.update({'image': 0})
        if checkLimits(options.get('height'), 5, 22, int) == False:
            options.update({'height': 22})
        if checkLimits(options.get('width'), 5, 44, int) == False:
            options.update({'width': 44})
    elif options.get('image') == 1:
        if checkLimits(options.get('height'), 10, 144, int) == False:
            options.update({'height': 144})
        if checkLimits(options.get('width'), 20, 256, int) == False:
            options.update({'width': 256})




    if checkLimits(options.get('frameskip'), 0, 90, int) == False:
        options.update({'frameskip': 5})
    if checkLimits(options.get('mapping'), 1, 3, int) == False:
        options.update({'mapping': 3})
    if checkLimits(options.get('symbols'), 1, 2, int) == False:
        options.update({'symbols': 2})



    options.update({'output': str(index)})
    options.update({'discord': True})

    print(options)

    editableMessage = False
    try:
        function = main(**options)
        for i in function:
            if i == None or origin not in rundict:
                break
            start_time = time.time()

            if editableMessage == False:
                if options.get('image') != 1:
                    message = await ctx.channel.send("```" + i + "```")
                    editableMessage = True
                else:
                    message = await ctx.channel.send(file=discord.File(i))

            elif editableMessage == True:
                await message.edit(content=("```" + i + "```"))

            end_time = time.time()
            exetime = 1 - (end_time - start_time) + 0.1
            if exetime < 0:
                exetime = 1
            if options.get('image') != 1:
                time.sleep(exetime)
    except:
        print("Error: " + str(e))
        await ctx.send("```Error has occured.```")

    index = index - 1

@bot.command()
async def stop(ctx):
    global rundict, index
    origin = ctx.channel.id
    if origin in rundict:
        del rundict[origin]
        await ctx.send("```Stopping...```")
    else:
        await ctx.send("```The bot is not currenctly not running any commands in this channel.```")



bot.run(TOKEN)
