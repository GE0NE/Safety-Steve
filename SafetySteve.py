#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import os                                                                                                       # import all sorts of shit
import platform
import sys                                                                                                      # like the OS and the System
import datetime                                                                                                 # and time itself
from datetime import date, time
import time
import json                                                                                                     # some dude named jason
import asyncio                                                                                                  # a kitchen sinkio
import re                                                                                                       # re:re:re:re:re: meeting time
import inspect
import praw
from prawcore import NotFound
import random
import math
import html
import shlex
from urllib import parse
from urllib.request import Request, urlopen
import aiohttp
import ctypes
from ctypes.util import find_library
import traceback
import git
import textwrap
import ast
import requests

try:
    import discord
except ImportError:
    from pip._internal import main as pip
    pip(['install', '-U', 'git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]'])
    import discord
from discord import opus
from discord.utils import get

try:
    import requests
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'requests'])
    import requests 

try:
    import bs4
except ImportError:
    from pip._internal import main as pip
    pip(['install', 'beautifulsoup4'])
    import bs4
from bs4 import BeautifulSoup

try:
    with open('config/default-config.json', encoding='utf8') as f:                                                             
        config = json.load(f)
except FileNotFoundError:
    with open('config/default-config.json', 'w', encoding='utf8') as f:
        config = {}
        json.dump({
            "description": "I keep us safe from evil words!",
            "name": "Safety Steve", "creator": "GEONE",
            "git_link": "https://github.com/GE0NE/Safety-Steve",
            "fileformat": ".mp3", "sunday_game": "Minecraft: Christian Edition",
            "monday_game": "Minecraft: Safety Edition", "tuesday_game": "Nekopara",
            "wednesday_game": "It is Wednesday, my dudes!",
            "thursday_game": "Minecraft: Extra Safe Edition (NSFW)",
            "friday_game": "Waifu Sex Simulator",
            "saturday_game": "Minecraft: Safety Edition", "embed_color": "0xeee657",
            "guild_admins": [[],"Users who can manage configs for this guild (mention)"],
            "invoker": ["^","Used as the prefix for commands (str)"],
            "vote_limit": [3,"How many times per day each user may vote using the good/bad bot command (int)"],
            "gild_limit": [1,"How many times per day each user may award a gild using the gild command (int)"],
            "point_value_in_currency": [10,"How much currency each point can be exchanged for using the exchange commmand (int)"],
            "gilding_value_in_currency": [50,"How much currency each gilding can be exchanged for using the exchange commmand (int)"],
            "currency_symbol": ["¤","The currency symbol (str)"],
            "weekly_score_decay": [1,"How many points each user's score will decay by every week (int)"],
            "bad_word_response": ["Hey! No bad words, please. This is a Christian server!","The respose to a bad word being said (str)"],
            "bad_words": [["heck","frick","fick","golly","gosh","jeeper","darn","drat","tarnation"],"The list of bad words the bot will respond to (list)"],
            "bad_words_exceptions": [["check","fickle","quadratic","hydrat"],
            "A list of words/prefixes that contain one of the bad words that the bot will ignore (list)"],
            "reaction_words": [{"word": "wednesday", "reaction": "🐸"}, {"word": "skeltal", "reaction": "💀#🎺"},
            {"word": "doot", "reaction": "🎺"}]}, f, indent = 4, ensure_ascii = False)
        sys.exit("default-config file created. "
            "Please fill out the default-config.json file and restart the bot.");

try:
    with open('config/user-info.json', encoding='utf8') as f:
        userInfo = json.load(f)
except FileNotFoundError:
    with open('config/user-info.json', 'w', encoding='utf8') as f:
        userInfo = {}
        json.dump({"general_info":{"discord_token": "","user_id": "","mention": "","client_id": "","client_secret": ""},
            "channel_ids":{"lobby": ""},"security":{"allowremoteshutdown": False,"admins":[]}}, f, indent = 4, ensure_ascii = False)
        sys.exit("user info file created. "
            "Please fill out the user-info.json file and restart the bot.");

try:
    with open('config/commands.json', encoding='utf8') as f:
        commandsFile = json.load(f)
except FileNotFoundError:
    with open('config/commands.json', 'w', encoding='utf8') as f:
        commandsFile = {}
        json.dump({'text_commands': [{'Command': '', 'Help': '', 'Params': ''}],
            'voice_commands': [{'Command': '', 'Help': '', 'Params': ''}]}, f, indent = 4, ensure_ascii = False)
        sys.exit("commands file created. "
            "Please fill out the commands.json file and restart the bot.");

try:
    with open('config/fonts.json', encoding='utf8') as f:
        fonts = json.load(f, strict=False)
except FileNotFoundError:
    with open('config/fonts.json', 'w', encoding='utf8') as f:
        font = {}
        json.dump({'bubble': [''], "bubble_mask": ['']}, f, indent = 4, ensure_ascii = False)
        sys.exit("fonts file created. "
            "Please fill out the fonts.json file and restart the bot.");

try:
    with open('config/dates.json', encoding='utf8') as f:
        date_list = json.load(f, strict=False)
except FileNotFoundError:
    with open('config/dates.json', 'w', encoding='utf8') as f:
        date_list = {}
        json.dump({'dates': [{"Name": "Safety Steve", "Day": 1, "Month": 4, "Year": 2018, 
            "Tag": "<@430061939805257749>", "Type": "birthday", "Message": "Happy #age #type, #tag!",
            "Channel": "lobby", "React": "🎉#🎂#🎊#🍰"}]}, f, indent = 4, ensure_ascii = False)
        sys.exit("dates file created. "
            "Optionally fill out the dates.json file and restart the bot.");

try:
    with open('config/items.json', encoding='utf8') as f:
        item_list = json.load(f, strict=False)
except FileNotFoundError:
    with open('config/items.json', 'w', encoding='utf8') as f:
        item_list = {}
        json.dump({"items":[{"Item": "Shield","Name": "Shield","Icon": ":shield:",
            "Description": "Protects you from recieving positive or negative votes","Id": 0,"Cost": 30},
            {"Item": "ActiveShield","Name": "Shield (Active)","Icon": "*:shield:*",
            "Description": "Protects you from recieving positive or negative votes","Id": 1,"Cost": -1}]},
            f, indent = 4, ensure_ascii = False)
        sys.exit("items file created. "
            "Optionally fill out the items.json file and restart the bot.");

# Bot info
desc = config['description']
generalInfo = userInfo['general_info']
userID = generalInfo['user_id']
mention = generalInfo['mention']
discordToken = generalInfo['discord_token']
name = config['name']

# Commands
textCommands = commandsFile['text_commands']
voiceCommands = commandsFile['voice_commands']
nsfwCommands = commandsFile['nsfw_commands']
textCommandList = []
voiceCommandList = []
nsfwCommandList = []

# Command info
textCommandHelp = []
textCommandParams = []
textCommandAlias = []
textCommandExample = []
voiceCommandHelp = []
voiceCommandParams = []
voiceCommandAlias  = []
nsfwCommandHelp = []
nsfwCommandParams = []
nsfwCommandAlias  = []
nsfwCommandExample = []

# Init command info
for command in textCommands:
    textCommandList.append(command['Command'])
    textCommandHelp.append(command['Help'])
    textCommandParams.append(command['Params'])
    textCommandAlias.append(command['Alias'].split('#'))
    textCommandExample.append(command['Examples'].split('#'))

for command in voiceCommands:
    voiceCommandList.append(command['Command'])
    voiceCommandHelp.append(command['Help'])
    voiceCommandParams.append(command['Params'])
    voiceCommandAlias.append(command['Alias'].split('#'))

for command in nsfwCommands:
    nsfwCommandList.append(command['Command'])
    nsfwCommandHelp.append(command['Help'])
    nsfwCommandParams.append(command['Params'])
    nsfwCommandAlias.append(command['Alias'].split('#'))
    nsfwCommandExample.append(command['Examples'].split('#'))

# List of commands
commandList = textCommandList + voiceCommandList + nsfwCommandList
commandHelp = textCommandHelp + voiceCommandHelp + nsfwCommandHelp
commandParams = textCommandParams + voiceCommandParams + nsfwCommandParams
commandAlias = textCommandAlias + voiceCommandAlias + nsfwCommandAlias

# Word Responses
reactionWords = config['reaction_words']

# Formatting
embedColor = int(config['embed_color'], 0)

# Channel IDs
channels = userInfo['channel_ids']

# Birthdays
dates = date_list['dates']

# Items
items = item_list['items']
shop = {}

# Init Shop
for item in items:
    if item['Cost'] > -1:
        shop[item['Item']] = item['Cost']

# Reddit Config
reddit_id = generalInfo['client_id']
reddit_secret = generalInfo['client_secret']
reddit_agent = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# Misc info for commands
gitLink = config['git_link']
fileExt = config['fileformat']
bubbleFont = fonts['bubble_letters']
bubbleFontMask = fonts['bubble_mask']

# The client
client = discord.Client(description=desc, max_messages=100)

async def throwError(msg, error=None, vocalize=True, custom=False, sayTraceback=False, 
    printTraceback=False, tracebackOverride='', printError=True, fatal=False):

    def open_layer(layer):
      if layer.tb_next == None:
        return layer
      else:
        return open_layer(layer.tb_next)

    if printError:
        print("ERROR:\n{}".format(error))
    if vocalize and msg:
        if error:
            await say(msg, "Woah! Something bad happened! ```\n{}\n```".format(error) if not custom else error)
        if sayTraceback and not custom:
            error = open_layer(error.__traceback__)
            tb = ''.join(traceback.format_tb(error))
            # Correct line numbers for exec traceback
            if tracebackOverride:
                tb = re.sub(r'line (\d+)', lambda m: 'line {0}'.format(int(m.group(1)) - 1), tb)
            dump = "```{}{}```".format(tb.replace("`", "\`"), tracebackOverride.split('\n')[error.tb_lineno - 2] if 
                tracebackOverride and len(tracebackOverride.split('\n')) >= error.tb_lineno - 2 else '')
            await say(msg, dump)
    if printTraceback:
        print("Traceback:")
        traceback.print_exc()

    if printError or printTraceback or sayTraceback:
        writeLog(error, fatal)
    return

