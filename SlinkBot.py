import discord
import Embed_Library
import Social_Link_Handler
import time

# main class for bot
class SlinkBot(discord.Bot):

    vc_conn_line = {}

    async def on_ready(self):
        print(f"{self.user} is ready and online!")

    async def on_message(self, message):
        print("Message sent from {0.author}: {0.content}".format(message))

    async def on_voice_state_update(self, member, before, after):

        if Social_Link_Handler.is_join_vc(before, after):

            # create global values for each member who join the vc
            global member_list
            member_list = member.voice.channel.members
            global calc
            calc = Social_Link_Handler.vc_time_calc(member)
            calc.set_join_time()

            print(f"{str(member)} join the vc at {calc.get_join_time()}")
            if len(member_list) > 1:
                for target in member_list:
                    conn = Social_Link_Handler.conn_line(member, target)
        elif Social_Link_Handler.is_join_vc(before, after) == False:
            print(before, after)
            calc.set_leave_time()
            print(f"{str(member)} left the vc at {calc.get_join_time()}")
            print(f"total time in vc: {calc.get_total_vc_time()}s")
