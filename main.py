# Import standard packages that we know we have access to
import datetime
import time
import os
import sys
import subprocess
import logging
import random
import typing

# Global variables
BOT_TOKEN = ""
LOG_TO_FILE = False
LOG_FILE_NAME = "bot.log"
TEST_GUILD_ID = 302584459579097118

# Delete the log file if it exists
if os.path.isfile(path=LOG_FILE_NAME):
    os.remove(path=LOG_FILE_NAME)

# Set up logging
if LOG_TO_FILE:
    log_handler = logging.basicConfig(format='%(asctime)s %(message)s', filename=LOG_FILE_NAME, encoding='utf-8', level=logging.INFO)
else:
    log_handler = logging.basicConfig(format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO)

# Try to import libraries
try:
    logging.info(msg="Importing libraries...")
    # TODO: Add other needed libraries here
    import discord
    from discord import app_commands
    from discord.ext import commands
    
except ImportError:
    # Log which libraries failed to import
    logging.error(msg="Failed to import libraries: " + str(sys.exc_info()[1]))

    # Install requirements from requirements.txt, restart the script and exit
    logging.error(msg="Failed to import libraries, installing requirements...")
    subprocess.call(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])

    # Restart the script
    logging.info(msg="Restarting script...")
    subprocess.call(['python', 'main.py'])
    exit()

def rtd_cmd(sides, modifier, number):
    NoOfDice = number
    SidesOfDice = sides
    Modifier = modifier

    try:
        runIt = True

        # Python doesn't have switch :(
        # Python does now, but I'm too lazy to change it

        #Input validation for sides of dice
        if (SidesOfDice < 2):
            logging.error(msg="Sides less than 2, aborting...")
            return "Sides less than 2, aborting roll"
            runIt = False

        #Input validation for number of dice
        if (NoOfDice < 1):
            logging.error(msg="Dice count less than 1, aborting...")
            return "Dice count less than 1, aborting roll"
            runIt = False
        elif (NoOfDice > 500):
            logging.error(msg="Dice count greater than 500, aborting")
            return "Dice count greater than 500. Please split into smaller rolls"
            runIt = False

        if (runIt == True):
            #Input is valid
            logging.info(msg='s = ' + str(SidesOfDice) + ", m = " + str(Modifier) +
                ", n = " + str(NoOfDice))

            #If there's only 1 dice, no need to add up and give total
            if (NoOfDice == 1):
                #Do roll
                rollRes = random.randint(1, SidesOfDice)
                rollMod = rollRes + Modifier
                logging.info(msg='Res = ' + str(rollMod))

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
                logging.info(msg='Res = ' + str(totalMod))
                return 'Your rolls: ' + rollStr + '\n' + 'Your total is ' + str(totalMod) + '! (' + str(total) + '+' + str(Modifier) + ')'

    except Exception as e:
        #Catch exception
        logging.info(msg='Exception occured, ' + str(e))
        #Tell the user to check their parameters
        return 'Something went wrong, did you type the parameters correctly?'
    
    # Catch all
    return 'Something went wrong'

def help_cmd():
    # TODO: Write a help function
    return ""    

def calc_cmd(expression):
    logging.info(msg="Expression = " + expression)
    res = str(eval(expression))
    logging.info(msg="Result = " + res)
    return expression + " = " + res

def adv_cmd(sides, modifier):
    #Input validation for sides of dice
    if (sides < 2):
        logging.error(msg="Sides less than 2, aborting...")
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

    logging.info(msg='Res = ' + str(rollMod))
    return responseStr

def dis_cmd(sides, modifier):
    #Input validation for sides of dice
    if (sides < 2):
        logging.error(msg="Sides less than 2, aborting...")
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

    logging.info(msg='Res = ' + str(rollMod))

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
        logging.error(msg="Max value less than 1, aborting...")
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
            logging.info(msg=str(roll) + " was generated at try " + str(t))
        checkList[roll - 1] = True

    if(success):
        tf = time.time_ns() - t0
        # Validated
        logging.info(msg="Validated in " + str(tf / 100000000) + "s")
        out += "Validated in " + str(tf / 100000000) + "s and " + str(t-1) + " tries\n"

    else:
        # Failed
        logging.error(msg="Failed to validate")
        out += "Failed to validate"

    return out

