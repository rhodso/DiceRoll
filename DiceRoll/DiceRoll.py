#Imports
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import datetime
import random
import time

#Set prefix character
prefix = "."
total = 0

#Def list of reasons to bin the dice
reasons = [
    "they were giving shite rolls",
    "I just _needed_ a new set, yaknow?",
    "it's what my character would do",
    "once you lose one you might as well throw the whole fucking set",
    "they were looking at me funny",
    "idk but it's totally not because a new set is on sale",
    "it got a bit chipped when I threw it at a wall for giving me a 1",
    "this new set is shinier",
    "[ERROR] - Could not find good reason",
    "my patron said I should"
]

#Def log method
def log(Message):
    print(str(datetime.datetime.now()) + '   ' + str(Message))


#Def Method to read token from the file
def getToken():
    tokenFile = open('token.txt', 'r')
    token = tokenFile.read()
    tokenFile.close()
    return token


#Def method to read prefix from file
def getPrefix():
    prefixFile = open('prefix.txt', 'r')
    prefix = prefixFile.read()
    prefixFile.close()
    return prefix


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
    s = time.time()
    random.seed(s)
    log("RNG seeded with " + str(s))
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
                'rtd [SidesOfDice] [Modifier] [Number of dice]**' +
                '\n**[SidesOfDice]** = The number of sides the dice has. Must be more than 1. **If blank then defaults to 20**'
                +
                '\n**[Modifier]** = The modifier for the dice, applied after total is calculated. **If blank defaults to 0**'
                +
                '\n**[NumberOfDice]** = The number of dice to roll. If more than 1, will add all scores together, max 500 dice. **If blank defaults to 1**'
            )

        #Ping command
        if (message.content == (prefix + "ping")):
            log("Running ping command...")
            await message.channel.send('Pong!')

        #Bin the dice command
        if (message.content.lower() == (prefix + "binthedice")):
            log("Binning dice..")
            s = time.time()  #Get new seed, and apply
            random.seed(s)
            log("Binned dice, new seed initialised as " + str(s))

            await message.channel.send("Binned dice because " + random.choice(reasons))

        #Validate command
        verbose = False
        if (message.content[:9] == (prefix + "validate")):
            SplitMessage = message.content.split(" ")
            maxValue = 0
            if (len(SplitMessage) == 1):
                maxValue = 20
            elif (len(SplitMessage) == 2):
                maxValue = int(SplitMessage[1])
            elif (len(SplitMessage) == 3):
                maxValue = int(SplitMessage[1])
                if (SplitMessage[2].lower() == "v"
                        or SplitMessage[2].lower() == "verbose"):
                    verbose = True

            log('Starting validation to ' + str(maxValue))
            await message.channel.send('Starting validation to ' +
                                       str(maxValue))

            checkList = [False for i in range(maxValue)]
            t0 = time.time_ns()
            success = False
            t = 0
            for t in range(0, (maxValue * 10000)):
                #Check to ensure that all numbers have been generated
                for c in checkList:
                    success = True
                    if (c == False):
                        success = False
                        break
                if (success):
                    break
                #Success if false, carry on generating numbers
                roll = random.randint(1, maxValue)
                if (verbose and checkList[roll - 1] == False):
                    await message.channel.send(
                        str(roll) + " was generated at try " + str(t))
                    log(str(roll) + " was generated at try " + str(t))
                checkList[roll - 1] = True

            #Either success is true, or we ran out of time
            if (success):
                tf = time.time_ns() - t0
                #Validated
                log("Validation complete in " + str(tf / 100000000) +
                    " seconds")
                await message.channel.send("Validation complete in " +
                                           str(tf / 100000000) +
                                           " seconds and " + str(t - 1) +
                                           " tries")
            else:
                #Not validated
                log("Validation failed")
                await message.channel.send("Validation failed")

        #RollTheDice Command
        if (message.content[:4] == (prefix + "rtd")):
            log("Running DiceRoll command...")

            #Split string
            SplitMessage = message.content.split(" ")

            #   1 = Sides of dice
            #   2 = Modifier
            #   3 = Number of dice

            #Setup vars so not out of scope when it runs
            NoOfDice = 1
            SidesOfDice = 20
            Modifier = 0

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
                    Modifier = int(SplitMessage[2])

                #Message is command + 3 args
                if (len(SplitMessage) > 3):
                    NoOfDice = int(SplitMessage[3])

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

                if (runIt == True):
                    #Input is valid
                    log('s = ' + str(SidesOfDice) + ", m = " + str(Modifier) +
                        ", n = " + str(NoOfDice))

                    #If there's only 1 dice, no need to add up and give total
                    if (NoOfDice == 1):
                        rollRes = random.randint(1, SidesOfDice)
                        rollMod = rollRes + Modifier
                        log('Res = ' + str(rollMod))
                        await message.channel.send('You rolled a ' +
                                                   str(rollMod) + '! (' +
                                                   str(rollRes) + '+' +
                                                   str(Modifier) + ')')
                    else:
                        total = 0
                        rollStr = ''
                        #Add the dice up and give total

                        for i in range(0, NoOfDice):
                            #Roll the dice and tell the user what they rolled
                            roll = random.randint(1, SidesOfDice)
                            rollStr = rollStr + str(roll) + ", "

                            #Add roll to total
                            total = total + roll

                        #Output total
                        totalMod = total + Modifier

                        #remove last 2 chars so that it doesn't look weird
                        rollStr = rollStr[:-2]
                        log('Res = ' + str(totalMod))
                        await message.channel.send('Your rolls: ' + rollStr +
                                                   '\n' + 'Your total is ' +
                                                   str(totalMod) + '! (' +
                                                   str(total) + '+' +
                                                   str(Modifier) + ')')

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