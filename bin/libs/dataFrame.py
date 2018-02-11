#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import pandas as pd
from .Sqlite import Sqlite as db


def filter(df, filtParas={}):
	for k, v in filtParas.items():
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
	return df


def render(df, sort='code', asc=True, limit=20, page=1):
	start = (page -1) * limit
	end   = start + limit
	df	= df.sort_values(sort, ascending=asc)

	df.reset_index(drop=True, inplace=True)
	print('\nResult:')
	print(df[start:end])


