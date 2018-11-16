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
    with open('config/config.json', encoding='utf8') as f:                                                             
        config = json.load(f)
except FileNotFoundError:
    with open('config/config.json', 'w', encoding='utf8') as f:
        config = {}
        json.dump({
            "description": "I keep us safe from evil words!",
            "name": "Safety Steve", "invoker": "^", "creator": "GEONE",
            "git_link": "https://github.com/GE0NE/Safety-Steve",
            "fileformat": ".mp3", "sunday_game": "Minecraft: Christian Edition",
            "monday_game": "Minecraft: Safety Edition", "tuesday_game": "Nekopara",
            "wednesday_game": "It is Wednesday, my dudes!",
            "thursday_game": "Minecraft: Extra Safe Edition (NSFW)",
            "friday_game": "Waifu Sex Simulator",
            "saturday_game": "Minecraft: Safety Edition",
            "vote_limit": 3,
            "gild_limit": 1,
            "embed_color": "0xeee657",
            "response": "Hey! No bad words, please. This is a Christian server!",
            "bad_words": ["heck"], "bad_word_exceptions": ["check", "checked", "checking", "checks"],
            "reaction_words": [{"word": "wednesday", "reaction": "🐸"}, {"word": "skeltal", "reaction": "💀#🎺"},
            {"word": "doot", "reaction": "🎺"}]}, f, indent = 4)
        sys.exit("config file created. "
            "Please fill out the config.json file and restart the bot.");

try:
    with open('config/user-info.json', encoding='utf8') as f:
        userInfo = json.load(f)
except FileNotFoundError:
    with open('config/user-info.json', 'w', encoding='utf8') as f:
        userInfo = {}
        json.dump({"general_info":{"discord_token": "","user_id": "","mention": "","client_id": "","client_secret": ""},
            "channel_ids":{"lobby": ""}}, f, indent = 4)
        sys.exit("user info file created. "
            "Please fill out the user-info.json file and restart the bot.");

try:
    with open('config/commands.json', encoding='utf8') as f:
        commandsFile = json.load(f)
except FileNotFoundError:
    with open('config/commands.json', 'w', encoding='utf8') as f:
        commandsFile = {}
        json.dump({'text_commands': [{'Command': '', 'Help': '', 'Params': ''}],
            'voice_commands': [{'Command': '', 'Help': '', 'Params': ''}]}, f, indent = 4)
        sys.exit("commands file created. "
            "Please fill out the commands.json file and restart the bot.");

try:
    with open('config/fonts.json', encoding='utf8') as f:
        fonts = json.load(f, strict=False)
except FileNotFoundError:
    with open('config/fonts.json', 'w', encoding='utf8') as f:
        font = {}
        json.dump({'bubble': [''], "bubble_mask": ['']}, f, indent = 4)
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
            "Channel": "lobby", "React": "🎉#🎂#🎊#🍰"}]}, f, indent = 4)
        sys.exit("dates file created. "
            "Optionally fill out the dates.json file and restart the bot.");


# Bot info
desc = config['description']
invoker = config['invoker']
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

# Bad words and the response to them
wordBlacklist = config['bad_words']
wordWhitelist = config['bad_words_exceptions']
badWordResponse = config['response']

# Word Responses
reactionWords = config['reaction_words']

# Restrictions
voteLimit = config['vote_limit']
gildLimit = config['gild_limit']

# Formatting
embedColor = int(config['embed_color'], 0)

# Channel IDs
channels = userInfo['channel_ids']

# Birthdays
dates = date_list['dates']

# Reddit Config
reddit_id = generalInfo['client_id']
reddit_secret = generalInfo['client_secret']
reddit_agent = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# Misc info for commands
gitLink = config['git_link']
fileExt = config['fileformat']
bubbleFont = fonts['bubble_letters']
bubbleFontMask = fonts['bubble_mask']
voice = None
player = None
isPlaying = False
currentDate = 999

# The client
client = discord.Client(description=desc, max_messages=100)


