# -*- coding: utf-8 -*-

import datetime

def timeString():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d %H:%M:%S")