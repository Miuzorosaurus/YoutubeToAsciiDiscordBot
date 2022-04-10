#!/usr/bin/env python

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

running = True

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("BOT is in " + str(guild_count))

@bot.command(brief="Plays a video url in ascii", description="Usage: !ascii Youtube_Link width(between 5 and 44, default is 44) height(between 5 and 22, default is 22) frameskip(between 0 and 90, default is 5) mapping(dictates which mapping type to use, can be A(average) or M(min-max) or L(luminosity)) charset(can be 1(better for color) or 2(better for black and white videos))")
async def ascii(ctx, *args):
    enabled = True
    print("starting command ascii")
    while enabled == True:
        #0: youtube link 1 and 2: resolution 3: frameskip 4: mapping 5: charset
        try:
            a = int(args[1])
        except:
            a = 44

        try:
            b = int(args[2])
        except:
            b = 22

        try:
            c = int(args[3])
        except:
            c = 5

        try:
            d = str(args[4])
        except:
            d = "L"

        try:
            e = int(args[5])
        except:
            e = 2


        if type(args[0])!= str:
            await ctx.channel.send("```" + "Invalid YouTube link." + "```")
            enabled = False
        try:
            if a:
                if type(a) == int and a <= 44 and a >= 5:
                    WIDTH = a
                else:
                    await ctx.channel.send("```" + "Invalid width given. Width must be a number between 5 and 44." + "```")
                    enabled = False
        except IndexError:
            WIDTH = 44
        try:
            if args[2]:
                if type(b) == int and b <= 22 and b >= 5:
                    HEIGHT = b
                else:
                    await ctx.channel.send("```" + "Invalid height given. Height must be a number between 5 and 22." + "```")
                    enabled = False
        except IndexError:
            HEIGHT = 22
        try:
            if c:
                if type(c) == int and c <= 90 and c >= 0:
                    FRAMESKIP = c
                else:
                    await ctx.channel.send("```" + "Invalid frameskip value given. Frameskip must be a number between 0 and 90." + "```")
                    enabled = False
        except IndexError:
            FRAMESKIP = 5
        try:
            if args[4]:
                if type(d) == str and (d == "A" or d == "M" or d == "L"):
                    MAPPING = d
                else:
                    await ctx.channel.send("```" + "Invalid mapping method given. Choose A (average), M (min-max) or L(luminosity)" + "```")
                    enabled = False
        except IndexError:
            MAPPING = "L"

        try:
            if args[5]:
                if type(e) == int and (e == 1 or e == 2):
                    CHARSET = e
                else:
                    await ctx.channel.send("```" + "Invalid character set given. Choose either 1 (better for colour) or 2 (better for grayscale)" + "```")
                    enabled = False
        except IndexError:
            CHARSET = 2

        global running
        running = True
        function = main(args[0], WIDTH, HEIGHT, FRAMESKIP, MAPPING, CHARSET)
        for i in function:
            if i == None or running == False:
                break
            start_time = time.time()
            await ctx.channel.send("```" + i + "```")
            end_time = time.time()
            exetime = end_time - start_time
            print(exetime)
#            time.sleep(1 - exetime)
        enabled = False

@bot.command()
async def stop(ctx):
    global running
    running = False
    await ctx.send("```Stopping...```")



bot.run(TOKEN)
