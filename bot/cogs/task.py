import json
import os
from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord import app_commands


class Task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        # await self.bot.tree.sync()
        await self.check_meeting.start()
        print('loaded : task.py')

    @tasks.loop(seconds=5)
    async def check_meeting(self):
        now = datetime.now()
        # now_str = now.strftime("%Y-%m-%d %H:%M")
        #
        # with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
        #     json_data = json.load(f)
        #
        # if now_str in json_data:
        #     print("会議あるよ")
        # else:
        #     print(await self.get_attendance_rate(now_str))

    async def get_attendance_rate(self, now_str: str):
        guild = discord.utils.get(self.bot.guilds, id=int(os.getenv("MEETING_GUILD_ID")))
        current_club_member_role = discord.utils.get(guild.roles, name="現役部員")
        number_of_current_club_member = 0
        for member in guild.members:
            if current_club_member_role in member.roles:
                number_of_current_club_member += 1

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        return number_of_current_club_member


async def setup(bot: commands.Bot):
    """
    Taskのcogを追加します
    """
    await bot.add_cog(Task(bot))
