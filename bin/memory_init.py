#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
from libs.Sqlite import Sqlite as db
from datetime import date


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: Init memory, will clear memory. Notice!!!')
	parser.add_argument('command', nargs='?', default='memory',  help='stock code')
	ps = parser.parse_args(args)

	if ps.command == 'memory':
		create_memory_tables()

		sql = "select * from monitor"
		print(db.conn(':memory:').one(sql))
								

def create_memory_tables():
	basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	f = open(basePath + '/admin/stock.sql')
	c = f.read()
	f.close()
	db.conn(':memory:').exes(c)
	print('Create tables in memory successed.')
#	db.close()



if __name__ == '__main__':
	main(sys.argv[1:])

