import discord
import User
import discord.ui.button as button

class reset_button(discord.ui.View):
    @button(label='Continue Reset', style=discord.ButtonStyle.danger, emoji="💥")
    async def reset_all(self, button, interaction):
        User.RESET_USER_DB(interaction)
        await interaction.response.edit_message(content=None, view=None, embed = discord.Embed.from_dict({'description': 'Wipe Successfull!', 'image':{'url':'https://c.tenor.com/TG5OF7UkLasAAAAC/thanos-infinity.gif'}}))

    @button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, button, interaction):
        await interaction.response.edit_message(content="Interaction Cancelled", view=None)

class register_button(discord.ui.View):
    @button(label='Continue', style=discord.ButtonStyle.success)
    async def reg_user(self, button, interaction):
        User.new_user(interaction)
        Arcana = User.get_arcana(author_id=interaction.user.id, guild_id=interaction.guild_id)
        print("Arcana: " + str(Arcana))
        IMThou = discord.Embed.from_dict(User.New_registered_user_embed(User.I_M_Thou_embed(Arcana), Arcana))
        await interaction.response.edit_message(content=f'<@!{str(interaction.user.id,)}>',embed=IMThou, view=None)

    @button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, button, interaction):
        await interaction.response.edit_message(content="Interaction Cancelled", view=None)