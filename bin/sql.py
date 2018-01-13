#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
from libs.Sqlite import Sqlite as db


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: Execute Structured Query Language')
	parser.add_argument('sql', nargs='*', help='Notice: replace * with \'*\' or . or all')
	ps = parser.parse_args(args)

	if ps.sql==[]:								
		while True:
			INPUT = input('stock-sql> ').strip()
			if INPUT == '':
				continue
			if INPUT in ['exit', 'e']:
				return

			if INPUT[0:3].upper() == 'SEL':
				fetchall(INPUT)
			else:
				execute(INPUT)
	else:
		sql = ' '.join(ps.sql)
		if sql[0:3].upper() == 'SEL':
			sql = sql.replace(" '*' ", ' * ').replace(' . ', ' * ').replace(' all ', ' * ')
			fetchall(sql)
		else:
			execute(sql)



def fetchall(sql):
	res = db.conn().all(sql)
	print([r[0] for r in db.cursor.description])
	print('--------------------------------------------------------------')
	for r in res:
		print(r)



def execute(sql):
	db.conn().exec(sql)
	print('execute SQL successed.')


if __name__ == '__main__':
	main(sys.argv[1:])

