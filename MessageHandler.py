import discord


# main class for bot
class MessageHandler(discord.Bot):

    async def on_ready(self):
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        print("Message sent from {0.author}: {0.content}".format(message))