@client.event
async def on_message(msg: discord.Message):

    rawContent = msg.content
    content = rawContent.lower()

    for entry in reactionWords:
        if entry['word'] in content:
            for reaction in entry['reaction'].split('#'):
                await react(msg, reaction)

    if msg.author.bot:
        return

    serverInvoker = await getServerConfig(msg.guild.id, ['configs', 'invoker'])
    if content.startswith(serverInvoker):
        rawMessage = rawContent[len(serverInvoker):].strip()
        message = rawMessage.lower()
        breakdown = message.split(" ")
        rawBreakdown = rawMessage.split(" ")
        command = breakdown[0]
        args = ' '.join(rawBreakdown[1:]) if len(breakdown) > 1 else ''
        try:
            argList = shlex.split(args)
        except ValueError:
            argList = args.split()

        if command == '':
            return

        #------- Bot developer commands -------
        if command == "restart":
            if isBotAdmin(msg.author.mention):
                await restart(msg)
            else:
                await throwError(msg, "You don't have permission to use that command!", custom=True, printError=False)
            return

        if command == "pull":
            if await isBotAdmin(msg.author.mention):
                await pullFromRepo(msg)
            else:
                await throwError(msg, "You don't have permission to use that command!", custom=True, printError=False)
            return

        if command == "func":
            if await isBotAdmin(msg.author.mention):
                if len(args.strip()) >= 1:
                    await handleFunc(msg, args)
            else:
                await throwError(msg, "You don't have permission to use that command!", custom=True, printError=False)
            return

        if command == "eval":
            if not argList:
                await throwError(msg, "Command must have parameters that can evaluate to python", custom=True, printError=False)
                return

            def insert_returns(body):
                # insert return stmt if the last expression is a expression statement
                if isinstance(body[-1], ast.Expr):
                    body[-1] = ast.Return(body[-1].value)
                    ast.fix_missing_locations(body[-1])

                # for if statements, we insert returns into the body and the orelse
                if isinstance(body[-1], ast.If):
                    insert_returns(body[-1].body)
                    insert_returns(body[-1].orelse)

                # for with blocks, again we insert returns into the body
                if isinstance(body[-1], ast.With):
                    insert_returns(body[-1].body)

            def strip_empty_lines(s):
                lines = s.splitlines()
                while lines and not lines[0].strip():
                    lines.pop(0)
                while lines and not lines[-1].strip():
                    lines.pop()
                return '\n'.join(lines)

            if await isBotAdmin(msg.author.mention):
                if len(args.strip()) >= 1:
                    try:
                        fn_name = "_eval_expr"

                        cmd = rawMessage[len('eval'):].strip("` ")

                        # add a layer of indentation
                        cmd = strip_empty_lines("\n".join(f"    {i}" for i in cmd.splitlines()))

                        # wrap in async def body
                        body = f"async def {fn_name}():\n{cmd}"

                        parsed = ast.parse(body)
                        body = parsed.body[0].body

                        insert_returns(body)

                        env = {
                            'client': client,
                            'discord': discord,
                            'config': config,
                            'msg': msg,
                            'embedColor' : embedColor,
                            'getVoiceClient' : getVoiceClient,
                            'isPlaying' : isPlaying,
                            'say' : say,
                            'subreddit' : subreddit,
                            'scoreDecay' : scoreDecay,
                            'readScores' : readScores,
                            'writeScore': writeScore,
                            'react' : react,
                            'throwError' : throwError,
                            'getServerConfig' : getServerConfig,
                            'voiceCommands' : voiceCommands,
                            'textCommands' : textCommands,
                            'playSound' : playSound,
                            '__import__': __import__
                        }
                        exec(compile(parsed, filename="<input>", mode="exec"), env)

                        result = (await eval(f"{fn_name}()", env))
                        await say(msg, result)
                    except Exception as e:
                        await throwError(msg, e, sayTraceback=True, tracebackOverride=cmd)
            else:
                await throwError(msg, "You don't have permission to use that command!", custom=True, printError=False)
            return
        #--------------------------------------

        if command == textCommands[0]['Command'] or command in textCommands[0]['Alias'].split('#'):
            if not args:
                await help(msg)
                return
            else:
                await helpCommand(args, msg) 
                return

        if command == textCommands[1]['Command'] or command in textCommands[1]['Alias'].split('#'):
            if not await isGuildAdmin(msg.guild.id, msg.author.mention):
                await throwError(msg, "You don't have permission to use that command!", custom=True, printError=False)
                return

            if len(args.strip()) < 1:
                await helpCommand(textCommands[1]['Command'], msg)
                return

            configs = await getServerConfig(msg.guild.id, ['configs'])
            if argList[0] in ['value', 'values', 'list']:
                if len(argList) > 1 and argList[1] in configs:
                    embed = discord.Embed(title="Config")
                    embed.add_field(name=argList[1], value=configs[argList[1]], inline=False)
                    await say(msg, "", embed=embed)
                    return
                elif len(argList) > 1:
                    await throwError(msg, "That is not a valid config", custom=True, printError=False)
                    return
                else:
                    embed = discord.Embed(title="Configs")
                    for conf in dict(configs):
                        embed.add_field(name=conf, value=configs[conf], inline=True)
                    await say(msg, "", embed=embed)
                    return

            if argList[0] in ['description', 'descriptions', 'help']:
                if len(argList) > 1 and argList[1] in configs:
                    embed = discord.Embed(title="Config")
                    embed.add_field(name=argList[1], value=config[argList[1]][1], inline=False)
                    await say(msg, "", embed=embed)
                    return
                elif len(argList) > 1:
                    await throwError(msg, "That is not a valid config", custom=True, printError=False)
                    return
                else:
                    embed = discord.Embed(title="Configs")
                    for conf in dict(configs):
                        embed.add_field(name=conf, value=config[conf][1], inline=False)
                    await say(msg, "", embed=embed)
                    return

            if argList[0] in configs:
                if len(argList) > 2:
                    if argList[1] in ['+','-','=']:
                        if argList[1] == '+':
                            await setServerConfig(msg.guild.id, argList[0], str(' '.join(rawBreakdown[1:][2:])), 1, msg=msg)
                        if argList[1] == '-':
                            await setServerConfig(msg.guild.id, argList[0], str(' '.join(rawBreakdown[1:][2:])), -1, msg=msg)
                        if argList[1] == '=':
                            await setServerConfig(msg.guild.id, argList[0], str(' '.join(rawBreakdown[1:][2:])), msg=msg)
                    return
                else:
                    embed = discord.Embed(title="Config")
                    embed.add_field(name=argList[0], value=config[argList[0]][1], inline=False)
                    embed.add_field(name="Value", value=configs[argList[0]], inline=False)
                    await say(msg, "", embed=embed)
                    return
            else:
                await throwError(msg, "That is not a valid config", custom=True, printError=False)
                return
            return

        if command == textCommands[2]['Command'] or command in textCommands[2]['Alias'].split('#'):
            await broadcastGitRepo(msg)

        if command == textCommands[3]['Command'] or command in textCommands[3]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[3]['Command'], msg)
                return
            await say(msg, args)
            await msg.delete()
            return

        if command == textCommands[4]['Command'] or command in textCommands[4]['Alias'].split('#'):
            await subreddit(msg, 'animemes', args=argList)
            return

        if command == textCommands[5]['Command'] or command in textCommands[5]['Alias'].split('#'):
            await subreddit(msg, argList[0], args=argList[1:] if len(argList) > 1 else [])
            return

        if command == textCommands[6]['Command'] or command in textCommands[6]['Alias'].split('#'):
            if len(args) > 30:
                await say(msg, "Woah! That's too many letters! Keep it below 30 please.")
                return
            if len(args.strip()) < 1:
                await helpCommand(textCommands[6]['Command'], msg)
                return
            await sayAscii(msg, args)
            return

        if command == textCommands[7]['Command'] or command in textCommands[7]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await setDailyGame()
                return
            typeindex = 0
            for i, index in enumerate(argList):
                if 'type=' in index:
                    typeindex = argList[i].replace('type=', '').strip()
                    args = re.sub(r'type=[\d\w]*', '', args)
                    break
            await setPlaying(args, typeindex)
            return

        if command == textCommands[8]['Command'] or command in textCommands[8]['Alias'].split('#'):
            await say(msg, "`༼ つ ◕_ ◕ ༽つ GIVE BAN ༼ つ ◕_ ◕ ༽つ`")

        if command == textCommands[9]['Command'] or command in textCommands[9]['Alias'].split('#'):
            usernamesFile = open("res/data/usernames.txt", "r")
            usernamesRaw = usernamesFile.read()
            usernames = usernamesRaw.split('\n')
            users = []
            karma = []
            nices = []
            for x in range(0, 5):
                users.append(random.choice(usernames))
                karma.append(random.randint(1, 1000))
                nices.append("nice.")
            poorSoul = random.randint(1, 4)
            nices[poorSoul] = "Nice"
            karma[poorSoul] = random.randrange(-10000, 0)
            thread = "```\n" \
                "▲   {0} • {5} points\n" \
                "▼   {10}" \
                "```\n" \
                "```\n" \
                "|  ▲   {1} • {6} points\n" \
                "|  ▼   {11}\n" \
                "```\n" \
                "```\n" \
                "|  |  ▲   {2} • {7} points\n" \
                "|  |  ▼   {12}\n" \
                "```\n" \
                "```\n" \
                "|  |  |  ▲   {3} • {8} points\n" \
                "|  |  |  ▼   {13}\n" \
                "```\n" \
                "```\n" \
                "|  |  |  |  ▲   {4} • {9} points\n" \
                "|  |  |  |  ▼   {14}\n" \
                "```".format(users[0], users[1], users[2], users[3], users[4], 
                    karma[0], karma[1], karma[2], karma[3], karma[4], nices[0], 
                    nices[1], nices[2], nices[3], nices[4])
            await say(msg, thread)

        if command == textCommands[10]['Command'] or command in textCommands[10]['Alias'].split('#'):
            text = args.strip()
            if len(text) < 1:
                await helpCommand(textCommands[10]['Command'], msg)
                return
            await sayIPA(msg, text)

        if command == textCommands[11]['Command'] or command in textCommands[11]['Alias'].split('#'): 
            try:
                if len(args.strip()) < 1:
                    await helpCommand(textCommands[11]['Command'], msg)
                    return
                question = args.split("[")[0]
                messageFormatted = " ".join(args.split())
                messageEmojis = None
                if '[' in messageFormatted and ']' in messageFormatted:
                    messageEmojis = messageFormatted.split("[")[1].split("]")[0]
                else:
                    messageEmojis = '👍 👎'
                emojis = messageEmojis.strip().split(" ")
                poll = await say(msg, question)
                try:
                    await msg.delete()
                except:
                    pass
                for emoji in emojis:
                    try:
                        await react(poll, emoji)
                    except:
                        continue
                return
            except:
                await helpCommand(textCommands[11]['Command'], msg)
                return

        if command == textCommands[12]['Command'] or command in textCommands[12]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[12]['Command'], msg)
                return
            await defineUrban(msg, args)
            return

        if command == textCommands[13]['Command'] or command in textCommands[13]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[13]['Command'], msg)
                return
            await defineGoogle(msg, args)
            return

        if command == textCommands[14]['Command'] or command in textCommands[14]['Alias'].split('#'):
            await mock(msg, text=args.strip())
            return

        if command == textCommands[15]['Command'] or command in textCommands[15]['Alias'].split('#'):
            if not argList:
                scores = await readScores(msg.guild.id)
                embed = discord.Embed(title="Scores:", description="_ _")
                for scoreEntry in scores:
                    try:
                        user = client.get_user(int(scoreEntry[0]))
                        score = scoreEntry[1]
                        if score != '0':
                            displayName = user.display_name
                            nick = msg.guild.get_member(user.id).nick
                            nick = displayName if nick is None else nick
                            sanitizedDisplayName = displayName.replace('_','\_')
                            displayName = "_AKA {}_\n".format(sanitizedDisplayName) if nick != displayName else ''
                            embed.add_field(name=nick, value="{}{}".format(displayName, score), inline=True)
                    except:
                        continue
                await say(msg, "", embed=embed)
                return
            else:
                if argList[0] in ['voted','votes']:
                    target = msg.author
                    if msg.mentions:
                        target = msg.mentions[0]
                    targetScores = await readScores(msg.guild.id, target.id)
                    await say(msg, "{} voted {} time{} today.".format("You've" if target is msg.author else target.mention + 
                        ' has', targetScores[3], '' if targetScores[3] == '1' else 's'))
                    return
                else:
                    if msg.mentions:
                        target = msg.mentions[0]
                        targetScores = await readScores(msg.guild.id, target.id)
                        await say(msg, "{}'s score is {}.".format(target.mention, targetScores[1]))
                    elif argList[0] in ['me','myself','self']:
                        target = msg.author
                        targetScores = await readScores(msg.guild.id, target.id)
                        await say(msg, "{}'s score is {}.".format(target.mention, targetScores[1]))
            return

        if command == textCommands[16]['Command'] or command in textCommands[16]['Alias'].split('#'):
            server = msg.guild
            invokerMessage = None
            author = None
            invokerScores = await readScores(server.id, userID=msg.author.id)

            serverGildLimit = await getServerConfig(msg.guild.id, ['configs', 'gild_limit'])
            if int(invokerScores[4]) >= serverGildLimit:
                await say(msg, "You have already gilded someone {}today!".format((str(serverGildLimit) + ' times ') if serverGildLimit != 1 else ''))
                return

            if len(args.strip()) < 1:
                async for invokerMessageTemp in msg.channel.history(limit=2):
                    invokerMessage = invokerMessageTemp
                if invokerMessage is not None:
                    author = invokerMessage.author
            else:
                author = msg.mentions[0] if msg.mentions is not None else msg.author

            if author == msg.author:
                await say(msg, "You can't gild yourself!")
                return

            await writeScore(server.id, author.id, gilding=1)
            await writeScore(server.id, msg.author.id, gilded=1)
            if invokerMessage is not None:
                await react(invokerMessage, "🔶")
            targetScores = await readScores(server.id, userID=author.id)
            embed = discord.Embed(title="_{} time{}_".format(targetScores[2], '' if targetScores[3] == '1' else 's'), 
                description="**You've been gilded!**", color=0xFFDF00)
            embed.set_thumbnail(url="https://i.imgur.com/UWWoFxe.png")
            await say(msg, "{}".format(author.mention), embed=embed)

        if command == textCommands[17]['Command'] or command in textCommands[17]['Alias'].split('#'):
            target = None
            nick = None

            gradient = [0xA8A8A8, 0xB0B097, 0xCACA64, 0xD9D950, 0xE4E448, 0xFFFF00]

            if msg.mentions:
                target = msg.mentions[0] 
            else:
                target = msg.author
            displayName = target.display_name
            nick = target.nick
            nick = displayName if nick is None else nick

            scores = await readScores(msg.guild.id, userID=target.id)
            gilded = scores[2]
            embed = discord.Embed(title="{} been gilded:".format("You have" if target == msg.author else nick + " has"), 
                description="_{} time{}_".format(gilded, 's' if int(gilded) != 1 else ''), 
                color=gradient[int(gilded) if int(gilded) < 6 else 5])
            embed.set_thumbnail(url="https://i.imgur.com/kD6NhBG.png")
            await say(msg, "", embed=embed)
            return

        if command == textCommands[18]['Command'] or command in textCommands[18]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[18]['Command'], msg)
                return
            await mal(msg, args.strip())
            return

        if command == textCommands[19]['Command'] or command in textCommands[19]['Alias'].split('#'):
            if not argList:
                await helpCommand(textCommands[19]['Command'], msg)
                return
            success = await exchange(msg, argList)
            if not success:
                await helpCommand(textCommands[19]['Command'], msg)

        if command == textCommands[20]['Command'] or command in textCommands[20]['Alias'].split('#'):
            if msg.mentions:
                target = msg.mentions[0] 
            else:
                target = msg.author
            if argList and argList[0] == 'all':
                await displayEveryonesCurrency(msg)
            elif argList and argList[0] == 'top':
                await displayTopCurrency(msg, int(argList[1]) if len(argList) > 1 and argList[1].isdigit() else 3)
            else:
                await displayCurrency(msg, target)
            return

        if command == textCommands[21]['Command'] or command in textCommands[21]['Alias'].split('#'):
            if msg.mentions and len(argList) >= 2:
                target = msg.mentions[0]
            else:
                await helpCommand(textCommands[21]['Command'], msg)
                return

            scoreEntry = await readScores(msg.guild.id, msg.author.id)

            try:
                amount = int(argList[1])
                if amount < 1:
                    await throwError(msg, "Woah! You must give a number greater than 0!", custom=True, printError=False)
                    return
            except ValueError:
                if str(argList[1]) == 'all':
                    amount = int(scoreEntry[5])
                else:
                    await helpCommand(textCommands[21]['Command'], msg)
                    return
            await giveCurrency(msg, target, amount)
            return

        if command == textCommands[22]['Command'] or command in textCommands[22]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[22]['Command'], msg)
                return
            await scp(msg, '-'.join(rawBreakdown) if len(breakdown) > 1 else '')
            return

        if command == textCommands[23]['Command'] or command in textCommands[23]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[23]['Command'], msg)
                return
            stringbuilder = ""
            for arg in argList:
                emote = await stringToEmoji(msg, arg, globalEmotes=True)
                if isinstance(emote, discord.Emoji):
                    stringbuilder = stringbuilder + "<{}:{}:{}>".format('a' if emote.animated else '', emote.name, emote.id)
                elif isinstance(emote, str):
                    stringbuilder = stringbuilder + emote
            await say(msg, stringbuilder)
            return

        if command == textCommands[24]['Command'] or command in textCommands[24]['Alias'].split('#'):
            helpList = ['help','info','about','descriptions','description']
            if argList and ' '.join(argList).lower() not in helpList:
                serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
                existingScore = await readScores(msg.guild.id, msg.author.id)
                currency = int(existingScore[6])
                itemSearchString = ' '.join(argList).lower()
                qty = int(argList[-1]) if argList[-1].isdigit() else 1
                if argList[-1].isdigit():
                    itemSearchString = ' '.join(argList[:-1]).lower()
                itemWanted = None
                for item in items:
                    try:
                        if item['Name'].lower() == itemSearchString and item['Item'] in shop:
                            itemWanted = item
                            break
                    except:
                        continue
                if itemWanted:
                    currentMoney = await readScores(msg.guild.id, msg.author.id)
                    currentMoney = int(currentMoney[6])
                    if currentMoney >= int(itemWanted['Cost']) * qty:
                        embed = discord.Embed(title="+%s _Purchased_" % (itemWanted['Icon']), 
                        description="**You've purchased %sx %s**" % (str(qty), itemWanted['Name']), color=0x17dd62)
                        await writeScore(msg.guild.id, msg.author.id, currency=-qty * int(itemWanted['Cost']), inventory={'%s'%(itemWanted['Item']):qty})
                        await say(msg, "", embed=embed)
                    else:
                        await throwError(msg, "You don't have enough %s to purchase %s of that item! You have %s%s, and you need %s%s." % (serverCurrencySymbol, 
                            str(qty), serverCurrencySymbol, currentMoney, serverCurrencySymbol, 
                            str((qty * int(itemWanted['Cost'])))), custom=True, printError=False)
                else:
                    await throwError(msg, "That's not a valid item! >`%s`<" % (itemSearchString), custom=True, printError=False)
                return

            embed = discord.Embed(title="Shop:", description="_ _", color=0x17dd62)
            for item in shop:
                try:
                    name = item
                    price = shop[item]
                    ico = '❔'
                    serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
                    for i in items:
                        if i['Item'] == name:
                            name = i['Name']
                            ico = i['Icon'] 
                            desc = i['Description']
                            break
                    if ' '.join(argList).lower() in helpList:
                        embed.add_field(name='_%s%s_ - %s' % (serverCurrencySymbol, str(price), name+ico), value='_%s_' % (desc), inline=False)
                    else:
                        embed.add_field(name=name+ico, value='_%s%s_' % (serverCurrencySymbol, str(price)), inline=True)
                except:
                    continue

            embed.set_footer(text="use %s%s <item> to purchase" % (serverInvoker, 'shop'), 
                    icon_url="https://i.imgur.com/331gN11.png")

            await say(msg, "", embed=embed)
            return

        if command == textCommands[25]['Command'] or command in textCommands[25]['Alias'].split('#'):
            existingScore = await readScores(msg.guild.id, msg.author.id)
            inventory = ast.literal_eval(existingScore[7])
            embed = discord.Embed(title="Inventory:", description="_ _")
            for item in inventory:
                try:
                    name = item
                    qty = inventory.get(item, 1)
                    ico = '❔'
                    for i in items:
                        if i['Item'] == name:
                            name = i['Name']
                            ico = i['Icon'] 
                            break
                    embed.add_field(name=str(qty)+'x '+name+ico, value='\u200b', inline=True)
                except:
                    continue
            await say(msg, "", embed=embed)
            return

        if command == textCommands[26]['Command'] or command in textCommands[26]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[26]['Command'], msg)
                return
            if argList:
                itemSearchString = ' '.join(argList).lower()
                itemInternalNameString = ''.join(argList).lower()
                if msg.mentions:
                    itemSearchString = ' '.join(argList[:-1]).lower()
                    itemInternalNameString = ''.join(argList[:-1]).lower()
                itemWanted = None
                for item in items:
                    try:
                        if item['Item'].lower() == itemInternalNameString and item['Item'] in shop:
                            itemWanted = item
                            break
                    except:
                        continue
                if not itemWanted:
                    await say(msg, "There is no item by that name! >`%s`"%(itemSearchString))
                    return
                elif itemWanted['Item'] in shop:
                    if await hasItem(msg.guild.id, msg.author.id, itemWanted['Item']):

                        target = None
                        if msg.mentions:
                            target = msg.mentions[0]
                            if target == msg.author and itemWanted['Item'] == "LoveBomb":
                                await say(msg, 'You cannot Love Bomb yourself! Nice try though.')
                                return
                        if not itemWanted['AcceptsTarget'] and target:
                            if target != msg.author:
                                await say(msg, 'You cannot use that item on someone else!')
                                return

                        if itemWanted['RequiresTarget'] and not target:
                            await say(msg, 'You need to specify a user to use this item on!')
                            return

                        if not target:
                            target = msg.author

                        if await hasItem(msg.guild.id, target.id, 'ActiveNazar') and target is not msg.author:
                            await say(msg, "This user was protected by a Nazar which caused the %s to vanish!"%(itemWanted['Name']))
                            await writeScore(msg.guild.id, target.id, inventory={'ActiveNazar':-1})
                            return

                        funcMap = {"say":say, "writeScore":writeScore}
                        localVarsMap = {"msg":msg, "target":target}

                        def isStringFuncCorutine(funcString, globalsVars, localVars):
                            try:
                                return inspect.iscoroutinefunction(eval(funcString.split('(', 1)[0], globalsVars, localVars))
                            except:
                                return False
                        for ACE in itemWanted['Exec']:
                            if isStringFuncCorutine(ACE, funcMap, localVarsMap):
                                await eval(ACE)
                            else:
                                eval(ACE)

                        if itemWanted['Usable'] == False:
                            return
                            
                        qty = -1
                        await writeScore(msg.guild.id, msg.author.id, inventory={'%s'%(itemWanted['Item']):qty})
                        embed = discord.Embed(title="-%s _Used_" % (itemWanted['Icon']), 
                        description="**You used %s on %s**" % (itemWanted['Name'], target.mention), color=0x17dd62)
                        await say(msg, "", embed=embed)

                    else:
                        await throwError(msg, "You don't have that item! >`%s`"%(itemWanted['Name']), custom=True, printError=False)
                else:
                    await throwError(msg, "That is not a valid item you can use! >`%s`"%(itemWanted['Name']), custom=True, printError=False)
            
        if command == textCommands[27]['Command'] or command in textCommands[27]['Alias'].split('#'):
            # Get rid of original command text
            message = rawMessage.replace(command, '', 1)

            # Get intensity level if applicable
            try:
                level = int(breakdown[1])
                message = message.replace(breakdown[1], '', 1)
                potential_text_breakdown_index = 2
            except (ValueError, IndexError):
                level = 5
                potential_text_breakdown_index = 1

            # Hacky. Sees if there's text in a string besides the command
            # itself and the intensity number, if present.
            try:
                breakdown[potential_text_breakdown_index]
            except IndexError:
                async for m in msg.channel.history(limit=2):
                    message = m.content

            zalgo_message = await zalgo_ify(message, level=level)
            if message == '':
                await say(msg, "Can't Zalgo an empty message or react.")
            else:
                await say(msg, zalgo_message)

        if command == textCommands[28]['Command'] or command in textCommands[28]['Alias'].split('#'):
            # Get rid of original command text
            message = rawMessage.replace(command, '', 1)

            if message.isspace() or message == '':
                async for m in msg.channel.history(limit=2):
                    message = m.content

            clappy_message = await clapify(message)

            # truncate over 2000 chars
            clappy_message = (clappy_message[:2000]) if len(clappy_message) > 2000 else clappy_message

            if message.isspace() or message == '':
                await throwError(msg, "Can't clap an empty message or react.", custom=True, printError=False)
            else:
                await say(msg, clappy_message)

        # now a redundant check as r/zerotwo is now treated as NSFW in the subreddit command
        # commenting out the check, but leaving the command as a template for future NSFW commands
        if command == nsfwCommands[0]['Command'] or command in nsfwCommands[0]['Alias'].split('#'):
            #if await checkNSFW(msg):
            await subreddit(msg, 'zerotwo', True)
            return

        if (command == voiceCommands[0]['Command'] or command in voiceCommands[0]['Alias'].split('#')):
            vc = getVoiceClient(msg.guild)
            if vc:
                await vc.disconnect()
            else:
                await throwError(msg, "I'm not in a voice channel!", custom=True, printError=False)
            return

        for i in range(1, len(voiceCommands)):
            if message == voiceCommands[i]['Command'] or command in voiceCommands[i]['Alias'].split('#'):
                await playSound(msg, voiceCommands[i])
                return

    elif any([badword in content for badword in await getServerConfig(msg.guild.id, ['configs', 'bad_words'])]):
        for word in content.split():
            try:
                for goodword in await getServerConfig(msg.guild.id, ['configs', 'bad_words_exceptions']):
                    if goodword in word:
                        raise Exception()
                for badword in await getServerConfig(msg.guild.id, ['configs', 'bad_words']):
                    if badword in word:
                        await say(msg, '{}: {}'.format(msg.author.mention, await getServerConfig(msg.guild.id, ['configs', 'bad_word_response'])))
                        return
            except:
                continue

    elif content in ['good bot', 'bad bot', 'medium bot', 'mega bad bot', 'mega good bot']:
        protected = 0
        votescast = 1
        deltascore = 1
        try:
            targetMessage = None
            server = msg.guild
            invokerScores = await readScores(server.id, userID=msg.author.id)

            async for targetMessageTemp in msg.channel.history(limit=2):
                targetMessage = targetMessageTemp

            if targetMessage is not None:
                serverVoteLimit = await getServerConfig(msg.guild.id, ['configs', 'vote_limit'])
                deltaTime = datetime.datetime.now() - targetMessage.created_at
                minutesSincePost = divmod(deltaTime.total_seconds(), 60)[0]
                if minutesSincePost > (60*16):
                    await say(msg, "You can't vote on posts older than 16 hours!")
                    return
                author = targetMessage.author
                server = targetMessage.guild
                if author == msg.author and 'good' in content:
                    await say(msg, "You can't vote positively for yourself!")
                    return

                elif int(invokerScores[3]) >=  serverVoteLimit:
                    await say(msg, "You can only vote {} per day!".format((str(serverVoteLimit) + ' times') if serverVoteLimit > 1 else 'once'))
                    return

                elif content == "medium bot":
                    await say(msg, "Thank you for voting on {}.\nTheir score is now {}.".format(author.mention, "medium-rare"))
                    return

                ###### Item ######                
                elif content == "mega bad bot" or content == "mega good bot":
                    itemInternalName = 'MegaVote'
                    itemName = itemInternalName
                    ico = '❔'
                    ###### Item ######
                    if await hasItem(msg.guild.id, msg.author.id, itemInternalName):
                        for item in items:
                            if item['Item'] == itemName:
                                itemName = item['Name']
                                ico = item['Icon']
                                break
                        await say(msg, "-{} You consumed a {} to use all your remaining votes today ({}) on {}!".format(ico, itemName, 
                            str(serverVoteLimit - int(invokerScores[3])), author.mention))
                        ###### Item ######
                        for i in range(0, serverVoteLimit - int(invokerScores[3])):
                            ###### Item ######
                            if 'bad' in content:
                                if await hasItem(server.id, author.id, 'ActiveWard'):
                                    await writeScore(server.id, author.id, inventory={'ActiveWard':-1})
                                    protected += 1
                                    continue

                            if await hasItem(server.id, author.id, 'ActiveShield'):
                                await writeScore(server.id, author.id, inventory={'ActiveShield':-1})
                                protected += 1
                        
                        if protected:
                            await say(msg, 
                                "This user was protected by an item and was unable to be voted on!{}".format(" (x{})".format(protected) if protected > 1 else ""))
                        ##################
                        deltascore = max(serverVoteLimit - int(invokerScores[3]) - protected, 0)
                        await writeScore(server.id, msg.author.id, inventory={'MegaVote':-1})
                        votescast = serverVoteLimit - int(invokerScores[3])
                    else:
                        await say(msg, "You don't have the item required to perform that action!")
                        return

                ##################
                elif await hasItem(server.id, author.id, 'ActiveShield') and not protected:
                    await say(msg, "This user was protected by a Shield and was unable to be voted on!")
                    await writeScore(server.id, author.id, inventory={'ActiveShield':-1})
                    protected = 1
                ##################

                elif 'bad' in content and not protected:
                    ###### Item ######
                    if await hasItem(server.id, author.id, 'ActiveWard'):
                        await say(msg, "This user was protected by a Ward and was unable to be negatively voted on!")
                        await writeScore(server.id, author.id, inventory={'ActiveWard':-1})
                        protected = 1
                ##################

                if not protected >= votescast:
                    await writeScore(server.id, author.id, score=deltascore * (1 if 'good' in content else -1))

                await writeScore(server.id, msg.author.id, voted=votescast)

                if max(votescast - protected, 0) != 0:
                    targetScores = await readScores(server.id, userID=author.id)
                    await say(msg, "Thank you for voting on {}.\nTheir score is now {}.".format(author.mention, targetScores[1]))

        except Exception as e:
            await throwError(msg, error=e, sayTraceback=True, printTraceback=True)
            return

    elif "r/" in content and not "http" in content:
        results = re.findall(r'(?:^| )\/?r\/([A-Za-z0-9_]{1,21})', content)
        for result in results:
            await linkSubreddit(msg, result.strip())

    elif "git " in content:
        gitCommand = re.split(r'^git\s|\sgit\s', content, flags=re.I)
        if len(gitCommand) > 1:
            gitArg = gitCommand[1].split(' ', 1)[0]
            output = "`>  git: '{}' is not a git command. See 'git --help'.`".format(gitArg)
            await say(msg, output)


    elif content in ['what','what?','wat','wat?','wut','wut?','nani','nani?','huh?']:
        try:
            targetMessage = None

            async for targetMessageTemp in msg.channel.history(limit=2):
                targetMessage = targetMessageTemp

            if targetMessage is not None:
                await say(msg, "**{}**".format(targetMessage.content.replace("**","").upper()))
        except:
            return


    elif content in ['time', 'time?', 'time.', 'time!']:
        now = datetime.datetime.now()
        await say(msg, "It is currently {}, my dude!".format(now.strftime('%H:%M')))

    elif content in ['this is so sad', 'this is sad', 'this is so sad, alexa play despacito', \
        'this is so sad. alexa play despacito', 'this is so sad. alexa, play despacito', \
        'this is so sad, play despacito', 'this is so sad. play despacito', \
        'this is so sad alexa play despacito', 'this is so sad.', 'this is sad.', \
        'this is so sad, alexa play despacito.', 'this is so sad. alexa play despacito.', \
        'this is so sad. alexa, play despacito.', 'this is so sad, play despacito.', \
        'this is so sad. play despacito.', 'this is so sad alexa play despacito.']:
        await say(msg, 'ɴᴏᴡ ᴘʟᴀʏɪɴɢ: Despacito\n─────⚪────────────────────────────\n◄◄⠀▐▐ ⠀►►⠀⠀ ⠀ 1:17 / 3:48 ⠀ ───○ 🔊⠀ ᴴᴰ ⚙ ❐ ⊏⊐')
        await playSound(msg, voiceCommands[80], True)
        return

    elif client.user.mentioned_in(msg) and not msg.mention_everyone:
        await say(msg, 'Use {}{} for a list of commands'.format(serverInvoker, textCommands[0]['Command']))
        return

    # Not `elif` so it can work with other commands
    if "scp" in content:
        await scp(msg, content)

