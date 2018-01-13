#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, argparse
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from bin.libs.Sqlite	import Sqlite as db
import numpy	as np
import tushare	as ts


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: Init database')
	parser.add_argument('command', nargs='?', help='stock code')
	ps = parser.parse_args(args)

	create_tables()
	refresh_baseinfo_table()
		

def create_tables():
	f = open(basePath + '/admin/stock.sql')
	c = f.read()
	f.close()
	db.conn().exes(c)
	print('Create tables from /admin/stock.sql success.')

	

def append_baseinfo():
	sql = "select code, name from today_all a where(select count(1) as num from baseinfo b where a.code=b.code)=0"
	rss = db.conn().all(sql)
	sql = "INSERT INTO baseinfo(code, name) VALUES(?,?)"
	db.conn().exem(sql, rss)
	print('newly stock info is appended to baseinfo table.')


def refresh_baseinfo_table():
	print("fetching area data (地域分类)")
	df = ts.get_area_classified()
	sql = "INSERT INTO baseinfo(code, name, area) VALUES(?, ?, ?)"
	rss = np.array(df).tolist()
	db.conn().exem(sql, rss)
	print("baseinfo table's code,name,area fields are appended success.")

	def update_baseinfo(df, field):
		sql = "UPDATE baseinfo SET " + field + "=1 WHERE code=?"
		css = np.array(df[['code']]).tolist()
		db.conn().exem(sql, css)
		print("baseinfo's " + field + " field is refreshed success.")

	print("fetching sme's data (中小板)")
	update_baseinfo (ts.get_sme_classified(), 'issme')
	print("fetching gem's data (创业板)")
	update_baseinfo (ts.get_gem_classified(), 'isgem')
	print("fetching st's data (风险警示板)")
	update_baseinfo (ts.get_st_classified(),  'isst')
	print("fetching hs300's data (沪深300成份股)")
	update_baseinfo (ts.get_hs300s(), 'ishs300')
	print("fetching sz50's data (上证50成份股权)")
	update_baseinfo (ts.get_sz50s(),  'issz50')
	print("fetching zz500's (中证500成份股)")
	update_baseinfo (ts.get_zz500s(), 'iszz500')






if __name__=='__main__':
	main(sys.argv[1:])
