import discord
import Embed_Library


# main class for bot
class MessageHandler(discord.Bot):

    vc_user = []

    async def on_ready(self):
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        print("Message sent from {0.author}: {0.content}".format(message))

    async def on_voice_state_update(self, member, before, after):
        if before.channel == None and after.channel != None:
            print(str(member) + " join the vc!")
        elif before.channel != None and after.channel == None:
            print(str(member) + " left the vc!")
    
    
