#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
@Author: Sphantix Hang
@Date: 2020-05-07 17:38:55
@LastEditors: Sphantix Hang
@LastEditTime: 2020-05-09 13:52:41
@FilePath: /Wesker/db.py
'''

import sqlite3

class DataBase(object):
    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass

class Sqlite3DataBase(DataBase):
    def __init__(self, db_path):
        super(Sqlite3DataBase, self).__init__()
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
