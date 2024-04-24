#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
register_data_manager.pyのdictでユーザごとにインスタンス変数を生成するために使用
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

import json
from datetime import datetime, timedelta


class RegisterData:
    """
    date, agenda, place のインスタンス変数を生成する
    """

    def __init__(self):
        self.date = datetime.now()
        self.agenda = None
        self.place = get_place_by_json()

    def save_to_json(self):
        date = self.date.strftime("%Y-%m-%d %H:%M")

        with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)

        data = {
            date: {
                "agenda": self.agenda,
                "place": self.place,
                "powerOfAttorney": {
                }
            }
        }
        existing_data.update(data)

        with open("./../json/meetingData.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)


def get_place_by_json():
    """
    直近の場所を取得してくる
    """

    most_recent_days = None
    current_date = datetime.now().date()
    with open("./../json/meetingData.json", encoding="utf-8") as f:
        json_dict = json.load(f)
    keys_list = list(json_dict.keys())
    for date_str in keys_list:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M").date()
        subtract_days = (current_date - date).days
        if subtract_days <= 0:
            continue
        if most_recent_days is None:
            most_recent_days = 10 ** 18
        most_recent_days = min(most_recent_days, subtract_days)

    if most_recent_days is None:
        first_element = json_dict[keys_list[0]]
        return first_element["place"]

    most_recent_date = current_date - timedelta(days=most_recent_days)
    date_str = most_recent_date.strftime("%Y-%m-%d")

    for key in json_dict.keys():
        if date_str in key:
            return json_dict[key]["place"]
    return None
