from dataclasses import MISSING
from logging import PlaceHolder
from tkinter.tix import Select
import discord
import User
import discord.ui.button as button
import discord.ui.select as select


class reset_button(discord.ui.View):
    '''buttons for /reset command'''
    def __init__(self, option: discord.Option, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option = option

    @button(label='Continue Reset', style=discord.ButtonStyle.danger, emoji="💥")
    async def reset_button(self, button, interaction):
        if self.option == 'all':
            User.RESET_USER_DB(interaction)
        elif self.option == 'user_level':
            User.RESET_USER_LEVEL(interaction)
        await interaction.response.edit_message(content=None, view=None, embed = discord.Embed.from_dict({'description': 'Wipe Successfull!', 'image':{'url':'https://c.tenor.com/TG5OF7UkLasAAAAC/thanos-infinity.gif'}}))

    @button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, button, interaction):
        await interaction.response.edit_message(content="Interaction Cancelled", view=None)

class register_button(discord.ui.View):
    @button(label='Continue', style=discord.ButtonStyle.success)
    async def reg_user(self, button, interaction):
        await User.new_user(interaction)
        Arcana = User.get_arcana(author_id=interaction.user.id, guild_id=interaction.guild_id)
        print("Arcana: " + str(Arcana))
        IMThou = discord.Embed.from_dict(User.New_registered_user_embed(User.I_M_Thou_embed(Arcana), Arcana))
        await interaction.response.edit_message(content=interaction.user.mention, embed=IMThou, view=None)

    @button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, button, interaction):
        await interaction.response.edit_message(content="Interaction Cancelled", view=None)

class slink_menu(discord.ui.View):
    
    # pass in 
    def __init__(self, Slink_level: dict, Slink_menu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Slink_level = Slink_level
        self.Slink_menu = Slink_menu
        self.pagenum = 0

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="Disabled all the components.", view=self)

    @button(emoji="⬅️")
    async def left_page(self, button, interaction):
        member = interaction.user
        self.pagenum -= 1
        if self.pagenum < 0:
            self.pagenum = 4
        slink_menu = slink_page_system(member, self.Slink_level, self.Slink_menu, self.pagenum)
        slink_embed = discord.Embed.from_dict(slink_menu)
        await interaction.response.edit_message(embed=slink_embed)

    @button(emoji='➡️')
    async def right_page(self, button, interaction):
        self.pagenum += 1
        if self.pagenum > 4:
            self.pagenum = 0
        member = interaction.user
        slink_menu = slink_page_system(member, self.Slink_level, self.Slink_menu, self.pagenum)
        slink_embed = discord.Embed.from_dict(slink_menu)
        await interaction.response.edit_message(embed=slink_embed)

def slink_page_system(slink_level: dict, slink_menu: dict, pagenum: int) -> dict:
    element_per_page = 6 # 6 items per page
    lo = element_per_page*pagenum
    hi = min(element_per_page*(pagenum+1), len(slink_level))
    slink_menu['title'] = f'Social Link [{lo+1}-{hi}/{len(slink_level)}]'
    # clear fields in slink_menu
    slink_menu['fields'] = []
    # sort slink_level and turn them into list of tuples
    sorted_tup = sorted(slink_level.items(), key=lambda item: item[1][0], reverse=True)
    # convert page num to elements
    for i in range(lo, hi):
        slink_menu['fields'].append(
            {
                'name': f'{sorted_tup[i][0]}: ', 
                'value': f'lvl **{sorted_tup[i][1][0]}** | next xp: {sorted_tup[i][1][1]}'
            }
        )
    # change title to current page
    return slink_menu

class settings(discord.ui.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @select(
        placeholder='Choose the settings you want to change',
        options=[
            discord.SelectOption(
                label='Bot Channel',
                description='set text channel where bot message send to'
            )
        ]
    )
    async def settings(self, select, interaction):
        print(f'{select.values[0]=}')
        
        if select.values[0] == 'Bot Channel':
            current_guild = interaction.guild
            channel_options = select_channel(current_guild.text_channels)
            if len(channel_options) <= 25: # option limit to 25
                view = bot_channel()
                view.children[0].options=channel_options
                await interaction.response.edit_message(content=f'set the default bot channel:',view=view)
            else:
                pass
            # add option for text channel > 25


class bot_channel(discord.ui.View):
    
    @select(
        placeholder='Choose the default text channel for the bot',
        options=[]
    )
    async def select_channel(self, select, interaction):
        from Main import bot
        bot.default_channel = select.values[0]
        await interaction.response.edit_message(content=f"default channel is now: **{bot.default_channel}**",view=None)

def select_channel(channel_lst: list):
    options = []
    for channel in channel_lst:
        options.append(
            discord.SelectOption(
                label=channel.name
            )
        )
    return options