def isPlaying(guild):
    vs = getVoiceClient(guild)
    return vs and vs.is_playing()

def getVoiceClient(guild):
    return guild.voice_client

async def setServerConfig(guildID, configKey, newValue, type=0, msg=None):
    """Modifies a config value in the guild's server's config file

    Parameters
            ----------
            msg : Discord.message, optional
                The message context to be used for replying (default is None)
            guildID : int or str
                The guild id to fetch configs from
            configKey : str
                The key to retrieve the value from
            newValue : int, str, list
                Value to append-to/remove-from/replace the old config value
            type : int (0, 1, -1), optional
                Represents the operation for the new value to interact with the old one. 
                0 is replace, 1 is add-to, and -1 is remove-from (default is 0)
    """
    oldValue = await getServerConfig(guildID, ['configs', configKey])
    newValue = newValue.replace('@!','@')
    with open('config/server_configs/%s.json' % (guildID), encoding='utf8') as f:
        serverConfigsFile = json.load(f)
    if type == 0:
        if not isinstance(serverConfigsFile['configs'][configKey], list) and isinstance(config[configKey][0], int) and newValue.isdigit():
            serverConfigsFile['configs'][configKey] = int(newValue)
        elif not isinstance(serverConfigsFile['configs'][configKey], list) and isinstance(config[configKey][0], int):
            await throwError(msg, 'This config value must be a positive integer', custom=True, printError=False)
            return
        elif isinstance(serverConfigsFile['configs'][configKey], list):
            try:
                newValueList = shlex.split(newValue)
            except ValueError:
                newValueList = newValue.split()
            serverConfigsFile['configs'][configKey] = newValueList
        else:
            serverConfigsFile['configs'][configKey] = newValue
    elif type == 1:
        if(isinstance(serverConfigsFile['configs'][configKey], list)):
            if newValue not in oldValue:
                try:
                    newValueList = shlex.split(newValue)
                except ValueError:
                    newValueList = newValue.split()
                if any(elem in newValueList for elem in serverConfigsFile['configs'][configKey]):
                    await throwError(msg, 'You cannot add a that value to that config because it already exsists', custom=True, printError=False)
                    return
                serverConfigsFile['configs'][configKey].extend(newValueList)
            else:
                await throwError(msg, 'You cannot add a that value to that config because it already exsists', custom=True, printError=False)
                return
        else:
            await throwError(msg, 'You cannot add a new value to that config because it\'s not a list', custom=True, printError=False)
            return
    elif type == -1:
        if(isinstance(serverConfigsFile['configs'][configKey], list)):
            try:
                try:
                    newValueList = shlex.split(newValue)
                except ValueError:
                    newValueList = newValue.split()
                if not set(newValueList).issubset(serverConfigsFile['configs'][configKey]):
                    raise ValueError
                serverConfigsFile['configs'][configKey] = [x for x in serverConfigsFile['configs'][configKey] if x not in set(newValueList)]
            except ValueError:
                await throwError(msg, 'You cannot remove that value because it doesn\'t already exist in that list', custom=True, printError=False)
                return
        else:
            await throwError(msg, 'You cannot remove a value from that config because it\'s not a list', custom=True, printError=False)
            return
    with open('config/server_configs/%s.json' % (guildID), 'w', encoding='utf8') as f:
        json.dump(serverConfigsFile, f, indent=4)
    embed = discord.Embed(title="Config was changed", color=embedColor)
    embed.add_field(name=configKey, value=config[configKey][1], inline=False)
    embed.add_field(name="From", value=oldValue, inline=False)
    embed.add_field(name="To", value=serverConfigsFile['configs'][configKey], inline=False)
    await say(msg, "", embed=embed)
    return