@client.event
async def on_message(msg: discord.Message):
    global voice
    global player
    global isPlaying

    rawContent = msg.content
    content = rawContent.lower()

    for entry in reactionWords:
        if entry['word'] in content:
            for reaction in entry['reaction'].split('#'):
                await react(msg, reaction)

    if msg.author.bot:
        return

    if content.startswith(invoker):
        rawMessage = rawContent[len(invoker):].strip()
        message = rawMessage.lower()
        breakdown = message.split(" ")
        rawBreakdown = rawMessage.split(" ")
        command = breakdown[0]
        args = ' '.join(rawBreakdown[1:]) if len(breakdown) > 1 else ''
        argList = shlex.split(args)

        if command == '':
            return

        if command == "react":                                                                 
            if len(args.strip()) >= 1:
                messageFormatted = " ".join(args.split())
                emojis = messageFormatted.strip().split(" ")
                for emoji in emojis:
                    await react(msg, emoji)
            return

        if command == "func":                                                                 
            if len(args.strip()) >= 1:
                await handleFunc(msg, args)
            return

        if command == textCommands[0]['Command'] or command in textCommands[0]['Alias'].split('#'):
            if not args:
                await help(msg)
                return
            else:
                await helpCommand(args, msg) 
                return                                            

        if command == textCommands[1]['Command'] or command in textCommands[1]['Alias'].split('#'):
            await git(msg)

        if command == textCommands[2]['Command'] or command in textCommands[2]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[2]['Command'], msg)
                return
            await say(msg, args)                                            
            await msg.delete()                                                                   
            return                                                                                              

        if command == textCommands[3]['Command'] or command in textCommands[3]['Alias'].split('#'):
            await subreddit(msg, 'animemes', True)
            return

        if command == textCommands[4]['Command'] or command in textCommands[4]['Alias'].split('#'):
            await subreddit(msg, args)
            return

        if command == textCommands[5]['Command'] or command in textCommands[5]['Alias'].split('#'):
            if len(args) > 30:
                await say(msg, "Whoah! That's too many letter! Keep it below 30 please.")
                return
            if len(args.strip()) < 1:
                await helpCommand(textCommands[5]['Command'], msg)
                return
            await sayAscii(msg, args)
            return

        if command == textCommands[6]['Command'] or command in textCommands[6]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await setDailyGame()
                return
            await setPlaying(args)
            return

        if command == textCommands[7]['Command'] or command in textCommands[7]['Alias'].split('#'):
            await say(msg, "`༼ つ ◕_ ◕ ༽つ GIVE BAN ༼ つ ◕_ ◕ ༽つ`")

        if command == textCommands[8]['Command'] or command in textCommands[8]['Alias'].split('#'):
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

        if command == textCommands[9]['Command'] or command in textCommands[9]['Alias'].split('#'):
            text = args.strip()
            if len(text) < 1:
                await helpCommand(textCommands[9]['Command'], msg)
                return
            await sayIPA(msg, text)

        if command == textCommands[10]['Command'] or command in textCommands[10]['Alias'].split('#'): 
            try:
                if len(args.strip()) < 1:
                    await helpCommand(textCommands[10]['Command'], msg)
                    return
                question = args.split("[")[0]
                messageFormatted = " ".join(args.split())
                messageEmojis = None
                if '[' in messageFormatted and ']' in messageFormatted:
                    messageEmojis = messageFormatted.split("[")[1].split("]")[0]
                else:
                    messageEmojis = '👍 👎'
                emojis = messageEmojis.strip().split(" ")
                await say(msg, question)
                poll = None
                async for sentMessage in msg.channel.history(limit=1):
                    poll = sentMessage
                    break
                for emoji in emojis:
                    await react(poll, emoji)
                return
            except:
                await helpCommand(textCommands[10]['Command'], msg)
                return

        if command == textCommands[11]['Command'] or command in textCommands[11]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[11]['Command'], msg)
                return
            await defineUrban(msg, args)
            return

        if command == textCommands[12]['Command'] or command in textCommands[12]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[12]['Command'], msg)
                return
            await defineGoogle(msg, args)
            return

        if command == textCommands[13]['Command'] or command in textCommands[13]['Alias'].split('#'):
            await mock(msg, text=args.strip())
            return

        if command == textCommands[14]['Command'] or command in textCommands[14]['Alias'].split('#'):
            if not argList:
                scores = await readScores(msg.guild.id)
                embed = discord.Embed(title="Scores:", description="_ _")
                for scoreEntry in scores:
                    try:
                        user = await client.get_user_info(scoreEntry[1])
                        score = scoreEntry[2]
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
                if argList[0] in ['voted']:
                    target = msg.author
                    if msg.mentions:
                        target = msg.mentions[0]
                    targetScores = await readScores(msg.guild.id, target.id)
                    await say(msg, "{} voted {} time{} today.".format("You've" if target is msg.author else target.mention+' has', targetScores[4], '' if targetScores[4] == '1' else 's'))
                    return
                if msg.mentions:
                    target = msg.mentions[0]
                    targetScores = await readScores(msg.guild.id, target.id)
                    await say(msg, "{}'s score is {}.".format(target.mention, targetScores[2]))

        if command == textCommands[15]['Command'] or command in textCommands[15]['Alias'].split('#'):
            server = msg.guild
            invokerMessage = None
            author = None
            invokerScores = await readScores(guild=server.id, userID=msg.author.id)

            if invokerScores[0] and int(invokerScores[5]) >= gildLimit:
                await say(msg, "You have already gilded someone {}today!".format((str(gildLimit) + ' times ') if gildLimit != 1 else ''))
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
            targetScores = await readScores(guild=server.id, userID=author.id)
            embed = discord.Embed(title="_{} time{}_".format(targetScores[3], '' if targetScores[3] == '1' else 's'), 
                description="**You've been gilded!**", color=0xFFDF00)
            embed.set_thumbnail(url="https://i.imgur.com/UWWoFxe.png")
            await say(msg, "{}".format(author.mention), embed=embed)

        if command == textCommands[16]['Command'] or command in textCommands[16]['Alias'].split('#'):
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

            scores = await readScores(guild=msg.guild.id, userID=target.id)
            gilded = scores[3]
            embed = discord.Embed(title="{} been gilded:".format("You have" if target == msg.author else nick + " has"), 
                description="_{} time{}_".format(gilded, 's' if int(gilded) != 1 else ''), 
                color=gradient[int(gilded) if int(gilded) < 6 else 5])
            embed.set_thumbnail(url="https://i.imgur.com/kD6NhBG.png")
            await say(msg, "", embed=embed)
            return

        if command == textCommands[17]['Command'] or command in textCommands[17]['Alias'].split('#'):
            if len(args.strip()) < 1:
                await helpCommand(textCommands[17]['Command'], msg)
                return
            await mal(msg, args.strip())
            return
            
        if command == nsfwCommands[0]['Command'] or command in nsfwCommands[0]['Alias'].split('#'):
            if await checkNSFW(msg):
                await subreddit(msg, 'zerotwo', True)
            return

        if command == voiceCommands[0]['Command'] and isPlaying:
            isPlaying = False
            await voice.disconnect()
            return

        for i in range(1, len(voiceCommands)):
            if message == voiceCommands[i]['Command'] or command in voiceCommands[i]['Alias'].split('#'):
                if isPlaying:
                    await say(msg, 'I\'m already playing a sound! Please wait your turn.')
                    return
                if msg.author.voice.channel:
                    try:
                        sounds = voiceCommands[i]['SoundFile'].split("#")
                        sound = random.choice(sounds)
                        voice = await msg.author.voice.channel.connect()
                        voice.play(discord.FFmpegPCMAudio('res/sound/' + sound + fileExt))
                        isPlaying = True
                        client.loop.create_task(donePlaying(voice, player))
                    except Exception as e:
                        throwError(msg, 'There was an issue playing the sound file 🙁', custom=True)
                        pass
                else:
                    await throwError(msg, 'You\'re not in a voice channel!', custom=True, printError=False)
                return

    elif any([badword in content for badword in wordBlacklist]):
        for word in content.split():
            try:
                for goodword in wordWhitelist:
                    if goodword in word:
                        raise Exception()
                for badword in wordBlacklist:
                    if badword in word:
                        await say(msg, '{}: {}'.format(msg.author.mention, badWordResponse))
                        return
            except:
                continue

    elif content in ['good bot', 'bad bot', 'medium bot']:
        try:
            targetMessage = None
            server = msg.guild
            invokerScores = await readScores(guild=server.id, userID=msg.author.id)

            async for targetMessageTemp in msg.channel.history(limit=2):
                targetMessage = targetMessageTemp

            if targetMessage is not None:
                author = targetMessage.author
                server = targetMessage.guild
                if author == msg.author and 'good' in content:
                    await say(msg, "You can't vote positively for yourself!")
                    return

                if int(invokerScores[4]) >= voteLimit:
                    await say(msg, "You can only vote {} per day!".format((str(voteLimit) + ' times') if voteLimit > 1 else 'once'))
                    return

                if content =="medium bot":
                    await say(msg, "Thank you for voting on {}.\nTheir score is now {}.".format(author.mention, "medium-rare"))
                    return

                await writeScore(server.id, author.id, score=1 if 'good' in content else -1)
                await writeScore(server.id, msg.author.id, voted=1)
                targetScores = await readScores(guild=server.id, userID=author.id)
                await say(msg, "Thank you for voting on {}.\nTheir score is now {}.".format(author.mention, targetScores[2]))
        except Exception as e:
            await throwError(msg, error=e, sayTraceback=True, printTraceback=True)
            return

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


    elif client.user.mentioned_in(msg) and not msg.mention_everyone:
        await say(msg, 'Use {}{} for a list of commands'.format(invoker, textCommands[0]['Command']))
        return


