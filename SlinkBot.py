import discord
import Social_Link_Handler
import time
import aiojobs

import Embed_Library
import User

vc_time_dict = {}
# record the vc time recorder for every member who join the vc

# main class for bot
class SlinkBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super(SlinkBot, self).__init__(*args, **kwargs)
        self.scheduler = None

    async def on_ready(self):
        self.scheduler = await aiojobs.create_scheduler(limit=None)
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        print("Message sent from {0.author}: {0.content}".format(message))

    async def on_voice_state_update(self, member, before, after):
        await VChandler(member, before, after, self.scheduler)# handle when user join/leave vc
        print(f"{Social_Link_Handler.CONN_LINE_DICT=}")
        print(f"{vc_time_dict=}")

async def if_emtpy(member_list, after, scheduler):
    # handle the case if the CONN_LINE_DICT is empty due to restart
    print("bot probably restarted")
    UserID = 0
    for mem in range(len(member_list)-1):
        UserID = User.get_UserID(member_list[0].id, after.channel.guild.id)
        if UserID == None:
            member_list.pop(0)
            continue
        else:
            await join_vc_handler(member_list, member_list[0], after, UserID, scheduler)
            member_list.pop(0)

async def VChandler(member, before, after, scheduler):
    UserID = None
    if Social_Link_Handler.is_join_vc(before, after):
        UserID = User.get_UserID(member.id, after.channel.guild.id)
    elif not Social_Link_Handler.is_join_vc(before, after):
        UserID = User.get_UserID(member.id, before.channel.guild.id)
    print(UserID)
    if UserID == None:
            return
    member_list = []

    if Social_Link_Handler.is_join_vc(before, after):
        # if join vc
        member_list = member.voice.channel.members
        calc = Social_Link_Handler.vc_time_calc(member)
        calc.set_join_time()
        vc_time_dict[UserID] = calc # record calc with the userid as the key
        print(f"{str(member)} join the vc at {calc.get_join_time()}")
        await join_vc_handler(member_list, member, after, UserID, scheduler)

    elif Social_Link_Handler.is_join_vc(before, after) == False:
        # if leave vc
        member_list = before.channel.members
        try:
            if vc_time_dict[UserID] != None:
                vc_time_dict[UserID].set_leave_time()
                print(f"{str(member)} left the vc at {vc_time_dict[UserID].get_join_time()}")
                print(f"total time in vc: {vc_time_dict[UserID].get_total_vc_time()}s")
                vc_time_dict.pop(UserID)
        except:
            print("calc is not defined probably due to bot restart")
        leave_vc_handler(member_list, before, member, UserID)
    elif before.channel != None and after.channel != None:
        # other action that trigger update
        #print(get_guild_in_Connlinedict(after.channel.guild.id))
        if get_guild_in_Connlinedict(after.channel.guild.id) == None:
            member_list = member.voice.channel.members
            await if_emtpy(member_list, after, scheduler)

async def join_vc_handler(member_list, member, after, UserID, scheduler):
    if len(member_list) <= 1:
        return
    for target in member_list:
        #print(f"{member=}, {target=}")
        if target != member and User.is_user_guild_exist(target.id, after.channel.guild.id):
            TargetID = User.get_UserID(target.id, after.channel.guild.id)
            if TargetID == None:
                continue
            conn = Social_Link_Handler.conn_line(member, target, after.channel)
            await conn.sleep_til_nxt_lvl(scheduler)
            key = (UserID, TargetID)
            write_conn_line_dict(after.channel.guild.id, key, conn) # record element into a dictionary

def leave_vc_handler(member_list, before, member, UserID):
    key_to_del = []
    for target in member_list:
        guild_id = before.channel.guild.id
        TargetID = User.get_UserID(target.id, guild_id)
        if target != member and User.is_user_guild_exist(target.id, guild_id):
            key = (TargetID, UserID)
            key_to_del.append(key)
            key = (UserID, TargetID)
            key_to_del.append(key)
            print(f'{key_to_del=}')
    for key in key_to_del:
        if key in list(Social_Link_Handler.CONN_LINE_DICT[guild_id].keys()):
            conn = Social_Link_Handler.CONN_LINE_DICT[guild_id][key]
            conn.is_destroy = False # break loop for leveling and record lvl and xp
            conn.on_destroy()
            Social_Link_Handler.CONN_LINE_DICT[guild_id].pop(key) # delete element from dict

def write_conn_line_dict(guild_id, key, conn):
    try:
        Social_Link_Handler.CONN_LINE_DICT[guild_id][key] = conn
    except Exception as error:
        if isinstance(error, KeyError):
            Social_Link_Handler.CONN_LINE_DICT[guild_id] = {key: conn}

def get_guild_in_Connlinedict(guild_id):
    try:
        return Social_Link_Handler.CONN_LINE_DICT[guild_id]
    except Exception as error:
        if isinstance(error, KeyError):
            print(f"error finding guild_id, probably due to bot restart")
            return None


# KOWN BUGS FOR CURRENT MODULE:
# - cannot handle if user switch to other vc, conn obj will not be deleted