async def getServerConfig(guildID, configKeys, maxRecursiveAttempts=3, recursiveAttempts=0):
    """Retreves a config value from the guild's server's config file

    Parameters
            ----------
            guildID : int or str
                The guild id to fetch configs from
            configKeys : list
                A list containing the keys to retrieve the value from
            recursiveAttempts : int, optional
                Internal value to track the current recursion level (default is 0)
            maxRecursiveAttempts : int, optional
                Maximum levels of recursion attempts to read the config file (default is 3)
    """
    if recursiveAttempts > maxRecursiveAttempts or not configKeys or (isinstance(guildID, str) and not guildID.isdigit()):
        return None
    try:
        with open('config/server_configs/%s.json' % (guildID), encoding='utf8') as f:
            serverConfigsFile = json.load(f)
            # create the directory if it doesn't exist
    except FileNotFoundError:
        if not os.path.exists(os.path.dirname('config/server_configs/')):
            try:
                os.makedirs(os.path.dirname('config/server_configs/'))
            except OSError as e:
                throwError(None, error=e, fatal=True)
        with open('config/server_configs/%s.json' % (guildID), 'w', encoding='utf8') as f:
            serverConfigsFile = {}
            json.dump({'guild_id': guildID, 'guild_name': client.get_guild(int(guildID)).name, 
                'configs': {'guild_admins': [client.get_guild(int(guildID)).owner.mention.replace('@!','@')],
                'invoker': config['invoker'][0], 'vote_limit': config['vote_limit'][0], 'gild_limit': config['gild_limit'][0], 
                'point_value_in_currency': config['point_value_in_currency'][0], 'gilding_value_in_currency': config['gilding_value_in_currency'][0],
                'currency_symbol': config['currency_symbol'][0], 'weekly_score_decay': config['weekly_score_decay'][0], 
                'bad_word_response': config['bad_word_response'][0], 'bad_words': config['bad_words'][0],
                'bad_words_exceptions': config['bad_words_exceptions'][0]}}, f, indent = 4)
        return await getServerConfig(guildID, configKeys, recursiveAttempts + 1)
    if not isinstance(configKeys, list):
        configKeys = [configKeys]
    recursiveValueSearch = serverConfigsFile
    try:
        for key in configKeys:
            recursiveValueSearch = recursiveValueSearch[key]
        return recursiveValueSearch
    except KeyError:
        await throwError(None, 'The server config value at key(s) %s could not be found' % (configKeys), custom=True, vocalize=False, printError=True)
        return None

async def isGuildAdmin(guildID, userMention):
    guildAdmins = await getServerConfig(guildID, ['configs','guild_admins'])
    return userMention.replace('@!','@') in guildAdmins

async def isBotAdmin(userMention):
    return userMention.replace('@!','@') in userInfo['security']['admins']

async def scp(msg, content):
    response = await respond_to_scp_references(content)
    if response != "":
        # Unpack response
        (title, url, exists, id_number, suffix) = response

        if not exists:
            await say(msg, "{} does not exist in the SCP Wiki.".format(title))
        else:
            embed = discord.Embed(title=title, url=url, color=embedColor)
            # TODO scrape website and add fields
            #embed.add_field(name='Description', value=desc)
            await say(msg, "", embed=embed)

async def playSound(msg, command, silent=False):
    if isPlaying(msg.guild):
        if not silent:
            await throwError(msg, 'I\'m already playing a sound! Please wait your turn.', custom=True, printError=False)
        return
    elif msg.author.voice and msg.author.voice.channel:
        try:
            channel = msg.author.voice.channel
            voice = get(client.voice_clients, guild=msg.guild)

            if not voice:
                voice = await channel.connect()

            sounds = command['SoundFile'].split("#")
            sound = random.choice(sounds)
            
            player = discord.FFmpegPCMAudio('res/sound/' + sound + fileExt)
            voice.play(player)
            client.loop.create_task(donePlaying(msg.guild))
        except Exception as e:
            if not silent:
                await throwError(msg, 'There was an issue playing the sound file 🙁', custom=True)
            return
    else:
        if not silent:
            await throwError(msg, 'You\'re not in a voice channel!', custom=True, printError=False)
    return

