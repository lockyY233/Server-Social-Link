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
        await VChandler(member, before, after) # handle when user join/leave vc
        debug_print(f"{CONN_LINE_DICT=}")
        debug_print(f"{PLAYER_DICT=}")

    async def on_reaction_add(self, reaction, user):
        if self.user == user:
            return
        # on addreaction
        pass

    async def on_shutdown(self):
        '''
        backup all crucial information before shutdown

        considering signing with hmac in the future
        '''
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
    '''
    force refresh dictionaries across all guilds.

    ---

    basic structure of data:
    bot -> guild -> members -> member

    '''
    for guild in bot.guilds:
            for voiceChannel in guild.voice_channels:
                if voiceChannel.members == []:
                    # pass if voice channel has no members
                    continue
                await refresh_guild_VC(voiceChannel)

async def refresh_guild_VC(voiceChannel):
    '''
    refresh_guild_VC() refresh one voice channel in one guild

    take in one voice channel
    '''
    debug_print("refreshing guilds")
    member_list = voiceChannel.members
    guild_id = voiceChannel.guild.id
    print(f"{member_list=}")

    # this for loop initializing PLAYER_DICT, it CANNOT merge with the for loop below
    for mem in member_list:
        UserID = User.get_UserID(mem.id, guild_id)
        if UserID == None:
            continue
        new_player_dict(mem, UserID)

    # this for loop trigger the join_vc_handler
    for mem in member_list.copy():
        UserID = User.get_UserID(member_list[0].id, guild_id)
        #print(f"{UserID=}")
        if UserID == None:
            member_list.pop(0)
            continue
        else:
            await join_vc_handler(member_list[0], guild_id, UserID, member_list=member_list)
            member_list.pop(0)

async def VChandler(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    '''
    handling all social link with voice chat, called directly by on_voice_state_update()

    mainly control by detecting if user leave or join the vc
    '''
    UserID = None

    if Social_Link_Handler.is_join_vc(before, after):
        # if user join vc, userID follow after voiceState
        UserID = User.get_UserID(member.id, after.channel.guild.id)
    elif not Social_Link_Handler.is_join_vc(before, after):
        # if user leave vc, userID follow before voiceState
        UserID = User.get_UserID(member.id, before.channel.guild.id)
    print(f"VChandler: {UserID=}")

    if UserID == None:
        return # if user is not registered
    
    #member_list = []# member list for if_empty()
    if Social_Link_Handler.is_join_vc(before, after):
        # if join vc
        new_player_dict(member, UserID)
        await join_vc_handler(member, after.channel.guild.id, UserID)

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
            await refresh_guild_VC(member.voice.channel)

async def join_vc_handler(member: discord.Member, guild_id: int, UserID: int, member_list=[]):
    '''create conn_line object between each target in the same voiceChannel

    ---

    this function is called in two different scenerio: when user join vc, and when refreshing
    
    - when user join:
    it will take the user as member, and run a for loop with all other member in the vc
    
    - when refreshing:
    similar to the first scenerio, but will pass in the modified member_list. 
    '''
    new_player = PLAYER_DICT[UserID] # get player from PLAYER_DICT
    if member_list == []:
        member_list = member.voice.channel.members # get all players from the same channel with member
    if len(member_list) <= 1:
        # ignore if there is only one person inside vc
        return

    # for loop include filters if members are not registered
    for target in member_list:
        #print(f"{member=}, {target=}")
        if target != member and User.is_user_guild_exist(target.id, guild_id):
            TargetID = User.get_UserID(target.id, guild_id)
            if TargetID == None:
                #pass if Target did not register
                continue
            conn = Social_Link_Handler.conn_line(new_player, PLAYER_DICT[TargetID], member.voice.channel)
            await conn.sleep_til_nxt_lvl(scheduler)# start leveling timer as soon as conn_line created
            key = (UserID, TargetID)
            write_conn_line_dict(guild_id, key, conn) # record element into a dictionary

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
    '''write new conn_line obj to CONN_LINE_DICT
    '''
    try:
        CONN_LINE_DICT[guild_id][key] = conn
    except Exception as error:
        if isinstance(error, KeyError):
            CONN_LINE_DICT[guild_id] = {key: conn}

def new_player_dict(member, UserID) -> Social_Link_Handler.player:
    '''create a new_player base on UserID and member obj

    **write the new player obj to PLAYER_DICT
    '''
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
