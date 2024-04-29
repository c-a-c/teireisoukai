#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
再起動したときに必要な処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/29(Created: 2024/04/29)"

import json
import os
from datetime import datetime

from discord.ext import commands
from bot.ui import view


class Restart(commands.Cog):
    """
    再起動したときにボタンのインタラクションを再設定します
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # インタラクションボタンが反応するように再度設定
        guild = self.bot.get_guild(int(os.getenv("CAC_GUILD_ID")))
        channel = guild.get_channel(int(os.getenv("CAC_CHANNEL_ID")))
        for date_str, data in json_data.items():
            message_id = data["messageID"]
            message = await channel.fetch_message(message_id)
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            await message.edit(view=view.PowerOfAttorneyView(bot=self.bot, date=date))

        print('loaded : restart.py')


async def setup(bot: commands.Bot):
    """
    Restartのcogを追加します
    """
    await bot.add_cog(Restart(bot))
