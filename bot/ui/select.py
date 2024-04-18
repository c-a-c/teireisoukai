#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
discord.ui.Selectを継承したクラスをまとめています
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

from datetime import datetime, timedelta
import discord

from bot.register_data_manager import RegisterDataManager
from bot.ui import view, modal


class DateSelect(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="次の水曜13:30-", value="one_week_later", description=""),
            discord.SelectOption(label="次々の水曜13:30-", value="two_week_later", description=""),
            discord.SelectOption(label="それ以外", value="other", description="自分で日時を指定できます"),
        ]

        super().__init__(
            placeholder="定例総会の日時を選択してください",
            custom_id="date_register",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        now = datetime.now()
        now_weekday = now.weekday()
        # 水曜日が2なので水曜日が0になるように9で調節
        until_next_wednesday = (-now_weekday + 7 + 2) % 7
        next_wednesday = now + timedelta(days=until_next_wednesday)
        register_data = RegisterDataManager.register_data_dict.get(interaction.user.id)

        match self.values[0]:
            case "one_week_later":
                register_data.date = next_wednesday.replace(hour=13, minute=30, second=0, microsecond=0)
                embed = discord.Embed(title="登録日時", description=register_data.date)
                await interaction.response.send_message(view=view.ContinueAgendaView(), embed=embed)
            case "two_week_later":
                next_next_wednesday = next_wednesday + timedelta(days=7)
                register_data.date = next_next_wednesday.replace(hour=13, minute=30, second=0, microsecond=0)
                embed = discord.Embed(title="登録日時", description=register_data.date)
                await interaction.response.send_message(view=view.ContinueAgendaView(), embed=embed)
            case "other":
                await interaction.response.send_modal(modal.IndividualDateModal())

            case _:
                print("選択外")
