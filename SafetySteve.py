import os                                                                                                       # import all sorts of shit
import sys                                                                                                      # like the OS and the System
import datetime                                                                                                 # and time itself
import json                                                                                                     # some dude named jason
import asyncio                                                                                                  # a kitchen sinkio
import re                                                                                                       # re:re:re:re:re: meeting time
import praw
import random

try:                                                                                                            # try to
    import discord                                                                                              # get discord in here
except ImportError:                                                                                             # but if he's too drunk
    import pip                                                                                                  # get his gf in here
    pip.main(['install', 'discord'])                                                                            # and sober him up
    import discord                                                                                              # then drag the fucker back here
from discord import opus                                                                                        # and his noisy dog, too


try:                                                                                                            # try to
    with open('config.json', encoding='utf8') as f:                                                             # get jason f. at the party
        config = json.load(f)
except FileNotFoundError:                                                                                       # if he's too drunk
    with open('config.json', 'w') as f:                                                                         # fuck it, we'll find another jason, jason w.
        config = {}
        print("config file created.")                                                                           # shout it to the mountain tops that we got a new friend
        json.dump({'discord_token': '', 'response': '', 'words': ['']}, f)                                      # then brief him in on his former self

try:                                                                                                            # rinse and repeat for the designated driver, also named jason
    with open('discord-token.json') as f:
        token = json.load(f)
except FileNotFoundError:
    with open('discord-token.json', 'w') as f:
        token = {}
        print("config file created.")
        json.dump({'discord_token': ''}, f)



desc = config['description']                                                                                    # initialize a bunch of info from jason's wallet
invoker = config['invoker']
now = datetime.datetime.now()
userID = token['user_id']
mention = token['mention']
name = config['name']
commands = config['commands']
commandDescriptions = config['command_descriptions']
commandParams = config['command_params']
wordBlacklist = config['words']
badWordResponse = config['response']
lobbyChannelID = config['lobby_channel_id']
vcStart = config['vc_start']
gitLink = config['git_link']
fileExt = config['fileformat']
weekday = 0

# Reddit Config
reddit_id = token['client_id']
reddit_secret = token['client_secret']
reddit_agent = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

copycat = ""                                                                                                    # and some global shit we'll use later
voice = None
player = None
isPlaying = False

client = discord.Client(description=desc, max_messages=100)                                                     # then create the client


@client.event
async def on_message(msg: discord.Message):                                                                         # When I get a message
    global voice                                                                                                # remember what my voice sounds like
    global player                                                                                               # and try to remember how to speak
    global isPlaying                                                                                            # and check is the music is playing

    if 'wednesday' in msg.content.lower():
        await react(msg, "🐸")

    if msg.author.bot:                                                                                          # if the message was from drunk-me
        return                                                                                                  # gtfo 

    if msg.content.startswith(invoker):                                                                         # if the message was directed at me
        message = msg.content.lower()[len(invoker):]                                                            # informalize it

        if message == commands[0]:                                                                              # if the message is asking for help
            await help(msg)
            return
            
        if message[:4] == commands[0] and message[5:].strip() != "":       
            for command in commands: 
                if message[5:].strip() == command:                                                                   
                    await helpCommand(command, msg) 
                    return                                                       

        if message == commands[1]:                                                                                  # if the message is asking for git
            await git(msg)

        if message[:3] == commands[2]:                                                                            # if they ask you to repeat after them
            if message[4:] == "":
                await helpCommand('say', msg)
                return                                                                                          
            await say(msg, msg.content[4:])                                            
            await client.delete_message(msg)                                                                   
            return                                                                                              

        if message == commands[3]:                                                                              # when you need some animemes
            await subreddit('animemes', msg)
            return

        if message[:6] == commands[4]:                                                                          # when you need some reddit
            await subreddit(msg.content[8:], msg)
            return

        if message == commands[vcStart] and isPlaying:                                                          # if they ask you to leave
            isPlaying = False                                                                                   # unflag isPlaying
            await voice.disconnect()                                                                            # then leave the channel
            return                                                                                              # and gtfo

        for i in range(vcStart + 1, len(commands)):                                                             # if they ask you to play a sound
            if isPlaying:                                                                                       # if a sound is already playing
                await say(msg, 'I\'m already playing a sound! Please wait your turn.')                  # inform the user of their negligence
                return                                                                                          # and gtfo. smh
            if message == commands[i]:                                                                          # otherwise
                if msg.author.voice_channel:                                                                    # if the command is valid
                    try:                                                                                        # try to
                        voice = await client.join_voice_channel(msg.author.voice_channel)                       # create a voice client
                        player = voice.create_ffmpeg_player(                                                    # create a ffmpeg player
                            'sound/' + message + fileExt)
                        isPlaying = True                                                                        # flag isPlaying
                        player.start()                                                                          # start the player
                        client.loop.create_task(donePlaying(voice, player))                                     # start a thread to keep track of when the sound is finished playing
                    except Exception as e:                                                                      # if you can't
                        print(e)                                                                                # notify the host that there was an issue
                        await say(msg, 'There was an issue playing the sound file 🙁')  # notify the client that there was an issue
                        pass                                                                                    # drakememe.jpg
                else:                                                                                           # otherwise
                    await say(msg, 'You\'re not in a voice channel!')                   # inform the user that they're trying to use a voice command without being in a voice channel
                return                                                                                          # gtfo

    elif any([word in msg.content.lower() for word in wordBlacklist]):                                            # if the message contains any bad words
        await say(msg, '{}: {}'.format(msg.author.mention, badWordResponse))            # tell them politely, yet firmly, to leave
        return                                                                                                  # then gtfo

    elif client.user.mentioned_in(msg) and msg.mention_everyone is False:                                           # if a user mentions me
        await say(msg, 'Use {}{} for a list of commands'.format(invoker, commands[0]))  # birect him to the help command
        return                                                                                                  # gtfo