async def subreddit(msg, sub, bypassErrorCheck=False):
    if not bypassErrorCheck and sub.strip() == "":
        await helpCommand('reddit', msg)
        return
    reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_agent)
    submissionList = []
    async with msg.channel.typing():
        try:
            if reddit.subreddit(sub).over18:
                if not await checkNSFW(msg):
                    return

            for submission in reddit.subreddit(sub).hot(limit=50):
                extensions = ["png","jpg","jpeg","gif"]
                if any([ext in submission.url[-len(ext):] for ext in extensions]):
                    submissionList.append(submission)
            if len(submissionList) > 0:
                submission = submissionList[random.randint(1, len(submissionList)-1)]
                embed = discord.Embed(title=submission.title, 
                    url="https://reddit.com{}".format(submission.permalink), color=embedColor)
                embed.set_image(url=submission.url)
                embed.set_footer(text=" via reddit.com/r/{}".format(str(submission.subreddit)), 
                    icon_url="http://www.google.com/s2/favicons?domain=www.reddit.com")
                await say(msg, "Here's a trending post from r/{}".format(str(submission.subreddit)), embed)
            else:
                await throwError(msg, "There's nothing in that subreddit!", custom=True)
        except:
            await throwError(msg, "reddit.com/r/{} couldn\'t be accessed.".format(sub), custom=True)

