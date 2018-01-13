#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, time, datetime, argparse
import pandas as pd
import tushare as ts
from libs.Sqlite import Sqlite as db
from libs import tdate
from tqdm import tqdm

ENG = db.conn().connect


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: fetch data and save into database')
	parser.add_argument('command', nargs='?', default='day', help='period choices=[add day] (default: day)')
	ps = parser.parse_args(args)
	if ps.command=='all':
		all()
	else:
		dayly()


def all():
	pass


def dayly():
	print('Fetching dayly data...')
	fetch_k_data()


def monthly():
	fetch_concept_classified()
	fetch_stock_basics()

def yearly():
	fetch_trade_calendar()


def fetch_trade_calendar():
	print('Fetching trade_calendar... ', end='')
	df = ts.trade_cal()
	df.to_sql('trade_cal', ENG, if_exists='replace')
	print('is done! And saved data to table [trade_cal] success.')

												  
def fetch_today_all():
	print('Fetching today_all... ')
	df = ts.get_today_all()
	df.to_sql('today_all', ENG, if_exists='replace')
	print('is done! AND saved data to table [today_all] success.')


def fetch_stock_basics():
	print('Fetching stock_basics... ')
	df = ts.get_stock_basics()
	df.to_sql('stock_basics', ENG, if_exists='replace')
	print('is done! And saved data to table [stock_basics] success')



def fetch_hist_data():
	codes = ['600300', '300347', '0000001', '000881']
	codes = ['300347']

	today = datetime.date.today()
	weekday = today.weekday()
	if weekday == 5:
		today -= datetime.timedelta(days=1)
	elif weekday == 6:
		today -= datetime.timedelta(days=2)

	pbar = tqdm(total=len(codes))
	for code in codes:
		sql = "SELECT date, close, hfq FROM hist WHERE code=? ORDER BY date DESC LIMIT 1"
		res = db.conn().one(sql, [code])
		p_date, p_close, p_hfq = res if res else ('2017-01-01', 0, 1)
		startdate = datetime.date(*map(int, p_date.split('-'))) + datetime.timedelta(days=1)

		if startdate <= today:
			try:		
				df = ts.get_hist_data(code, start=startdate.strftime('%Y-%m-%d'))
			except Exception as e:
				print(e)
			else:
				pass

			if any(df):
				df = df.sort_index()
				hfqs, needFQ = [], False
				if p_close == 0:
					r0 = df.iloc[0]
					p_close = round(r0['close'] - r0['price_change'], 2)

				for idx in df.index:
					r = df.loc[idx]
					E = round(r['close'] - r['price_change'], 2)
					if abs(E - p_close) < 0.02:
						hfq = p_hfq
					else:
						hfq = round(p_hfq * p_close / E, 9)
						needFQ = True
					hfqs.append(hfq)
					p_close, p_hfq = r['close'], hfq
					
				df.insert(0, 'code', pd.Series([code], index=df.index))
				df.insert(1, 'hfq',  pd.Series(hfqs,   index=df.index))
				df.insert(2, 'qfq',  pd.Series([1],    index=df.index))
				df.to_sql('hist', db.conn().connect, if_exists='append')
				if needFQ:
					sql = "UPDATE kdata SET qfq = hfq/? WHERE code=?"
					db.conn().showsql().exec(sql, [hfq, code])
		pbar.update(1)
	pbar.close()
	print('fetch data successed.')


	sql = "SELECT code, date, hfq, qfq FROM kdata ORDER BY date"
	res = db.conn().all(sql)
	for r in res:
		print(r)



def fetch_k_data():
	codes = ['300347']
	today = datetime.date.today()
	startday = today - datetime.timedelta(days=500)

	# 获取最新交易数据（全部股票）
	sql = "INSERT INTO log (symbol, end) VALUES (?, ?)"
	id = db.conn().exec(sql, ['fetch_to_log', now()]).cursor.lastrowid
	df = ts.get_day_all()
	df = df.loc[df.price > 0]
	df.to_sql('dayall', ENG, if_exists='replace')
	sql = "UPDATE log SET start=? WHERE id=?"
	db.conn().exec(sql, [now(), id])
	return 
	# 判断是否为今日的交易数据



#		df = df.loc[df.price>0, ['code', 'price']]

	for code in codes:
		sql = "SELECT date FROM kdata WHERE code=?"

		df = ts.get_k_data(code, start=startday.strftime('%Y-%m-%d'))
		df = df.set_index('date')


		
		df.to_sql('kdata', ENG, if_exists='append')


	pass


def now():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')





def fetch_concept_classified():
	print("fetching concept classified data (概念分类)")
	df = ts.get_concept_classified()
	df.to_sql('concept', ENG, if_exists='replace')
	print("Concept classified data is saved to [concept] table success.")





if __name__ == '__main__':
	main(sys.argv[1:])
