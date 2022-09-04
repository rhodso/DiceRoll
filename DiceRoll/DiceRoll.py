#Imports
import asyncio
import platform
import datetime
import random
import time
import math
import os

# Discord imports
import discord
from discord import Option
from discord.ext import commands

def log(Message):
    print(str(datetime.datetime.now()) + '   ' + str(Message))

def getToken():
    tokenFile = open('token.txt', 'r')
    token = tokenFile.read()
    tokenFile.close()
    return token

def help_cmd():
    return '**Roll the dice command** Usage: _' + "/" + 'rtd [SidesOfDice] [Modifier] [Number of dice]_' + '\n**[SidesOfDice]** = The number of sides the dice has. Must be more than 1. **If blank then defaults to 20**'+ '\n**[Modifier]** = The modifier for the dice, applied after total is calculated. **If blank defaults to 0**'+ '\n**[NumberOfDice]** = The number of dice to roll. If more than 1, will add all scores together, max 500 dice. **If blank defaults to 1**'+ "\n\n" + "**Advantage and Disadvantage commands** Usage: _" + "/" + 'adv or dis [Modifier] [SidesOfDice]' + '\n**[Modifier]** = The modifier for the dice, applied after total is calculated. **If blank defaults to 0**'+ '\n**[SidesOfDice]** = The number of sides the dice has. Must be more than 1. **If blank then defaults to 20**'+ "\n\n" + "**Do maths command** Usage _" + "/" + "calc [Expression]_\n" + "**[Expression]** = The maths problem to solve. Must use pyhton formatting for it to work (i.e ** for exponents, not ^)"

def ping_cmd():
    return "Pong!"

def rtd_cmd(sides, modifier, number):
    NoOfDice = number
    SidesOfDice = sides
    Modifier = modifier

    try:
        runIt = True

        #Python doesn't have switch :(

        #Input validation for sides of dice
        if (SidesOfDice < 2):
            log("Sides less than 2, aborting...")
            return "Sides less than 2, aborting roll"
            runIt = False

        #Input validation for number of dice
        if (NoOfDice < 1):
            log("Dice count less than 1, aborting...")
            return "Dice count less than 1, aborting roll"
            runIt = False
        elif (NoOfDice > 500):
            log("Dice count greater than 500, aborting")
            return "Dice count greater than 500. Please split into smaller rolls"
            runIt = False

        if (runIt == True):
            #Input is valid
            log('s = ' + str(SidesOfDice) + ", m = " + str(Modifier) +
                ", n = " + str(NoOfDice))

            #If there's only 1 dice, no need to add up and give total
            if (NoOfDice == 1):
                #Do roll
                rollRes = random.randint(1, SidesOfDice)
                rollMod = rollRes + Modifier
                log('Res = ' + str(rollMod))

                if(SidesOfDice == 20 and rollRes == 1):
                    return "You rolled a nat 1 :(\n(With mod roll is a " + str(rollMod) + ")"

                elif(SidesOfDice == 20 and rollRes == 20):    
                    return "You rolled a nat 20!\n(With mod roll is a " + str(rollMod) + ")"

                else:
                    return 'You rolled a ' + str(rollMod) + '! (' + str(rollRes) + '+' + str(Modifier) + ')'

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
                return 'Your rolls: ' + rollStr + '\n' + 'Your total is ' + str(totalMod) + '! (' + str(total) + '+' + str(Modifier) + ')'

    except Exception as e:
        #Catch exception
        log('Exception occured, ' + str(e))
        #Tell the user to check their parameters
        return 'Something went wrong, did you type the parameters correctly?'
    
    # Catch all
    return 'Something went wrong'

def calc_cmd(expression):
    log("Expression = " + expression)
    res = str(eval(expression))
    log("Result = " + res)
    return res

