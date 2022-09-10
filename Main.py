# Hongjie Yang 2022
# _ __   ___ _ __ ___  ___  _ __   __ _ 
#| '_ \ / _ \ '__/ __|/ _ \| '_ \ / _` |
#| |_) |  __/ |  \__ \ (_) | | | | (_| |
#| .__/ \___|_|  |___/\___/|_| |_|\__,_|
#| |                                    
#|_|  
  
import discord

###################################TOKEN##########################################
TOKEN = "MTAxODA1MTY2MTAyMjkwMDI4Nw.GeKhtQ.5-HYRKyiaz4CtNdYd2QwELHUO1KjnWQRnC5jDg"
##################################################################################

#default intent
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    print('Message sent from {0.author}: {0.content}'.format(message))
    #print(message.content)

    #if message sent by self
    if message.author == client.user:
        return


client.run(TOKEN)