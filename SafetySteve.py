import os                                                                                                       # import all sorts of shit
import sys                                                                                                      # like the OS and the System
import datetime                                                                                                 # and time itself
from datetime import date, time
import time
import json                                                                                                     # some dude named jason
import asyncio                                                                                                  # a kitchen sinkio
import re                                                                                                       # re:re:re:re:re: meeting time
import praw
import random
import math
import html
from urllib import parse
from urllib.request import Request, urlopen
import aiohttp

try:                                                                                                            # try to
    import discord                                                                                                  # import discord.py
except ImportError:                                                                                             # if discord.py isn't installed
    import pip                                                                                                      # import pip
    pip.main(['install', 'discord'])                                                                                # install discord.py
    import discord                                                                                              # import discord.py
from discord import opus                                                                                        # inport opus, the discord sound lib
from discord.utils import get

try:
    import requests
except ImportError:
    import pip
    pip.main(['install', 'requests'])
    import requests 

try:
    import bs4
except ImportError:
    import pip
    pip.main(['install', 'beautifulsoup4'])
    import bs4
from bs4 import BeautifulSoup

try:
    with open('config.json', encoding='utf8') as f:                                                             
        config = json.load(f)
except FileNotFoundError:
    with open('config.json', 'w', encoding='utf8') as f:
        config = {}
        print("config file created. Please restart the bot.")
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
    with open('user-info.json', encoding='utf8') as f:
        userInfo = json.load(f)
except FileNotFoundError:
    with open('user-info.json', 'w', encoding='utf8') as f:
        userInfo = {}
        json.dump({"general_info":{"discord_token": "","user_id": "","mention": "","client_id": "","client_secret": ""},
            "channel_ids":{"lobby": ""}}, f, indent = 4)
        sys.exit("user info file created. "
            "Please fill out the user-info.json file and restart the bot.");

try:
    with open('commands.json', encoding='utf8') as f:
        commandsFile = json.load(f)
except FileNotFoundError:
    with open('commands.json', 'w', encoding='utf8') as f:
        commandsFile = {}
        json.dump({'text_commands': [{'Command': '', 'Help': '', 'Params': ''}],
            'voice_commands': [{'Command': '', 'Help': '', 'Params': ''}]}, f, indent = 4)
        sys.exit("commands file created. "
            "Please fill out the commands.json file and restart the bot.");

try:
    with open('fonts.json', encoding='utf8') as f:
        fonts = json.load(f, strict=False)
except FileNotFoundError:
    with open('fonts.json', 'w', encoding='utf8') as f:
        font = {}
        json.dump({'bubble': [''], "bubble_mask": ['']}, f, indent = 4)
        sys.exit("fonts file created. "
            "Please fill out the fonts.json file and restart the bot.");

try:
    with open('dates.json', encoding='utf8') as f:
        date_list = json.load(f, strict=False)
except FileNotFoundError:
    with open('dates.json', 'w', encoding='utf8') as f:
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
textCommandList = []
voiceCommandList = []

# Command info
textCommandHelp = []
textCommandParams = []
textCommandAlias = []
textCommandExample = []
voiceCommandHelp = []
voiceCommandParams = []
voiceCommandAlias  = []

# Init command info
for command in textCommands:
    textCommandList.append(command['Command'])
    textCommandHelp.append(command['Help'])
    textCommandParams.append(command['Params'])
    if command['Alias']:
        textCommandAlias.append(command['Alias'].split('#'))
    textCommandExample.append(command['Examples'].split('#'))

for command in voiceCommands:
    voiceCommandList.append(command['Command'])
    voiceCommandHelp.append(command['Help'])
    voiceCommandParams.append(command['Params'])
    if command['Alias']:
        voiceCommandAlias.append(command['Alias'].split('#'))

# List of commands
commandList = textCommandList + voiceCommandList
commandHelp = textCommandHelp + voiceCommandHelp
commandParams = textCommandParams + voiceCommandParams
commandAlias = textCommandAlias + voiceCommandAlias

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
weekday = 999

# The client
client = discord.Client(description=desc, max_messages=100)                                                     # create the client