def adv_cmd(modifier, sides):
    #Input validation for sides of dice
    if (sides < 2):
        log("Sides less than 2, aborting...")
        return "Sides less than 2, aborting roll"
        runIt = False

    responseStr = ''

    #Do roll
    rollRes1 = random.randint(1, sides)
    rollRes2 = random.randint(1, sides)
    rollRes = 0

    #Get the higher roll
    if (rollRes1 > rollRes2):
        rollRes = rollRes1
    else:
        rollRes = rollRes2

    rollMod = rollRes + modifier

    # Result
    if(rollRes == sides):
        responseStr += "You rolled a nat " + str(sides) + "!\n (with mod roll is a " + str(rollMod) + ")"
    elif(rollRes == 1):
        responseStr = responseStr + "You rolled a nat 1 :(\n (with mod roll is a " + str(rollMod) + ")\n_How do you even manage a nat 1 with advantage?_"
    else:
        responseStr += "You rolled a " + str(rollMod) + "! (" + str(rollRes) + "+" + str(modifier) + ")"

    log('Res = ' + str(rollMod))
    return responseStr

def dis_cmd(modifier, sides):
    #Input validation for sides of dice
    if (sides < 2):
        log("Sides less than 2, aborting...")
        return "Sides less than 2, aborting roll"
        runIt = False

    responseStr = ''

    #Do roll
    rollRes1 = random.randint(1, sides)
    rollRes2 = random.randint(1, sides)
    rollRes = 0

    #Get the higher roll
    if (rollRes1 < rollRes2):
        rollRes = rollRes1
    else:
        rollRes = rollRes2

    rollMod = rollRes + modifier

    # Result
    if(rollRes == sides):
        responseStr = responseStr + "You rolled a nat " + str(sides) + "!\n (with mod roll is a " + str(rollRes + modifier) + ")" + "_You got a nat "+ str(sides) + " with disadvantage? That's just impressive_"
    elif(rollRes == 1):
        responseStr = responseStr + "You rolled a nat 1 :(\n (with mod roll is a " + str(rollRes + modifier) + ")\n"
    else:
        responseStr = responseStr + "You rolled a " + str(rollRes + modifier) + "! (" + str(rollRes) + "+" + str(modifier) + ")"

    log('Res = ' + str(rollMod))

    return responseStr    

def binTheDice_cmd():
    reasons = [
        "they were giving shite rolls", "I just _needed_ a new set, yaknow?",
        "it's what my character would do",
        "once you lose one you might as well throw the whole fucking set",
        "they were looking at me funny",
        "idk but it's totally not because a new set is on sale",
        "it got a bit chipped when I threw it at a wall for giving me a 1",
        "this new set is shinier", "[ERROR] - Could not find good reason",
        "my patron said I should"
    ]

    # Reseed the RNG
    s = time.time()
    random.seed(s)

    #Get a random reason
    return "Binned the dice because " + random.choice(reasons)

def validate_cmd(maxVal, verbose):
    if (maxVal < 1):
        log("Max value less than 1, aborting...")
        return "Max value less than 1, aborting roll"

    checkList = [False for i in range(maxVal)]
    t0 = time.time_ns()
    success = False
    t = 0
    out = ""
    for t in range(0, (maxVal * 10000)):
        # Check to ensure that all numbers have been generated
        for c in checkList:
            success = True
            if (c == False):
                success = False
                break
        if(success):
            break
        # Success if false, carry on generating numbers
        roll = random.randint(1, maxVal)
        if(verbose and checkList[roll - 1] == False):
            out += str(roll) + " was generated at try " + str(t) + "\n"
            log(str(roll) + " was generated at try " + str(t))
        checkList[roll - 1] = True

    if(success):
        tf = time.time_ns() - t0
        # Validated
        log("Validated in " + str(tf / 100000000) + "s")
        out += "Validated in " + str(tf / 100000000) + "s and " + str(t-1) + " tries\n"

    else:
        # Failed
        log("Failed to validate")
        out += "Failed to validate"

    return out

