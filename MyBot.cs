using Discord;
using Discord.Commands;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DiscordBot
{
    class MyBot
    {
        string botToken = "[Your Token Here]";
        DiscordClient discord;

        public MyBot()
        {
            
            discord = new DiscordClient(x =>
            {
                x.LogLevel = LogSeverity.Info;
                x.LogHandler = Log;
            });

            discord.UsingCommands(x =>
            {
                x.PrefixChar = '|';
                x.AllowMentionPrefix = true;

            });

            var commands = discord.GetService<CommandService>();

            /*
             * This is how to create a command
            commands.CreateCommand("") //Command here (Remember prefix)
                .Do(async (e) =>
                {
                 //Do stuff here

                });
           */

            //Ping command to test bot
            commands.CreateCommand("Ping")//Command here (Remember prefix)
                .Do(async (e) =>
                {
                    //Do stuff here
                    await e.Channel.SendMessage("Pong");
                });

            commands.CreateCommand("Truth") //Command here (Remember prefix)
                .Do(async (e) =>
                {
                    //Do stuff here
                    await e.Channel.SendMessage("Life isn't real");

                });

            commands.CreateCommand("rtd").Parameter("Number", ParameterType.Required).Parameter("Sides", ParameterType.Required).Parameter("Modifier", ParameterType.Optional) //Command here (Remember prefix)
                .Do(async(e) =>
                {
                    //Get the variables
                    var number = e.Args[0];
                    var sides = e.Args[1];
                    var mod = e.Args[2];
                    
                    //Convert them to integers
                    int numberint = Convert.ToInt32(number);
                    int sidesint = Convert.ToInt32(sides);
                    int modint = Convert.ToInt32(mod);
                    int total = 0;
                    
                    
                    //Get the name of the person who sent the command
                    string name;
                    if (e.User.Nickname != null)
                    {
                        name = e.User.Nickname;
                    }
                    else
                    {
                        name = e.User.Name;
                    }

                    //Rolling the dice
                    for (int i = 0; i < numberint; i++)
                      {
                        int collation = Convert.ToInt32(rtd(sidesint, modint, numberint));
                        string resultStr = collation.ToString();

                        if(numberint != 1)
                        {

                            total = total + collation;

                        }    
                            string finalStr;
                            finalStr = name + " rolled a " + resultStr + "!";

                            await e.Channel.SendMessage(finalStr);                         
                    }

                    if (numberint != 1)
                    {
                        await e.Channel.SendMessage(name + "'s total is: " + total.ToString());
                    }

                });

            discord.ExecuteAndWait(async () =>
            {
                //Use the bot token from above. Makes it easier to find
                await discord.Connect(botToken, TokenType.Bot);

            });

        }

        private void Log(Object sender, LogMessageEventArgs e)
        {
            Console.WriteLine(e.Message);
        }

        private static string rtd(int sidesint, int modint, int numberint)
        {
            int rnd = 0;
            System.Threading.Thread.Sleep(1000);
            rnd = new Random().Next(1, sidesint + 1);
            rnd = rnd + modint;
            string resultStr = rnd.ToString();
                        
            return resultStr;

        }
    }
}