async def subreddit(sub, msg):
    if msg.content[8:].strip() == "":
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
        await client.send_message(msg.channel, message)
    else:
        await client.send_message(msg.channel, message, embed=embed)
    return

async def react(msg, emote):
    await client.add_reaction(msg, "🐸")
    return

async def help(msg):
    textCommandList = ""                                                                                
    voiceCommandList = ""                                                                               

    for command in commands[:vcStart]:                                                                 
        textCommandList = textCommandList + ", " + command
    for command in commands[vcStart:]:                                                                  
        voiceCommandList = voiceCommandList + ", " + command 

    embed = discord.Embed(title=name, description=desc, color=0xeee657)                                
    embed.add_field(name="🥕 Prefix", value="```" + invoker + "```", inline=False)                      
    embed.add_field(name="🔤 Text Commands", value=textCommandList[2:], inline=False)                  
    embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel', value=voiceCommandList[2:], inline=False)
    embed.set_footer(text="Created by {}".format(config['creator']))                                    

    await say(msg, "", embed)                                                 
    return                                                                                             

async def helpCommand(command, msg):
    embed = discord.Embed(title="Command:", description=command, color=0xeee657) #                      
    embed.add_field(name="Description:", 
        value=commandDescriptions[commands.index(command)], inline=False)
    embed.add_field(name="Usage:", 
        value="```" + invoker + command + " " +
        commandParams[commands.index(command)] + "```", inline=False)
    await say(msg, "", embed)                                      
    return

async def setPlaying(name, type=0):
    await client.change_presence(game=discord.Game(type=0, name=name))
    return


async def status_task():                                                                                            # choose what game to play based on the day of the week
    while True:
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
                channel = client.get_channel(lobbyChannelID)
                async for message in client.logs_from(channel, limit=1):
                    if message.author != client.user:
                        await say(channel, "Happy Wednesday, my dudes!")
                        break;
            except:
                print('Channel does not exist: {}'.format(channel))
        if now.weekday() == 3 and weekday != 3:
            await setPlaying(config['thursday_game'])
        if now.weekday() == 4 and weekday != 4:
            await setPlaying(config['friday_game'])
        if now.weekday() == 5 and weekday != 5:
            await setPlaying(config['saturday_game'])
        await asyncio.sleep(1800)                                                                               # only look at the clock every 30 minutes


async def donePlaying(voice, player):                                                                               # look to see if the sound stopped playing
    global isPlaying                                                                                            # try to remember if it was playing in the first place
    while isPlaying:                                                                                            # if was is playing
        if player.is_done():                                                                                    # and the sound's now over
            await voice.disconnect()                                                                            # leave the house, this party's lame af
            isPlaying = False                                                                                   # unflag isPlaying
        await asyncio.sleep(0.5)                                                                                # only pay attention to the music every 500 milliseconds

@client.event
async def on_ready():                                                                                               # When the bot has logged in and is ready to start receiving commands
    app_info = await client.application_info()                                                                  # get the client info
    client.owner = app_info.owner                                                                               # get the owner's name from the info
    await client.change_presence(game=discord.Game(type = 0, name = config['monday_game']))                     # set the game the bot is playing                                                                         

    print('Bot: {0.name}:{0.id}'.format(client.user))                                                           # print the bot info to the console
    print('Owner: {0.name}:{0.id}'.format(client.owner))                                                        # print the owner info to the console
    print('------------------')                                                                                 # a line seperator thingy
    perms = discord.Permissions.none()
    perms.administrator = True                                                                                  # this makes the bot an admin. Oh the possibilities
    url = discord.utils.oauth_url(app_info.id, perms)                                                           #   *Note to Self: do not abuse
    print('To invite me to a server, use this link\n{}'.format(url))                                            # print out the discord invitation url to the console

    if sys.maxsize > 2**32:                                                                                     # if the current system is x64 bit
        opus.load_opus('libopus-0.x64.dll')                                                                     # load opus x64 Windows library
    else:                                                                                                       # otherwise
        opus.load_opus('libopus-0.x86.dll')                                                                     # load opus x32 Windows library
#                                                                                                               # fuck linux
    client.loop.create_task(status_task())                                                                      # sed a thread to periodically check what day of the week it is



if __name__ == '__main__':                                                                                          # if the program has started
    try:                                                                                                        # try to
        client.run(token['discord_token'])                                                                      # run the client
    except KeyError:                                                                                            # if the config file isn't filled out
        print("config not yet filled out.")                                                                     # say that thing I just said
    except discord.errors.LoginFailure as e:                                                                    # if the discord token is not correct
        print("Invalid discord token.")                                                                         # hey, you're not me... stop editing my code
