#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, time, getpass, readline
from libs.Sqlite import Sqlite as db

def main(argString=''):
	ps = {
		'page': '1'
	}

#	ps.update(paras)
	offset = (int(ps.get('page', 1)) - 1) * 10
	sql = "SELECT code, name from stock_basics LIMIT {offset}, 10"\
		   .format(offset=offset, **ps)
	
	res = db.conn().all(sql)
	for r in res:
		print(r)
	print()
	print(ps)




def help():
	print('''
This is help content:

''')

if __name__ == '__main__':
	main()
