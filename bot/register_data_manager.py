#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/registerコマンドの使用時に入力したユーザのデータを辞書に格納します。
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/04/06(Created: 2024/04/06)"

from bot.data.register_data import RegisterData


class RegisterDataManager:
    """
    同時に登録を可能にするために、複数のユーザーの入力を管理するクラス
    """
    register_data_dict = {}

    @classmethod
    def add_data(cls, user_id: int):
        """
        RegisterDataを追加する
        """
        cls.register_data_dict[user_id] = RegisterData()
