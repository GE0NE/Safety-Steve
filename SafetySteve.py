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

try:                                                                                                            # try to
    import discord                                                                                                  # import discord.py
except ImportError:                                                                                             # if discord.py isn't installed
    import pip                                                                                                      # import pip
    pip.main(['install', 'discord'])                                                                                # install discord.py
    import discord                                                                                              # import discord.py
from discord import opus                                                                                        # inport opus, the discord sound lib
from discord.utils import get

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
            "response": "Hey! No bad words, please. This is a Christian server!",
            "words": ["heck", "frick", "fick", "golly", "gosh", "jeeper", "darn", 
            "drat"]}, f, indent = 4)
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
        json.dump({'dates': [{"Name": "John Doe", "Day": 31, "Month": 12, "Year": 1990, 
            "Tag": "<@430061939805257749>", "Type": "birthday", "Message": "Happy #age #type, #tag!",
            "Channel": "#lobby", "React": "🎉#🎂#🎊#🍰"}]}, f, indent = 4)
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
voiceCommandHelp = []
voiceCommandParams = []

# Init command info
for command in textCommands:
    textCommandList.append(command['Command'])
    textCommandHelp.append(command['Help'])
    textCommandParams.append(command['Params'])

for command in voiceCommands:
    voiceCommandList.append(command['Command'])
    voiceCommandHelp.append(command['Help'])
    voiceCommandParams.append(command['Params'])

# List of commands
commandList = textCommandList + voiceCommandList
commandHelp = textCommandHelp + voiceCommandHelp
commandParams = textCommandParams + voiceCommandParams

# Bad words and the response to them
wordBlacklist = config['words']
badWordResponse = config['response']

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
copycat = ""
voice = None
player = None
isPlaying = False
weekday = 0

# The client
client = discord.Client(description=desc, max_messages=100)                                                     # create the client


@client.event
async def on_message(msg: discord.Message):                                                                     # When a message is sent to a channel
    global voice
    global player
    global isPlaying
    if 'wednesday' in msg.content.lower():                                                                      # if the message contains 'wednesday'
        await react(msg, "🐸")                                                                                      # react with a frog emoji

    if msg.author.bot:                                                                                          # if the message was from the bot
        return                                                                                                      # ignore it

    if msg.content.startswith(invoker):                                                                         # if the message starts with the invoker
        message = msg.content.lower()[len(invoker):]                                                            

        if message == textCommands[0]['Command']:                                                                   # help command
            await help(msg)
            return       

        if message[:4] == textCommands[0]['Command']:                                                               # help [command] command
            await helpCommand(message[5:], msg) 
            return                                            

        if message == textCommands[1]['Command']:                                                                   # git command
            await git(msg)

        if message[:3] == textCommands[2]['Command']:                                                               # say <text> command
            if message[4:] == "":
                await helpCommand('say', msg)
                return                                                                                          
            await say(msg, msg.content[4:])                                            
            await client.delete_message(msg)                                                                   
            return                                                                                              

        if message == textCommands[3]['Command']:                                                                   # animeme command
            await subreddit('animemes', msg, True)
            return

        if message[:6] == textCommands[4]['Command']:                                                               # reddit [subreddit] command
            await subreddit(msg.content[8:], msg)
            return

        if message[:5] == textCommands[5]['Command']:                                                               # ascii command
            if len(message[6:]) > 30:
                await say(msg, "Whoah! That's too many letter! Keep it below 30 please.")
                return
            if len(message[6:].strip()) < 1:
                await helpCommand('ascii', msg)
                return
            await sayAscii(msg, message[6:])
            return


        if message == voiceCommands[0]['Command'] and isPlaying:                                                    # leave command
            isPlaying = False
            await voice.disconnect()
            return

        for i in range(1, len(voiceCommands)):                                                                      # handler for all voice commands
            if isPlaying:                                                                                               # if a sound is already playing
                await say(msg, 'I\'m already playing a sound! Please wait your turn.')                                      # send a message informing them
                return
            if message == voiceCommands[i]['Command']:                                                                  # otherwise
                if msg.author.voice_channel:                                                                                # if the user is in a voice channel
                    try:                                                                                                        # try to
                        voice = await client.join_voice_channel(msg.author.voice_channel)                                           # create a voice clientw
                        player = voice.create_ffmpeg_player(                                                                        # create a ffmpeg player
                            'sound/' + message + fileExt)
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

    elif any([word in msg.content.lower() for word in wordBlacklist]):                                          # if the message does not start with the invoker but it contains bad words
        await say(msg, '{}: {}'.format(msg.author.mention, badWordResponse))                                        # tell them politely, yet firmly, to leave
        return

    elif client.user.mentioned_in(msg) and msg.mention_everyone is False:                                       # if a user mentions the bot
        await say(msg, 'Use {}{} for a list of commands'.format(invoker, textCommands[0]['Command']))               # send the help command
        return


async def subreddit(sub, msg, bypassErrorCheck = False):
    if not bypassErrorCheck and msg.content[8:].strip() == "":
        await helpCommand('reddit', msg)
        return
    reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_agent)
    submissionList = []
    try:
        for submission in reddit.subreddit(sub).hot(limit=100):
            if submission.url[-3:] == "png" or submission.url[-3:] == "jpg":
                submissionList.append(submission)
        if len(submissionList) > 0:
            submission = submissionList[random.randint(1, len(submissionList))]
            embed = discord.Embed(title=submission.title, 
                url="https://reddit.com{}".format(submission.permalink), color=0xeee657)
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
    embed = discord.Embed(title="", description=gitLink, color=0xeee657)                                
    await say(msg, gitMessage, embed)                                     
    return                                                                                              