async def git(msg):
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

async def checkNSFW(msg):
    if not msg.channel.is_nsfw():
        await throwError(msg, "You can't do that here. This channel is not maked as NSFW.", custom=True, printError=False)
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
    embed.add_field(name="🥕 Prefix", value="```" + invoker + "```", inline=False)                      
    embed.add_field(name="🔤 Text Commands", value=", ".join(textCommandList), inline=False)                  
    embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel', value=", ".join(voiceCommandList), inline=False)
    if msg.channel.is_nsfw():
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
                    
    embed = discord.Embed(title="Command:", description=command, color=embedColor) #                      
    embed.add_field(name="Description:", value=commandHelp[commandList.index(command)], inline=False)
    embed.add_field(name="Usage:", value="```" + invoker + command + " " + commandParams[commandList.index(command)] + "```", inline=False)
    if ('-e' in args or 'example' in args or 'all' in args) and command in textCommandList:
        examples = []
        for example in textCommandExample[commandList.index(command)]:
            examples.append(invoker + example)
        embed.add_field(name="Examples:", value="```\n" + '\n'.join(examples) + "```", inline=False)
    if '-a' in args or 'alias' in args or 'all' in args:
        aliases = []
        for alias in commandAlias[commandList.index(command)]:
            if alias:
                aliases.append(invoker + alias)
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

