import sqlite3
import leveling

'''
Note:
problem with built-in sqlite is that it is not asynchronous

one solution can be utilizing aiosqlite library

since you can connect to the database the entirty of the time when bot running
'''

def sql_cmd(*args, use_fk = False):
    # basic connection command flow
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    if use_fk:
        conn.execute("PRAGMA foreign_keys = ON")
    curs.execute(*args)
    conn.commit()
    conn.close()

def sql_reset(guild_id):
    sql_cmd(f"DELETE FROM User WHERE guild_id={guild_id}", use_fk=True)

def sql_reset_level(guild_id):
    '''resetting all levels from user, return the ID_to_del for more purpose'''
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON")
    #fetch userid for people within the same guild
    curs.execute(f"SELECT UserID FROM User WHERE guild_id={guild_id}")
    ID_to_del = curs.fetchall()
    # i.e ID_to_del=[(11,), (12,)]
    for ID in ID_to_del:
        # delete rows and re-add them 
        curs.execute(f"DELETE FROM Arcana_level WHERE UserID={ID[0]}")
        curs.execute(f"DELETE FROM Arcana_xp WHERE UserID={ID[0]}")
        curs.execute(f"INSERT INTO ARcana_level (UserID) VALUES ({ID[0]})")
        curs.execute(f"INSERT INTO ARcana_xp (UserID) VALUES ({ID[0]})")
    conn.commit()
    conn.close()
    return ID_to_del

def sql_register(user_info):
    # take in a user dictionary with basic info, register info into dbconn = sqlite3.connect('data/USER.sqlite')
    Insert_User = """INSERT INTO User (name, user_id, guild_id, user_level, arcana)
                 VALUES (:name, :user_id, :guild_id, :user_level, :arcana);"""
    Insert_Arca_lvl = "INSERT INTO Arcana_level DEFAULT VALUES"
    Insert_Arca_xp = "INSERT INTO Arcana_xp DEFAULT VALUES"
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(Insert_User, user_info)
    curs.execute(Insert_Arca_lvl)
    curs.execute(Insert_Arca_xp)
    conn.commit()
    conn.close()

def get_level_xp(UserID):
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()

    curs.execute(
        f"SELECT * FROM Arcana_level WHERE UserID={UserID}"
    )
    UserLvl = curs.fetchall()
    UserLvl[0] = UserLvl[0][1:] # remove UserID column
    UserLvl = UserLvl[0] # break out the tuple from the list

    curs.execute(
        f"SELECT * FROM Arcana_xp WHERE UserID={UserID}"
    )
    UserXp = curs.fetchall()
    UserXp[0] = UserXp[0][1:]
    UserXp = UserXp[0] 

    # fill info into this dictionary and return it 
    S_Link_Level = {
                    'Fool': [],# [lvl, xp needed]
                    'Jester': [],
                    'Magician': [],
                    'Councillor': [],
                    'Priestess': [],
                    'Empress': [],
                    'Emperor': [],
                    'Hierophant': [],
                    'Lovers': [],
                    'Chariot': [],
                    'Justice': [],
                    'Hermit': [],
                    'Fortune': [],
                    'Strength': [],
                    'Hunger': [],
                    'Hanged Man': [],
                    'Death': [],
                    'Temperance': [],
                    'Devil': [],
                    'Tower': [],
                    'Star': [],
                    'Moon': [],
                    'Sun': [],
                    'Judgement': [],
                    'Aeon': [],
                    'World': [],
                    'Faith': []
    }
    keys_lst = list(S_Link_Level)
    for i in range(len(keys_lst)):
        lvl = UserLvl[i]
        xp = UserXp[i]
        xp_need = leveling.xp_need(lvl, xp)
        S_Link_Level[keys_lst[i]] = [lvl, xp_need]
    conn.commit()
    conn.close()
    return S_Link_Level

def set_level_xp(UserID, arcana, lvl, xp):
    lvl_querry = f"UPDATE Arcana_level SET {arcana}={lvl} WHERE UserID = {UserID}"
    xp_querry = f"UPDATE ARcana_xp SET {arcana}={xp} WHERE UserID = {UserID} "
    print(f"{lvl_querry=}, {xp_querry=}")
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(lvl_querry)
    curs.execute(xp_querry)
    conn.commit()
    conn.close()

def get_data(value, table,  condition) -> list:
    '''will return a list of tuples like this: [(9,),(8,)]'''
    querry = f"SELECT {value} from {table} WHERE {condition}"
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(querry)
    rtn_data = curs.fetchall()
    conn.commit()
    conn.close()
    return rtn_data

