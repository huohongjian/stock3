#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2017-11-22

import sqlite3
import os
import pandas

class Sqlite:
	conns = {}
	connect = None
	cursor = None
	showSQL = False

	@classmethod
	def conn(cls, filename=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/data/stock.sqlite3'):
		if cls.conns.get(filename, None) is None:
			cls.conns[filename] = sqlite3.connect(filename)

		cls.connect = cls.conns[filename]
		cls.cursor = cls.connect.cursor()
		return cls


	@classmethod
	def close(cls):
		for c in cls.conns:
			if cls.conns[c]:
				cls.conns[c].close()
				cls.conns[c] = None
				print('This connection is closed.')
		return cls


	@classmethod
	def showsql(cls, isshow=True):
		cls.showSQL = isshow
		return cls


	@classmethod
	def commit(cls, iscommit=True):
		if iscommit:
			cls.connect.commit()
		return cls
	
	
	@classmethod
	def exes(cls, script, iscommit=True):
		if cls.showSQL:
			print('SQL:[{}]\nPAS:{}'.format(sql,paras))

		cls.cursor.executescript(script)
		cls.commit(iscommit)
		return cls


	@classmethod
	def exem(cls, sql, paras=[], iscommit=True):
		if cls.showSQL:
			print('SQL:[{}]\nPAS:{}'.format(sql,paras))

		cls.cursor.executemany(sql, paras)
		cls.commit(iscommit)
		return cls

	
	@classmethod
	def exec(cls, sql, paras=[],iscommit=True):
		if cls.showSQL:
			print('SQL:[{}]\nPAS:{}'.format(sql,paras))

		try:
			cls.cursor.execute(sql, paras)
			cls.commit(iscommit)
		except Exception as e:
			print('SQL:[{}]\nPAS:{}'.format(sql,paras))
			print(e)
		else:
			return cls


	@classmethod
	def all(cls, sql, paras=[]):
		cls.exec(sql, paras, False)
		return cls.cursor.fetchall()


	@classmethod
	def one(cls, sql, paras=[]):
		cls.exec(sql, paras, False)
		return cls.cursor.fetchone()


	@classmethod
	def val(cls, sql, paras=[]):
		res = cls.one(sql, paras)
		return res[0] if res else None

	
	@classmethod
	def df(cls, sql, paras=[]):
		res = cls.all(sql, paras)
		return pandas.DataFrame(res, columns=cls.fields())


	@classmethod
	def fields(cls):
		des = cls.cursor.description
		return [x[0] for x in des]
