#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@task.loop(一定周期処理)に関する処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/24(Created: 2024/04/24)"

import json
import os
from datetime import datetime, timedelta
from typing import List

import discord
from discord.ext import commands, tasks

from bot.ui import view
from bot import json_process


class Task(commands.Cog):
    """
    @task.loop(一定周期処理)に関する処理
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        self.check_meeting.start()
        self.check_resend.start()

        print('loaded : task.py')

    @tasks.loop(seconds=5)
    async def check_meeting(self):
        """
        現在時刻に会議があるか確認します
        """
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M")

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if now_str not in json_data:
            # print("会議ないよ")
            return

        if self.get_attendance_rate(now_str) > 2 / 3:
            print("定例総会を開催できます。")
        else:
            print("開催できません。")
            await self.send_dm_to_members(self.get_absence_member_list(now_str))

    @tasks.loop(seconds=5)
    async def check_resend(self):
        """
        会議の1日前であればメールを再送するようにします
        """
        one_day_later = datetime.now() + timedelta(days=1)
        one_day_later_str = one_day_later.strftime("%Y-%m-%d %H:%M")

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if one_day_later_str not in json_data:
            print("1日後に定例総会ないよ")
            return

        guild = self.bot.get_guild(int(os.getenv("CAC_GUILD_ID")))
        channel = guild.get_channel(int(os.getenv("CAC_CHANNEL_ID")))
        await channel.send(
            json_process.get_resend_mail_text(date_str=one_day_later_str),
            view=view.PowerOfAttorneyView(bot=self.bot, date=one_day_later)
        )

    async def send_dm_to_members(self, members: List[discord.Member]):
        """
        あるユーザー達に定例総会に出席していないとDMを送信します
        """
        with open("./../text/dm.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        for member in members:
            if member.bot:
                continue
            await member.send("".join(lines))

    def get_attendance_rate(self, now_str: str):
        """
        ある会議の出席率を返します
        """
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

        attendance_rate = (
                (number_of_vc_member + number_of_power_of_attorney) / number_of_current_club_member
        )

        return attendance_rate

    def get_absence_member_list(self, now_str: str):
        """
        ある会議の欠席者リストを返します
        """
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