async def setPlaying(name, type=0):
    await client.change_presence(activity=discord.Game(type=0, name=name))
    return

async def sayIPA(msg, text):
    async with msg.channel.typing():
        try:
            with requests. Session() as c: 
                url = 'https://tophonetics.com/'
                c.get(url)
                data = dict(text_to_transcribe=text, output_dialect='am') 
                page = c.post(url, data=data, headers={"Referer": "https://tophonetics.com/"})
                soup = BeautifulSoup(page.text, 'html.parser')
                results = soup.find_all('span', attrs={'class':'transcribed_word'})
                resultStringList = (result.text for result in results)
                resultStringConcat = ' '.join(resultStringList)
                if len(resultStringConcat) < 1:
                    await throwError(msg, "I wasn't able to convert that word!", custom=True, printError=False)
                    return
                else:
                    await say(msg, resultStringConcat)
        except:
            await throwError(msg, "I couldn't access `{}`!".format(url), custom=True)

async def defineUrban(msg, message=None, term='', num=1, edit=None):

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
            async with msg.channel.typing():
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
                        len(result["list"]), invoker, textCommands[11]['Command'], term, number))
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
                await say(msg, "That result doesn't exist! Try {}{} {}.".format(invoker, textCommands[11]['Command'], term))

            except Exception as e:
                await throwError(msg, e, vocalize=False)
        return 

async def defineGoogle(msg, message):
    async with msg.channel.typing():
        async with aiohttp.ClientSession() as session:
            term = message.strip()
            search = term.split(" ")[0]
            async with session.get("https://googledictionaryapi.eu-gb.mybluemix.net/", params={"define": search}) as resp:
                try:
                    payload = await resp.json()
                except ValueError:
                    await say(msg, "I couldn't define {}.".format(term))
                    return
            try:
                embed=discord.Embed(color=embedColor)
                embed.set_thumbnail(url="http://icons.iconarchive.com/icons/osullivanluke/orb-os-x/48/Dictionary-icon.png")
                values = list(payload.values())

                word = values[0]
                ipa = values[2][0][0]

                embed.add_field(name="{}".format(word), value="/{}/".format(ipa), inline=False)
                for pos in list(values[3].keys())[:3]:
                    postxt = pos
                    definitionCount = 1
                    definitions = ""
                    for entry in values[3][pos][:2]:

                        definition = ""
                        if 'definition' in entry:
                            definition = entry['definition']

                        example = ""
                        if 'example' in entry:
                            example = entry['example']

                        synonyms = ""
                        if 'synonyms' in entry:
                            synonyms = entry['synonyms'][:4]
                            synonyms = ', '.join(synonyms)
                            
                        seperator = "_ _\n" if definitionCount == 1 else ""
                        definitions += str(definitionCount) + ". " + definition + "\n"
                        definitionCount += 1

                    embed.add_field(name="{}".format(postxt), value="{}".format(definitions), inline=False)
                    postxt = u'\u200b'
                embed.set_footer(text="Powered by googledictionaryapi.eu-gb.mybluemix.net")
                await say(msg, "", embed=embed)
                    
            except:
                return
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
            await say(msg, "Yo, dude! I can't dispatch a blank message! This can happen if you try to mock an embeded message.")
        else:
            await say(msg, result)