async def linkSubreddit(msg, sub):
    exists = True
    try:
        reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_agent)
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    if exists:
        if reddit.subreddit(sub).over18 and msg.channel.is_nsfw() or not reddit.subreddit(sub).over18:
            embed = discord.Embed(title="r/"+sub, url="http://old.reddit.com/r/{}".format(sub), color=embedColor)
            await say(msg, "", embed)
        else:
            await react(msg, '😲')

async def subreddit(msg, sub, bypassErrorCheck=False, args=[], filterNSFW=-1, filtertype='hot', pool=50):
    maxPoolSize = 1000
    softMaxPoolSize = 500

    if not bypassErrorCheck and sub.strip() == "":
        await helpCommand('reddit', msg)
        return

    # ----- Args -----
    if len(args) > 0:
        if any(x in args for x in ['filtered', 'filternsfw', 'safe', 'sfw']):
            filterNSFW = 1
        if any(x in args for x in ['nsfw', 'nsfwonly', 'lewd']):
            filterNSFW = 0
        if any('pool=' in s for s in args):
            matching = [a for a in args if 'pool=' in a]
            try:
                pool=int(matching[0].partition('=')[2]) if matching[0].partition('=')[2] is not '' else pool
            except TypeError:
                pool = pool
        if any('type=' in s for s in args):
            matching = [a for a in args if 'type=' in a]
            filtertype=matching[0].partition('=')[2] if matching[0].partition('=')[2] is not '' else filtertype
    # ----- Args -----

    reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_agent)
    submissionList = []
    if pool > softMaxPoolSize:
        if pool > maxPoolSize:
            pool = maxPoolSize
            await throwError(msg, "1000 is the maximum pool size! This may take a while...", custom=True, printError=False)
        else:
            await throwError(msg, "Pools greater than 500 may take several minutes...", custom=True, printError=False)
    if filtertype not in ['hot', 'new', 'top', 'controversial', 'gilded']:
        filtertype = 'hot'

    try:
        await msg.channel.trigger_typing()
        sub = str(sub)
        for s in sub.split('+'):
            if reddit.subreddit(s).over18:
                if not await checkNSFW(msg):
                    return
        filt = getattr(reddit.subreddit(sub), filtertype)
        submissions = filt(limit=pool)
        for submission in submissions:
            extensions = ["png","jpg","jpeg","gif"]
            if any([ext in submission.url[-len(ext):] for ext in extensions]):
                submissionList.append(submission)
        if filterNSFW != -1:
            submissionList = list(filter(lambda x: x.over_18 != filterNSFW, submissionList))
        if len(submissionList) > 0:
            submission = submissionList[random.randint(0, len(submissionList)-1)]
            embed = discord.Embed(title=submission.title, 
                url="https://reddit.com{}".format(submission.permalink), color=embedColor)
            embed.set_image(url=submission.url)
            embed.set_footer(text=" via reddit.com/r/{}".format(str(submission.subreddit)), 
                icon_url="http://www.google.com/s2/favicons?domain=www.reddit.com")
            await say(msg, "Here's a {} post from r/{}".format(filtertype, str(submission.subreddit)), embed)
            return
        else:
            await throwError(msg, "There's nothing I can post in that subreddit!", custom=True, printError=False)
    except:
        await throwError(msg, "reddit.com/r/{} couldn\'t be accessed.".format(sub), custom=True, printError=False)

async def broadcastGitRepo(msg):
    gitMessage = 'Check me out on GitHub, the only -Hub website you visit, I hope...'                                                                                      
    embed = discord.Embed(title="", description=gitLink, color=embedColor)                                
    await say(msg, gitMessage, embed)                                     
    return                                                                                              

async def say(msg, message, embed=None):
    if message is None:
        return
    sentMessage = None
    if embed == None:
        sentMessage = await sayInChannel(msg.channel, message)
    else:
        sentMessage = await sayInChannel(msg.channel, message, embed=embed)
    return sentMessage

async def sayInChannel(channel, message, embed=None):
    if message is None:
        return
    sentMessage = None
    if embed == None:
        sentMessage = await channel.send(message)
    else:
        sentMessage = await channel.send(message, embed=embed)
    return sentMessage

async def react(msg, emote):
    try:
        await msg.add_reaction(emote)
    except:
        try:
            reaction = emote.replace("<:", "")
            reaction = reaction.replace(">", "")
            reaction = reaction.split(':')[-1]
            reaction = client.get_emoji(int(reaction))
            await msg.add_reaction(reaction)
        except:
            try:
                reaction = next((x for x in msg.guild.emojis if x.name == emote), None)
                await msg.add_reaction(reaction)
            except:
                await throwError(msg, "I don't know that emoji: " + "`" + str(emote) + "`", custom=True, printError=False)
    return

async def stringToEmoji(msg, emote, globalEmotes=False, vocalizeMissing=False):
    string = emote
    emote = emote.replace("<", "")
    emote = emote.replace(">", "")
    emote = emote.replace(":", "")
    if globalEmotes:
        emote = next((x for x in client.emojis if x.name == emote), None)
    else:
        emote = next((x for x in msg.guild.emojis if x.name == emote), None)
    if not emote:
        await throwError(msg, "I don't know that emoji: " + "`" + str(emote) + "`", vocalize=vocalizeMissing, custom=True, printError=False)
        return string
    return emote

async def checkNSFW(msg):
    if not msg.channel.is_nsfw():
        await throwError(msg, "You can't do that here. This channel is not marked as NSFW.", custom=True, printError=False)
        return False
    return True

async def handleFunc(msg, filename, channel=None):

    variables = {}

    def setVar(key, value):
        variables[key] = value

    def getVar(key):
        if key not in variables:
            setVar(key, 0)
        return variables[key]

    def var(key, value=None):
        if value:
            setVar(key, value)
        else:
            return getVar(key)

    def isStringFuncCorutine(funcString, globalsVars, localVars):
        try:
            return inspect.iscoroutinefunction(eval(funcString.split('(', 1)[0], globalsVars, localVars))
        except:
            return False

    def isStringCallable(funcString):
        funcString = str(funcString)
        funcString = funcString.split('(', 1)[0] if '(' in funcString else funcString
        return callable(eval(funcString, commandMap, localVars))

    def sanitizeSpaces(arg, forward=False):
        if forward:
            sanatize = re.findall(r'''\"(.+?)\"''', arg)
            for result in sanatize:
                if result in arg:
                    modResult = result.replace(" ", "%20")
                    arg = arg.replace(result, modResult)
            return arg
        else:
            try:
                return arg.replace("%20", " ")
            except:
                return arg

    def formatArg(arg, spaceSeperated=False):
        if spaceSeperated:
            arg = re.sub(r'(.*)->(".*")', "var {} {}".format(r'\2', r'\1'), arg)
            arg = re.sub(r'(".*")<-(.*)', "var {} {}".format(r'\1', r'\2'), arg)

            arg = re.sub(r'(.*)->(.*)', "var {} \"{}\"".format(r'\2', r'\1'), arg)
            arg = re.sub(r'(.*)<-(.*)', "var \"{}\" {}".format(r'\1', r'\2'), arg)

            arg = formatArg(arg, False)
        else:
            arg = re.sub(r'(.*)->(".*")', "var({},{})".format(r'\2', r'\1'), arg)
            arg = re.sub(r'(".*")<-(.*)', "var({},{})".format(r'\1', r'\2'), arg)

            arg = re.sub(r'(.*)->(.*)', "var({},\"{}\")".format(r'\2', r'\1'), arg)
            arg = re.sub(r'(.*)<-(.*)', "var(\"{}\",{})".format(r'\1', r'\2'), arg)

            arg = re.sub(r'\|("[^\|]*")\|', "var({})".format(r'\1'), arg)
            arg = re.sub(r'\|([^\|]*)\|', "var(\"{}\")".format(r'\1'), arg)
        return arg

    commandMap = {"say":say, "subreddit":subreddit, "scoreDecay":scoreDecay, "sayAscii":sayAscii, "readScores":readScores, "react":react}
    data = {}
    if not msg:
        if not channel:
            async for message in channel.history(limit=2):
                msg = message
        else:
            await throwError(None, error="No message or channel objects provided", vocalize=False)
    try:
        with open("res/func/" + filename + ".func","r", encoding='utf8') as funcFile:
            data = funcFile.read()
            funcFile.close()
    except FileNotFoundError as e:
        await throwError(None, error="File {}.func not found!".format(filename), vocalize=False)
        return

    if data:
        lines = data.split("\n")
        for line in lines:
            line = sanitizeSpaces(line, True)
            localVars = {"msg":msg, "var":var}
            args = line.split(' ') if ' ' in line else [line]
            args = [formatArg(arg, spaceSeperated=(True if i == 0 else False)) for i, arg in enumerate(args)]
            tempArgs = []
            for i, arg in enumerate(args):
                if ' ' in arg:
                    tempArgs[i:i] = arg.split(' ')
                else:
                    tempArgs.insert(i, arg)
            args = list(filter(None, tempArgs))
            funcArgs = []
            for i, arg in enumerate(args[1:]):
                if isStringFuncCorutine(arg, commandMap, localVars):
                    funcArgs.append(await eval(sanitizeSpaces(arg), commandMap, localVars))
                else:
                    funcArgs.append(eval(sanitizeSpaces(arg), commandMap, localVars))
            if args:
                if isStringCallable(args[0]):
                    if isStringFuncCorutine(args[0], commandMap, localVars):
                        await eval(sanitizeSpaces(args[0]), commandMap, localVars)(*funcArgs)
                    else:
                        eval(sanitizeSpaces(args[0]), commandMap, localVars)(*funcArgs)
                else:
                    eval(sanitizeSpaces(args[0]), commandMap, localVars)
    return

async def help(msg):
    embed = discord.Embed(title=name, description=desc, color=embedColor)                                
    embed.add_field(name="🥕 Prefix", value="```" + await getServerConfig(msg.guild.id, ['configs', 'invoker']) + "```", inline=False)
    if len(", ".join(textCommandList)) > 1000:
        tcSplitList = textwrap.wrap(", ".join(textCommandList), 1000)
        embed.add_field(name='🔤 Text Commands', value=tcSplitList[0], inline=False)
        for i in range(1, math.ceil(len(", ".join(textCommandList)) / 1000)):
            embed.add_field(name='🔤 Text Commands Part %s' % str(i+1), value=tcSplitList[i], inline=False)
    else:
        embed.add_field(name="🔤 Text Commands", value=", ".join(textCommandList), inline=False)                  
    if len(", ".join(voiceCommandList)) > 1000:
        vcSplitList = textwrap.wrap(", ".join(voiceCommandList), 1000)
        embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel', value=vcSplitList[0], inline=False)
        for i in range(1, math.ceil(len(", ".join(voiceCommandList)) / 1000)):
            embed.add_field(name='🔊 Voice Commands Part %s' % str(i+1), value=vcSplitList[i], inline=False)
    else:
        embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel', value=", ".join(voiceCommandList), inline=False)
    if msg.channel.is_nsfw():
        if len(", ".join(nsfwCommandList)) > 1000:
            nsfwcSplitList = textwrap.wrap(", ".join(nsfwCommandList), 1000)
            embed.add_field(name='😲 NSFW Commands - These require you to be in a NSFW channel', value=nsfwcSplitList[0], inline=False)
            for i in range(1, math.ceil(len(", ".join(nsfwCommandList)) / 1000)):
                embed.add_field(name='😲 NSFW Commands Part %s' % str(i+1), value=nsfwcSplitList[i], inline=False)
        else:
            embed.add_field(name='😲 NSFW Commands - These require you to be in a NSFW channel', value=", ".join(nsfwCommandList), inline=False)
    embed.set_footer(text="Created by {}".format(config['creator']))                                    

    await say(msg, "", embed)                                                 
    return                                                                                        

async def helpCommand(command, msg):

    args = command.strip().split(" ")[1:] if len(command.strip().split(" ")) > 1 else ''
    
    command = command.strip().split(" ")[0]

    if command not in commandList and command not in commandAlias:
        await say(msg, "That's not a command I know or it is an alias.")
        return
    serverInvoker = await getServerConfig(msg.guild.id, ['configs', 'invoker'])
    embed = discord.Embed(title="Command:", description=command, color=embedColor)
    embed.add_field(name="Description:", value=commandHelp[commandList.index(command)], inline=False)
    embed.add_field(name="Usage:", value="```" + serverInvoker + command + " " + commandParams[commandList.index(command)] + "```", inline=False)
    if ('-e' in args or 'example' in args or 'all' in args) and command in textCommandList:
        examples = []
        for example in textCommandExample[commandList.index(command)]:
            examples.append(serverInvoker + example)
        if not examples:
            examples.append('None')
        embed.add_field(name="Examples:", value="```\n" + '\n'.join(examples) + "```", inline=False)
    if '-a' in args or 'alias' in args or 'all' in args:
        aliases = []
        for alias in commandAlias[commandList.index(command)]:
            if alias:
                aliases.append(serverInvoker + alias)
        if not aliases:
            aliases.append('None')
        embed.add_field(name="Alias:", value=', '.join(aliases), inline=False)
    await say(msg, "", embed)
    return

