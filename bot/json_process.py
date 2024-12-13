#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
json関連の処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/29(Created: 2024/04/29)"

import json
import os
from datetime import datetime, timedelta


def delete_meeting(date_str):
    """
    jsonからある日程の会議データを削除する
    """
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_data.pop(date_str)

    with open("../json/meetingData.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


def delete_power_of_attorney(date: datetime, user_id: int):
    """
    jsonからある日程のある委任状を削除する
    """
    date_str = date.strftime("%Y-%m-%d %H:%M")

    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    try:
        power_of_attorney = json_data[date_str]["powerOfAttorney"]
        power_of_attorney.pop(str(user_id))
        json_data[date_str]["powerOfAttorney"] = power_of_attorney
    except KeyError:
        return False

    with open("../json/meetingData.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return True


def get_power_of_attorney_text(date: datetime, user_id: int):
    """
    ある日程のある委任状の委任状の文字列を返す
    """
    date_str = date.strftime("%Y-%m-%d %H:%M")
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    power_of_attorney = json_data[date_str]["powerOfAttorney"]
    for element in power_of_attorney:
        if int(element) == user_id:
            return power_of_attorney[element]

    return None


def get_meeting_data_text(date_str):
    """
    ある日程の会議の議題と場所を書いた文字列を返す
    """
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    meeting_data = json_data[date_str]

    return_text = ""
    return_text += "◎議題\n" + meeting_data["agenda"] + "\n"
    return_text += "場所: " + meeting_data["place"]

    return return_text


def update_power_of_attorney(date: datetime, user_id: int, reason_text: str):
    """
    ある日程のあるユーザーの委任状データを更新する
    """
    with open('../json/meetingData.json', 'r', encoding='utf-8') as f:
        existing_json = json.load(f)

    date_str = date.strftime("%Y-%m-%d %H:%M")
    if existing_json[date_str]["powerOfAttorney"]:
        existing_json[date_str]["powerOfAttorney"][str(user_id)] = reason_text
    else:
        existing_json[date_str]["powerOfAttorney"] = {str(user_id): reason_text}

    with open('../json/meetingData.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(existing_json, indent=4, ensure_ascii=False))


def get_place():
    """
    直近の場所を取得してくる
    """

    most_recent_days = None
    current_date = datetime.now().date()
    with open("../json/meetingData.json", encoding="utf-8") as f:
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


def get_resend_mail_text(date_str):
    """
    メールを再送する際の文字列を返す
    """
    with open("../text/discordMail.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    meeting_data = json_data[date_str]
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    mail_text = "[再送]\n"

    for line in lines:
        line = line.replace("roleID", os.getenv("MEMBER_ROLE_ID"))
        line = line.replace("year", str(date.year))
        line = line.replace("month", str(date.month))
        line = line.replace("weekday", weekdays[date.weekday()])
        line = line.replace("day", str(date.day))
        line = line.replace("hour", str(date.hour))
        line = line.replace("minute", str(date.minute))
        line = line.replace("agenda", meeting_data["agenda"])
        line = line.replace("place", meeting_data["place"])

        mail_text += line

    return mail_text


def get_json_date_list():
    """
    会議の日程を文字列リストにして返す
    """

    def get_datetime(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')

    def get_date_str(date):
        return datetime.strftime(date, '%Y-%m-%d %H:%M')

    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 現在より先の日程を取得する
    date_str_list = list(json_data.keys())
    date_list = list(map(get_datetime, date_str_list))
    date_list = [date for date in date_list if datetime.now() < date]
    date_list.sort()
    date_str_list = list(map(get_date_str, date_list))

    # 最大5つまで取得するようにする
    return_date_list = []
    for i in range(5):
        if i >= len(date_str_list):
            break
        return_date_list.append(date_str_list[i])

    return return_date_list


def get_within_15minutes_date_str():
    """
    開催時間+15分以内に存在するdate_strを返す
    （開催時間丁度は含めない）
    """
    now = datetime.now()
    now = now.replace(second=0, microsecond=0)

    with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    for date_str in json_data.keys():
        # 既に開催されたものを除外
        if json_data[date_str]["heldBool"]:
            continue

        # +1~15分で確認
        start_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        for i in range(1, 16):
            current_time = start_time + timedelta(minutes=i)
            if now == current_time:
                print(now, current_time)
                return date_str

    return None


def update_held_bool_true(date_str):
    with open("./../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_data[date_str]["heldBool"] = True

    with open("../json/meetingData.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


