#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/delete_meetingコマンドの処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/25(Created: 2024/04/25)"

import json
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands
from bot.ui import view


class DeleteMeeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete_meeting", description="会議を削除します")
    async def delete_meeting(self, interaction: discord.Interaction):
        """
        会議を削除します
        """
        if len(get_json_date_list()) == 0:
            await interaction.response.send_message("会議が存在しません。")
        else:
            await interaction.response.send_message(
                view=view.DeleteDateSelectView(bot=self.bot, date_list=get_json_date_list()))

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """
        await self.bot.tree.sync()
        print('loaded : delete_meeting.py')


def get_json_date_list():
    def get_datetime(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')

    def get_date_str(date):
        return datetime.strftime(date, '%Y-%m-%d %H:%M')

    with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    #現在より先の日程を取得する
    date_str_list = list(json_data.keys())
    date_list = list(map(get_datetime, date_str_list))
    date_list = [date for date in date_list if datetime.now() < date]
    date_list.sort()
    date_str_list = list(map(get_date_str, date_list))

    #最大5つまで取得するようにする
    return_date_list = []
    for i in range(5):
        if i >= len(date_str_list):
            break
        return_date_list.append(date_str_list[i])

    return return_date_list


async def setup(bot: commands.Bot):
    await bot.add_cog(DeleteMeeting(bot))
