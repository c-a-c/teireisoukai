#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/registerコマンドの処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import discord
from discord.ext import commands
from discord import app_commands

from bot.register_data_manager import RegisterDataManager
from bot.ui import view


class Register(commands.Cog):
    """
    /registerコマンドの処理を記述したクラスです
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="会議を登録します")
    async def register_meeting(self, interaction: discord.Interaction):
        """
        会議を登録します
        """
        RegisterDataManager.add_data(interaction.user.id)
        await interaction.response.send_message(view=view.DateSelectView())

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """
        await self.bot.tree.sync()
        print('loaded : register.py')


async def setup(bot: commands.Bot):
    """
    Registerのcogを追加します
    """
    await bot.add_cog(Register(bot))
