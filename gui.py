import PySimpleGUI as sg
import asyncio
import json
import copy

import SlinkBot

# initializing bot control window

def init_window():
    layout = [
    [sg.Text("Welcome to SlinkBot control pannel!", background_color= '#000000')],
    [sg.Text(size=(50, 20), key='-DEBUG OUTPUT-')],
    [sg.Text("Dictionary to print: ", background_color= '#000000'),
    sg.Button("PLAYER_DICT", tooltip="display current PLAYER_DICT"), 
    sg.Button("CONN_LINE_DICT", tooltip="display current CONN_LINE_DICT")],
    [sg.Button("Refresh Dictionaries", target=(2,1), tooltip="refreshing PLAYER_DICT and CONN_LINE_DICT")],
    [sg.Button("Shut Down", button_color='#ff7369')]
    ]
    sg.theme('Black')
    window = sg.Window(title="SlinkBot", layout=layout)
    return window

async def window_loop(bot, window, event):
    # pass in event(can be none), will change the event into pysimplegui event
    fps = 10 # window currently running in 10fps to give more rescourse to the bot
    while True:
        await asyncio.sleep(1/fps)
        event, values = window.read(timeout=1)
        if is_shutdown(event, "Shut Down"):
            print("Bot has successfully shutdown!")
            await on_shutdown(bot)
            window.close()
            break
        if event != '__TIMEOUT__':
            pass
            #print(f"{event} - {values}")
        await event_handler(event, window)



# print debug message to a seperate window
def debug_print(*args):
    sg.easy_print(*args)

async def event_handler(event, window):
    if event == "PLAYER_DICT":
        from Social_Link_Handler import PLAYER_DICT
        window['-DEBUG OUTPUT-'].update(pretty_PLAYER_DICT(PLAYER_DICT))
    elif event == "CONN_LINE_DICT":
        from Social_Link_Handler import CONN_LINE_DICT
        window['-DEBUG OUTPUT-'].update(pretty_CONN_DICT(CONN_LINE_DICT))
    elif event == "Refresh Dictionaries":
        import SlinkBot
        from Main import bot
        await SlinkBot.refresh_dict(bot)
def pretty_PLAYER_DICT(dict):
    c_dict = {}
    for player in dict:
        c_dict[player] = str(dict[player])
    return json.dumps(c_dict, indent=2)

def pretty_CONN_DICT(dict):
    c_dict = {}
    for guild in dict:
        c_dict[guild] = {}
        for conn in dict[guild].copy():
            c_dict[guild][str(conn)] = str(dict[guild][conn])
    return json.dumps(c_dict, indent=2)

def is_shutdown(event, closeMessage):
    if event in (f"{closeMessage}", sg.WIN_CLOSED):
        return True
    else:
        return False

async def on_shutdown(bot):
        await bot.on_shutdown()
        await bot.close()
        loop = asyncio.get_running_loop()
        loop.stop()
        loop.close()
        try:
            await SlinkBot.scheduler.close()
        except Exception as error:
            print(f"{error}")

def print_error(error):
    layout = [
    [sg.Text(f"{error}")],
    [sg.Text("Press the close button to continue")],
    [sg.Button("Close")]
    ]
    window = sg.Window(title="Error!", layout= layout)
    while True:
        event, values = window.read(timeout=1)
        if is_shutdown(event, "Close"):
            window.close()
            break
        if event != '__TIMEOUT__':
            print(f"{event} - {values}")