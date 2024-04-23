#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
discord.ui.Modalを継承したクラスをまとめています
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import json
from datetime import datetime
import discord
from overrides import overrides

from bot.register_data_manager import RegisterDataManager
from bot.ui import view


class IndividualDateModal(discord.ui.Modal, title="個別の日時設定"):
    """
    日時の個別設定を選択した際に表示するmodal
    """
    date = discord.ui.TextInput(
        label='日時',
        placeholder='入力例: 2024/04/01/13/30',
        min_length=16,
        max_length=16
    )

    async def on_submit(self, interaction: discord.Interaction):
        date_format = "%Y/%m/%d/%H/%M"
        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)
        register_data.date = datetime.strptime(self.date.value, date_format)
        embed = discord.Embed(title="登録日時", description=register_data.date)
        await interaction.response.send_message(view=view.ContinueAgendaView(), embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class RegisterAgenda(discord.ui.Modal, title="議題の登録"):
    agenda = discord.ui.TextInput(
        label="議題 (、で区切ってください）",
        placeholder="入力例: 神山祭について、サタジャンについて"
    )

    async def on_submit(self, interaction: discord.Interaction):
        agenda_text = self.agenda.value.replace("、", "\n・")
        agenda_text = "・" + agenda_text

        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)
        register_data.agenda = agenda_text

        embed = discord.Embed(
            title="メール確認",
            description=return_mail_text(interaction.user.id)
        )
        await interaction.response.send_message(view=view.SendMailView(), embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class RegisterPlace(discord.ui.Modal, title="場所の登録"):
    place = discord.ui.TextInput(
        label="場所",
        placeholder="例: 10201教室, Discord"
    )

    async def on_submit(self, interaction: discord.Interaction):
        data_dict = RegisterDataManager.register_data_dict.get(interaction.user.id)
        data_dict.place = self.place.value
        embed = discord.Embed(
            title="メール確認",
            description=return_mail_text(interaction.user.id)
        )
        await interaction.response.send_message(view=view.SendMailView(), embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class RegisterPowerOfAttorney(discord.ui.Modal, title="委任状登録"):
    power_of_attorney = discord.ui.TextInput(
        label="欠席理由",
        placeholder="例: 授業があるため"
    )

    def __init__(self, date: datetime):
        self.date = date

        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        update_power_of_attorney(self.date, interaction.user.id, self.power_of_attorney.value)
        await interaction.response.send_message(self.date)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


def return_mail_text(id: int):
    register_data = RegisterDataManager.register_data_dict.get(id)
    date = register_data.date
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    with open('./../text/discordMail.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    mail_text = ""
    for line in lines:
        line = line.replace("year", str(date.year))
        line = line.replace("month", str(date.month))
        line = line.replace("weekday", weekdays[date.weekday()])
        line = line.replace("day", str(date.day))
        line = line.replace("hour", str(date.hour))
        line = line.replace("minute", str(date.minute))
        line = line.replace("agenda", register_data.agenda)
        line = line.replace("place", register_data.place)

        mail_text += line + "\n"

    return mail_text


def update_power_of_attorney(date: datetime, id: int, reason_text: str):
    with open('./../json/meetingData.json', 'r', encoding='utf-8') as f:
        existing_json = json.load(f)

    date_str = date.strftime("%Y-%m-%d %H:%M")
    if existing_json[date_str]["powerOfAttorney"]:
        existing_json[date_str]["powerOfAttorney"][str(id)] = reason_text
    else:
        existing_json[date_str]["powerOfAttorney"] = {str(id): reason_text}

    with open('./../json/meetingData.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(existing_json, indent=4, ensure_ascii=False))
