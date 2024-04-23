#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C.A.C.の定例総会を便利にするdiscord bot です。
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


INITIAL_EXTENTIONS = [
    "cogs.register",
    "cogs.task",
    "cogs.vote"
]

Intents = discord.Intents.all()
Intents.message_content = True
Intents.members = True
bot = commands.Bot(command_prefix="!", intents=Intents)


async def main():
    """
    botを起動します。
    """
    load_dotenv()
    async with bot:
        await load_extension()
        await bot.start(os.getenv("TOKEN"))


async def load_extension():
    for cog in INITIAL_EXTENTIONS:
        await bot.load_extension(cog)


@bot.event
async def on_message(message):

    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_ready():

    print("Bot is ready.")


if __name__ == "__main__":
    asyncio.run(main())
