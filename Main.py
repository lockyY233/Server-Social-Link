# Hongjie Yang 2022
#  _ __   ___ _ __ ___  ___  _ __   __ _ 
# | '_ \ / _ \ '__/ __|/ _ \| '_ \ / _` |
# | |_) |  __/ |  \__ \ (_) | | | | (_| |
# | .__/ \___|_|  |___/\___/|_| |_|\__,_|
# | |                                    
# |_|  
# API: Pycord 
#
# debug guild id: 805739900850536478
#

import discord
import Embed_Library


from MessageHandler import MessageHandler
import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file

# configure intents
intent = discord.Intents.all()
intent.message_content = True

bot = MessageHandler(debug_guilds=[], intents=intent)
# debug_guilds=[805739900850536478]

# velvet room command / home screen command
@bot.slash_command(name = "velvetroom", description = "Welcome to the Velvet Room!")
async def velvetRoom (ctx):
    menu = discord.Embed.from_dict(Embed_Library.Menu_embed)
    await ctx.respond(embed=menu)

# Social link status command
@bot.slash_command(name = "slink", description = "Check your Social Link progress on different arcana")
async def slink_menu(ctx):
    slink_menu = discord.Embed.from_dict(Embed_Library.Slink_embed)
    await ctx.respond(embed=slink_menu)
bot.run(os.getenv('TOKEN')) # run the bot with the token

# Persona Status Command
@bot.slash_command(name = "persona", description = "Check your current Persona")
async def persona(ctx):
    persona_menu = discord.Embed.from_dict(Embed_Library.Persona_embed)
    await ctx.respond(embed=persona_menu)

# Dungeon Status Command
@bot.slash_command(name = "dungeon", description = "Check your current dungeon progress")
async def persona(ctx):
    dungeon_menu = discord.Embed.from_dict(Embed_Library.Dungeon_embed)
    await ctx.respond(embed=dungeon_menu)