@client.event
async def on_message(msg: discord.Message):                                                                     # When a message is sent to a channel
    global voice
    global player
    global isPlaying

    rawContent = msg.content
    content = rawContent.lower()

    for entry in reactionWords:
        if entry['word'] in content:
            for reaction in entry['reaction'].split('#'):
                await react(msg, reaction)

    if msg.author.bot:                                                                                          # if the message was from the bot
        return                                                                                                      # ignore it

    if content.startswith(invoker):                                                                         # if the message starts with the invoker
        rawMessage = rawContent[len(invoker):].strip()
        message = rawMessage.lower()
        breakdown = message.split(" ")
        rawBreakdown = rawMessage.split(" ")
        command = breakdown[0]
        args = ' '.join(rawBreakdown[1:]) if len(breakdown) > 1 else ''

        if command == '':
            return

        if command == "react":                                                                 
            if len(args.strip()) >= 1:
                messageFormatted = " ".join(args.split())
                emojis = messageFormatted.strip().split(" ")
                for emoji in emojis:
                    await react(msg, emoji)
            return       

        if command == textCommands[0]['Command'] or command in textCommands[0]['Alias'].split('#'):                # help command
            if not args:
                await help(msg)
                return                                                                     # help [command] command
            else:
                await helpCommand(args, msg) 
                return                                            

        if command == textCommands[1]['Command'] or command in textCommands[1]['Alias'].split('#'):              # git command
            await git(msg)

        if command == textCommands[2]['Command'] or command in textCommands[2]['Alias'].split('#'):                                                               # say <text> command
            if len(args.strip()) < 1:
                await helpCommand(textCommands[2]['Command'], msg)
                return
            await say(msg, args)                                            
            await client.delete_message(msg)                                                                   
            return                                                                                              

        if command == textCommands[3]['Command'] or command in textCommands[3]['Alias'].split('#'):                                                                   # animeme command
            await subreddit('animemes', msg, True)
            return

        if command == textCommands[4]['Command'] or command in textCommands[4]['Alias'].split('#'):                                                               # reddit [subreddit] command
            await subreddit(args, msg)
            return

        if command == textCommands[5]['Command'] or command in textCommands[5]['Alias'].split('#'):                                                               # ascii command
            if len(args) > 30:
                await say(msg, "Whoah! That's too many letter! Keep it below 30 please.")
                return
            if len(args.strip()) < 1:
                await helpCommand(textCommands[5]['Command'], msg)
                return
            await sayAscii(msg, args)
            return

        if command == textCommands[6]['Command'] or command in textCommands[6]['Alias'].split('#'):                                                               # reddit [subreddit] command
            if len(args.strip()) < 1:
                await status_task(False, True)
                return
            await setPlaying(args)
            return

        if command == textCommands[7]['Command'] or command in textCommands[7]['Alias'].split('#'):
            await say(msg, "`༼ つ ◕_ ◕ ༽つ GIVE BAN ༼ つ ◕_ ◕ ༽つ`")

        if command == textCommands[8]['Command'] or command in textCommands[8]['Alias'].split('#'):
            usernamesFile = open("usernames.txt", "r")
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
            ipa = await textToIPA(text)
            if len(ipa) < 1:
                await say(msg, "I wasn't able to convert that word!")
                return
            await say(msg, ipa)

        if command == textCommands[10]['Command'] or command in textCommands[10]['Alias'].split('#'): 
            try:                                                                  
                if len(args.strip()) < 1:
                    await helpCommand(textCommands[10]['Command'], msg)
                    return
                question = args.split("[")[0]
                messageFormatted = " ".join(args.split())
                messageEmojis = messageFormatted.split("[")[1].split("]")[0]
                emojis = messageEmojis.strip().split(" ")
                await say(msg, question)
                poll = None
                async for sentMessage in client.logs_from(msg.channel, limit=1):
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
            scores = await readScores(msg.server.id)
            embed = discord.Embed(title="Scores:", description="_ _")
            for scoreEntry in scores:
                user = await client.get_user_info(scoreEntry[1])
                score = scoreEntry[2]
                if score != '0':
                    displayName = user.display_name
                    nick = msg.server.get_member(user.id).nick
                    nick = displayName if nick is None else nick
                    displayName = "_AKA {}_\n".format(displayName) if nick != displayName else ''
                    embed.add_field(name=nick, value="{}{}".format(displayName, score), inline=True)
            await say(msg, "", embed=embed)
            return

        if command == textCommands[15]['Command'] or command in textCommands[15]['Alias'].split('#'):
            server = msg.server
            invokerMessage = None
            author = None
            invokerScores = await readScores(guild=server.id, userID=msg.author.id)

            if invokerScores is not None and int(invokerScores[5]) >= gildLimit:
                await say(msg, "You have already gilded someone {}today!".format((str(gildLimit) + ' times ') if gildLimit != 1 else ''))
                return

            if len(args.strip()) < 1:
                async for invokerMessageTemp in client.logs_from(msg.channel, limit=2):
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

            scores = await readScores(guild=msg.server.id, userID=target.id)
            gilded = '0' if scores is None else scores[3]
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

        if command == voiceCommands[0]['Command'] and isPlaying:                                                    # leave command
            isPlaying = False
            await voice.disconnect()
            return

        for i in range(1, len(voiceCommands)):                                                                      # handler for all voice commands
            if isPlaying:                                                                                               # if a sound is already playing
                await say(msg, 'I\'m already playing a sound! Please wait your turn.')                                      # send a message informing them
                return
            if message == voiceCommands[i]['Command'] or command in voiceCommands[i]['Alias'].split('#'):                                                                  # otherwise
                if msg.author.voice_channel:                                                                                # if the user is in a voice channel
                    try:                                                                                                        # try to
                        sounds = voiceCommands[i]['SoundFile'].split("#")
                        sound = random.choice(sounds)
                        voice = await client.join_voice_channel(msg.author.voice_channel)                                           # create a voice clientw
                        player = voice.create_ffmpeg_player(                                                                        # create a ffmpeg player
                            'sound/' + sound + fileExt)
                        isPlaying = True                                                                                            # flag isPlaying
                        player.start()                                                                                              # start the player
                        client.loop.create_task(donePlaying(voice, player))                                                         # start a thread to keep track of when the sound is finished playing
                    except Exception as e:                                                                                      # if you can't
                        print(e)                                                                                                    # notify the host that there was an issue
                        await say(msg, 'There was an issue playing the sound file 🙁')                                              # notify the client that there was an issue
                        pass                                                                                                        # drakememe.jpg
                else:                                                                                                       # otherwise
                    await say(msg, 'You\'re not in a voice channel!')                                                           # inform the user that they're not in a voice channel
                return

    elif any([badword in content for badword in wordBlacklist]):                                          # if the message does not start with the invoker but it contains bad words
        for word in content.split():
            if word in wordWhitelist:
                continue
            for badword in wordBlacklist:
                if badword in word:
                    await say(msg, '{}: {}'.format(msg.author.mention, badWordResponse))                                        # tell them politely, yet firmly, to leave
                    return

    elif content == "good bot" or content == "bad bot":
        try:
            targetMessage = None
            server = msg.server
            invokerScores = await readScores(guild=server.id, userID=msg.author.id)

            async for targetMessageTemp in client.logs_from(msg.channel, limit=2):
                targetMessage = targetMessageTemp

            if targetMessage is not None:
                author = targetMessage.author
                server = targetMessage.server
                if author == msg.author and 'good' in content:
                    await say(msg, "You can't vote positively for yourself!")
                    return

                if invokerScores is not None and int(invokerScores[4]) >= voteLimit:
                    await say(msg, "You can only vote {} per day!".format((str(voteLimit) + ' times') if voteLimit > 1 else 'once'))
                    return

                await writeScore(server.id, author.id, score=1 if 'good' in content else -1)
                await writeScore(server.id, msg.author.id, voted=1)
                targetScores = await readScores(guild=server.id, userID=author.id)
                await say(msg, "Thank you for voting on {}.\nTheir score is now {}.".format(author.mention, targetScores[2]))
        except:
            return
        

    elif client.user.mentioned_in(msg) and not msg.mention_everyone:                                       # if a user mentions the bot
        await say(msg, 'Use {}{} for a list of commands'.format(invoker, textCommands[0]['Command']))               # send the help command
        return


