# Managing users or players, handling User.json

import json
from data.Persona_Data import ARCANA
import Embed_Library
import discord
import random

class user:

    def __init__(self, Name, Userid, Guild_id, Arcana):
        self.Name = Name
        self.Userid = Userid
        self.Guild_id = Guild_id
        self.Arcana = Arcana

    Name = ''
    Userid = 0
    Guild_id = 0
    Arcana = 'ARCANA_DEFAULT'
    Persona = 'PERSONA_DEFAULT'
    Persona_level = 1
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

    

def RESET_USER_JSON(ctx):
    with open('data/USER.json', 'r') as f:
        USERS = json.load(f)
        for x in USERS['Users'][:]:
            #print(x)
            if x['Guild_id'] == ctx.guild_id:
                USERS['Users'].remove(x)
        with open('data/USER.json', 'w') as f:
                json.dump(USERS, f, indent=2)

def is_user_exist(userid, USER):
    # username is a id int, USER is the imported list of dictionary
    for x in USER['Users']:
        try: 
            if x['id'] == userid:
                return True
        except:
            continue
    return False

def is_user_guild_exist(ctx):
    with open('data/USER.json', 'r') as f:
        USER = json.load(f)
        for x in USER['Users']:
            #print(str(ctx.guild_id) + ',  ' + str(x['Guild_id']))
            #print(x['id'] == ctx.author.id and x['Guild_id'] == ctx.guild_id)
            
            if (x['id'] == ctx.author.id and x['Guild_id'] == ctx.guild_id):
                return True
        return False


def user_register(user):# take in a user object, create a user
    with open('data/USER.json', 'r') as f:
        USER = json.load(f)

    # User json default format
    user_info = {'Name': user.Name,
                'id': user.Userid,
                'Guild_id': user.Guild_id,
                'Arcana': user.Arcana, 
                'Persona': user.Persona,
                'Persona_level': user.Persona_level,
                'S_Link_Level': user.S_Link_Level
                }

    #if is_user_exist(user.Name, USER) == False:
    with open('data/USER.json', 'w') as f:
        USER['Users'].append(user_info)
        #print(USER)
        json.dump(USER, f, indent = 2)

def new_user(ctx):
    Arcana = random_arca()
    new_user = user(str(ctx.author), ctx.author.id, ctx.guild_id, Arcana)
    if user_register(new_user) == False:
        return False

def get_arcana(ctx):
    # take in user with string
    with open('data/USER.json', 'r') as f:
        f = json.load(f)
        for User in f['Users']:
            #print(User)
            if (User['id'] == ctx.author.id and User['Guild_id'] == ctx.guild_id):
                return User['Arcana']

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

