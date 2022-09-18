import discord
import Embed_Library


# main class for bot
class MessageHandler(discord.Bot):

    async def on_ready(self):
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        print("Message sent from {0.author.id}: {0.content}".format(message))
    
    
    
