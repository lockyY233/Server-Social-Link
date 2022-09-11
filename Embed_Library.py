import discord

from Main import slink_menu
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

Slink_embed = {
    #dict for Slink status embed 
}

Persona_embed = {
    #dict for persona status embed
}

Dungeon_embed = {
    #dict for dungeon status embed
}