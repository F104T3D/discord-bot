import discord
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands
from utility.constants import INAPPROPRRIATE_WORDS, FUNNY_WORDS, WELCOME_CHANNEL, LOGGING_CHANNEL


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(LOGGING_CHANNEL)
    if channel:
        await channel.send(f"**[Deleted]** {message.author}: {message.content} in {message.channel}")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(WELCOME_CHANNEL)
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.lower() in FUNNY_WORDS[0]: # !Add more to this 
        await message.channel.send("gurt: yo")

    if message.content.lower() in INAPPROPRRIATE_WORDS:
        await message.delete()
        await message.channel.send(f'{message.author.mention}, your message contained inappropriate content and has been deleted.')
    
    await bot.process_commands(message)

@bot.command()
async def member_join_date(ctx, user: str):
    if ctx.guild:
        for member in ctx.guild.members:
            if member.name == user:
                formatted_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
                await ctx.send(f"{member.name} joined on {formatted_date}")
                return
        await ctx.send("User not found.")

@bot.command()
async def newest_member(ctx):
    if ctx.guild:
        newest = None
        for member in ctx.guild.members:
            if newest is None or (member.joined_at and member.joined_at > newest.joined_at):
                newest = member
        if newest:
            await ctx.send(f"The newest member is {newest.name}, who joined on {newest.joined_at.strftime('%Y-%m-%d %H:%M:%S')}.")
        else:
            await ctx.send("Could not determine the newest member.")
    else:
        await ctx.send("This command can only be used in a server.")

@bot.command() # !Add more to this help command :P
async def help(ctx, arg: str = None):
    if arg is None:
        await ctx.send("Please provide a valid argurment.")
    if arg == "commands":
        if not bot.commands:
            await ctx.send("No commands found.")
        else:        
            for command in bot.commands:
                await ctx.send(command.name)


@bot.command()   
async def clear(ctx, arg: str = None):
    if arg is None:
        await ctx.send('Please provide a valid number of messages to purge. OR use "all" to purge all messages in the channel.')
    if arg == 'all':
        await ctx.send('Purging curent channel messages...')
        await ctx.channel.purge()
    if arg.isdigit():
        await ctx.send(f'Purging {arg} messages...')
        await ctx.channel.purge(limit=int(arg))

@bot.command() # There's probably a better way to do this lol
async def members(ctx):
    memb_count = 0
    if ctx.guild:
        for member in ctx.guild.members:
            memb_count+=1
    await ctx.send(f"There are a total of {memb_count} members in this server!")

@bot.command()
async def member_info(ctx, arg):
    for member in ctx.guild.members:
        if arg == member.name:
            await ctx.send(f"{member.name} User info:\nrole(s) - {member.roles}\nID - {member.id}\navatar - {member.avatar}")

@bot.command()
async def echo(ctx, channel_id: int, *, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


bot.run(token, log_handler=handler, log_level=logging.DEBUG)