async def writeScore(guild, user, score=0, gilding=0, voted=0, gilded=0):
    userObj = "GUILD={} USER={} SCORE={} GILDING={} VOTED={} GILDED={}".format(guild, user, str(score), str(gilding), 
        str(voted), str(gilded))
    existingScores = await readScores()
    for existingScore in existingScores:
        if int(existingScore[0]) == guild and int(existingScore[1]) == user:
            oldUserObj = userObj
            newScore = str(int(existingScore[2]) + score)
            newGilding = str(int(existingScore[3]) + gilding) if (int(existingScore[3]) + gilding) > 0 else '0'
            newVoted = str(int(existingScore[4]) + voted) if (int(existingScore[4]) + voted) > 0 else '0'
            newGilded = str(int(existingScore[5]) + gilded) if (int(existingScore[5]) + gilded) > 0 else '0'
            userObj = "GUILD={} USER={} SCORE={} GILDING={} VOTED={} GILDED={}".format(guild, user, newScore, newGilding,
                newVoted, newGilded)
            oldScores = await getScores()
            oldScores = oldScores.split("\n")[:-1]
            with open("res/data/user-data.dat","w") as scores:
                for oldScore in oldScores:
                    if oldScore.split(' ')[0] == oldUserObj.split(' ')[0] and oldScore.split(' ')[1] == oldUserObj.split(' ')[1]:
                        if not (newScore == '0' and newGilding == '0' and newVoted == '0' and newGilded == '0'):
                            scores.write(userObj + "\n")
                    else:
                        scores.write(oldScore + "\n")
                scores.close()
                return
    with open("res/data/user-data.dat","a") as scores:
        scores.write(userObj + "\n")
        scores.close()
    return

async def readScores(guild=None, userID=None):
    blankEntry = ['0','0','0','0','0','0']
    data = await getScores()
    if not data:
        return blankEntry
    entries = data.split("\n")[:-1]
    guildEntries = []
    for i in range(0, len(entries)):
        entries[i] = entries[i].split(' ')
        for j in range(0, len(entries[i])):
            entries[i][j] = entries[i][j].split('=')[1]
        if guild is not None and int(entries[i][0]) == guild:
            guildEntries.append(entries[i])
    if guild is not None:
        if userID is not None:
            found = None
            for entry in guildEntries:
                if int(entry[1]) == userID:
                    found = entry
                    break
            if found is not None:
                return found
            else:
                return blankEntry
        else:
            return guildEntries
    return sorted(entries, key=lambda x: x[0])

async def getScores(iteration=0):
    try:
        with open("res/data/user-data.dat","r") as scores:
            data = scores.read()
            scores.close()
            return data
    except FileNotFoundError as e:
        if iteration <= 1:
            with open("res/data/user-data.dat","w+") as scores:
                scores.close()
                await getScores(iteration=iteration+1)
        else:
            throwError(msg, e)

async def scoreDecay():
    scores = await readScores()
    for entry in scores:
        if int(entry[2]) == 0:
            continue
        elif int(entry[2]) > 0:
            await writeScore(int(entry[0]), int(entry[1]), score=-1)
        else:
            await writeScore(int(entry[0]), int(entry[1]), score=1)

async def mal(msg, name, mediaType="anime", displayFormat="tv"):

    async def notFound():
        await throwError(msg, "{} couldn't be found on MyAnimeList.".format(name), custom=True, printError=False)

    async with msg.channel.typing():
        name = parse.quote_plus(name)
        async with aiohttp.ClientSession(headers={"User-Agent": "{}".format(client.user)}) as session:
            async with session.get("https://api.jikan.moe/search/{0}?q={1}&type={2}&page=1".format(mediaType, name, displayFormat)) as resp:
                result = await resp.json()
                results = None
                try:
                    results = result["result"]
                except:
                    pass
            try:
                if result["error"]:
                    await notFound()
                    return
            except:
                pass
            if not results:
                await throwError(msg, "{} couldn't be found on MyAnimeList.".format(name), custom=True, printError=False)
                return
            else:
                try:
                    top_result = results[0]
                    result_id = top_result["mal_id"]
                    result_image = top_result["image_url"]                
                    
                    async with session.get("https://api.jikan.moe/{0}/{1}".format(mediaType, result_id)) as resp:
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
                        result_type = result["type"]
                        result_score = str(result["score"])
                        result_episodes = str(result["episodes"])
                        result_rank = str(result["rank"])
                        result_status = result["status"]
                        result_air_time = result["aired_string"]
                        result_synopsis = html.unescape(result["synopsis"])
                        
                        
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

