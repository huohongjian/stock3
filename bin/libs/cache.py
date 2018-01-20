#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import time
import pandas as pd
from .Sqlite import Sqlite as db

_MAXLENGTH = 10
_length = 0
_buff = {}
_head = None
_last = None

def size():
	return _length

def has(key):
	return key in _buff

def isHead(key):
	return key == _head

def isLast(key):
	return key == _last

def remove(key):
	if has(key):
		global _MAXLENGTH, _length, _head, _last
		prevKey  = _buff.get(key).get('prev')
		nextKey = _buff.get(key).get('next')
		if isHead(key):
			_head = nextKey
			_buff[nextKey]['prev'] = None

		elif isLast(key):
			_last = prevKey
			_buff[prevKey]['next'] = None
		else:
			_buff[prevKey]['next'] = nextKey
			_buff[nextKey]['prev'] = prevKey

		del _buff[key]
		_length -= 1


def add(key, data): 
	global _MAXLENGTH, _length, _head, _last
	
	if _length > _MAXLENGTH:
		remove(_head)

	node = {
		'data': data,
		'prev': _last,
		'next': None,
	}
	if _head is None:
		_head = key
	else:
		_buff[_last]['next'] = key
	_last = key

	_buff[key] = node
	_length += 1


def get(key):
	if has(key):
		global _MAXLENGTH, _length, _head, _last
		cNode = _buff[key]
		if not isLast(key):
			prevKey = cNode.get('prev')
			nextKey= cNode.get('next')
			if isHead(key):
				_head = nextKey
				_buff[nextKey]['prev'] = None
			else:
				_buff[prevKey]['next'] = nextKey
				_buff[nextKey]['prev'] = prevKey

			_buff[_last]['next'] = key
			cNode['prev'] = _last
			cNode['next'] = None
			_last = key
		print('get from cache')
		return cNode.get('data')

# ----------------------------------------------------------- #


def exec(sql, key=None):
	key = key or hash(sql)
	if not has(key):
		df = db.conn().df(sql)
		add(key, df)
	else:
	 	df = get(key)
	return df


def filter(df, conditions={}, salt='HuoHongJian'):
	key = hash(str(conditions) + salt)
	if has(key):
		df = get(key)
	else:
		for k, v in conditions.items():
			if k in df.columns:
				if v.startswith(','):
					df = df[df[k]<=float(v[1:])]
				elif v.endswith(','):
					df = df[df[k]>=float(v[:-1])]
				elif v.find(',')>0:
					a = v.split(',')
					df = df[(df[k] >= float(a[0])) & (df[k] <= float(a[1]))]
				else:
					if df[k].dtype.name.startswith('float'):
						vv=float(v)
					else:
						vv = v
					df = df[df[k]==v]
			else:
				print('parameter:{} is not in columns. Please remove it.'.format(k))
		add(key, df)
	return df

def render(df, sort='code', asc=True, limit=20, page=1):
	start = (page -1) * limit
	end   = start + limit
	df	= df.sort_values(sort, ascending=asc)

	df.reset_index()
	print('\nResult:')
	print(df[start:end])
	print()

# ---------------------------------------------------------------------------- #

def get_stock_basics():
	sql = '''SELECT a.code, b.price, b.p_change AS pc, b.pe, a.pb, a.esp, a.bvps,
			(a.name||' '||a.industry||' '||a.area) as extrainfo
			FROM stock_basics AS a
			LEFT JOIN day_all AS b
			ON a.code = b.code
			ORDER BY a.code'''
	return exec(sql, 'stock_basics')