async def sayAscii(msg, message):
    ascii = []
    message = message.lower()
    output = ""
    limit = 6
    if len(message) > limit:
        await sayAscii(msg, message[:limit])
        await sayAscii(msg, message[limit:])
        return
    for letter in list(message):
        if letter in bubbleFontMask:
            ascii.append(bubbleFont[bubbleFontMask.index(letter)])
    for i in range(0, limit):
        for letterBlock in ascii:
            letterBreakdown = letterBlock.splitlines()
            for j, line in enumerate(letterBreakdown):
                while len(line) < limit-1:
                    line += " "
                    letterBreakdown[j] += "╱"
            output = output + letterBreakdown[i]
        output = output + '\n'

    await say(msg, output)

async def setPlaying(name, activitytype=0):
    try:
        activitytype = int(activitytype)
    except:
        activityTypes = ['playing', 'streaming', 'listening', 'watching']
        if isinstance(activitytype, str):
            if activitytype.lower() in activityTypes:
                activitytype = activityTypes.index(activitytype.lower())
            else:
                activitytype = 0
        else:
            activitytype = 0
    activityEnumType = [discord.ActivityType.playing, discord.ActivityType.streaming, discord.ActivityType.listening, discord.ActivityType.watching]
    activityTypeIndexClamped = 3 if activitytype > 3 else (0 if activitytype < 0 else activitytype)
    activity = discord.Activity(type=activityEnumType[activityTypeIndexClamped], name=name)
    await client.change_presence(activity=activity)
    return

async def sayIPA(msg, text):
    await msg.channel.trigger_typing()
    IPA_text = await getIPA(text)
    if IPA_text == '':
        await throwError(msg, "I wasn't able to convert that word!", custom=True, printError=False)
    elif IPA_text == None:
        await throwError(msg, "I couldn't access `{}`!".format(url), custom=True)
    await say(msg, IPA_text)

async def getIPA(text):
    IPA_text = ''
    try:
        with requests. Session() as c: 
            url = 'https://tophonetics.com/'
            c.get(url)
            data = dict(text_to_transcribe=text, output_dialect='am', submit="Show+transcription")
            page = c.post(url, data=data, headers={"Referer": "https://tophonetics.com/"})
            soup = BeautifulSoup(page.text, 'html.parser')
            try:
                IPA_text = "/%s/" % (soup.find(id='transcr_output').text)
            except AttributeError:
                pass
    except:
        return None
    return IPA_text

async def defineUrban(msg, message=None, term='', num=1, edit=None):

    serverInvoker = await getServerConfig(msg.guild.id, ['configs', 'invoker'])

    async def getPayload():
        async with session.get("http://api.urbandictionary.com/v0/define", params={"term": search}) as resp:
            return await resp.json()

    async with aiohttp.ClientSession(headers={"User-Agent": "{}".format(client.user)}) as session:
        number = num
        if message is not None:
            term = message.strip()
            regexResult = list(filter(None, re.compile(r'page ([1-9]{1,3})$|-p ([1-9]{1,3})$').split(term)))
            if len(regexResult) > 1:
                number = regexResult[1]
                term = regexResult[0]
                await defineUrban(msg, term=term, num=int(number))
        if not term:
            return
        search = "\""+term+"\""
        if not edit:
            await msg.channel.trigger_typing()
            result = await getPayload()
        else:
            result = await getPayload()
        if not result["list"]:
            await say(msg, "{} couldn't be found on Urban Dictionary.".format(term))
        else:
            try:
                top_result = result["list"][int(number) - 1]
                result_definition = top_result["definition"][:800] + "..." if len(top_result["definition"]) > 800 else top_result["definition"]
                example = top_result["example"][:800] + "..." if len(top_result["example"]) > 800 else top_result["example"]
                embed = discord.Embed(title=top_result["word"], description=result_definition, url=top_result["permalink"])
                if top_result["example"]:
                    embed.add_field(name="Example:", value=example)
                embed.set_author(name="Submitted by " + top_result["author"],
                                 icon_url="https://lh5.ggpht.com/oJ67p2f1o35dzQQ9fVMdGRtA7jKQdxUFSQ7vYstyqTp-Xh-H5BAN4T5_abmev3kz55GH=w300")
                number = str(int(number) + 1)
                if num < len(result["list"]):
                    embed.set_footer(text="{} results were found. To see a different result, use {}{} {} -p {}.".format( 
                        len(result["list"]), serverInvoker, textCommands[11]['Command'], term, number))
                else:
                    embed.set_footer(text="{} results were found.".format(len(result["list"])))
                definition = edit
                if definition is not None:
                    await definition.edit(embed=embed)
                else:
                    definition = await say(msg, "", embed=embed)
                if num > 1:
                    await react(definition, "⬅")
                if num < len(result["list"]):
                    await react(definition, "➡")
                def check(reaction, user):
                    return reaction.message.id == definition.id and user == msg.author and (str(reaction.emoji) == "⬅" or str(reaction.emoji) == "➡")
                res = None
                try:
                    res = await client.wait_for('reaction_add', timeout=20.0, check=check)
                    if num > 1:
                        await definition.remove_reaction("⬅", msg.author)
                        await definition.remove_reaction("⬅", definition.author)
                    if num < len(result["list"]):
                        await definition.remove_reaction("➡", msg.author)
                        await definition.remove_reaction("➡", definition.author)
                except asyncio.TimeoutError:
                    await definition.remove_reaction("⬅", definition.author)
                    await definition.remove_reaction("➡", definition.author)
                    return
                else:
                    if res is None:
                        return
                    await defineUrban(msg, term, num=(num + ( 1 if res[0].emoji == "➡" else -1)), edit=definition)
                    return

            except IndexError:
                await say(msg, "That result doesn't exist! Try {}{} {}.".format(serverInvoker, textCommands[11]['Command'], term))

            except Exception as e:
                await throwError(msg, e, vocalize=False)
        return 

async def defineGoogle(msg, message):
    await msg.channel.trigger_typing()
    async with aiohttp.ClientSession() as session:
        term = message.strip()
        search = term.split(" ")[0]
        async with session.get("https://api.dictionaryapi.dev/api/v2/entries/en/%s" % (search)) as resp:
            try:
                payload = await resp.json(content_type=None)
                if isinstance(payload, dict):
                    raise Exception
            except:
                payload = [{'failure': True}]

        embed=discord.Embed(color=embedColor)
        embed.set_thumbnail(url="http://icons.iconarchive.com/icons/osullivanluke/orb-os-x/48/Dictionary-icon.png")

        values = payload[0]
        word = values.get('word', '')
        ipa = values.get('phonetic', await getIPA(word))

        embed.add_field(name="{}".format(word), value="{}".format(ipa), inline=False)

        for entry in values.get('meanings', []):  
            partOfSpeech = entry.get('partOfSpeech', 'Unknown')
            definitions = ""
            definitionCount = 1
            for defin in entry.get('definitions', [])[:3]:
                definition = defin.get('definition', 'Unknown')
                example = defin.get('example', '')
                synonyms = ', '.join(defin.get('synonyms', [])[:4])
                  
                seperator = "_ _\n" if definitionCount == 1 else ""
                definitions += str(definitionCount) + ". " + definition + "\n" + ('_%s_' % (synonyms) + "\n" if synonyms else '')
                definitionCount += 1

            embed.add_field(name=partOfSpeech, value="{}".format(definitions), inline=False)
        embed.set_footer(text="Powered by dictionaryapi.dev")

        if not values.get('failure', False):
            await say(msg, "", embed=embed)
            return
        else:
            await say(msg, "I couldn't define {}.".format(term))
            
        return 

async def mock(msg, *, text=""):
            #check for string or message id
        if text.isdigit():
            async for message in msg.channel.history(limit=100):
                if text == str(message.id):
                    text = message.content
        elif text == "":
            async for message in msg.channel.history(limit=2):
                text = message.content

            #randomize
        fakeresult = ""
        for char in text:
            value = random.choice([True, False])
            if value == True:
                fakeresult += char.upper()
            if value == False:
                fakeresult += char.lower()

            #ensure random isn't too random™
        caps = ""
        for char in fakeresult:
            if char.isupper():
                caps += "1"
            else:
                caps += "0"
        while "000" in caps or "111" in caps:
            caps = caps.replace("111", "101").replace("000", "010")
        result = ""
        for idx, char in enumerate(fakeresult):
            if caps[idx] == "0":
                result += char.lower()
            else:
                result += char.upper()

        if result == "":
            await say(msg, "Yo, dude! I can't dispatch a blank message! This can happen if you try to mock an embedded message.")
        else:
            await say(msg, result)

async def hasItem(guildID, user, item, qty=1):
    existingScore = await readScores(guildID, user)
    inventory = ast.literal_eval(existingScore[6])
    return True if item in inventory and inventory[item] >= qty else False

async def writeScore(guildID, user, score=0, gilding=0, voted=0, gilded=0, currency=0, inventory={}, ignoreItems=False):
    if not ignoreItems:
    ###### Item ######
        if await hasItem(guildID, user, 'ActiveEvilEye'):
            score *= 2
    ##################

    # Create file if it doesn't already exist
    try:
        with open("res/data/server_data/%s.dat" % (guildID), encoding='utf8') as f:
            pass
    except FileNotFoundError:
        # Create the directory is it doesn't already exist
        if not os.path.exists(os.path.dirname('res/data/server_data/')):
            try:
                os.makedirs(os.path.dirname('res/data/server_data/'))
            except OSError as e:
                throwError(None, error=e, fatal=True)
        with open("res/data/server_data/%s.dat" % (guildID), 'w', encoding='utf8') as f:
            pass

    userObj = "USER={} SCORE={} GILDING={} VOTED={} GILDED={} CURRENCY={} INVENTORY={}".format(user, str(score), str(gilding), 
        str(voted), str(gilded), str(currency), str(inventory).replace(' ',''))
    existingScores = await readScores(guildID)
    for existingScore in existingScores:
        if int(existingScore[0]) == user:
            oldUserObj = userObj
            newScore = str(int(existingScore[1]) + score)
            newGilding = str(int(existingScore[2]) + gilding) if (int(existingScore[2]) + gilding) > 0 else '0'
            newVoted = str(int(existingScore[3]) + voted) if (int(existingScore[3]) + voted) > 0 else '0'
            newGilded = str(int(existingScore[4]) + gilded) if (int(existingScore[4]) + gilded) > 0 else '0'
            newCurrency = str(int(existingScore[5]) + currency) if (int(existingScore[5]) + currency) > 0 else '0'
            newInventory = ast.literal_eval(existingScore[6])
            if inventory:
                if list(inventory.keys())[0] in newInventory:
                    newInventory[list(inventory.keys())[0]] += list(inventory.values())[0]
                else:
                    newInventory.update(inventory)
                if newInventory[list(inventory.keys())[0]] <= 0:
                    del newInventory[list(inventory.keys())[0]]
            newInventory = str(newInventory).replace(' ','')
            userObj = "USER={} SCORE={} GILDING={} VOTED={} GILDED={} CURRENCY={} INVENTORY={}".format(user, newScore, newGilding,
                newVoted, newGilded, newCurrency, newInventory)
            oldScores = await getScores(guildID)
            oldScores = oldScores.split("\n")[:-1]
            with open("res/data/server_data/%s.dat" % (guildID),"w") as scores:
                for oldScore in oldScores:
                    if oldScore.split(' ')[0] == oldUserObj.split(' ')[0]:
                        if not (newScore == '0' and newGilding == '0' and newVoted == '0' and newGilded == '0' and newCurrency == '0' \
                            and newInventory):
                            scores.write(userObj + "\n")
                    else:
                        scores.write(oldScore + "\n")
                scores.close()
                return
    with open("res/data/server_data/%s.dat" % (guildID), "a") as scores:
        scores.write(userObj + "\n")
        scores.close()
    return

async def readScores(guildID, userID=None):
    blankEntry = ['0','0','0','0','0','0','{}']
    data = await getScores(guildID)
    if not data:
        return blankEntry if userID is not None else [blankEntry]
    # Confusing as hell list comprehention
    # creates a list of lists. For each entry, it makes all the values into an element in a list and strips the key and '=' sign
    entries = [y.split(' ') for y in data.split("\n")[:-1]]
    guildEntries = [[x.split('=')[1] for x in entries[j]] for j in range(0, len(entries))]
    guildEntries.sort(key=lambda score:int(score[1]), reverse=True)
    if userID is not None:
        found = None
        for entry in guildEntries:
            if int(entry[0]) == userID:
                found = entry
                break
        if found is not None:
            return found
        else:
            return blankEntry
    else:
        return guildEntries
    return entries

