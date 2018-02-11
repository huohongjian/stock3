#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import sys, getpass
from libs.Sqlite import Sqlite as db


def main(argString):

	if argString[0:3].upper() == 'SEL':
		fetchall(argString)
	else:
		execute(argString)



def fetchall(sql):
	res = db.conn().all(sql)
	print([r[0] for r in db.cursor.description])
	print('-'*30)
	for r in res:
		print(r)



def execute(sql):
	db.conn().exec(sql)
	print('execute SQL successed.')


if __name__ == '__main__':
	main(' '.join(sys.argv[1:]))

