#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
task.loop(一定周期処理)に関する処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/24(Created: 2024/04/24)"

import json
import os
from datetime import datetime
from typing import List

import discord
from discord.ext import commands, tasks


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
        now_str = now.strftime("%Y-%m-%d %H:%M")

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if now_str not in json_data:
            print("会議ないよ")
            return

        if self.get_attendance_rate(now_str) > 2 / 3:
            print("定例総会を開催できます。")
        else:
            print("開催できません。")
            await self.send_dm_to_members(self.get_absence_member_list(now_str))

    async def send_dm_to_members(self, members: List[discord.Member]):
        with open("./../text/dm.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        for member in members:
            if member.bot:
                continue
            await member.send("".join(lines))

    def get_attendance_rate(self, now_str: str):
        guild = discord.utils.get(self.bot.guilds, id=int(os.getenv("MEETING_GUILD_ID")))
        meeting_vc_channel = guild.get_channel(int(os.getenv("MEETING_VC_CHANNEL_ID")))
        current_club_member_role = guild.get_role(int(os.getenv("CURRENT_MEMBER_ROLE_ID")))

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        number_of_current_club_member = len(current_club_member_role.members)
        number_of_vc_member = 0
        number_of_power_of_attorney = len(json_data[now_str]["powerOfAttorney"])

        power_of_attorney_members_list = list(json_data[now_str]["powerOfAttorney"].keys())
        print(power_of_attorney_members_list)

        for member in meeting_vc_channel.members:
            if current_club_member_role not in member.roles:
                continue
            if str(member.id) in power_of_attorney_members_list:
                continue

            number_of_vc_member += 1

        print("number_of_current_club_member", len(current_club_member_role.members))
        print("number_of_vc_member", number_of_vc_member)
        print("number_of_power_of_attorney", number_of_power_of_attorney)

        attendance_rate = (number_of_vc_member + number_of_power_of_attorney) / number_of_current_club_member

        return attendance_rate

    def get_absence_member_list(self, now_str: str):
        guild = discord.utils.get(self.bot.guilds, id=int(os.getenv("MEETING_GUILD_ID")))
        meeting_vc_channel = guild.get_channel(int(os.getenv("MEETING_VC_CHANNEL_ID")))
        current_club_member_role = guild.get_role(int(os.getenv("CURRENT_MEMBER_ROLE_ID")))

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        power_of_attorney_members_list = list(json_data[now_str]["powerOfAttorney"].keys())

        attendance_list = []
        for member in meeting_vc_channel.members:
            attendance_list.append(member)

        for member_id in power_of_attorney_members_list:
            member = guild.get_member(int(member_id))
            attendance_list.append(member)

        absence_list = []
        for member in current_club_member_role.members:
            if member not in attendance_list:
                absence_list.append(member)

        return absence_list


async def setup(bot: commands.Bot):
    """
    Taskのcogを追加します
    """
    await bot.add_cog(Task(bot))
