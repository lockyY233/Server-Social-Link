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
# other external library: 
# - pycord, 
# - aiojobs, 
# - jupyter-spaces, 
# - dill, 
# - pysimplegui

import discord
from discord.ext.commands import has_permissions, CheckFailure

from SlinkBot import SlinkBot
from SlinkBot import *
from data.sql_utils import get_data, sql_cmd
import gui
import Embed_Library
import User
from data import Persona_Data
import discordUI
from data import sql_utils

import os # default module
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv() # load all the variables from the env file
def set_intent(intent):
    # configure intents
    intent.message_content = True
    intent.voice_states = True
    intent.members = True
    intent.guilds = True

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
        await ctx.respond("**Warning**: Once you register, you will be randomly assign an Arcana.\n**You will not be allowed to change your Arcana!**", view=discordUI.register_button())
    else:
        await ctx.respond("You have already registered! Please visit Velvet Room for more info!")

# ------ Reset Command Group------
@bot.slash_command(name = "reset", description = "Are You Worthy?")
@has_permissions(administrator = True)
async def reset_user(ctx, option: discord.Option(choices=['all', 'user_level'])):
    print(f"reset! {ctx=}, {option=}")
    await ctx.response.send_message(f"**WARNING** The action you are about to conduct is **IRREVERSIBLE**\n Are you sure to continue resetting **{option}**?", view=discordUI.reset_button(option=option))
        
@reset_user.error
async def reset_user_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.respond(embed = discord.Embed.from_dict({'description': 'Your will is not strong enough', 'image':{'url':'https://media4.giphy.com/media/Q9ALJWddHdQketr7D8/giphy.gif'}}))
    else:
        print("Reset Error" + str(error))
# ------ Reset Error ------

# - set bot channel - 
@bot.slash_command(name = 'settings', description='settings for Server S.Link')
async def settings(ctx):
    await ctx.respond('Settings for Server S.Link:', view=discordUI.settings())

# - Social link status command
@bot.slash_command(name = "slink", description = "Check your Social Link progress on different arcana")
async def slink_menu(ctx):
    UserID = User.get_UserID(ctx.author.id, ctx.guild_id)
    S_link_level = sql_utils.get_level_xp(UserID)
    slink_menu = Embed_Library.Slink_embed
    slink_menu['author']['name'] = ctx.author.name
    slink_menu = discordUI.slink_page_system(S_link_level, slink_menu, 0)
    slink_embed = discord.Embed.from_dict(slink_menu)
    await ctx.respond(embed=slink_embed, view=discordUI.slink_menu(Slink_level=S_link_level, Slink_menu=slink_menu))

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
def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(os.getenv('TOKEN')))
    except aiohttp.client_exceptions.ClientConnectorError as ConnectError:
        # implement with gui
        gui.print_error(ConnectError)
        return
if __name__ == '__main__':
    main()
######################################################


