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
    print(str(datetime.datetime.now()) + '   ' + str(Message))


#Def Method to read token from the file
def getToken():
    tokenFile = open('token.txt', 'r')
    token = tokenFile.read()
    return token


#Define client
client = Bot(description='', command_prefix=prefix, pm_help=False)


#Startup sequence
@client.event
async def on_ready():
    log('Initialising...')
    log('Logged in as ' + str(client.user.name) + ' (ID:' +
        str(client.user.id) + ') | Connected to ' + str(len(client.guilds)) +
        ' servers | Connected to ' + str(len(set(client.get_all_members()))) +
        ' users')
    log('')
    log('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    log('Ready!')
    game = discord.Game("with dice")
    await client.change_presence(status=discord.Status.online, activity=game)


#Commands
@client.event
async def on_message(message):
    if (message.content[:1] == prefix):
        #If message starts with the prefix, it's a command. Handle it as such

        #Command structure:
        #if(message.content == (prefix + "[Command Invoker]")):
        #   log("Running [Command name] command...")
        #   Do stuff
        #   End with:
        #   await message.channel.send( [Message (result of command)])

        #Help command
        if (message.content == (prefix + "help")):
            log("Running help command...")
            await message.channel.send(
                'Usage: **' + prefix +
                'rtd [SidesOfDice] [Number of dice] [Modifier]**' +
                '\n**[SidesOfDice]** = The number of sides the dice has. Must be more than 1. **If blank then defaults to 20**'
                +
                '\n**[NumberOfDice]** = The number of dice to roll. If more than 1, will add all scores together, max 500 dice. **If blank defaults to 1**'
                +
                '\n**Modifier]** = The modifier for the dice, applied after total is calculated. **If blank defaults to 0**'
            )

        #Ping command
        if (message.content == (prefix + "ping")):
            log("Running ping command...")
            await message.channel.send('Pong!')

        #RollTheDice Command
        if (message.content[:4] == (prefix + "rtd")):
            log("Running DiceRoll command...")

            #Split string
            SplitMessage = message.content.split(" ")

            #   1 = Sides of dice
            #   2 = Number of dice
            #   3 = Modifier

            #Setup vars so not out of scope when it runs
            NoOfDice = 1
            SidesOfDice = 20
            Modifer = 0

            try:
                runIt = True

                #Python doesn't have switch :(

                #Message is command + 1 arg
                if (len(SplitMessage) > 1):
                    SidesOfDice = int(SplitMessage[1])

                #Input validation for sides of dice
                if (SidesOfDice < 2):
                    log("Sides less than 2, aborting...")
                    await message.channel.send(
                        "Sides less than 2, aborting roll")
                    runIt = False

                #Message is command + 2 args
                if (len(SplitMessage) > 2):
                    NoOfDice = int(SplitMessage[2])

                #Input validation for number of dice
                if (NoOfDice < 1):
                    log("Dice count less than 1, aborting...")
                    await message.channel.send(
                        "Dice count less than 1, aborting roll")
                    runIt = False
                elif (NoOfDice > 500):
                    log("Dice count greater than 500, aborting")
                    await message.channel.send(
                        "Dice count greater than 500. Please split into smaller rolls"
                    )
                    runIt = False

                #Message is command + 3 args
                if (len(SplitMessage) > 3):
                    Modifer = int(SplitMessage[3])

                if (runIt == True):
                    #Input is valid
                    log('s = ' + str(SidesOfDice) + ", n = " + str(NoOfDice) +
                        ", m = " + str(Modifer))

                    #If there's only 1 dice, no need to add up and give total
                    if (NoOfDice == 1):
                        rollRes = random.randint(1, SidesOfDice)
                        rollMod = rollRes + Modifer
                        log('Res = ' + str(rollMod))
                        await message.channel.send('You rolled a ' +
                                                   str(rollRes) + '! (' +
                                                   str(rollRes) + '+' +
                                                   str(Modifer) + ')')
                    else:
                        total = 0
                        rollStr = ''
                        #Add the dice up and give total

                        for i in range(0, NoOfDice):
                            #Roll the dice and tell the user what they rolled
                            roll = random.randint(1, SidesOfDice - 1)
                            rollStr = rollStr + str(roll) + ", "

                            #Add roll to total
                            total = total + roll

                        #Output total
                        totalMod = total + Modifer

                        #remove last 2 chars so that it doesn't look weird
                        rollStr = rollStr[:-2]
                        log('Res = ' + str(totalMod))
                        await message.channel.send('Your rolls: ' + rollStr +
                                                   '\n' + 'Your total is ' +
                                                   str(totalMod) + '! (' +
                                                   str(total) + '+' +
                                                   str(Modifer) + ')')

            except Exception as e:
                #Catch exception
                log('Exception occured, ' + str(e))
                #Tell the user to check their parameters
                await message.channel.send(
                    'Something went wrong, did you type the parameters correctly?'
                )

    else:
        #Message is not a command, ignore
        pass


#Run bot
client.run(str(getToken()))