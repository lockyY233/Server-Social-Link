import discord
import json
import random

from data.Persona_Data import ARCANA
import Embed_Library
from data import sql_utils
import SlinkBot

class user:
    # user object created only for register purpose
    def __init__(self, Name, Userid, Guild_id, Arcana):
        self.Name = Name
        self.Userid = Userid
        self.Guild_id = Guild_id
        self.Arcana = Arcana

    Name = ''
    Userid = 0
    Guild_id = 0
    Arcana = 'ARCANA_DEFAULT'
    User_level = 0
    S_Link_Level = {
                    'Fool': 0,
                    'Jester': 0,
                    'Magician': 0,
                    'Councillor': 0,
                    'Priestess': 0,
                    'Empress': 0,
                    'Emperor': 0,
                    'Hierophant': 0,
                    'Lovers': 0,
                    'Chariot': 0,
                    'Justice': 0,
                    'Hermit': 0,
                    'Fortune': 0,
                    'Strength': 0,
                    'Hunger': 0,
                    'Hanged Man': 0,
                    'Death': 0,
                    'Temperance': 0,
                    'Devil': 0,
                    'Tower': 0,
                    'Star': 0,
                    'Moon': 0,
                    'Sun': 0,
                    'Judgement': 0,
                    'Aeon': 0,
                    'World': 0,
                    'Faith': 0
    }  

def random_arca():
    # randomly select an arcana from ARCANA.json and return it as a string
    with open("data/ARCANA.json", 'r') as f:
        arcana_lst = json.load(f)
        arcana = random.choice(list(arcana_lst.values()))
        for x in arcana_lst:
            if arcana_lst[x] == arcana:
                return x

def RESET_USER_DB(ctx):
    '''remove all users with the same guild id'''
    sql_utils.sql_reset(ctx.guild_id)

def RESET_USER_LEVEL(ctx):
    '''remove all users level within the same guild'''
    sql_utils.sql_reset_level(ctx.guild_id)

def is_user_guild_exist(user_id, guild_id):
    # fetch user info in db
    if get_UserID(user_id, guild_id) != None:
        return True
    else:
        return False

def user_register(user):# take in a user object, create a user
    user_info = {'name': user.Name,
            'user_id': user.Userid,
            'guild_id': user.Guild_id,
            'user_level': user.User_level,
            'arcana': user.Arcana
            }
    print(user_info)
    sql_utils.sql_register(user_info) 

async def new_user(interaction: discord.Interaction):
    '''
    directly called after register button pressed, creating a new profile inside the database
    '''
    Arcana = random_arca()
    new_user = user(str(interaction.user), interaction.user.id, interaction.guild_id, Arcana)
    if interaction.user.voice != None:
        # user already in vc
        await SlinkBot.refresh_guild_VC(interaction.user.voice.channel)
    user_register(new_user)

def get_arcana(author_id=0, guild_id=0, UserID = None): 
    # similar to get_UserID. Not recommand to use get_UserID to aquire UserID= if not neccessary
    if author_id != 0 and guild_id != 0:
        condition = f'user_id = {author_id} AND guild_id = {guild_id}'
        arcana = sql_utils.get_data('arcana','User', condition)
        # arcana will be return as list
    elif UserID != None:
        condition = f'UserID = {UserID}'
        arcana = sql_utils.get_data('arcana','User', condition)
    else:
        raise Exception("Wrong argument presented. Must either have both author id and guild id or have UserID present")

    if arcana != []:
        return arcana[0][0]
    else: 
        return None

def get_UserID(user_id, guild_id):
    condition = f'user_id = {user_id} AND guild_id = {guild_id}'
    UserID = sql_utils.get_data("UserID", 'User', condition)
    if UserID != []:
        return UserID[0][0]
    else: 
        return None

def random_I_M_Thou(arcana):
    # return the string of one of the I am Thou message located in Embed library
    #print(Embed_Library.I_M_Thou.values())
    I_M_Thou = random.choice(list(Embed_Library.I_M_Thou.values()))
    I_M_Thou =I_M_Thou.replace("ARCANA_DEFAULT", "**" + arcana + "**", 1)
    return I_M_Thou

def I_M_Thou_embed(arcana):
    # return the dict of the I_M_Thou embed 
    embed_form = Embed_Library.Register_embed
    I_M_Thou = random_I_M_Thou(arcana)
    embed_form['description'] = I_M_Thou
    #print(embed_form)

    with open("data/ARCANA.json", "r") as f:
        f = json.load(f)
        for arca in f:
            if arca == arcana:
                embed_form['thumbnail']['url'] = f[arca]["URL"]
                #print(embed_form)

    return embed_form

def New_registered_user_embed(embed_form, arcana):
    embed_form['fields'][0]['name'] = 'Henceforth, may ARCANA_DEFAULT be with you...'
    embed_form['fields'][0]['name'] = embed_form['fields'][0]['name'].replace("ARCANA_DEFAULT", "**" + arcana + "**", 1)
    embed_form['fields'][0]['value'] = 'You have unlock the ability to obtain a persona!\nPlease visit command **/slink** and **/persona** for more info!'
    return embed_form

