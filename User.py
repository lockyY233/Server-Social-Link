# Managing users or players, handling User.json

import json
import Embed_Library
import discord
import random



def RESET_JSON():
    with open('data/USER.json', 'w') as f:
        default = {
            'Users': [
            ]
        }
        json.dump(default, f) # reset the json library

def is_user_exist(username, USER):
    for x in USER['Users']:
        try: 
            if x['Name'] == username:
                return True
        except:
            continue
    return False

def user_register(username, Arcana, Persona):
    with open('data/USER.json', 'r') as f:
        USER = json.load(f)

    user_info = {'Name': username,
                'Arcana': Arcana, 
                'Persona': Persona
                }

    if is_user_exist(username, USER) == False:
        with open('data/USER.json', 'w') as f:
            USER['Users'].append(user_info)
            print(USER)
            json.dump(USER, f, indent = 2)

def random_arca():
    # randomly select an arcana from ARCANA.json and return it as a string
    with open("data/ARCANA.json", 'r') as f:
        arcana_lst = json.load(f)
        arcana = random.choice(list(arcana_lst.values()))
        for x in arcana_lst:
            if arcana_lst[x] == arcana:
                return x

def random_I_M_Thou(arcana):
    # return the string of one of the I am Thou message located in Embed library
    I_M_Thou = random.choice(list(Embed_Library.I_M_Thou.values()))
    I_M_Thou =I_M_Thou.replace("ARCANA_DEFAULT", "**" + arcana + "**", 1)
    return I_M_Thou

def I_M_Thou_embed():
    # return the dict of the I_M_Thou embed 
    embed_form = Embed_Library.Register_embed
    arcana = random_arca()
    I_M_Thou = random_I_M_Thou(arcana)

    embed_form['description'] = I_M_Thou
    
    with open("data/ARCANA.json", "r") as f:
        f = json.load(f)
        for arca in f:
            if arca == arcana:
                embed_form['thumbnail']['url'] = f[arca]["URL"]
    return embed_form
