import discord, datetime, time
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime as dt
import random, string
from discord.ui import View, button
import psutil
import socket

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=("Insert your own Preix", intents=intents)

bot.launch_time = datetime.datetime.now(datetime.UTC) # This is for the uptime part of the stats command

# Change strings to match your server's configuration
honeypot = id # This is the Role ID for your Honeypot role
honeypot_channel = id # Honeypot channel ID
test_server = id # my testing server ID
honeypot_test = id # My testing server's honeypot role ID

# Sends a message in the terminal when the bot goes online
@bot.event
async def on_ready():
    on_start_ping = round(bot.latency * 1000) 
    print(f"{bot.user.name} is online!\n My ping is {on_start_ping} ms!")
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Sends a message in the terminal when a user uses a command
@bot.event
async def on_command_completion(ctx):
    latency = round(bot.latency * 1000)
    print(f"{ctx.author.name} // {ctx.author.id} used PREFIX{ctx.command.name} || My ping is currently {latency}ms")

# This bans users if they grab a honeypot role
@bot.event 
async def on_member_update(before, after):
    honey_pot = discord.utils.get(after.guild.roles, id=honeypot)
    age_pot = discord.utils.get(after.guild.roles, id=agepot)
    if honey_pot in after.roles and honey_pot not in before.roles:
        await after.ban(reason = "User grabbed the Honeypot role")
        print(f"{after.name} // {after.id} got banned for grabbing the honeypot role")
    if age_pot in after.roles and age_pot not in before.roles:
        await after.ban(reason="User grabbed the under 13 role")
        print(f"{after.name} // {after.id} got banned for grabbing the under 13 role")
    else:
        return

# honeypot channel
@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    if message.channel.id == honeypot_channel:
        await message.author.ban(reason="User typed in the honeypot channel")
        await message.delete()
        print(f"{message.author.name} // {message.author.id} got banned for typing in the honeypot")
    
    await bot.process_commands(message)

# This shows you your bots uptime and ping, (prefix)ping is a separate command, though
@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user) # this prevents the command from being spammed
async def stats(ctx):
    delta_uptime = datetime.datetime.now(datetime.UTC) - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    latency = round(bot.latency * 1000)
    days, hours = divmod(hours, 24)

    embed = discord.Embed(title=f"{bot.user.name}'s stats", color=discord.Color.pink())
    embed.add_field(name="Ping:", value=f"{latency}ms")
    embed.add_field(name="Uptime:", value=f"{days}d, {hours}h, {minutes}m, {seconds}s")
    
    await ctx.message.reply(embed=embed)


# Command shows you the ping of your bot
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user) # this prevents the command from being spammed
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.message.reply(f"Pong! {latency} ms")

# This shows the server's CPU and RAM usage + other stuff
@app_commands.command(name="server", description="Check the server's CPU & RAM Usage + other stuff")
async def server(interaction: discord.Interaction):

    if interaction.user.id == PUT YOUR OWN ID HERE:
        ram = psutil.virtual_memory()

        delta_uptime = datetime.datetime.now(datetime.UTC) - bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        latency = round(bot.latency * 1000)
        days, hours = divmod(hours, 24)

        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)


        embed = discord.Embed(title="LLH Server Stats", color=discord.Color.pink())
        embed.add_field(name="Host", value=hostname)
        embed.add_field(name="IPv4", value=IPAddr)
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent(interval=1)}%")
        embed.add_field(name="RAM(%)", value=f"{ram.percent}%")
        embed.add_field(name="RAM(GB)", value=f"{round(ram.used / 1e9, 2)}/8 GB")
        embed.add_field(name="Uptime", value=f"{days}d, {hours}h, {minutes}m, {seconds}s")
        embed.add_field(name="Ping", value=f"{latency} ms")
        await interaction.response.send_message(embed = embed, ephemeral=True)
    else:
        await interaction.response.send_message("INPUT YOUR OWN MESSAGE", ephemeral=True)


# If a command is on cooldown, it'll display this message
@bot.event
async def on_command_error(ctx, error):
    latency = round(bot.latency * 1000)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.reply(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds')
        print(f"{ctx.author.name} // {ctx.author.id} is spamming PREFIX{ctx.command.name} || My ping is currently {latency}ms\nhttps://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}")

bot.tree.add_command(server)

# This lets the bot run
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
