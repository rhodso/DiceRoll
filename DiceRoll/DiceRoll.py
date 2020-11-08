#Imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import datetime
import random

#Set prefix character
prefix = "|"
total = 0

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
    log('Logged in as '+str(client.user.name)+' (ID:'+str(client.user.id)+') | Connected to '+str(len(client.guilds))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    log('')
    log('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    log('Ready!')
    game = discord.Game("with dice")
    await client.change_presence(status=discord.Status.online, activity=game)

#Commands
@client.event
async def on_message(message):
    if(message.content[:1] == prefix):
        #If message starts with the prefix, it's a command. Handle it as such

        #Command structure:
        #if(message.content == (prefix + "[Command Invoker]")):
        #   log("Running [Command name] command...")
        #   Do stuff
        #   End with:
        #   await message.channel.send( [Message (result of command)])

        #Help command
        if(message.content == (prefix + "help")):
            log("Running help command...")
            await message.channel.send('Usage: |rtd [NumberOfDice] [SidesOfDice]')
            await message.channel.send('[NumberOfDice] = The number of dice to roll. If more than 1, will add all scores together')
            await message.channel.send('[SidesOfDice] = The number of sides the dice has. Must be more than 1')

        #Ping command
        if(message.content == (prefix + "ping")):
            log("Running ping command...")
            await message.channel.send( 'Pong!')

        #RollTheDice Command
        if(message.content[:4] == (prefix + "rtd")):
            log("Running DiceRoll command...")
            
            #Split string
            SplitMessage = message.content.split(" ")
            
            #   1 = Number of dice
            #   2 = Sides of dice

            #Setup vars so not out of scope when it runs
            NoOfDice = 1
            SidesOfDice = 100

            try:
                #Try to parse parameters
                NoOfDice = int(SplitMessage[1])
                SidesOfDice = int(SplitMessage[2])

                #If there's only 1 dice, no need to add up and give total
                if(NoOfDice == 1):
                    await message.channel.send( 'You rolled a ' + str(random.randint(1,SidesOfDice)) + '!')
                else:
                    total = 0
                    #Add the dice up and give total
                    
                    for i in range (0,NoOfDice):
                        #Roll the dice and tell the user what they rolled
                        roll = random.randint(1,SidesOfDice-1)
                        await message.channel.send( 'You rolled a ' + str(roll) + '!')
                        #Add roll to total
                        total = total + roll
                    
                        #Output total
                    await message.channel.send( 'Your total is ' + str(total) + '!')      
            
            except:
                #Catch exception
                log("Something went wrong in rtd command. Parameters probably not typed correctly")
                #Tell the user to check their parameters 
                await message.channel.send( 'Something went wrong, did you type the parameters correctly?')

    else:
        #Message is not a command, ignore
        pass

#Run bot
client.run(str(getToken()))