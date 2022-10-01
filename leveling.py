# calculate and write in the leveling for social link
import math
import User
from data import sql_utils

def xp_need(level, current_xp = 0):
    # return the xp needed to reach the next level
    # the limit will be 300xp per level.
    y = 300/(1+math.exp(-0.7*(7/100*level-6)))
    y = round(y)
    return y - current_xp

def get_level(arcana, UserID):
    level = sql_utils.get_data(arcana, 'Arcana_level', f'UserID = {UserID}')
    return level[0][0]

def get_xp(arcana, UserID):
    # arcana is a string
    xp = sql_utils.get_data(arcana, 'Arcana_xp', f'UserID = {UserID}')
    return xp[0][0]

def set_arcana_level(UserID, arcana, level, xp):
    print(f"{UserID} has wriiten on {arcana} to {level} with {xp=}")
    sql_utils.set_level_xp(UserID, arcana, level, xp)
