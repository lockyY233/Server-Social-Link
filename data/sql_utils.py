import sqlite3

def sql_cmd(*args):
    # basic connection command flow
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(*args)
    conn.commit()
    conn.close()

def sql_reset(guild_id):
    sql_cmd("DELETE FROM User WHERE guild_id={0}".format(guild_id))

def sql_register(user_info):
    # take in a user dictionary with basic info, register info into db
    sql_cmd("INSERT INTO User (name, user_id, guild_id, user_level, arcana) VALUES (:name, :user_id, :guild_id, :user_level, :arcana);", user_info)

def get_data(value, condition):
    querry = "SELECT {} from User WHERE {}".format(value, condition)
    conn = sqlite3.connect('data/USER.sqlite')
    curs = conn.cursor()
    curs.execute(querry)
    rtn_data = curs.fetchall()
    conn.commit()
    conn.close()
    return rtn_data

