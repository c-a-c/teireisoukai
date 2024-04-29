#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
register_data_manager.pyのdictでユーザごとにインスタンス変数を生成するために使用
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import json
import os
from datetime import datetime, timedelta

from bot import json_process


class RegisterData:
    """
    date, agenda, place のインスタンス変数を生成する
    """

    def __init__(self):
        self.date = datetime.now()
        self.agenda = None
        self.place = json_process.get_place()
        self.message_id = None

    def save_to_json(self):
        date = self.date.strftime("%Y-%m-%d %H:%M")

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)

        data = {
            date: {
                "agenda": self.agenda,
                "place": self.place,
                "messageID": self.message_id,
                "powerOfAttorney": {
                }
            }
        }
        existing_data.update(data)

        with open("./../json/meetingData.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

    def return_mail_text(self):
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        with open('../text/discordMail.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        mail_text = ""
        for line in lines:
            line = line.replace("roleID", os.getenv("MEMBER_ROLE_ID"))
            line = line.replace("year", str(self.date.year))
            line = line.replace("month", str(self.date.month))
            line = line.replace("weekday", weekdays[self.date.weekday()])
            line = line.replace("day", str(self.date.day))
            line = line.replace("hour", str(self.date.hour))
            line = line.replace("minute", str(self.date.minute))
            line = line.replace("agenda", self.agenda)
            line = line.replace("place", self.place)

            mail_text += line

        return mail_text