intents = discord.Intents.default()
bot = discord.Bot()

def on_startup():
    s = time.time()
    random.seed(s)

    log('Starting up...')
    log('Python version: ' + platform.python_version())
    log('pycord version: ' + discord.__version__)
    log("RNG seeded with " + str(s))

def on_shutdown():
    log('Shutting down...')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with dice"))
    log('Bot ready')
    log('Logged in as ' + bot.user.name + ' (' + str(bot.user.id) + ')')

# Help command
@bot.slash_command(description="Lists commands")
async def help(ctx):
    log('Running help command')
    await ctx.respond(help_cmd())
        
# Ping command
@bot.slash_command(description="Ping the bot to see if it's alive")
async def ping(ctx):
    log("Running ping command")
    await ctx.respond(ping_cmd())

# Roll the dice command
@bot.slash_command(description="Roll a dice with specified sides and modifier, as well as a number of dice")
async def rtd(ctx, 
        sides: Option(discord.SlashCommandOptionType.integer, description="Number of sides on the dice", required=True, default=20, min_value=2, max_value=999, name="sides", type=4), 
        modifier: Option(discord.SlashCommandOptionType.integer, description="Modifier to add to the dice roll", required=True, default=0, min_value=-999, max_value=999, name="modifier", type=4),
        number: Option(discord.SlashCommandOptionType.integer, description="The Number of dice to roll", required=True, default=1, min_value=1, max_value=999, name="number", type=4)
    ):
    log("Running rtd command")
    await ctx.respond(rtd_cmd(sides, modifier, number))

# Calculator command
@bot.slash_command(description="Perform mathematical operations because maths is hard")
async def calc(ctx, 
        expression: Option(discord.SlashCommandOptionType.string, description="The expression to evaluate", required=True, name="expression", type=3)
    ):
    log("Running calc command")
    await ctx.respond(calc_cmd(expression))

# Roll with advantage command
@bot.slash_command(description="Rolls a dice with advantage")
async def adv(ctx, 
        sides: Option(discord.SlashCommandOptionType.integer, description="Number of sides on the dice", required=True, default=20, min_value=2, max_value=999, name="sides", type=4), 
        modifier: Option(discord.SlashCommandOptionType.integer, description="Modifier to add to the dice roll", required=True, default=0, min_value=-999, max_value=999, name="modifier", type=4),
    ):
    log("Running adv command")
    await ctx.respond(adv_cmd(modifier, sides))
    
# Roll with disadvantage command
@bot.slash_command(description="Rolls a dice with disadvantage")
async def dis(ctx,         
        sides: Option(discord.SlashCommandOptionType.integer, description="Number of sides on the dice", required=True, default=20, min_value=2, max_value=999, name="sides", type=4), 
        modifier: Option(discord.SlashCommandOptionType.integer, description="Modifier to add to the dice roll", required=True, default=0, min_value=-999, max_value=999, name="modifier", type=4),
    ):
    log("Running dis command")
    await ctx.respond(dis_cmd(modifier, sides))

# Bin the dice command
@bot.slash_command(description="Bins the dice (resets the RNG) and tells you why")
async def bin_the_dice(ctx):
    log("Running binTheDice command")
    await ctx.respond(binTheDice_cmd())

# Validate command
@bot.slash_command(description="Validates the RNG by checking that all numbers are generated")
async def validate(ctx, 
        max_val: Option(discord.SlashCommandOptionType.integer, description="The maximum value to validate to", required=True, default=20, min_value=2, max_value=999, name="max_val", type=4),
        verbose: Option(discord.SlashCommandOptionType.boolean, description="Whether to output the numbers generated", required=True, default=False, name="verbose", type=5)
    ):
    log("Running validate command")
    await ctx.respond(validate_cmd(max_val, verbose))

# Starting the bot
on_startup()
bot.run(getToken())
on_shutdown()