async def subreddit(sub, msg, bypassErrorCheck=False):
    if not bypassErrorCheck and sub.strip() == "":
        await helpCommand('reddit', msg)
        return
    reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_agent)
    submissionList = []
    try:
        for submission in reddit.subreddit(sub).hot(limit=50):
            extensions = ["png","jpg","jpeg","gif"]
            if any([ext in submission.url[-len(ext):] for ext in extensions]):
                submissionList.append(submission)
        if len(submissionList) > 0:
            submission = submissionList[random.randint(1, len(submissionList))]
            embed = discord.Embed(title=submission.title, 
                url="https://reddit.com{}".format(submission.permalink), color=embedColor)
            embed.set_image(url=submission.url)
            embed.set_footer(text=" via reddit.com/r/{}".format(str(submission.subreddit)), 
                icon_url="http://www.google.com/s2/favicons?domain=www.reddit.com")
            await say(msg, "Here's a trending post from r/{}".format(str(submission.subreddit)), embed)
        else:
            await say(msg, "We're out of memes!")
    except:
        await say(msg, 'reddit.com/r/{} couldn\'t be accessed.'.format(sub))

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
        sentMessage = await client.send_message(channel, message)
    else:
        sentMessage = await client.send_message(channel, message, embed=embed)
    return sentMessage

