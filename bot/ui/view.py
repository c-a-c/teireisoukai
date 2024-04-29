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
from bot import json_process


class DateSelectView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.add_item(select.DateSelect(bot=self.bot))


class DeleteDateSelectView(discord.ui.View):
    def __init__(self, bot, date_list):
        self.bot = bot

        super().__init__()

        self.add_item(select.DeleteDateSelect(bot=self.bot, date_list=date_list))


class ContinueAgendaView(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot

        super().__init__()

    @discord.ui.button(label="議題登録へ移る", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(modal.RegisterAgenda(bot=self.bot))
        await _disable_button_by_followup(self, interaction)

    @discord.ui.button(label="戻る", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message(view=DateSelectView(bot=self.bot))
        await _disable_button_by_followup(self, interaction)


class SendMailView(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot

        super().__init__()

    @discord.ui.button(label="この内容で送信する", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)

        guild = self.bot.get_guild(int(os.getenv("CAC_GUILD_ID")))
        channel = guild.get_channel(int(os.getenv("CAC_CHANNEL_ID")))
        message = await channel.send(
            register_data.return_mail_text(),
            view=PowerOfAttorneyView(bot=self.bot, date=register_data.date)
        )
        await interaction.response.send_message("送信しました。")
        await _disable_button_by_followup(self, interaction)

        register_data.message_id = message.id
        register_data.save_to_json(register_data=register_data)

    @discord.ui.button(label="場所を変更する", style=discord.ButtonStyle.gray)
    async def gray(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(modal.RegisterPlace(bot=self.bot))
        await _disable_button_by_followup(self, interaction)

    @discord.ui.button(label="戻る", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        data_dict = RegisterDataManager.register_data_dict.get(interaction.user.id)
        embed = discord.Embed(title="登録日時", description=data_dict.date)
        await interaction.response.send_message(view=ContinueAgendaView(bot=self.bot), embed=embed)
        await _disable_button_by_followup(self, interaction)


class PowerOfAttorneyView(discord.ui.View):

    def __init__(self, bot, date: datetime):
        self.bot = bot
        self.date = date

        super().__init__(
            timeout=None
        )

    @discord.ui.button(label="委任状を提出", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_modal(modal.RegisterPowerOfAttorney(bot=self.bot, date=self.date))

    @discord.ui.button(label="委任状を取り消す", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        text = json_process.get_power_of_attorney_text(date=self.date, id=interaction.user.id)
        embed = discord.Embed(
            description=text
        )

        if text is None:
            await interaction.response.send_message("あなたの委任状は存在しません。", ephemeral=True)
        else:
            await interaction.response.send_message(
                "以下の委任状を取り消しますか？",
                embed=embed,
                view=DeletePowerOfAttorneyView(bot=self.bot, date=self.date),
                ephemeral=True
            )


class SubmitPowerOfAttorneyView(discord.ui.View):

    def __init__(self, bot, date: datetime):
        self.bot = bot
        self.date = date

        super().__init__()

    @discord.ui.button(label="提出", style=discord.ButtonStyle.green)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message("委任状が受理されました。提出ありがとうございます。", ephemeral=True)
        await _disable_button_by_followup(self, interaction)


class DeletePowerOfAttorneyView(discord.ui.View):

    def __init__(self, bot, date: datetime):
        self.bot = bot
        self.date = date

        super().__init__()

    @discord.ui.button(label="取り消す", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if json_process.delete_power_of_attorney(date=self.date, id=interaction.user.id):
            await interaction.response.send_message("委任状が取り消されました。", ephemeral=True)
            await _disable_button_by_followup(self, interaction)
        else:
            await interaction.response.send_message("削除時にエラーが発生しました。")


class DeleteMeetingView(discord.ui.View):
    def __init__(self, bot, date_str):
        self.bot = bot
        self.date_str = date_str

        super().__init__()

    @discord.ui.button(label="取り消す", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        json_process.delete_meeting(date_str=self.date_str)
        await interaction.response.send_message(self.date_str + "会議を取り消しました。")
        await _disable_button_by_followup(self, interaction)


async def _disable_button_by_followup(view: discord.ui.View, interaction: discord.Interaction):
    for item in view.children:
        item.disabled = True
    await interaction.followup.edit_message(interaction.message.id, view=view)