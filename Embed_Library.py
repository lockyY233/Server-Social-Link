import discord
import random

""" Embed Template: 
-------------------------------------
'title': 'Test_title', 
    'type': 'rich', 
    'description': 'test_descrip', 
    'url': None, 
    'timestamp': None,
    'color': 0x9500ff,
    'footer': {
        'text': None,
        'icon_url': None,
        'proxy_icon_url': None
    },
    'image': {
        'url': None,
        'proxy_url': None,
        'height': None,
        'width': None
    },
    'thumbnail': {
        'url': None,
        'proxy_url': None,
        'height': None,
        'width': None
    },
    'video': {
        'url': None,
        'proxy_url': None,
        'height': None,
        'width': None
    },
    'provider': {
        'name': None,
        'url': None
    },
    'author': {
        'name': None,
        'url': None,
        'icon_url': None,
        'proxy_icon_url': None
    },
    'fields': {
        'name': None,
        'value': None,
        'inline': None
    }
-------------------------------------
"""
Menu_embed = {
    'title': 'Welcome to the Velvet Room', 
    'type': 'rich', 
    'description': 'This project is work in progress!', 
    'color': 0x9500ff,
    'thumbnail': {
        'url': "https://res.cloudinary.com/lmn/image/upload/e_sharpen:100/f_auto,fl_lossy,q_auto/v1/gameskinnyc/p/4/v/p4velvetroom-f3dad.png",
        'height': 1023,
        'width': 752
    },
    'fields': [
        {
            'name': 'Social Link',
            'value': 'Increase your social link by spending time with your friends on the discord server!'
        },
        {
            'name': "Persona",
            'value': "Check your persona from xxx command!"
        },
        {
            'name': "Shadows",
            'value': "I'm looking forward seeing you"
        }
    ]
}
I_M_Thou = {
    "Persona 3 Portable": "Thou art I... And I am thou...\nThou hast established a new bond...\nThou shalt be blessed when creating\nPersonas of the ARCANA_DEFAULT Arcana...",
    "Persona 4": "Thou art I... And I am thou...\nThou hast established a new bond...\nIt brings thee closer to the truth...\nThou shalt be blessed when creating\nPersonas of the ARCANA_DEFAULT Arcana...",
    "Persona 4 Golden": "Thou art I... And I am thou...\nThou hast seen how bonds may change...\nThe bond that hath changed... It is thy\nfirst step in learning the truth.\nThou must bear thine inner power of ARCANA_DEFAULT",
    "Persona 5": "I am thou... Thou art I...\nThou hast acquired a new vow...\nIt shall become the wings of rebellion\nThat breaketh thy chains of captivity.\nWith the birth of ARCANA_DEFAULT Persona\nI have obtained the winds of blessing that\nshall lead to freedom and new power...",
    "Persona 5 Royal": "I am thou, thou art I...\nMy vow stands renewed in pursuit of the truth.\nIn breaking free of doubt, the chain that impedes\nthee, is thy strength of heart made manifest.\nWith the rebirth of the ARCANA_DEFAULT,\nThou hast obtained the winds of blessing that\nshall guide thee to the furthest depths."
}

Register_embed = {
    'title': 'I am Thou ...Thou art I...',
    'description': '',
    'color': 0x3532d9,
    'thumbnail': {
        'url':''
    }
}

Slink_embed = {
    #dict for Slink status embed 
}

Persona_embed = {
    #dict for persona status embed
}

Dungeon_embed = {
    #dict for dungeon status embed
}