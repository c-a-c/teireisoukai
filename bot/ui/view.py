# !/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
discord.ui.Viewを継承したクラスをまとめています
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import discord
from discord.ui import Item

from bot.register_data_manager import RegisterDataManager
from bot.ui import select
from bot.ui import modal


class DateSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(select.DateSelect())


class ContinueAgendaView(discord.ui.View):

    @discord.ui.button(label="議題登録へ移る", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(modal.RegisterAgenda())
        await disable_button_by_followup(self, interaction)

    @discord.ui.button(label="戻る", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message(view=DateSelectView())
        await disable_button_by_followup(self, interaction)





class SendMailView(discord.ui.View):

    @discord.ui.button(label="この内容で送信する", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("送信しました")
        await disable_button_by_followup(self, interaction)

    @discord.ui.button(label="場所を変更する", style=discord.ButtonStyle.gray)
    async def gray(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(modal.RegisterPlace())
        await disable_button_by_followup(self, interaction)

    @discord.ui.button(label="戻る", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        data_dict = RegisterDataManager.register_data_dict.get(interaction.user.id)
        embed = discord.Embed(title="登録日時", description=data_dict.date)
        await interaction.response.send_message(view=ContinueAgendaView(), embed=embed)
        await disable_button_by_followup(self, interaction)


async def disable_button_by_followup(view: discord.ui.View, interaction: discord.Interaction):
    for item in view.children:
        item.disabled = True
    await interaction.followup.edit_message(interaction.message.id, view=view)
