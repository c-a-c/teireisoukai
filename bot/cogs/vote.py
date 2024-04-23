#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
投票チャンネルに◯✗の絵文字を付与する処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/23(Created: 2024/04/23)"

import os
from discord.ext import commands


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        # await self.bot.tree.sync()
        print('loaded : vote.py')

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.id == int(os.environ.get('VOTE_CHANNEL_ID')):
            await message.add_reaction("✅")
            await message.add_reaction("❌")


async def setup(bot: commands.Bot):
    """
    Voteのcogを追加します
    """
    await bot.add_cog(Vote(bot))
