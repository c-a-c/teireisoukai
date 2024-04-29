import json
import os
from datetime import datetime, timedelta


def delete_meeting(date_str):
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_data.pop(date_str)

    with open("../json/meetingData.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


def delete_power_of_attorney(date: datetime, id: int):
    date_str = date.strftime("%Y-%m-%d %H:%M")

    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    try:
        power_of_attorney = json_data[date_str]["powerOfAttorney"]
        power_of_attorney.pop(str(id))
        json_data[date_str]["powerOfAttorney"] = power_of_attorney
    except KeyError:
        return False

    with open("../json/meetingData.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return True


def get_power_of_attorney_text(date: datetime, id: int):
    date_str = date.strftime("%Y-%m-%d %H:%M")
    with open("../json/meetingData.json") as f:
        json_data = json.load(f)
    power_of_attorney = json_data[date_str]["powerOfAttorney"]
    for element in power_of_attorney:
        if int(element) == id:
            return power_of_attorney[element]

    return None


def get_delete_text(date_str):
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    meeting_data = json_data[date_str]

    return_text = ""
    return_text += "◎議題\n" + meeting_data["agenda"] + "\n"
    return_text += "場所: " + meeting_data["place"]

    return return_text


def update_power_of_attorney(date: datetime, id: int, reason_text: str):
    with open('../json/meetingData.json', 'r', encoding='utf-8') as f:
        existing_json = json.load(f)

    date_str = date.strftime("%Y-%m-%d %H:%M")
    if existing_json[date_str]["powerOfAttorney"]:
        existing_json[date_str]["powerOfAttorney"][str(id)] = reason_text
    else:
        existing_json[date_str]["powerOfAttorney"] = {str(id): reason_text}

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
    with open("../text/discordMail.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("../json/meetingData.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    meeting_data = json_data[date_str]
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    weekdays = ['月', '火', '水', '木', '金', '土', '日']

    mail_text = "[再送]\n"
    for line in lines:
        line = line.replace("roleID", os.getenv("MEETING_ROLE_ID"))
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
