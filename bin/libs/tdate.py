#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import datetime
from .Sqlite import Sqlite as db


def now():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def today():
	return datetime.date.today().strftime('%Y-%m-%d')

def yestday():
	return (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def tomorrow():
	return (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def isTrade(day=today()):
	sql = "SELECT isOpen FROM trade_cal WHERE calendarDate=?"
	res = db.conn().val(sql, [day])
	return True if res else False

def nextTrade(day=today()):
	sql = "SELECT calendarDate FROM trade_cal WHERE calendarDate>? AND isOpen=1 ORDER BY calendarDate LIMIT 1"
	return db.conn().val(sql, [day])

def lastTrade(day=today()):
	sql = "SELECT calendarDate FROM trade_cal WHERE calendarDate<? AND isOpen=1 ORDER BY calendarDate DESC LIMIT 1"
	return db.conn().val(sql, [day])