async def getScores(guildID, iteration=0):
    try:
        with open("res/data/server_data/%s.dat" % (guildID),"r") as scores:
            data = scores.read()
            scores.close()
            return data
    except FileNotFoundError as e:
        # Create the directory is it doesn't already exist
        if not os.path.exists(os.path.dirname('res/data/server_data/')):
            try:
                os.makedirs(os.path.dirname('res/data/server_data/'))
            except OSError as e:
                throwError(msg, error=e, fatal=True)
        if iteration <= 1:
            with open("res/data/server_data/%s.dat" % (guildID),"w+") as scores:
                scores.close()
                await getScores(guildID, iteration=iteration+1)
        else:
            throwError(msg, e)

async def scoreDecayGuild(guildID):
    scores = await readScores(guildID)
    for i in range(0, await getServerConfig(guildID, ['configs', 'weekly_score_decay'])):
        for entry in scores:
            if int(entry[1]) == 0:
                continue
            elif int(entry[1]) > 0:
                await writeScore(int(guildID), int(entry[0]), score=-1, ignoreItems=True)
            else:
                await writeScore(int(guildID), int(entry[0]), score=1, ignoreItems=True)

async def scoreDecay(msg=None):
    if not msg:
        for guild in client.guilds:
            await scoreDecayGuild(guild.id)
    else:
        await scoreDecayGuild(msg.guild.id)

async def exchange(msg, args):
    serverPointValueInCurrency = await getServerConfig(msg.guild.id, ['configs', 'point_value_in_currency'])
    serverGildingValueInCurrency = await getServerConfig(msg.guild.id, ['configs', 'gilding_value_in_currency'])

    def pointsToCurrency(points):
        if points <= 0:
            return 0
        return points * serverPointValueInCurrency
    def gildingsToCurrency(gildings):
        if gildings <= 0:
            return 0
        return gildings * serverGildingValueInCurrency
    async def notEnoughToExchange(_type):
        await throwError(msg, "You cannot exchange your %s; you have negative or 0 %s." % (_type, _type), custom=True, printError=False)
        return
    async def unknownValue(value):
        await throwError(msg, "%s is not an amount I know." % (str(value)), custom=True, printError=False)
    amountQueried = 0
    scoreEntry = await readScores(msg.guild.id, msg.author.id)
    if args:
        serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
        if args[0] == 'all':
            returnCurrency = pointsToCurrency(int(scoreEntry[1])) + gildingsToCurrency(int(scoreEntry[2]))
            if returnCurrency <= 0:
                await notEnoughToExchange('points and gildings')
                return True
            confirmation = await confirm(msg, "Are you sure you want to exchange all your score points (%s) and gildings (%s) for %s%s?" % \
                (scoreEntry[1], scoreEntry[2], serverCurrencySymbol, str(returnCurrency)))
            if confirmation:
                await writeScore(msg.guild.id, msg.author.id, gilding=-int(scoreEntry[2]), score=-int(scoreEntry[1]), currency=returnCurrency, ignoreItems=True)
            else:
                return True
        elif args[0] in ['score','points','point','scores']:
            if len(args) <= 1 or (len(args) > 1 and args[1] == 'all'):
                returnCurrency = pointsToCurrency(int(scoreEntry[1]))
                if returnCurrency <= 0:
                    await notEnoughToExchange('points')
                    return True
                confirmation = await confirm(msg, "Are you sure you want to exchange all your score points (%s) for %s%s?" % \
                    (scoreEntry[1], serverCurrencySymbol, str(returnCurrency)))
                if confirmation:
                    await writeScore(msg.guild.id, msg.author.id, score=-int(scoreEntry[1]), currency=returnCurrency, ignoreItems=True)
                else:
                    return True
            else:
                try:
                    amountQueried = int(args[1])
                    if amountQueried > int(scoreEntry[1]):
                        amountQueried = int(scoreEntry[1])
                    returnCurrency = pointsToCurrency(amountQueried)
                    if returnCurrency <= 0:
                        await notEnoughToExchange('points')
                        return True
                    confirmation = await confirm(msg, "Are you sure you want to exchange %s score point%s for %s%s?" % \
                        (amountQueried, 's' if amountQueried > 1 else '', serverCurrencySymbol, str(returnCurrency)))
                    if confirmation:
                        await writeScore(msg.guild.id, msg.author.id, score=-amountQueried, currency=returnCurrency, ignoreItems=True)
                    else:
                        return True
                except ValueError:
                    await unknownValue(args[1])
        elif args[0] in ['gildings','gild','gilding','gold']:
            if len(args) <= 1 or (len(args) > 1 and args[1] == 'all'):
                returnCurrency = gildingsToCurrency(int(scoreEntry[2]))
                if returnCurrency <= 0:
                    await notEnoughToExchange('gildings')
                    return True
                confirmation = await confirm(msg, "Are you sure you want to exchange all your gildings (%s) for %s%s?" % \
                    (scoreEntry[2], serverCurrencySymbol, str(returnCurrency)))
                if confirmation:
                    await writeScore(msg.guild.id, msg.author.id, gilding=-int(scoreEntry[2]), currency=returnCurrency, ignoreItems=True)
                else:
                    return True
            else:
                try:
                    amountQueried = int(args[1])
                    if amountQueried > int(scoreEntry[2]):
                        amountQueried = int(scoreEntry[2])
                    returnCurrency = gildingsToCurrency(amountQueried)
                    if returnCurrency <= 0:
                        await notEnoughToExchange('gildings')
                        return True
                    confirmation = await confirm(msg, "Are you sure you want to exchange %s gilding%s for %s%s?" % \
                        (amountQueried, 's' if amountQueried > 1 else '', serverCurrencySymbol, str(returnCurrency)))
                    if confirmation:
                        await writeScore(msg.guild.id, msg.author.id, gilding=-amountQueried, currency=returnCurrency, ignoreItems=True)
                    else:
                        return True
                except ValueError:
                    await unknownValue(args[1])
        else:
            return False
        await displayCurrency(msg, msg.author)
        return True


async def giveCurrency(msg, otherUser, amount):
    scoreEntry = await readScores(msg.guild.id, msg.author.id)
    if int(scoreEntry[5]) < 1:
        await throwError(msg, "You're broke, my dude! You can't give anything!", custom=True, printError=False)
        return
    if amount > int(scoreEntry[5]):
        amount = int(scoreEntry[5])
    await writeScore(msg.guild.id, msg.author.id, currency=-int(amount), ignoreItems=True)
    await writeScore(msg.guild.id, otherUser.id, currency=int(amount), ignoreItems=True)

    displayName = otherUser.display_name
    nick = otherUser.nick
    nick = displayName if nick is None else nick

    scores = await readScores(msg.guild.id, userID=otherUser.id)
    currency = scores[5]
    serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
    embed = discord.Embed(title="{}:".format("You got money!"), 
        description="{} -> {} {}{}".format(msg.author.mention, otherUser.mention, serverCurrencySymbol, amount), 
        color=embedColor)
    embed.add_field(name="_You now have {}{}_".format(serverCurrencySymbol, currency), 
        value="_{} now has {}{}_".format(msg.author.mention, serverCurrencySymbol, int(scoreEntry[5]) - amount))
    embed.set_thumbnail(url="https://i.imgur.com/BVRyJEr.png")
    await say(msg, "{}".format(otherUser.mention), embed=embed)
    return

async def displayCurrency(msg, target):
    displayName = target.display_name
    nick = target.nick
    nick = displayName if nick is None else nick

    scores = await readScores(msg.guild.id, userID=target.id)
    currency = scores[5]
    serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
    embed = discord.Embed(title="{}:".format("You have" if target == msg.author else nick + " has"), 
        description="_{}{}_".format(serverCurrencySymbol, currency), 
        color=embedColor)
    embed.set_thumbnail(url="https://i.imgur.com/BVRyJEr.png")
    await say(msg, "", embed=embed)
    return

async def displayEveryonesCurrency(msg):
    scores = await readScores(msg.guild.id)
    try:
        scores.sort(key=lambda score:int(score[5]), reverse=True)
    except:
        pass
    embed = discord.Embed(title="Balance:", description="_ _")
    serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
    for scoreEntry in scores:
        try:
            user = await client.fetch_user(scoreEntry[0])
            balance = scoreEntry[5]
            if balance != '0':
                displayName = user.display_name
                nick = msg.guild.get_member(user.id).nick
                nick = displayName if nick is None else nick
                sanitizedDisplayName = displayName.replace('_','\_')
                displayName = "_AKA {}_\n".format(sanitizedDisplayName) if nick != displayName else ''
                embed.add_field(name=nick, value="{}{}{}".format(displayName, serverCurrencySymbol, balance), inline=True)
        except:
            continue
    await say(msg, "", embed=embed)
    return

async def displayTopCurrency(msg, amount=3):
    scores = await readScores(msg.guild.id)
    try:
        scores.sort(key=lambda score:int(score[5]), reverse=True)
    except:
        pass
    embed = discord.Embed(title="Balance:", description="_ _")
    serverCurrencySymbol = await getServerConfig(msg.guild.id, ['configs','currency_symbol'])
    for scoreEntry in scores[:amount]:
        try:
            user = await client.fetch_user(scoreEntry[0])
            balance = scoreEntry[5]
            if balance != '0':
                displayName = user.display_name
                nick = msg.guild.get_member(user.id).nick
                nick = displayName if nick is None else nick
                sanitizedDisplayName = displayName.replace('_','\_')
                displayName = "_AKA {}_\n".format(sanitizedDisplayName) if nick != displayName else ''
                embed.add_field(name=nick, value="{}{}{}".format(displayName, serverCurrencySymbol, balance), inline=False)
        except:
            continue
    await say(msg, "", embed=embed)
    return

async def confirm(msg, string):
    confirmMessage = await say(msg, string)
    yesEmoji = '✅'
    noEmoji = '❌'
    await react(confirmMessage, yesEmoji)
    await react(confirmMessage, noEmoji)
    def check(reaction, user):
        return reaction.message.id == confirmMessage.id and user == msg.author and (str(reaction.emoji) in [yesEmoji, noEmoji])
    res = None
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
        await confirmMessage.remove_reaction(yesEmoji, confirmMessage.author)
        await confirmMessage.remove_reaction(noEmoji, confirmMessage.author)
        if str(reaction.emoji) == yesEmoji:
            return True
        else:
            return False
    except asyncio.TimeoutError:
        await confirmMessage.remove_reaction(yesEmoji, confirmMessage.author)
        await confirmMessage.remove_reaction(noEmoji, confirmMessage.author)
        return False
    except:
        return False
    return False

async def mal(msg, name, mediaType="anime", displayFormat="tv"):

    async def notFound():
        await throwError(msg, "{} couldn't be found on MyAnimeList.".format(name), vocalize=True, custom=True, printError=False)

    await msg.channel.trigger_typing()
    name = parse.quote_plus(name)
    async with aiohttp.ClientSession(headers={"User-Agent": "{}".format(client.user)}) as session:
        #async with session.get("https://api.jikan.moe/v3/search/{0}?q={1}&type={2}&page=1".format(mediaType, name, displayFormat)) as resp:
        async with session.get("https://api.jikan.moe/v3/search/{0}?q={1}&page=1".format(mediaType, name)) as resp:
            result = await resp.json()
            results = None
            try:
                results = result["results"]
            except:
                pass
        try:
            if result["error"]:
                await notFound()
                return
        except:
            pass
        if not results:
            await notFound()
            return
        else:
            try:
                top_result = results[0]
                result_id = top_result["mal_id"]
                result_image = top_result["image_url"]                
                
                async with session.get("https://api.jikan.moe/v3/{0}/{1}".format(mediaType, result_id)) as resp:
                    result = await resp.json()
                try:
                    if result["error"]:
                        await notFound()
                        return
                except:
                    pass
                try:
                    result_name = html.unescape(result["title"])
                    result_name_english = result["title_english"]
                    result_url = 'https://myanimelist.net/{0}/{1}'.format(mediaType, result_id)
                    result_type = result.get("type")
                    result_score = result.get("score")
                    result_episodes = result.get("episodes")
                    result_rank = result.get("rank")
                    result_status = result.get("status")
                    result_air_time = result.get("aired_string")
                    result_synopsis = result.get("synopsis")

                    try:
                        result_synopsis = html.unescape(result.get("synopsis"))
                    except:
                        pass

                    result_name = "Unknown" if result_name is None else result_name
                    result_name_english = "Unknown" if result_name_english is None else result_name_english
                    result_url = "Unknown" if result_url is None else result_url
                    result_type = "Unknown" if result_type is None else result_type
                    result_score = "?" if result_score is None else str(result_score)
                    result_episodes = "Unknown" if result_episodes is None else str(result_episodes)
                    result_rank = "Unknown" if result_rank is None else str(result_rank)
                    result_status = "Unknown" if result_status is None else result_status
                    result_air_time = "Unknown" if result_air_time is None else result_air_time
                    result_synopsis = "No synopsis available" if result_synopsis is None else result_synopsis
                    
                    embed = discord.Embed(description=result_url, colour=embedColor)
                    if result_name_english:
                        result_name_english = html.unescape(result_name_english)
                    else:
                        result_name_english = result_name
                    embed.add_field(name='English Title', value=result_name_english)
                    embed.add_field(name='Rank', value='#' + result_rank)
                    embed.add_field(name='Type', value=result_type)
                    episodes = 'Unknown' if result_episodes == '0' else result_episodes
                    embed.add_field(name='Episodes', value=episodes)
                    score = '?' if result_score == 0 else str(result_score) + '/10'
                    embed.add_field(name='Score', value=score)
                    embed.add_field(name='Status', value=result_status)
                    try:
                        synop = result_synopsis[:400].split('.')
                        text = ''
                        if len(synop)-1 <= 1:
                            text = synop[0]
                        for i in range(0, len(synop)-1):
                            text += synop[i] + '.'
                    except:
                        text = result_synopsis
                    embed.add_field(name='Synopsis', value=text + '..   [More »]({})'.format(result_url))
                    embed.add_field(name='Airing Time:', value=result_air_time.replace('?', 'Unknown'))
                    embed.set_thumbnail(url=result_image)
                    embed.set_author(name=result_name,
                                  icon_url='https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png')
                    embed.set_footer(text='Powered by api.jikan.moe')
                    await say(msg, "", embed=embed)

                except IndexError:
                    await notFound()
                except:
                    return
            except IndexError:
                await notFound()
            except Exception:
                return
        return 