async def throwError(msg, error=None, vocalize=True, custom=False, sayTraceback=False, printTraceback=False, printError=True, fatal=False):
    if printError:
        print("ERROR:\n{}".format(error))
    if vocalize:
        if error:
            await say(msg, "Woah! Something bad happened! ```\n{}\n```".format(error) if not custom else error)
        if sayTraceback:
            dump = "```{}```".format(''.join(traceback.format_stack()).replace("`", "\`"))
            await say(msg, dump)
    if printTraceback:
        print("Traceback:")
        traceback.print_exc()

    if printError or printTraceback or sayTraceback:
        writeLog(error, fatal)
    return

async def clearDailyRestrictions():
    scores = await readScores()
    for entry in scores:
        await writeScore(int(entry[0]), int(entry[1]), voted=-100, gilded=-100)

async def onNewDay():
    await checkDailyEvents()
    await clearDailyRestrictions()

async def tickClock():
    now = datetime.datetime.now()
    with open("res/data/clock.dat","w") as clock:
        day = str(now.day)
        month = str(now.month)
        year = str(now.year)
        clock.write("{}-{}-{}".format(day, month, year))
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
        day = str(now.day)
        month = str(now.month)
        year = str(now.year)
        localDate = "{}-{}-{}".format(day, month, year)

        global currentDate
        oldDate = await getClock()
        
        #if currentDate != localDate or bypassCheck:
            #await setDailyGame()
        currentDate = localDate

        
        await tickClock()

        if oldDate != currentDate:
            await onNewDay()
        
        currentDate = localDate
        oldDate = currentDate

        if not loop:
            return
        await asyncio.sleep(300)

async def checkDailyEvents():
    today = datetime.datetime.today()
    weekday = today.weekday()
    
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
            dateChannels = date['Channel'].replace(" ", "").split('#')
            reacts = date.get('React')
            dateFunc = date.get('Func')
            formattedDateMessage = None

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
                channel = client.get_channel(int(userInfo['channel_ids'][dateChannel]))
                if formattedDateMessage:
                    reactCondition = await sayInChannelOnce(channel, formattedDateMessage) and reacts
                    async for message in channel.history(limit=1):
                        msg = message
                        break
                    if reactCondition:
                        for emojis in reacts:
                            await react(msg, emojis)
                if dateFunc:
                    data = {"id": 0,"size": 0,"":""}
                    dummyMessage = discord.Message(state=None, channel=channel, data=data)
                    dummyMessage.author = client.user
                    dummyMessage.content = ""
                    dummyMessage.channel = channel
                    await handleFunc(dummyMessage, dateFunc, channel=channel)
    return

def writeLog(e, crash=False):
    logTime = datetime.datetime.now()
    filename = 'res/data/logs/log-{}'.format(str(logTime)) if crash else 'res/data/logs/log.txt'
    with open(filename, 'a') as log:
        log.write("Time: " + str(logTime) + "\n")
        log.write("-\/-----------------------------\/-" + "\n")
        log.write(str(e)+"\n")
        log.write("-/\-----------------------------/\-" + "\n")
        log.write("\n")

async def sayInChannelOnce(channel, message, embed=None):
    today = datetime.datetime.combine(date.today(), datetime.time())
    async for msg in channel.history(limit=100, after=today):
        if msg.author == client.user and msg.content == message:
           return False
    await sayInChannel(channel, message, embed)
    return True

async def donePlaying(voice, player):
    global isPlaying
    while isPlaying:
        if not voice.is_playing():
            await voice.disconnect()
            isPlaying = False
        await asyncio.sleep(0.5)

def clearTerminal():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system("clear && printf \'\\e[3J\'")

def ord(n):
    return "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

@client.event
async def on_ready():
    app_info = await client.application_info()
    client.owner = app_info.owner

    await setDailyGame()
    global currentDate
    try:
        currentDate = await getClock()
    except IOError:
        await tickClock()
    await status_task(False)

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