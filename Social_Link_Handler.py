# handling social link algorithms
import asyncio
import time
import aiojobs
import discord

import leveling
import User
from gui import debug_print

#-- Dictionary define
CONN_LINE_DICT = {
}
# dict containing all conn obj with a tuple key(UserID, UserID)
'''dictionary structure: 
    guild_id : {
        (user1_id, user2_id): <conn_line obj>
    }
'''
PLAYER_DICT = {
}
'''
this dict contains the task object with a userid as the key
use for easy look up when creating conn_line object
'''
#-----------------------
class player:
    '''
    hold a member class as its attribute since we cannot access __dict__ from it

    player object recording xp and level information

    take in leveling task obj to manage it

    will be put in PLAYER_DICT to call it later

    destroy it when task is destroyed

    merge with vc_time_calc
    '''

    join_time = 0
    leave_time = 0
    is_left = False

    def __init__(self, member, UserID):
        self.member = member
        # instead inheit member, take member as part of attribute
        self.UserID = UserID
        self.job = {}
        self.arcana = User.get_arcana(UserID=UserID)
        self.Slink_lvl ={}
        """
        {
            "arcana name": [13, 0] <-- [0] is level, [1] is xp
        }
        """
        
    def __str__(self) -> str:
        attrs = [
            ("UserID", self.UserID),
            ("arcana", self.arcana)
        ]
        inner = " ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inner}>"

    def __repr__(self) -> str:
        attrs = [
            ("UserID", self.UserID),
            ("arcana", self.arcana),
            ("runningJobs", self.job),
            ("Slink_lvl", self.Slink_lvl)
        ]
        inner = " ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inner}>"
    
    def init_level(self, targetArcana):
        # targetArcana is a string
        # request user arcana's lvl&xp from target player
        tup_player = (targetArcana, self.UserID)
        lvl = leveling.get_level(*tup_player)
        xp = leveling.get_xp(*tup_player)
        self.Slink_lvl[targetArcana] = [lvl, xp]
    
    def del_level(self, targetArcana, xp):
        # called when target destroyed
        self.Slink_lvl[targetArcana][1] += xp
        leveling.set_arcana_level(self.UserID, targetArcana, self.Slink_lvl[targetArcana][0], self.Slink_lvl[targetArcana][1])
        self.Slink_lvl.pop(targetArcana)

    def setjob(self, targetArcana, job):
        self.job[targetArcana] = job
        #print(f"job is set, {job}")
        self.is_left = True

    async def closejob(self, targetArcana):
        # force closing the task/job
        debug_print(f"{self.job[targetArcana]} has closed")
        await self.job[targetArcana].close()
        self.job.pop(targetArcana)
    
    def set_join_time(self):
        self.join_time = round(time.time())

    def get_join_time(self):
        return self.join_time

    def set_leave_time(self):
        self.leave_time = round(time.time())
    
    def get_leave_time(self):
        return self.leave_time

    def get_total_vc_time(self):
        return self.leave_time - self.join_time
    
    def level_up(self, TargetArcana):
        self.Slink_lvl[TargetArcana][0] += 1
        self.Slink_lvl[TargetArcana][1] = 0
        debug_print(f"{self} has forged the bond with {TargetArcana} to {self.Slink_lvl[TargetArcana][0]}")
        #leveling.set_arcana_level(self.UserID, TargetArcana, (self.lvl+1))

class conn_line:
    # create "bond" between each two members in the voice chat
    def __init__(self, player1, player2, channel):
        # member1 and 2 are player obj inehrited member ,
        self.player1 = player1
        self.player2 = player2
        self.start_time = time.time()
        # start_time records when obj created
        self.channel = channel

        self.player1.init_level(player2.arcana)
        self.player2.init_level(player1.arcana)

    def __str__(self) -> str:
        attrs = [
            ("channel", self.channel.name)
        ]
        inner = " ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inner}>"

    def __repr__(self):
        attrs = [
            ("Player1", self.player1),
            ("Player2", self.player2),
            ("channel", self.channel)
        ]
        inner = " ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inner}>"

    async def on_destroy(self, UserID):
        PLAYER_DICT[UserID].leave_time = time.time()
        time_gained = PLAYER_DICT[UserID].leave_time - self.start_time
        xp = xp_gained(time_gained)
        self.player2.del_level(self.player1.arcana, xp)
        self.player1.del_level(self.player2.arcana, xp)
        await self.player1.closejob(self.player2.arcana)
        await self.player2.closejob(self.player1.arcana)
        # only call this when someone dc

    async def sleep_til_nxt_lvl(self, scheduler):
        #initialize the leveling loop
        job1 = await scheduler.spawn(lvling_loop(self.player1, self.player2, scheduler))
        job2 = await scheduler.spawn(lvling_loop(self.player2, self.player1, scheduler))
        self.player1.setjob(self.player2.arcana, job1)
        self.player2.setjob(self.player1.arcana, job2)

async def level_coro(player, time_need):
    await asyncio.sleep(time_need)
    debug_print(f"{player} done sleeping for {time_need}s")


async def lvling_loop(player, target, scheduler):
    # handling the level coroutine
    while True:
        xp1_need = leveling.xp_need(player.Slink_lvl[target.arcana][0], player.Slink_lvl[target.arcana][1])
        timeneed = time_need(xp1_need)
        debug_print(f"{player}: {timeneed=}")
        task = await scheduler.spawn(level_coro(player, timeneed))
        await task.wait()
        player.level_up(target.arcana)
        # break loop
        if not player.is_left:
            debug_print(f"{player}'s leveling has stopped")
            break

# check if user is join/leave vc (but not muted/deafen)
def is_join_vc(before, after):
    # return true if join vc, false if left
    if before.channel == None and after.channel != None:
        return True
    elif before.channel != None and after.channel == None:
        return False

def time_need(xp_need):
    # calculate the time needed for the member to level up
    # return seconds needed to level up
    return 60*2*xp_need # default 60*2*xp_need
    # current speed 2 min/xp

def xp_gained(time_gained):
    # reverse of the time_need function
    return round(time_gained/(60*2)) # default time_gained/(60*2)

# create a new conn_line for newly joined user
# conn_line is an object that record the timer between two users for every users inside a vc