async def clearDailyRestrictions():
    for guild in client.guilds:
        scores = await readScores(guild.id)
        for entry in scores:
            await writeScore(int(guildID), int(entry[0]), voted=-999, gilded=-999, ignoreItems=True)

async def onNewDay():
    await setDailyGame()
    await checkDailyEvents()
    await clearDailyRestrictions()

async def tickClock():
    now = datetime.datetime.now()
    realDate = "%d-%d-%d" % (now.day, now.month, now.year)

    with open("res/data/clock.dat","w") as clock:
        clock.write(realDate)
        clock.close()

async def getClock():
    date = "0-0-0"
    with open("res/data/clock.dat","r") as clock:
        date = clock.read()
        clock.close()
    return date

async def setDailyGame():
    now = datetime.datetime.now()
    await setPlaying(config['{}_game'.format(now.strftime("%A").lower())])

async def status_task(loop):
    while True:

        now = datetime.datetime.now()

        realDate = "%d-%d-%d" % (now.day, now.month, now.year)

        recordDate = await getClock()
        
        if recordDate != realDate:
            await tickClock()
            await onNewDay()

        if not loop:
            return
        await asyncio.sleep(60)

async def reloadDates():
    global date_list
    global dates
    try:
        with open('config/dates.json', encoding='utf8') as f:
            date_list = json.load(f, strict=False)
    except FileNotFoundError:
        with open('config/dates.json', 'w', encoding='utf8') as f:
            date_list = {}
            json.dump({'dates': [{"Name": "Safety Steve", "Day": 1, "Month": 4, "Year": 2018, 
                "Tag": "<@430061939805257749>", "Type": "birthday", "Message": "Happy #age #type, #tag!",
                "Channel": "lobby", "React": "🎉#🎂#🎊#🍰"}]}, f, indent = 4)
            await throwError(None, error="dates.json could not be reloaded because the file does not exsist! dates.json file created.", 
                vocalize=False, custom=True, printError=True)
    dates = date_list['dates']

async def checkDailyEvents():
    today = datetime.datetime.today()
    weekday = today.weekday()
    
    await reloadDates()

    for date in dates:
        dateDay = date['Day']
        dateMonth = date.get('Month', 0)
        dateYear = date.get('Year', 0)
        dateType = date['Type']

        if (today.day == dateDay and today.month == dateMonth) or (dateType == 'weekday' and weekday == dateDay):
            dateName = date['Name']
            dateMessage = date.get('Message')
            dateAge = today.year - dateYear
            dateOrdAge = ord(dateAge)
            dateTag = date.get('Tag', '')
            dateType = date['Type']
            dateChannels = date.get('Channel', 'None')
            reacts = date.get('React')
            dateFunc = date.get('Func')
            dateActivity = date.get('Activity')
            dateActivityType = date.get('ActivityType')
            formattedDateMessage = None

            if dateChannels:
                dateChannels = dateChannels.replace(" ", "").split('#')

            if reacts:
                reacts = reacts.split("#")

            if dateMessage:
                formattedDateMessage = dateMessage.replace("#day", str(dateDay))
                formattedDateMessage = formattedDateMessage.replace("#month", str(dateMonth))
                formattedDateMessage = formattedDateMessage.replace("#year", str(dateYear))
                formattedDateMessage = formattedDateMessage.replace("#name", str(dateName))
                formattedDateMessage = formattedDateMessage.replace("#age", str(dateOrdAge))
                formattedDateMessage = formattedDateMessage.replace("#tag", str(dateTag))
                formattedDateMessage = formattedDateMessage.replace("#type", str(dateType))

            for dateChannel in dateChannels:
                channel = client.get_channel(int(userInfo['channel_ids'][dateChannel] if not dateChannel.isdigit() \
                    else dateChannel)) if dateChannel != 'None' else ''
                if formattedDateMessage and channel:
                    reactCondition = await sayInChannelOnce(channel, formattedDateMessage) and reacts
                    async for message in channel.history(limit=1):
                        msg = message
                        break
                    if reactCondition:
                        for emojis in reacts:
                            await react(msg, emojis)
                if dateFunc:
                    data = {'id':0,'attachments':[],'embeds':[],'edited_timestamp':0,'type':discord.MessageType.default, \
                        'pinned':False,'mention_everyone':False,'tts': False,'content':''}
                    dummyMessage = discord.Message(state=None, channel=channel, data=data)
                    dummyMessage.author = client.user
                    dummyMessage.content = ""
                    dummyMessage.channel = channel
                    await handleFunc(dummyMessage, dateFunc, channel=channel)
                if dateActivity:
                    await setPlaying(dateActivity, dateActivityType)
    return

def writeLog(e, crash=False):
    logTime = datetime.datetime.now()
    filename = 'res/data/logs/log-{}.txt'.format(str(logTime).replace(' ','').replace(':','-')) if crash else 'res/data/logs/log.txt'
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            throwError(None, error=e, fatal=True)
            return
    with open(filename, 'a+', encoding='utf8') as log:
        log.write("Time: " + str(logTime) + "\n")
        log.write("-\/-----------------------------\/-" + "\n")
        log.write(str(e)+"\n")
        log.write("-/\-----------------------------/\-" + "\n")
        log.write("\n")
    return

async def sayInChannelOnce(channel, message, embed=None):
    today = datetime.datetime.combine(date.today(), datetime.time())
    async for msg in channel.history(limit=100, after=today):
        if msg.author == client.user and msg.content == message:
           return False
    await sayInChannel(channel, message, embed)
    return True

async def donePlaying(guild, waitTime=0.5):
    voiceClient = getVoiceClient(guild)
    while voiceClient and voiceClient.is_connected():
        if not voiceClient.is_playing():
            await voiceClient.disconnect()
        await asyncio.sleep(waitTime)

def clearTerminal():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system("clear && printf \'\\e[3J\'")

def ord(n):
    return "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

def findInfo():
    return

async def zalgo_ify(text, level=3):
    ''' Takes some normal text and zalgo-ifies it.
    
    Text is passed through a diacritic-adding phase as many times as specified
    (up to ten).

    Args:
        text (str): The string to be Zalgo-ified.
        level (int): The number of times the text will be passed through the
            system.

    Returns:
        str: Zalgo-ified text.
    '''

    async def zalgo_pass(text):
        ''' A single Zolgo-ification passthrough. '''

        # Chars in "Combining Diacritical Marks" Unicode block.
        combining_chars = [chr(n) for n in range(768, 878)]

        zalgo_text = ''
        for char in text:
            combining_char = random.choice(combining_chars)
            zalgo_text += char + combining_char
        return zalgo_text

    if level < 0:
        level = 1
    elif level > 10:
        level = 10

    # Discord strips diacritics when there's too many chars
    if len(text) > 30:
        level = 1

    for i in range(level):
        text = await zalgo_pass(text)

    return text

async def clapify(text):
    """ Puts clap emojis between words and makes everything all-caps. """

    # empty split() splits on *any* whitespace
    words = text.split()
    clappy_text = " 👏 ".join(words).upper()

    return clappy_text

async def respond_to_scp_references(text):
    """ Find references to SCPs is text, return their wiki entries if they
    exist.

    Returns an empty str if no proper references found. The following are valid
    SCP references: "SCP-400", "scp 400", "SCP-400j", "scp-400-ex", "scp 69 j",
    "SCP 01 ex".
    """
    package = ""
    # Capture the base number and suffix as different groups
    scp_references = re.findall("(^| )scp[ -]?(\d+)-?([a-z0-9:]*)", text.lower())
    message = ""

    for scp_ref in scp_references:
        id_number = scp_ref[1].zfill(3)  # eg. 69 -> 069
        suffix = "-" + scp_ref[2] if (scp_ref[2] != "") else ""  # Add dash to suffix if it exists
        prefixes = ["decomm:"]
        prefix = prefixes[0] if suffix == '-d' else ''

        formatted = id_number + suffix

        # Make and check URL.
        url = "http://www.scp-wiki.net/{}scp-{}".format(prefix, formatted)
        
        package = ("SCP-" + formatted.upper(), url, requests.get(url).status_code != 404, id_number, suffix)
                 #(title, url, page exists, number, suffix)
    return package


@client.event
async def on_ready():
    app_info = await client.application_info()
    client.owner = app_info.owner

    await status_task(False)
    await tickClock()
    await setDailyGame()

    def isx64System():
        if sys.maxsize > 2**32:
            return True
        else:
            return False

    def loadOpus():
        if platform.system() == 'Windows':
            if isx64System():
                opus.load_opus('res/lib/opus/win/x64/libopus-0.x64.dll')
            else:
                opus.load_opus('res/lib/opus/win/x86/libopus-0.x86.dll')
        elif platform.system() == 'Linux':
            opusPath=find_library('opus')
            if opusPath:
                opus.load_opus(opusPath)
            else:
                if isx64System():
                    opus.load_opus('res/lib/opus/linux/x64/libopus.so')
                else:
                    opus.load_opus('res/lib/opus/linux/x86/libopus.so')
        else:
            print('Your OS is not supported.')
            sys.exit("OS not supported")

    print('Bot: {0.name}:{0.id}'.format(client.user))
    print('Owner: {0.name}:{0.id}'.format(client.owner))
    print('------------------')
    perms = discord.Permissions.none()
    perms.administrator = True
    url = discord.utils.oauth_url(app_info.id, perms)
    print('To invite me to a server, use this link\n{}'.format(url))
    loadOpus()
    client.loop.create_task(status_task(True))
    findInfo()

async def pullFromRepo(msgLogCxt = None):
    await setPlaying("Pulling...")
    try:
        repo = git.Repo(os.path.dirname(os.path.realpath(__file__)))
        repo.remotes.origin.pull()
        await restart(msgLogCxt)
    except Exception as e:
        if msgLogCxt:
            await throwError(msgLogCxt, e)

async def restart(msgLogCxt = None):
    await setPlaying("Restarting...")
    if msgLogCxt:
        await throwError(msgLogCxt, "Restarting. This may take a while.", vocalize=True, custom=True, printError=False)
    if userInfo['security']['allowremoteshutdown'] and platform.system() == 'Linux':
        try:
            os.system('sudo reboot now')
        except:
            await throwError(msgLogCxt, e, vocalize=True, printError=False)
            await throwError(msgLogCxt, "Ensure you are running me with administrator privileges on a Linux-based system.", \
                vocalize=True, custom=True, printError=False)
    else:
        os.execl(sys.executable, sys.executable, * sys.argv)

def run_client(Client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Client.start(*args, **kwargs))

if __name__ == '__main__':
    while True:
        try:
            run_client(client, discordToken)
        except KeyError:
            print("config not yet filled out.")
        except discord.errors.LoginFailure as e:
            print("Invalid discord token.")
        except Exception as e:
            writeLog(e, True)
            clearTerminal()
            print("An error occured! See log for details.\nRestarting...")
            time.sleep(10)
Client.logout()
Client.close()
