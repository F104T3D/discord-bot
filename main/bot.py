import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from utility.constants import innappropriate_words

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Load the token from .env file

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # Log file
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents) # Prefix for commands (!)


@bot.event  # Welcome message when a user joins the server
async def on_member_join(member):
    channel = member.guild.get_channel(1368097954090450976)
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')

@bot.event # Profanity filter
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() in INNA_WORD_LIST.innappropriate_words:
        await message.delete()
        await message.channel.send(f'{message.author.mention}, your message contained inappropriate content and has been deleted.')
    
    await bot.process_commands(message)

@bot.command()   
async def purge(ctx, arg: str = None): # Command to delete messages in a channel
    if arg is None:
        await ctx.send('Please provide a valid number of messages to purge. OR use "all" to purge all messages in the channel.')
    if arg == 'all':
        await ctx.send('Purging curent channel message...')
        await ctx.channel.purge()
    if arg.isdigit():
        await ctx.send(f'Purging {arg} messages...')
        await ctx.channel.purge(limit=int(arg))
    else:
        await ctx.send('Invalid argument. Please provide a valid number of messages to purge.')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)