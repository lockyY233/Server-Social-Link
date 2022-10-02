import discord
import Social_Link_Handler
from Social_Link_Handler import CONN_LINE_DICT, PLAYER_DICT
import json
import aiojobs
import dill as pickle

import Embed_Library
import User
import gui
from gui import debug_print
import threading

scheduler = None
window_lib = {}
# record the vc time recorder for every member who join the vc

# main class for bot
class SlinkBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super(SlinkBot, self).__init__(*args, **kwargs)
        self.event = None # event for the control pannel window

    async def on_ready(self):
        # set global scheduler for all jobs
        global scheduler
        scheduler = await aiojobs.create_scheduler(limit=None)
        # init windows for control pannel
        window = gui.init_window()
        global window_job
        window_job = await scheduler.spawn(gui.window_loop(self, window, self.event))
        #window_lib["ControlPannel"] = window_job
        await refresh_dict(self)
        debug_print(f"{self.user} is ready and online!")
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        print("Message sent from {0.author}: {0.content}".format(message))

    async def on_voice_state_update(self, member, before, after):
        await VChandler(member, before, after, scheduler)# handle when user join/leave vc
        debug_print(f"{CONN_LINE_DICT=}")
        debug_print(f"{PLAYER_DICT=}")

    async def on_reaction_add(self, reaction, user):
        if self.user == user:
            return
        # on addreaction
        pass

    async def on_shutdown(self):
        # backup all crucial information before shutdown
        # write using pickle
        # considering signing with hmac in the future
        # -------------------------------------
        # closing all task before shutdown
        for guild in CONN_LINE_DICT.copy():
            # for every conn_line obj in the dictionary
            # close conn_line using on_destroy,
            for conn in CONN_LINE_DICT[guild].copy():
                await CONN_LINE_DICT[guild][conn].on_destroy(conn[0])
                CONN_LINE_DICT[guild][conn] = None 
        for player in PLAYER_DICT:
            # unbind the member subclass, can rebind it using its id lookup
            PLAYER_DICT[player].member = None
        print(f"closing: {CONN_LINE_DICT=}")
        print(f"closing: {PLAYER_DICT=}")
        # dumping all dictionary into a pickle file before shutdown
        with open("data/SAVE", "wb") as f: 
            dict = {"CONN_LINE_DICT": CONN_LINE_DICT, "PLAYER_DICT": PLAYER_DICT}
            pickle.dump(dict, f)

async def refresh_dict(bot):
    for guild in bot.guilds:
            for voiceChannel in guild.voice_channels:
                if voiceChannel.members == []:
                    # pass if voice channel has no members
                    continue
                member_list = voiceChannel.members
                await if_emtpy(member_list, voiceChannel)

async def if_emtpy(member_list, after):
    guild = after.guild
    # handle the case if the CONN_LINE_DICT is empty due to restart
    if after.__class__.__name__ == 'VoiceState':
        guild = after.channel.guild.id
    print(f"{member_list=}")
    for mem in member_list:
        UserID = User.get_UserID(mem.id, guild.id)
        if UserID == None:
            continue
        new_player_dict(mem, UserID)
    for mem in range(len(member_list)-1):
        UserID = User.get_UserID(member_list[0].id, guild.id)
        #print(f"{UserID=}")
        if UserID == None:
            member_list.pop(0)
            continue
        else:
            #global scheduler
            new_player = PLAYER_DICT[UserID]
            await join_vc_handler(member_list, member_list[0], after, UserID, scheduler, new_player)
            member_list.pop(0)

