#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Author: Sphantix Hang
@Date: 2020-04-22 15:50:16
@LastEditors: Sphantix Hang
@LastEditTime: 2020-05-13 09:58:23
@FilePath: /Wesker/core/mods/helper.py
'''

import datetime
import hashlib
import os
import random
import shutil
import socket
import time
import urllib.request
from urllib.parse import urlparse
from zipfile import ZipFile


def is_directory_exist(dir_full_path):
    return (os.path.exists(dir_full_path) and os.path.isdir(dir_full_path))


def create_directory(dir_full_path):
    if not is_directory_exist(dir_full_path):
        os.makedirs(dir_full_path)


def is_file_exist(file_full_path):
    return (os.path.exists(file_full_path) and os.path.isfile(file_full_path))


def remove(full_path):
    if not os.path.exists(full_path):
        return
    else:
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path, ignore_errors=True)


def create_file(full_path):
    if os.path.exists(full_path):
        return False

    f = open(full_path, 'w')
    f.close()
    return True


def copy_file(src_full_path, dst_full_path):
    shutil.copy2(src_full_path, dst_full_path)


def format_time_use(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return ("Cost: %dh%02dm%02ds" % (h, m, s))
    elif m > 0:
        return ("Cost: %02dm%02ds" % (m, s))
    else:
        return ("Cost: %02ds" % (s))


def get_current_timestamp():
    return time.mktime(
        time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      "%Y-%m-%d %H:%M:%S"))


def get_current_time_string():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


def get_current_time_string_accurate():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')


def check_url_access(url):
    USER_AGENT = {
        "Android": [
            "Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 6.0; MotoG3 Build/MPIS24.65-33.1-2-16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"
        ]
    }
    try_times = 5
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          USER_AGENT["Android"][random.randint(
                              0,
                              len(USER_AGENT["Android"]) - 1)])]

    connect = False
    for _ in range(try_times):
        try:
            opener.open(url, timeout=10)
            connect = True
            break
        except Exception:
            continue

    return connect


def get_domain_from_url(url):
    netloc = urlparse(url).netloc
    domain = netloc.split(":")[0]
    return domain


def get_ip_from_domain(url_domain):
    try_times = 5

    ip = ""
    for _ in range(try_times):
        try:
            addr = socket.getaddrinfo(url_domain, 'http')
        except Exception:
            continue

        ip = addr[0][4][0]
        if len(ip) != 0 and ip != '0.0.0.0':
            break

    return ip


def get_ip_from_url(url):
    return get_ip_from_domain(get_domain_from_url(url))


def get_file_md5(file_full_path):
    if not os.path.isfile(file_full_path):
        return
    md5hash = hashlib.md5()
    with open(file_full_path, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            md5hash.update(b)

    return md5hash.hexdigest()


def create_zip_file(output_full_path, input_dir):
    shutil.make_archive(output_full_path, 'zip', input_dir)
