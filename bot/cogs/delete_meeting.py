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


class DeleteMeeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete_meeting", description="会議を削除します")
    async def delete_meeting(self, interaction: discord.Interaction):
        """
        会議を削除します
        """

        await interaction.response.send_message("削除する会議を選択してください。")

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """
        await self.bot.tree.sync()
        print('loaded : delete_meeting.py')


async def setup(bot: commands.Bot):
    await bot.add_cog(DeleteMeeting(bot))