# Bot class
class Bot(commands.Bot):
    def __init__(self, prefix, intents):    
        logging.info(msg="Initializing bot...")
        super().__init__(command_prefix=prefix,intents=intents)

    def getTree(self):
        return self.tree
        
    async def setup_hook(self):
        logging.info(msg="Syncing commands...")
        self.tree.copy_global_to(guild=TEST_GUILD_ID)
        await self.tree.sync(guild=TEST_GUILD_ID)

    async def on_ready(self):
        # Log that the bot is ready
        logging.info(msg="Bot ready, logged in as " + self.user.name + "#" + self.user.discriminator)

# Create some variables here that will get populated later
intents = None
client = None

# Re-create the TEST_GUILD_ID variable to be a discord.Guild object
TEST_GUILD_ID = discord.Object(id=TEST_GUILD_ID)

# *****************
# Startup sequence
# *****************

# Log version information
logging.info(msg="Startup")
logging.info(msg="Python version: " + sys.version)
logging.info(msg="Discord.py version: " + discord.__version__)

# Get the bot token from the file
# First, check if the file exists and if it doesn't, create it and show an error message, then exit

if not os.path.isfile('token.txt'):
    logging.warning(msg="Token file not found, creating file...")
    with open('token.txt', 'w') as f:
        f.write("")
    logging.error(msg="Token file created, please add your bot token to the file and restart the bot")
    exit()

# If the file exists, open it and read the token
with open('token.txt', 'r') as f:
    BOT_TOKEN = f.read()
# Ensure that the token is not empty
if BOT_TOKEN == "":
    logging.error(msg="Token file is empty, please add your bot token to the file and restart the bot")
    exit()

# If we get to this point, the token is a thing that exists
logging.info(msg="Token found")

# Set the intents
logging.info(msg="Setting intents...")
intents = discord.Intents.default()
intents.message_content = True

# Create the bot
logging.info(msg="Creating bot...")
client = Bot(prefix="!", intents=intents)
client_tree = client.getTree()

@client_tree.command(name="ping")
async def ping(interaction):
    await interaction.response.defer()
    await interaction.followup.send(content="Pong!")

@client_tree.command(name="rtd")
async def rtd(interaction, sides:typing.Optional[int] = 20, modifier:typing.Optional[int] = 0, number:typing.Optional[int] = 1):
    await interaction.response.defer()
    await interaction.followup.send(content=rtd_cmd(sides, modifier, number))

@client_tree.command(name="adv")
async def adv(interaction, modifier:typing.Optional[int] = 0, sides:typing.Optional[int] = 20):
    await interaction.response.defer()
    await interaction.followup.send(content=adv_cmd(sides, modifier))

@client_tree.command(name="dis")
async def dis(interaction, modifier:typing.Optional[int] = 0, sides:typing.Optional[int] = 20):
    await interaction.response.defer()
    await interaction.followup.send(content=dis_cmd(sides, modifier))

@client_tree.command(name="bin_the_dice")
async def bin(interaction):
    await interaction.response.defer()
    await interaction.followup.send(content=binTheDice_cmd())

@client_tree.command(name="validate")
async def validate(interaction, max_val:typing.Optional[int] = 20, verbose:typing.Optional[bool] = False):
    await interaction.response.defer()
    await interaction.followup.send(content=validate_cmd(max_val, verbose))

@client_tree.command(name="help")
async def help(interaction):
    await interaction.response.defer()
    await interaction.followup.send(content=help_cmd())

@client_tree.command(name="calc")
async def calc(interaction, expression:str):
    await interaction.response.defer()
    await interaction.followup.send(content=calc_cmd(expression))

@client_tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    await interaction.response.defer()
    logging.info('Sync command called')
    if interaction.user.id == 262753744280616960:
        await client_tree.sync()
        logging.info('Command tree synced.')
    else:
        await interaction.followup.send('You must be the owner to use this command!')
    await interaction.followup.send('Synced!')

# Run the bot
logging.info(msg="Running bot...")
client.run(BOT_TOKEN, log_handler=log_handler)