async def react(msg, emote):
    try:
        await client.add_reaction(msg, emote)
    except:
        try:
            reaction = get(client.get_all_emojis(), name=emote)
            await client.add_reaction(msg, reaction)
        except:
            try:
                reaction = emote.replace("<:", "")
                reaction = ':'.join(reaction.split(':')[:-1])
                reaction = get(client.get_all_emojis(), name=reaction)
                await client.add_reaction(msg, reaction)
            except:
                await say(msg, "I don't know that emoji: " + "`" + str(emote) + "`")
    return

async def help(msg):

    embed = discord.Embed(title=name, description=desc, color=embedColor)                                
    embed.add_field(name="🥕 Prefix", value="```" + invoker + "```", inline=False)                      
    embed.add_field(name="🔤 Text Commands", value=", ".join(textCommandList), inline=False)                  
    embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel', value=", ".join(voiceCommandList), inline=False)
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
    await client.change_presence(game=discord.Game(type=0, name=name))
    return

async def textToIPA(text):
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
            return resultStringConcat
    except:
        return ""

async def defineUrban(msg, message, num=1, edit=None):
    async with aiohttp.ClientSession(headers={"User-Agent": "{}".format(client.user)}) as session:
        number = num
        term = message.strip()
        regexResult = list(filter(None, re.compile(r'page ([1-9]{1,3})$|-p ([1-9]{1,3})$').split(term)))
        if len(regexResult) > 1:
            number = regexResult[1]
            term = regexResult[0]
        search = "\""+term+"\""
        async with session.get("http://api.urbandictionary.com/v0/define", params={"term": search}) as resp:
            result = await resp.json()
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
                embed.set_footer(text="{} results were found. To see a different result, use {}{} {} -p {}.".format( 
                    len(result["list"]), invoker, textCommands[11]['Command'], term, number))
                definition = edit
                if definition is not None:
                    await client.edit_message(definition, embed=embed)
                else:
                    definition = await say(msg, "", embed=embed)
                if num > 1:
                    await react(definition, "⬅")
                if num < len(result["list"]):
                    await react(definition, "➡")
                res = await client.wait_for_reaction(["⬅","➡"], message=definition, timeout=20.0, user=msg.author)
                if num > 1:
                    await client.remove_reaction(definition, "⬅", msg.author)
                    await client.remove_reaction(definition, "⬅", definition.author)
                if num < len(result["list"]):
                    await client.remove_reaction(definition, "➡", msg.author)
                    await client.remove_reaction(definition, "➡", definition.author)
                if res is None:
                    return
                await defineUrban(msg, term, num=(num + ( 1 if res.reaction.emoji == "➡" else -1)), edit=definition)

            except IndexError:
                await say(msg, "That result doesn't exist! Try {}{} {}.".format(invoker, textCommands[11]['Command'], term))

            except Exception as e:
                print(e)
        return 

