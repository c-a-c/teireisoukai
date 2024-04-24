# !/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
discord.ui.Viewを継承したクラスをまとめています
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import json
import os
from datetime import datetime

import discord

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
        channel_id = int(os.getenv("CAC_CHANNEL_ID"))
        target_channel = interaction.guild.get_channel(channel_id)
        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)
        register_data.save_to_json()
        await target_channel.send(
            modal.return_mail_text(interaction.user.id),
            view=PowerOfAttorneyView(register_data.date)
        )
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


class PowerOfAttorneyView(discord.ui.View):

    def __init__(self, date: datetime):
        self.date = date

        super().__init__(
            timeout=None
        )

    @discord.ui.button(label="委任状を提出", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(modal.RegisterPowerOfAttorney(self.date))

    @discord.ui.button(label="委任状を取り消す", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        text = get_power_of_attorney_text(self.date, interaction.user.id)
        embed = discord.Embed(
            description=text
        )

        if text is None:
            await interaction.response.send_message("あなたの委任状は存在しません。", ephemeral=True)
        else:
            await interaction.response.send_message(
                "以下の委任状を取り消しますか？",
                embed=embed,
                view=DeletePowerOfAttorneyView(self.date),
                ephemeral=True
            )


class SubmitPowerOfAttorneyView(discord.ui.View):

    def __init__(self, date: datetime):
        self.date = date

        super().__init__()

    @discord.ui.button(label="提出", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("委任状が受理されました。提出ありがとうございます。", ephemeral=True)
        await disable_button_by_followup(self, interaction)


class DeletePowerOfAttorneyView(discord.ui.View):

    def __init__(self, date: datetime):
        self.date = date

        super().__init__()

    @discord.ui.button(label="取り消す", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if delete_power_of_attorney(self.date, interaction.user.id):
            await interaction.response.send_message("委任状が取り消されました。", ephemeral=True)
            await disable_button_by_followup(self, interaction)
        else:
            await interaction.response.send_message("削除時にエラーが発生しました。")


async def disable_button_by_followup(view: discord.ui.View, interaction: discord.Interaction):
    for item in view.children:
        item.disabled = True
    await interaction.followup.edit_message(interaction.message.id, view=view)


def get_power_of_attorney_text(date: datetime, id: int):
    date_str = date.strftime("%Y-%m-%d %H:%M")
    with open("./../json/meetingData.json") as f:
        json_data = json.load(f)
    power_of_attorney = json_data[date_str]["powerOfAttorney"]
    for element in power_of_attorney:
        if int(element) == id:
            return power_of_attorney[element]

    return None


def delete_power_of_attorney(date: datetime, id: int):
    date_str = date.strftime("%Y-%m-%d %H:%M")

    with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    try:
        power_of_attorney = json_data[date_str]["powerOfAttorney"]
        power_of_attorney.pop(str(id))
        json_data[date_str]["powerOfAttorney"] = power_of_attorney
    except KeyError:
        return False

    with open("./../json/meetingData.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return True