async def say(msg, message, embed=None):
    if embed == None:
        await sayInChannel(msg.channel, message)
    else:
        await sayInChannel(msg.channel, message, embed=embed)
    return

async def sayInChannel(channel, message, embed=None):
    if embed == None:
        await client.send_message(channel, message)
    else:
        await client.send_message(channel, message, embed=embed)
    return

async def react(msg, emote):
    try:
        await client.add_reaction(msg, emote)
    except:
        try:
            emote = get(client.get_all_emojis(), name=emote)
            await client.add_reaction(msg, emote)
        except:
            await say(msg, "I don't know that emoji");
    return

async def help(msg):

    embed = discord.Embed(title=name, description=desc, color=0xeee657)                                
    embed.add_field(name="🥕 Prefix", value="```" + invoker + "```", inline=False)                      
    embed.add_field(name="🔤 Text Commands", value=", ".join(textCommandList), inline=False)                  
    embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel', value=", ".join(voiceCommandList), inline=False)
    embed.set_footer(text="Created by {}".format(config['creator']))                                    

    await say(msg, "", embed)                                                 
    return                                                                                             

async def helpCommand(command, msg):

    command = command.strip()

    if command not in commandList:
        await say(msg, "That's not a command I know.")
        return
                    
    embed = discord.Embed(title="Command:", description=command, color=0xeee657) #                      
    embed.add_field(name="Description:", value=commandHelp[commandList.index(command)], inline=False)
    embed.add_field(name="Usage:", value="```" + invoker + command + " " + commandParams[commandList.index(command)] + "```", inline=False)
    await say(msg, "", embed)                                      
    return

async def sayAscii(msg, message):
    ascii = []
    output = ""
    if len(message) > 6:
        await sayAscii(msg, message[:6])
        await sayAscii(msg, message[6:])
        return
    for letter in list(message):
        if letter in bubbleFontMask:
            ascii.append(bubbleFont[bubbleFontMask.index(letter)])
    for i in range(0, 6):
        for letterBlock in ascii:
            letterBreakdown = letterBlock.splitlines()
            for j, line in enumerate(letterBreakdown):
                while len(line) < 5:
                    line += " "
                    letterBreakdown[j] += "╱"
            output = output + letterBreakdown[i]
        output = output + '\n'

    await say(msg, output)

async def setPlaying(name, type=0):
    await client.change_presence(game=discord.Game(type=0, name=name))
    return


async def status_task(wait):                                                                                        # choose what game to play based on the day of the week
    while True:
        global weekday
        oldWeekday = weekday
        now = datetime.datetime.now()
        if now.weekday() == 6 and weekday != 6:
            await setPlaying(config['sunday_game'])
        if now.weekday() == 0 and weekday != 0:
            await setPlaying(config['monday_game'])
        if now.weekday() == 1 and weekday != 1:
            await setPlaying(config['tuesday_game'])
        if now.weekday() == 2 and weekday != 2:
            await setPlaying(config['wednesday_game'])
            try:
                wednesdayChannels = config['wednesday_channels'].replace(" ", "").split('#')
                for wednesdayChannel in wednesdayChannels:
                    channel = client.get_channel(userInfo['channel_ids'][wednesdayChannel])
                    await sayInChannelOnce(channel, "Happy Wednesday, my dudes!")
                break;
            except:
                print('Channel does not exist: {}'.format(channel))
        if now.weekday() == 3 and weekday != 3:
            await setPlaying(config['thursday_game'])
        if now.weekday() == 4 and weekday != 4:
            await setPlaying(config['friday_game'])
        if now.weekday() == 5 and weekday != 5:
            await setPlaying(config['saturday_game'])
        if oldWeekday != weekday:
            await checkBDays()
        weekday = now.weekday()
        oldWeekday = weekday
        if wait != True:
            return
        await asyncio.sleep(900)                                                                               # only look at the clock every 30 minutes

async def checkBDays():
    today = datetime.datetime.today()
    
    for date in dates:
        dateDay = date['Day']
        dateMonth = date['Month']
        dateYear = date['Year']
        if today.day == dateDay and today.month == dateMonth:
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
                reactCondition = await sayInChannelOnce(channel, formattedDateMessage)
                async for message in client.logs_from(channel, limit=1):
                    msg = message
                    break
                if reactCondition:
                    for emojis in reacts:
                        await react(msg, emojis)
                    return
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
    await status_task(False)                                                                                         # set the game the bot is playing                                                                         

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
    client.loop.create_task(status_task(True))                                                                          # send a thread to periodically check what day of the week it is

def run_client(Client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(Client.start(*args, **kwargs))
        except Exception as e:
            print("Error", e)  # or use proper logging
            time = datetime.datetime.now()
            log = open("log.txt","a")
            log.write("----------------------------" + "\n")
            log.write("----------------------------" + "\n")
            log.write("Log: " + str(time) + "\n")
            log.write("\n")
            log.write(str(e))
            log.write("\n")
            os.system('cls')
            print("An error occured! Restarting...")
            time.sleep(10)

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
            time = datetime.datetime.now()
            log = open("log.txt","a")
            log.write("----------------------------" + "\n")
            log.write("----------------------------" + "\n")
            log.write("Log: " + str(time) + "\n")
            log.write("\n")
            log.write(str(e))
            log.write("\n")
            os.system('cls')
            print("An error occured! Restarting...")
            time.sleep(10)