async def defineGoogle(msg, message):
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
                #embed.add_field(name="{}".format(pos), value="\a", inline=False)
                postxt = pos
                definitionCount = 1
                definitions = ""
                for entry in values[3][pos][:2]:

                    definition = ""
                    if 'definition' in entry:
                        definition = entry['definition']
                        #definition += "\n"
                        #embed.add_field(name="\a", value="{}".format("1. {}".format(definition)), inline=False)

                    example = ""
                    if 'example' in entry:
                        example = entry['example']
                        #example += "\n"
                        #embed.add_field(name="example:", value="{}".format(example), inline=False)

                    synonyms = ""
                    if 'synonyms' in entry:
                        synonyms = entry['synonyms'][:4]
                        synonyms = ', '.join(synonyms)
                        
                        #embed.add_field(name="synonyms:", value="{}".format(synonyms), inline=False)
                    seperator = "_ _\n" if definitionCount == 1 else ""
                    definitions += str(definitionCount) + ". " + definition + "\n"
                    definitionCount += 1
                    #embed.add_field(name=("synonyms" if not example else "example"), value=("{}" + (" " if not synonyms else "\n___synonyms: "+synonyms+"___")).format("_" + example + "_"), inline=True)
                    
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
            async for message in client.logs_from(msg.channel, limit=100):
                if text == str(message.id):
                    text = message.content
        elif text == "":
            async for message in client.logs_from(msg.channel, limit=2):
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
    try:
        existingScores = await readScores()
        for existingScore in existingScores:
            if existingScore[0] == guild and existingScore[1] == user:
                oldUserObj = userObj
                newScore = str(int(existingScore[2]) + score)
                newGilding = str(int(existingScore[3]) + gilding) if (int(existingScore[3]) + gilding) > 0 else '0'
                newVoted = str(int(existingScore[4]) + voted) if (int(existingScore[4]) + voted) > 0 else '0'
                newGilded = str(int(existingScore[5]) + gilded) if (int(existingScore[5]) + gilded) > 0 else '0'
                userObj = "GUILD={} USER={} SCORE={} GILDING={} VOTED={} GILDED={}".format(guild, user, newScore, newGilding,
                    newVoted, newGilded)
                oldScores = await getScores()
                oldScores = oldScores.split("\n")[:-1]
                with open("botScores.txt","w") as scores:
                    for oldScore in oldScores:
                        if oldScore.split(' ')[0] == oldUserObj.split(' ')[0] and oldScore.split(' ')[1] == oldUserObj.split(' ')[1]:
                            if not (newScore == '0' and newGilding == '0' and newVoted == '0' and newGilded == '0'):
                                scores.write(userObj + "\n")
                        else:
                            scores.write(oldScore + "\n")
                    scores.close()
                    return
    except:
        with open("botScores.txt","w") as writer:
            writer.close()
    with open("botScores.txt","a") as scores:
        scores.write(userObj + "\n")
        scores.close()
    return

async def readScores(guild=None, userID=None):
    data = await getScores()
    entries = data.split("\n")[:-1]
    guildEntries = []
    for i in range(0, len(entries)):
        entries[i] = entries[i].split(' ')
        for j in range(0, len(entries[i])):
            entries[i][j] = entries[i][j].split('=')[1]
        if guild is not None and entries[i][0] == guild:
            guildEntries.append(entries[i])
    if guild is not None:
        if userID is not None:
            found = None
            for entry in guildEntries:
                if entry[1] == userID:
                    found = entry
                    break
            if found is not None:
                return found
            else:
                return None
        else:
            return guildEntries
    return sorted(entries, key=lambda x: x[0])

async def getScores(guild=None):
    with open("botScores.txt","r") as scores:
        data = scores.read()
        scores.close()
        return data

async def mal(msg, name, mediaType="anime", displayFormat="tv"):
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
                await throwError(msg, result["error"])
                return
        except:
            pass
        if not results:
            await throwError(msg, "{} couldn't be found on MyAnimeList.".format(name), custom=True)
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
                        await throwError(msg, result["error"])
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
                    await throwError(msg, "That result doesn't exist!", custom=True)
                except:
                    return
            except IndexError:
                await throwError(msg, "That result doesn't exist!", custom=True)
            except Exception:
                return
        return 

async def throwError(msg, error, custom=False):
    pass#await say(msg, "Woah! Something bad happened! `{}`".format(error) if not custom else error)

async def clearDailyRestrictions():
    scores = await readScores()
    for entry in scores:
        await writeScore(entry[0], entry[1], voted=-100, gilded=-100)

async def onNewDay():
    await checkBDays()
    await clearDailyRestrictions()

async def status_task(loop, bypassCheck):                                                                                        # choose what game to play based on the day of the week
    while True:
        global weekday
        oldWeekday = weekday
        now = datetime.datetime.now()
        if weekday != now.weekday() or bypassCheck:
            await setPlaying(config['{}_game'.format(now.strftime("%A").lower())])
        if not bypassCheck:
            weekday = now.weekday()
            
            if oldWeekday != weekday:
                await onNewDay()
            
            weekday = now.weekday()
            oldWeekday = weekday
        if not loop:
            return
        await asyncio.sleep(300)                                                                               # only look at the clock every 5 minutes

