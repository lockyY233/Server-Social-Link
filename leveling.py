# calculate and write in the leveling for social link
import math

def xp_need(level, current_xp = 0):
    # take in level and subtract with the current xp
    y = 1000/(1+math.exp(-(13/50*level-5)))
    return round(y) - current_xp
