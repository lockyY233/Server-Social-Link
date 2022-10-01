import PySimpleGUI as sg
import asyncio

import SlinkBot

# initializing bot control window
def init_window():
    layout = [
    [sg.Text("Welcome to SlinkBot control pannel!")],
    [sg.Button("Shut Down")]
    ]
    window = sg.Window(title="SlinkBot", layout= layout)
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
            print(f"{event} - {values}")

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

def debug_print(*args):
    sg.easy_print(*args)

def print_error(error):
    layout = [
    [sg.Text(f"{error}")],
    [sg.Text("Press the close button to continue")]
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