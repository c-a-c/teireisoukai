#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/delete_meetingコマンドの処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/25(Created: 2024/04/25)"

import discord
from discord.ext import commands
from discord import app_commands

from bot.ui import view
from bot import json_process



class DeleteMeeting(commands.Cog):
    """
    /delete_meetingコマンドの処理
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete_meeting", description="会議を削除します")
    async def delete_meeting(self, interaction: discord.Interaction):
        """
        会議を削除します
        """
        if len(json_process.get_json_date_list()) == 0:
            await interaction.response.send_message("会議が存在しません。")
        else:
            await interaction.response.send_message(
                view=view.DeleteDateSelectView(
                    bot=self.bot,
                    date_list=json_process.get_json_date_list()
                )
            )

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """
        await self.bot.tree.sync()
        print('loaded : delete_meeting.py')


async def setup(bot: commands.Bot):
    """
    DeleteMeetingのcogを追加します
    """
    await bot.add_cog(DeleteMeeting(bot))
