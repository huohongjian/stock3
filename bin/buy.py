#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
from libs.Sqlite import Sqlite as db
from datetime import date


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: the detail info of buy stock saved into database')
	parser.add_argument('code', help='stock code')
	parser.add_argument('price', type=float, help='stock price')
	parser.add_argument('volume', type=int, help='stock volume')
	parser.add_argument('-u', '--user', default=getpass.getuser(), help='default value is system login.')
	parser.add_argument('-d', '--date', default=date.today(), metavar='xxxx-xx-xx', help='the date of buy stock(default: today)')
	parser.add_argument('-m', '--message', default='', help='extra message')
	
	try:
		ps = parser.parse_args(args)
	except Exception as e:
		print(e)
	else:
		print('the detail info of buy stock:')
		print('user:   {}'.format(ps.user))
		print('date:   {}'.format(ps.date))
		print('code:   {}'.format(ps.code))
		print('price:  {}'.format(ps.price))
		print('volume: {}'.format(ps.volume))
		print('message:{}'.format(ps.message))

		I = input('confirm(yes/no):')
		if I in ('y', 'Y', 'yes', 'YES'):
			buystock(ps.code, ps.price, ps.volume, ps.user, ps.date, ps.message)
		else:
			print('no saved')


def buystock(code, price, volume, user, date, remark):
	sql = "INSERT INTO trade(user, date, deal, code, price, volume, amount, remark) VALUES(?,?,'b',?,?,?,?,?)"
	db.conn().showsql(False).exec(sql, [user, date, code, price, volume, price*volume, remark])
	print('add the info of buy stock is successed.')


if __name__ == '__main__':
	main(sys.argv[1:])