async def VChandler(member, before, after, scheduler):
    UserID = None

    if Social_Link_Handler.is_join_vc(before, after):
        UserID = User.get_UserID(member.id, after.channel.guild.id)
    elif not Social_Link_Handler.is_join_vc(before, after):
        UserID = User.get_UserID(member.id, before.channel.guild.id)
    print(f"VChandler: {UserID=}")

    if UserID == None:
        return # if user is not registered
    
    member_list = []# member list for if_empty()
    if Social_Link_Handler.is_join_vc(before, after):
        # if join vc
        new_player = new_player_dict(member, UserID)
        await join_vc_handler(member_list, member, after, UserID, scheduler, new_player)

    elif Social_Link_Handler.is_join_vc(before, after) == False:
        # if leave vc
        member_list = before.channel.members
        await leave_vc_handler(member_list, before, member, UserID)
        try:
            if PLAYER_DICT[UserID] != None:
                PLAYER_DICT[UserID].set_leave_time()
                print(f"{str(member)} left the vc at {PLAYER_DICT[UserID].get_join_time()}")
                print(f"total time in vc: {PLAYER_DICT[UserID].get_total_vc_time()}s")
                PLAYER_DICT.pop(UserID)
        except:
            # if restart, PLAYER_DICT will be empty
            print("player is not defined probably due to bot restart")
    elif before.channel != None and after.channel != None:
        # other action that trigger update
        if get_guild_in_Connlinedict(after.channel.guild.id) == None:
            #print(f"{member.voice.channel.members=}")
            member_list = member.voice.channel.members
            await if_emtpy(member_list, after)

async def join_vc_handler(member_list, member, after, UserID, scheduler, new_player):
    # transfer information to player object
    guild = after.guild
    channel = after
    if after.__class__.__name__ == 'VoiceState':
        guild = after.channel.guild.id
        channel = after.channel

    if len(member_list) <= 1:
        # ignore if there is only one person inside vc
        return
    
    for target in member_list:
        #print(f"{member=}, {target=}")
        if target != member and User.is_user_guild_exist(target.id, guild.id):
            TargetID = User.get_UserID(target.id, guild.id)
            if TargetID == None:
                continue
            conn = Social_Link_Handler.conn_line(new_player, PLAYER_DICT[TargetID], channel)
            await conn.sleep_til_nxt_lvl(scheduler)
            key = (UserID, TargetID)
            write_conn_line_dict(guild.id, key, conn) # record element into a dictionary

async def leave_vc_handler(member_list, before, member, UserID):
    # Delete conn_line obj from CONN_LINE_DICT by predicting key 
    key_to_del = []
    for target in member_list:
        guild_id = before.channel.guild.id
        TargetID = User.get_UserID(target.id, guild_id)
        if target != member and User.is_user_guild_exist(target.id, guild_id):
            key = (TargetID, UserID)
            key_to_del.append(key)
            key = (UserID, TargetID)
            key_to_del.append(key)
            # predict the key in order to look up in the dictionary
        print(f"{key_to_del=}")
    for key in key_to_del:
        if key in list(CONN_LINE_DICT[guild_id].keys()):
            print(f"{key} is getting destroyed")
            conn = CONN_LINE_DICT[guild_id][key]
            await conn.on_destroy(UserID)
            CONN_LINE_DICT[guild_id].pop(key) # delete element from dict

def write_conn_line_dict(guild_id, key, conn):
    try:
        CONN_LINE_DICT[guild_id][key] = conn
    except Exception as error:
        if isinstance(error, KeyError):
            CONN_LINE_DICT[guild_id] = {key: conn}

def new_player_dict(member, UserID) -> Social_Link_Handler.player:
    # create a new_player base on UserID and member obj
    new_player = Social_Link_Handler.player(member, UserID)
    new_player.set_join_time()
    PLAYER_DICT[UserID] = new_player
    print(f"{str(member)} join the vc at {new_player.get_join_time()}")
    return new_player

def get_guild_in_Connlinedict(guild_id):
    try:
        return CONN_LINE_DICT[guild_id]
    except Exception as error:
        if isinstance(error, KeyError):
            print(f"error finding guild_id, probably due to bot restart")
            return None


# KOWN BUGS FOR CURRENT MODULE:
# - cannot handle if user switch to other vc, conn obj will not be deleted
