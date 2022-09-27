# handling social link algorithms
import asyncio
import time
import aiojobs

import leveling
import User

class vc_time_calc:
    join_time = 0
    leave_time = 0
    def __init__(self, member):
        self.member = member

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

CONN_LINE_DICT = {
}
# dict containing all conn obj with a tuple key(UserID, UserID)
'''dictionary structure: 
    guild_id : {
        (user1_id, user2_id): <conn_line obj>
    }
'''

class conn_line:
    # create "bond" between each two members in the voice chat
    end_time = 0
    is_destroy = False

    def __init__(self, member1, member2, channel):
        # member1 and 2 are member obj,
        self.member1 = member1
        self.User1_ID = User.get_UserID(member1.id, channel.guild.id)
        self.arcana1 = User.get_arcana(member2.id, channel.guild.id)
        self.member2 = member2
        self.User2_ID = User.get_UserID(member2.id, channel.guild.id)
        self.arcana2 = User.get_arcana(member2.id, channel.guild.id)
        # tuples contains userid, guild_id, and arcana
        t_mem1 = (self.arcana1, self.User1_ID)
        t_mem2 = (self.arcana2, self.User2_ID)

        self.lvl_1 = leveling.get_level(*t_mem1)
        self.xp_1 = leveling.get_xp(*t_mem1)
        self.lvl_2 = leveling.get_level(*t_mem2)
        self.xp_2 = leveling.get_xp(*t_mem2)
        self.channel = channel
        self.start_time = time.time()
        # start_time records when obj created

    def on_destroy(self):
        # only call this when someone dc
        # 
        pass

    async def sleep_til_nxt_lvl(self, scheduler):

        xp1_need = leveling.xp_need(self.lvl_1, self.xp_1)
        time1_need = time_need(xp1_need)

        xp2_need = leveling.xp_need(self.lvl_2, self.xp_2)
        time2_need = time_need(xp2_need)
        print(f"{time1_need=}, {time2_need=}")

        #initialize the leveling loop
        await lvling_loop(self, self.User1_ID, time1_need, scheduler)
        await lvling_loop(self, self.User2_ID, time2_need, scheduler)
    
async def level_coro(self, UserID, time_need):
    await asyncio.sleep(time_need)
    if UserID == self.User1_ID:
        self.lvl_1 += 1
        self.xp_1 = 0
        self.lvl_up(UserID, self.arcana1, self.lvl_1)
        print(f"{UserID} leveld Up to {self.lvl_1}!")
    elif UserID == self.User2_ID:
        self.lvl_2 += 1
        self.xp_2 = 0
        self.lvl_up(UserID, self.arcana2, self.lvl_2)
        print(f"{UserID} leveld Up to {self.lvl_2}!")

# hasnt debug yet
async def lvling_loop(self, UserID, time_need, scheduler):
    # handling the level coroutine
    while True:
        task = await scheduler.spawn(level_coro(self, UserID, time_need))
        await task.wait()
        # break loop
        if self.is_destroy == True:
            await task.close()
            break

# hasnt debug yet
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
    return 0.5*2*xp_need # default 60*2*xp_need, means 2min/xp gain


# create a new conn_line for newly joined user
# conn_line is an object that record the timer between two users for every users inside a vc
