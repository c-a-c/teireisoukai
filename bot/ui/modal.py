#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
discord.ui.Modalを継承したクラスをまとめています
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import json
import os
from datetime import datetime
import discord

from bot.register_data_manager import RegisterDataManager
from bot.ui import view
from bot import json_process

class IndividualDateModal(discord.ui.Modal):
    """
    日時の個別設定を選択した際に表示するmodal
    """

    def __init__(self, bot):
        self.bot = bot
        self.date = discord.ui.TextInput(
            label='日時',
            placeholder='入力例: 2024/04/01/13/30',
            min_length=16,
            max_length=16
        )

        super().__init__(
            title="個別の日時設定"
        )

        self.add_item(self.date)

    async def on_submit(self, interaction: discord.Interaction):
        date_format = "%Y/%m/%d/%H/%M"
        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)
        register_data.date = datetime.strptime(self.date.value, date_format)
        embed = discord.Embed(title="登録日時", description=register_data.date)
        await interaction.response.send_message(view=view.ContinueAgendaView(bot=self.bot), embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class RegisterAgenda(discord.ui.Modal):

    def __init__(self, bot):
        self.bot = bot
        self.agenda = discord.ui.TextInput(
            label="議題 (、で区切ってください）",
            placeholder="入力例: 神山祭について、サタジャンについて"
        )

        super().__init__(
            title="議題登録"
        )

        self.add_item(self.agenda)

    async def on_submit(self, interaction: discord.Interaction):
        agenda_text = self.agenda.value.replace("、", "\n・")
        agenda_text = "・" + agenda_text

        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)
        register_data.agenda = agenda_text

        embed = discord.Embed(
            title="メール確認",
            description=register_data.return_mail_text()
        )
        await interaction.response.send_message(view=view.SendMailView(bot=self.bot), embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class RegisterPlace(discord.ui.Modal):

    def __init__(self, bot):
        self.bot = bot
        self.place = discord.ui.TextInput(
            label="場所",
            placeholder="例: 10201教室, Discord"
        )

        super().__init__(
            title="場所の登録"
        )

        self.add_item(self.place)

    async def on_submit(self, interaction: discord.Interaction):
        data_dict = RegisterDataManager.register_data_dict.get(interaction.user.id)
        data_dict.place = self.place.value
        embed = discord.Embed(
            title="メール確認",
            description=data_dict.return_mail_text()
        )
        await interaction.response.send_message(view=view.SendMailView(bot=self.bot), embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class RegisterPowerOfAttorney(discord.ui.Modal):

    def __init__(self, bot, date: datetime):
        self.bot = bot
        self.power_of_attorney = discord.ui.TextInput(
            label="欠席理由",
            placeholder="例: 授業があるため"
        )
        self.date = date

        super().__init__(
            title="委任状登録"
        )

        self.add_item(self.power_of_attorney)

    async def on_submit(self, interaction: discord.Interaction):
        now = datetime.now()
        text = f"議長殿 私は{self.date.year}年{self.date.month}月{self.date.day}日実施の定例総会において、決議権を行使する一切の権限を委任いたします。\n"
        text += f"提出日: {now.year}年{now.month}月{now.day}日\n"
        text += f"discord名: {interaction.user.name}\n"
        text += f"理由: {self.power_of_attorney.value}\n"

        embed = discord.Embed(
            description=text
        )

        json_process.update_power_of_attorney(date=self.date, id=interaction.user.id, reason_text=text)
        await interaction.response.send_message("以下の内容で提出しますか？", embed=embed,
                                                view=view.SubmitPowerOfAttorneyView(bot=self.bot, date=self.date), ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)