async def checkBDays():
    today = datetime.datetime.today()
    weekday = today.weekday()
    
    for date in dates:
        dateDay = date['Day']
        dateMonth = date['Month']
        dateYear = date['Year']
        dateType = date['Type']
        if (today.day == dateDay and today.month == dateMonth) or (dateType == 'weekday' and weekday == dateDay):
            dateName = date['Name']
            dateMessage = date['Message']
            dateAge = today.year - dateYear
            dateOrdAge = ord(dateAge)
            dateTag = date['Tag']
            dateType = date['Type']
            dateChannels = date['Channel'].replace(" ", "").split('#')
            reacts = date['React'].split("#")

            formattedDateMessage = dateMessage.replace("#day", str(dateDay)).replace("#month", str(dateMonth)).replace("#year", str(dateYear)).replace("#name", dateName).replace("#age", dateOrdAge).replace("#tag", dateTag).replace("#type", dateType)
            for dateChannel in dateChannels:
                channel = client.get_channel(userInfo['channel_ids'][dateChannel])
                reactCondition = await sayInChannelOnce(channel, formattedDateMessage) and reacts
                async for message in client.logs_from(channel, limit=1):
                    msg = message
                    break
                if reactCondition:
                    for emojis in reacts:
                        await react(msg, emojis)
    return

async def sayInChannelOnce(channel, message, embed=None):
    today = datetime.datetime.combine(date.today(), datetime.time())
    async for msg in client.logs_from(channel, limit=100, after=today):
        if msg.author == client.user and msg.content == message:
           return False
    await sayInChannel(channel, message, embed)
    return True

async def donePlaying(voice, player):                                                                           # checks if the sound stopped playing
    global isPlaying
    while isPlaying:                                                                                                # if the sound is playing
        if player.is_done():                                                                                            # and the sound's now over
            await voice.disconnect()                                                                                    # leave the channel
            isPlaying = False                                                                                               # unflag isPlaying
        await asyncio.sleep(0.5)                                                                                        # only check if the sound is playing every 500 milliseconds

def ord(n):                                                                                                     # this adds an ordinal indicator to a number and returns it as a string
    return "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])                                   # IE: 1st 2nd 3rd 4th

@client.event
async def on_ready():                                                                                           # When the bot has logged in and is ready to start receiving commands
    app_info = await client.application_info()                                                                      # get the client info
    client.owner = app_info.owner                                                                                   # get the owner's name from the info
    await status_task(False, False)                                                                                         # set the game the bot is playing                                                                         

    print('Bot: {0.name}:{0.id}'.format(client.user))                                                               # print the bot info to the console
    print('Owner: {0.name}:{0.id}'.format(client.owner))                                                            # print the owner info to the console
    print('------------------')                                                                                     # a line seperator thingy
    perms = discord.Permissions.none()
    perms.administrator = True                                                                                      # this makes the bot an admin. Oh the possibilities
    url = discord.utils.oauth_url(app_info.id, perms)                                                               #   *Note to Self: do not abuse
    print('To invite me to a server, use this link\n{}'.format(url))                                                # print out the discord invitation url to the console
    if sys.maxsize > 2**32:                                                                                         # if the current system is x64 bit
        opus.load_opus('libopus-0.x64.dll')                                                                             # load opus x64 Windows library
    else:                                                                                                           # if the current system is x32 bit
        opus.load_opus('libopus-0.x86.dll')                                                                             # load opus x32 Windows library
    await checkBDays()
#                                                                                                                   # check if it's anyone's bithday today
    client.loop.create_task(status_task(True, False))                                                                          # send a thread to periodically check what day of the week it is

def run_client(Client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Client.start(*args, **kwargs))

if __name__ == '__main__':                                                                                      # weird preformance trick
    while True:
        try:                                                                                                            # try to
            run_client(client, discordToken)                                                                                               # run the client
        except KeyError:                                                                                                # if the config file isn't filled out
            print("config not yet filled out.")                                                                             # print to the console
        except discord.errors.LoginFailure as e:                                                                        # if the discord token is not correct
            print("Invalid discord token.")                                                                                 # hey, you're not me... stop editing my code
        except Exception as e:
            print("Error", e)  # or use proper logging
            logTime = datetime.datetime.now()
            log = open("log.txt","a")
            log.write("----------------------------" + "\n")
            log.write("----------------------------" + "\n")
            log.write("Log: " + str(logTime) + "\n")
            log.write("\n")
            log.write(str(e))
            log.write("\n")
            log.close()
            os.system('cls')
            print("An error occured! Restarting...")
            time.sleep(10)
Client.logout()
Client.close()