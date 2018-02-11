#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import re


def parse(argString='', sqls={}, filt={}, disp={}):
	_sqls = {}
	_filt = {'pe':'0,120', 'esp':'0.05,'}
	_disp = {'sort':'pe', 'asc':True, 'limit':20, 'page':1}
	_sqls.update(sqls)
	_filt.update(filt)
	_disp.update(disp)
		
	argString = re.sub('\s*:\s*', ':', argString)
	argString = re.sub('\s*,\s*', ',', argString)
	args = argString.split()	
	for a in args:
		i = a.find(':')
		if i>0:
			k, v = a[:i], a[(i+1):]
			if k == 'page':
				if v.startswith('+'):
					_disp[k] += int(v[1:])
				elif v.startswith('-'):
					_disp[k] -= int(v[1:])
				else:
			   		_disp[k] = int(v)
			elif k == 'limit':
		   		_disp[k] = int(v)
			elif k == 'asc':
				_disp[k] = v.lower() not in ('0', 'f', 'false', 'd', 'desc')
			elif k == 'sort':
				_disp[k] = v
			elif k in _sqls:
				_sqls[k] = v
			else:
#				删除缓存的参数
				if k.startswith('-'):
					key = k[1:].strip()
					if key in _filt:
						_filt.pop(key)
				else:
					_filt[k] = v
	return (_sqls, _filt, _disp)
		


def render(sqls, filt, disp, total=None):
	for key, val in zip(['sqls', 'filt', 'disp'],[sqls, filt, disp]):
		print()
		print('[{}]'.format(key), end=' ')
		for k, v in val.items():
			print('{}:{}'.format(k, v), end='  ')
	if total is None:
		print()
	else:
		print('[Total={:,}]'.format(total))


def extreme(val, ext=('0','100'), isMax=True, toFloat=True):
	val = val.strip()
	if val.startswith(','):
		val = ext[0] + val
	elif val.endswith(','):
	 	val += ext[1]
	elif val.find(',')<0:
		if isMax:
			val = ext[0] + ',' + val
		else:
			val = val + ',' + ext[1]

	vs = val.split(',')
	if toFloat:
		vs = map(lambda x:float(x), vs)
	return vs

