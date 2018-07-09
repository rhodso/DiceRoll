#Imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import datetime

#Set prefix character
prefix = "|"

#Def log method
def log(Message):
    print(str(datetime.datetime.now())+ '   ' + str(Message))

#Def Method to read token from the file
def getToken():
    tokenFile = open('token.txt','r')
    token = tokenFile.read()
    return token

#Define client
client = Bot(description='', command_prefix=prefix, pm_help = False)

#Startup sequence
@client.event
async def on_ready():
    log('Initialising...')
    log('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    log('')
    log('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    log('Ready!')
    return await client.change_presence(game=discord.Game(name='with dice')) 


##Commands
#@client.command()
#async def ping(*args):
#    log("Runing ping command...")
#    await client.say('Pong!')

#async def rtd(*args):
#    log("Running rtd command...")
#    await client.say("WIP")

@client.event
async def on_message(message):
    if(message.content[:1] == prefix):
        
        if(message.content == (prefix + "ping")):
            log("Running ping command...")
            await client.send_message(client.get_channel(), 'Pong!')

    else:
        pass

client.run(str(getToken()))