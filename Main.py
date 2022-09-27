# Hongjie Yang 2022
#  _ __   ___ _ __ ___  ___  _ __   __ _ 
# | '_ \ / _ \ '__/ __|/ _ \| '_ \ / _` |
# | |_) |  __/ |  \__ \ (_) | | | | (_| |
# | .__/ \___|_|  |___/\___/|_| |_|\__,_|
# | |                                    
# |_|  
# Used API: Pycord 
#
# debug guild id: 805739900850536478
# other external library: pycord, aiojobs, jupyter-spaces

import discord
from discord.ext.commands import has_permissions, CheckFailure

from SlinkBot import SlinkBot
import Embed_Library
import User
from data import Persona_Data

import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
def set_intent(intent):
    # configure intents
    intent.message_content = True
    intent.voice_states = True
    intent.members = True

intent = discord.Intents.all()
set_intent(intent)
bot = SlinkBot(debug_guilds=[], intents=intent)
# debug_guilds=[805739900850536478]

#--------------------------------------COMMANDS--------------------------------------#

# velvet room command / home screen command
@bot.slash_command(name = "velvetroom", description = "Welcome to the Velvet Room!")
async def velvetRoom (ctx):
    menu = discord.Embed.from_dict(Embed_Library.Menu_embed)
    await ctx.respond(embed=menu)

# - Register / sign up for the game
@bot.slash_command(name = "register", description = "sign up to join this server game with your friends!")
async def register(ctx):
    if not User.is_user_guild_exist(ctx.author.id, ctx.guild_id):
        await ctx.respond("**Warning: you will be randomly assign an arcana**")
        User.new_user(ctx)
        Arcana = User.get_arcana(author_id = ctx.author.id, guild_id = ctx.guild_id)
        print("Arcana: " + str(Arcana))
        IMThou = discord.Embed.from_dict(User.New_registered_user_embed(User.I_M_Thou_embed(Arcana), Arcana))
        await ctx.channel.send('<@!' + str(ctx.author.id) + '>', embed=IMThou)
    else:
        await ctx.respond("You have already registered! Please visit Velvet Room for more info!")

# ------ Reset Command ------
@bot.slash_command(name = "reset", description = "Are You Worthy?")
@has_permissions(administrator = True)
async def reset_user(ctx):
    User.RESET_USER_DB(ctx)
    await ctx.respond(embed = discord.Embed.from_dict({'description': 'Wipe Successfull!', 'image':{'url':'https://c.tenor.com/TG5OF7UkLasAAAAC/thanos-infinity.gif'}}))
        
@reset_user.error
async def reset_user_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.respond(embed = discord.Embed.from_dict({'description': 'Your will is not strong enough', 'image':{'url':'https://media4.giphy.com/media/Q9ALJWddHdQketr7D8/giphy.gif'}}))
    else:
        print("Reset Error" + str(error))
# ------ Reset Error ------

# - Social link status command
@bot.slash_command(name = "slink", description = "Check your Social Link progress on different arcana")
async def slink_menu(ctx):
    slink_menu = discord.Embed.from_dict(Embed_Library.Slink_embed)
    await ctx.respond(embed=slink_menu)

# - Persona Status Command
@bot.slash_command(name = "persona", description = "Check your current Persona")
async def persona(ctx):
    persona_menu = discord.Embed.from_dict(Embed_Library.Persona_embed)
    await ctx.respond(embed=persona_menu)

# - Dungeon Status Command
@bot.slash_command(name = "dungeon", description = "Check your current dungeon progress")
async def persona(ctx):
    dungeon_menu = discord.Embed.from_dict(Embed_Library.Dungeon_embed)
    await ctx.respond(embed=dungeon_menu)
#------------------------------------------------------------------------------------#

############# run the bot with the token #############
bot.run(os.getenv('TOKEN'))
######################################################


