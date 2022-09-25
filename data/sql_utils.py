import sqlite3

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
    
def set_level_xp(UserID, arcana, lvl):
    lvl_querry = f"""UPDATE Arcana_level
                    SET {arcana}={lvl}
                    WHERE UserID = {UserID}"""
    xp_querry = f"""UPDATE ARcana_xp
                    SET {arcana}=0
                    WHERE UserID{UserID}
                    """
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(lvl_querry)
    curs.execute(xp_querry)
    conn.commit()
    conn.close()

def get_data(value, table,  condition):
    querry = f"SELECT {value} from {table} WHERE {condition}"
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(querry)
    rtn_data = curs.fetchall()
    conn.commit()
    conn.close()
    return rtn_data

