import os                                                                                                       # import all sorts of shit
import sys                                                                                                      # like the OS and the System
import datetime                                                                                                 # and time itself
import json                                                                                                     # some dude named jason
import asyncio                                                                                                  # a kitchen sinkio
import re                                                                                                       # re:re:re:re:re: meeting time
try:                                                                                                            # try to
    import discord                                                                                              # get discord in here
except ImportError:                                                                                             # but if he's too drunk
    import pip                                                                                                  # get his gf in here
    pip.main(['install', 'discord'])                                                                            # and sober him up
    import discord                                                                                              # then drag the fucker back here
from discord import opus                                                                                        # and his noisy dog, too


try:                                                                                                            # try to
    with open('config.json') as f:                                                                              # get jason f. at the party
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
userID = '<@430061939805257749>'
mention = '@Safety-Steve#1394'
name = config['name']
commands = config['commands']

copycat = ""                                                                                                    # and some global shit we'll use later
voice = None
player = None
isPlaying = False

client = discord.Client(description=desc, max_messages=100)                                                     # then create the client



async def status_task():                                                                                            # choose what game to play based on the day of the week
    while True:
        now = datetime.datetime.now()
        if now.weekday() == 6:
            await client.change_presence(game=discord.Game(type = 0, name = config['sunday_game']))
        if now.weekday() == 0:
            await client.change_presence(game=discord.Game(type = 0, name = config['monday_game']))
        if now.weekday() == 1:
            await client.change_presence(game=discord.Game(type = 0, name = config['tuesday_game']))
        if now.weekday() == 2:
            await client.change_presence(game=discord.Game(type = 0, name = config['wednesday_game']))
        if now.weekday() == 3:
            await client.change_presence(game=discord.Game(type = 0, name = config['thursday_game']))
        if now.weekday() == 4:
            await client.change_presence(game=discord.Game(type = 0, name = config['friday_game']))
        if now.weekday() == 5:
            await client.change_presence(game=discord.Game(type = 0, name = config['saturday_game']))
        await asyncio.sleep(1800)                                                                               # only look at the clock every 30 minutes



async def donePlaying(voice, player):                                                                               # look to see if the sound stopped playing
    global isPlaying                                                                                            # try to remember if it was playing in the first place
    while isPlaying:                                                                                            # if was is playing
        if player.is_done():                                                                                    # and the sound's now over
            await voice.disconnect()                                                                            # leave the house, this party's lame af
            isPlaying = False                                                                                   # unflag isPlaying
        await asyncio.sleep(0.5)                                                                                # only pay attention to the music every 500 milliseconds



