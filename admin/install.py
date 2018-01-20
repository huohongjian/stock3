#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys, argparse
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from bin.libs.Sqlite	import Sqlite as db
from bin.libs import fetch
from tqdm import tqdm
import numpy	as np
import tushare	as ts


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: Init database')
	parser.add_argument('command', nargs='?', help='stock code')
	ps = parser.parse_args(args)

	create_tables()
	fetch.get_stock_basics()
	refresh_baseinfo_table()
	fetch_trade_calendar()
	fetch_k_data()



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
	print("Fetching area data (地域分类)... ", end='')
	df = ts.get_area_classified()
	sql = "INSERT INTO baseinfo(code, name, area) VALUES(?, ?, ?)"
	rss = np.array(df).tolist()
	db.conn().exem(sql, rss)
	print("is done! And saved data to table [baseinfo] success.")

	def update_baseinfo(df, field):
		sql = "UPDATE baseinfo SET " + field + "=1 WHERE code=?"
		css = np.array(df[['code']]).tolist()
		db.conn().exem(sql, css)
		print("is done! And update table [baseinfo] success.")

	print("fetching sme's data (中小板)... ", end='')
	update_baseinfo (ts.get_sme_classified(), 'issme')
	print("fetching gem's data (创业板)... ", end='')
	update_baseinfo (ts.get_gem_classified(), 'isgem')
	print("fetching st's data (风险警示板)... ", end='')
	update_baseinfo (ts.get_st_classified(),  'isst')
#	print("fetching hs300's data (沪深300成份股)... ", end='')
#	update_baseinfo (ts.get_hs300s(), 'ishs300')
#	print("fetching sz50's data (上证50成份股权)... ", end='')
#	update_baseinfo (ts.get_sz50s(),  'issz50')
#	print("fetching zz500's (中证500成份股)... ", end='')
#	update_baseinfo (ts.get_zz500s(), 'iszz500')



def fetch_trade_calendar():
	print('Fetching trade_calendar... ', end='')
	df = ts.trade_cal()
	df.to_sql('trade_cal', db.conn().connect, if_exists='replace')
	print('is done! And saved data to table [trade_cal] success.')


def fetch_k_data():
	print('First fetch k_data... ')
	sql = "SELECT code FROM baseinfo"
	res = db.conn().all(sql)
	codes = [x[0] for x in res]

	pbar = tqdm(total=len(codes))
	for code in codes:
		pbar.set_description('[{}]'.format(code))
		fetch.get_k_data(code, remove=False)
		pbar.update(1)
	pbar.close()
	print('All k_data fetched seccess first.')



if __name__=='__main__':
	main(sys.argv[1:])
