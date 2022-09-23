# handling social link algorithms
import asyncio
import time
import leveling

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
    """
    key is the member1
    value is a list of conn_line obj, recording: member2, expected time to level up
    """

}

class conn_line:
    # create between each two members in the voice chat
    conn_time = 0
    end_time = 0

    def __init__(self, member2):
        self.member2 = member2
        self.start_time = time.time()

    async def next_leveling(self, xp_had):
        time_need = leveling.xp_need()
        await asyncio.sleep(time_need)
    
# check if user is join/leave vc (but not muted/deafen)
def is_join_vc(before, after):
    # return true if join vc, false if left
    if before.channel == None and after.channel != None:
        return True
    elif before.channel != None and after.channel == None:
        return False

# create a new conn_line for newly joined user
# conn_line is an object that record the timer between two users for every users inside a vc