@client.event
async def on_message(msg: discord.Message):                                                                         # When I get a message
    global voice                                                                                                # remember what my voice sounds like
    global player                                                                                               # and try to remember how to speak
    global isPlaying                                                                                            # and check is the music is playing
    if msg.author.bot:                                                                                          # check if the message was from drunk-me
        return                                                                                                  # if it was, gtfo

    if msg.content.startswith(invoker):                                                                         # if the message was directed at me
        message = msg.content.lower()[len(invoker):]                                                            # informalize it
        if message == commands[0]:                                                                              # if the message is asking for help

            textCommandList = ""                                                                                # take a deep breath
            voiceCommandList = ""                                                                               # _deeper_

            for command in commands[:config['vc_start']]:                                                       # recite to them the constitution
                textCommandList = textCommandList + ", " + command
            for command in commands[config['vc_start']:]:                                                       # and their freedom of speech laws
                voiceCommandList = voiceCommandList + ", " + command 

            embed = discord.Embed(title=name, description=desc, color=0xeee657)                                 # and make a colorful paper
            embed.add_field(name="🥕 Prefix", value="```" + invoker + "```", inline=False)                      
            embed.add_field(name="🔤 Text Commands", value=textCommandList[2:], inline=False)                   # with what you just told them written on it
            embed.add_field(name='🔊 Voice Commands - These require you to be in a voice channel',              # and remind them not to be an idiot
                value=voiceCommandList[2:], inline=False)
            embed.set_footer(text="Created by {}".format(config['creator']))                                    # and slap my name on it 

            await client.send_message(msg.channel, embed=embed)                                                 # then hand them the paper
            return                                                                                              # and gtfo

        if message[:4] == commands[0] and message[5:].strip() != "":       
            for command in commands: 
                if message[5:].strip() == command:                                                                   
                    embed = discord.Embed(title="Command:", description=command, color=0xeee657) #                      
                    embed.add_field(name="Description:", 
                        value=config['command_descriptions'][commands.index(command)], inline=False)
                    embed.add_field(name="Usage:", 
                        value="```" + invoker + command + " " +
                        config['command_params'][commands.index(command)] + "```", inline=False)
                    await client.send_message(msg.channel, embed=embed)                                      
                    return                                                         

        if message == commands[1]:                                                                                  # if the message is asking for git
            gitMessage = 'Check me out on GitHub, the only -Hub website you visit, I hope...'                   # make sure they're christian enough                                                                   
            embed = discord.Embed(title="", description=config['git_link'], color=0xeee657)                     # prepare the git link
            await client.send_message(msg.channel, gitMessage, embed=embed)                                                 # send it
            return                                                                                              # gtfo

        if message[:3] == commands[2] and msg.content[4:] != "":                                                    # if they ask you to repeat after them
            copy = msg.content[4:]                                                                              # remember what they say
            await client.send_message(msg.channel, copy)                                                        # and mock them like a parrot
            await client.delete_message(msg)                                                                    # then make them take it back
            return                                                                                              # and gtfo

        if message == commands[config['vc_start']] and isPlaying:                                                   # if they ask you to leave
            isPlaying = False                                                                                   # unflag isPlaying
            await voice.disconnect()                                                                            # then leave the channel
            return                                                                                              # and gtfo

        for i in range(config['vc_start'] + 1, len(commands)):                                                      # if they ask you to play a sound
            if isPlaying:                                                                                       # if a sound is already playing
                await client.send_message(msg.channel, 'I\'m already playing a sound! Please wait your turn.')  # inform the user of their negligence
                return                                                                                          # and gtfo. smh
            if message == commands[i]:                                                                          # otherwise
                if msg.author.voice_channel:                                                                    # if the command is valid
                    try:                                                                                        # try to
                        voice = await client.join_voice_channel(msg.author.voice_channel)                       # create a voice client
                        player = voice.create_ffmpeg_player(                                                    # create a ffmpeg player
                            'sound/' + message + config['fileformat'])
                        isPlaying = True                                                                        # flag isPlaying
                        player.start()                                                                          # start the player
                        client.loop.create_task(donePlaying(voice, player))                                     # start a thread to keep track of when the sound is finished playing
                    except Exception as e:                                                                      # if you can't
                        print(e)                                                                                # notify the host of their idiocy
                        await client.send_message(msg.channel, 'There was an issue playing the sound file 🙁')  # notify the client of their inability to preform simple cognition
                        pass                                                                                    # drakememe.jpg
                else:                                                                                           # otherwise
                    await client.send_message(msg.channel, 'You\'re not in a voice channel!')                   # inform the user that they're an imbicel for trying to use a voice command without being in a voice channel
                return                                                                                          # gtfo

    elif any([word in msg.content.lower() for word in config['words']]):                                            # if the message contains any bad words
        await client.send_message(msg.channel, '{}: {}'.format(msg.author.mention, config['response']))         # tell them politely, yet firmly, to leave
        return                                                                                                  # then gtfo

    elif client.user.mentioned_in(msg) and msg.mention_everyone is False:                                           # if a user yells at me
        await client.send_message(msg.channel, 'Use {}{} for a list of commands'.format(invoker, commands[0]))  # fuck him, here's a hint ya idiot
        return                                                                                                  # gtfo



@client.event
async def on_ready():                                                                                               # When the bot has logged in and is ready to start receiving commands
    app_info = await client.application_info()                                                                  # get the client info
    client.owner = app_info.owner                                                                               # get the owner's name from the info
    await client.change_presence(game=discord.Game(type = 0, name = config['game']))                            # set the game the bot is playing, this will only stay if the current day is not one of the 7 days of the week
#                                                                                                               # if you are reading this in the far furture when the now-imortal president Danny DeVito
#                                                                                                               # has ruled that there are actually 10 days in a week, God help you.

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
