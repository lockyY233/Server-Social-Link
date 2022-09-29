# handling social link algorithms
import asyncio
import time
import aiojobs
import discord

import leveling
import User

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
    # inherit many important stats from member class since we cannot access __dict__ from it
    # player object recording xp and level information
    # take in leveling task obj to manage it
    # will be put in PLAYER_DICT to call it later
    # destroy it when task is destroyed
    # merge with vc_time_calc
    
    join_time = 0
    leave_time = 0
    is_left = False

    def __init__(self, member, UserID):
        self.member = member
        # instead inheit member, take member as part of attribute
        self.UserID = UserID
        self.job = None
        self.arcana = User.get_arcana(UserID=UserID)
        tup_player = (self.arcana, self.UserID)
        self.lvl = leveling.get_level(*tup_player)
        self.xp = leveling.get_xp(*tup_player)

    def __repr__(self) -> str:
        attrs = [
            ("UserID", self.UserID),
            ("arcana", self.arcana),
            ("level", self.lvl),
            ("xp", self.xp)
        ]
        inner = " ".join("%s=%r" % t for t in attrs)
        return f"<{self.__class__.__name__} {inner}>"
        
    def setjob(self, job):
        print("job is set")
        self.job = job
        self.is_left = True

    async def closejob(self):
        # force closing the task/job
        await self.job.close()
    
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
        self.lvl += 1
        self.xp = 0
        print(f"{self} has forged the bond with {TargetArcana} to {self.lvl}")
        #leveling.set_arcana_level(self.UserID, TargetArcana, (self.lvl+1))

class conn_line:
    # create "bond" between each two members in the voice chat
    def __init__(self, player1, player2, channel):
        # member1 and 2 are player obj inehrited member ,
        self.player1 = player1
        self.player2 = player2
        self.start_time = time.time()
        self.channel = channel
        # start_time records when obj created

    def on_destroy(self, UserID):
        PLAYER_DICT[UserID].leave_time = time.time()
        time_gained = PLAYER_DICT[UserID].leave_time - self.start_time
        xp_gained = xp_gained(time_gained)
        # only call this when someone dc
        pass

    async def sleep_til_nxt_lvl(self, scheduler):
        #initialize the leveling loop
        job1 = await scheduler.spawn(lvling_loop(self.player1, self.player2, scheduler))
        job2 = await scheduler.spawn(lvling_loop(self.player2, self.player1, scheduler))
        self.player1.setjob(job1)
        self.player2.setjob(job2)

async def level_coro(player, time_need):
    await asyncio.sleep(time_need)
    print(f"{player} done sleeping for {time_need}s")


async def lvling_loop(player, target, scheduler):
    # handling the level coroutine
    while True:
        xp1_need = leveling.xp_need(player.lvl, player.xp)
        timeneed = time_need(xp1_need)
        print(f"{player}: {timeneed=}")
        task = await scheduler.spawn(level_coro(player, timeneed))
        await task.wait()
        player.level_up(target.arcana)
        # break loop
        if not player.is_left:
            print(f"{player}'s leveling has stopped")
            break

def lvl_up(UserID, lvl, arcana):
    leveling.set_arcana_level(UserID, arcana, lvl)

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
    return xp_need # default 60*2*xp_need
    # current speed 1 second/xp

def xp_gained(time_gained):
    # reverse of the time_need function
    return time_gained # default time_gained/(60*2)


# create a new conn_line for newly joined user
# conn_line is an object that record the timer between two users for every users inside a vc
