using System;
using System.Threading.Tasks;
using System.Reflection;
using Discord;
using Discord.WebSocket;
using Discord.Commands;
using Microsoft.Extensions.DependencyInjection;
using Discord.Net.Providers.WS4Net;

namespace DiceRoll
{
    using System;
    using System.Threading.Tasks;
    using System.Reflection;
    using Discord;
    using Discord.WebSocket;
    using Discord.Commands;
    using Microsoft.Extensions.DependencyInjection;

    public class Program
    {
        private CommandService commands;
        private DiscordSocketClient client;
        private IServiceProvider services;

        static void Main(string[] args) => new Program().Start().GetAwaiter().GetResult();
                       
        public async Task Start()
        {
            Console.WriteLine("===  Initializing DiceRoll bot   ===");
            ConsoleLog("Starting process...");
            client = new DiscordSocketClient(new DiscordSocketConfig
            {
                WebSocketProvider = Discord.Net.Providers.WS4Net.WS4NetProvider.Instance,
                LogLevel = LogSeverity.Info
            });
            
            string token = "[Your token here]";

            ConsoleLog("Token established");
            
            commands = new CommandService();
            ConsoleLog("Set commands as new CommandService");

            services = new ServiceCollection()
                    .BuildServiceProvider();

            ConsoleLog("Set services as new ServiceCollection");

            await InstallCommands();
            ConsoleLog("Installed Commands");

            client.Log += Log;
            ConsoleLog("The Logging thing");

            await client.LoginAsync(TokenType.Bot, token);
            await client.StartAsync();

            ConsoleLog("Logged in");

            await Task.Delay(-1);
        }

        private Task Log(LogMessage message)
        {
            var cc = Console.ForegroundColor;
            switch (message.Severity)
            {
                case LogSeverity.Critical:
                case LogSeverity.Error:
                    Console.ForegroundColor = ConsoleColor.Red;
                    break;
                case LogSeverity.Warning:
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    break;
                case LogSeverity.Info:
                    Console.ForegroundColor = ConsoleColor.White;
                    break;
                case LogSeverity.Verbose:
                case LogSeverity.Debug:
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    break;
            }
            ConsoleLog(message.Message);
            Console.ForegroundColor = cc;

            return Task.CompletedTask;
        }

        public async Task InstallCommands()
        {
            // Hook the MessageReceived Event into our Command Handler
            client.MessageReceived += HandleCommand;
            // Discover all of the commands in this assembly and load them.
            await commands.AddModulesAsync(Assembly.GetEntryAssembly());
        }

        public async Task HandleCommand(SocketMessage messageParam)
        {
            // Don't process the command if it was a System Message
            var message = messageParam as SocketUserMessage;
            if (message == null) return;
            // Create a number to track where the prefix ends and the command begins
            int argPos = 0;
            // Determine if the message is a command, based on if it starts with '|' or a mention prefix
            if (!(message.HasCharPrefix('|', ref argPos) || message.HasMentionPrefix(client.CurrentUser, ref argPos))) return;
            // Create a Command Context
            var context = new CommandContext(client, message);
            IServiceProvider service = null;
            // Execute the command. (result does not indicate a return value, 
            // rather an object stating if the command executed successfully)
            var result = await commands.ExecuteAsync(context, argPos, service);
            if (!result.IsSuccess)
                await context.Channel.SendMessageAsync(result.ErrorReason);
        }

        public void ConsoleLog(string message)
        {
            Console.WriteLine(DateTime.Now.TimeOfDay.Hours.ToString("00") + ":" + DateTime.Now.TimeOfDay.Minutes.ToString("00") + ":" + DateTime.Now.TimeOfDay.Seconds.ToString("00") + " " + "{0}", message);
        }
        
    }
    public class Info : ModuleBase
    {
        [Command("Ping"), Summary("Pings the bot to see if it's working")]
        public async Task Ping()
        {
            string name;
            ConsoleLog("Running ping command...");
            await ReplyAsync("Pong!");
        }

        public void ConsoleLog(string message)
        {
            Console.WriteLine(DateTime.Now.TimeOfDay.Hours.ToString("00") + ":" + DateTime.Now.TimeOfDay.Minutes.ToString("00") + ":" + DateTime.Now.TimeOfDay.Seconds.ToString("00") + " " + "{0}", message);
        }

        [Command("rtd"), Summary("Rolls the dice.")]
        public async Task RTD([Summary("")] int numberint, int sidesint,  int modint)
        {
            int total = 0;

            //Get the name of the person who sent the command
            string name = Context.Message.Author.Username;

            if (((Context.Message.Author as SocketGuildUser).Nickname != null))
            {
                name = (Context.Message.Author as SocketGuildUser).Nickname;
            }
            else
            {
                name = Context.User.Username;
            }

            //Rolling the dice
            for (int i = 0; i < numberint; i++)
            {
                int collation = Convert.ToInt32(rtd(sidesint, modint, numberint));
                string resultStr = collation.ToString();

                if (numberint != 1)
                {

                    total += collation;

                }
                string finalStr;
                finalStr = name + " rolled a " + resultStr + "!";

                await ReplyAsync(finalStr);
            }

            if (numberint != 1)
            {
                await ReplyAsync(name + "'s total is: " + total.ToString());
            }

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
