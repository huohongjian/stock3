#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
from libs.Sqlite import Sqlite as db


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s show stocks list')
	parser.add_argument('code', nargs='*', help='stock code')
	parser.add_argument('-u', '--user', default=getpass.getuser(), help='default value is system login.')
	parser.add_argument('-d', '--date', help='form start date to end date (default:None)')
	parser.add_argument('-s', '--sum', action='store_const', const='sum', help='sum the integers')
	parser.add_argument('-n', '--num', type=int, default=10, help='max rows of result')
	ps = parser.parse_args(args)
	
	if ps.code==[]:
		getAll()
	else:
		getByCode(ps.code)


def getAll():
	sql = "SELECT * FROM trade"
	rs = db.conn().all(sql)
	render(rs)

def getByCode(code):
	sql = "SELECT * FROM trade WHERE code=?"
	rs = db.conn().all(sql, code)
	render(rs)


def render(rs):
	placeholder0 = '{:>3} {:^5} {:^10} {:>2} {:^8} {:>6} {:>6} {:^10}  {}'
	placeholder1 = '{:>3} {:^5} {:<10} {:>2} {:^8} {:>6.2f} {:>6} {:>10.2f}  {}'
	print(placeholder0.format('NO','user','date','F','code','price','volume','amount','message'))
	for r in rs:
		print(placeholder1.format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))


if __name__ == '__main__':
	main(sys.argv[1:])

