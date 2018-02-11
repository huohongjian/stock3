#!/usr/bin/env python
# author: HuoHongJian
# date: 2018-01-05
# -*- coding:utf-8 -*-

import sys, time, datetime, argparse, random
import numpy as np
import pandas as pd
import tushare as ts
from libs.Sqlite import Sqlite as db
from libs import fetch
from libs import tdate
from tqdm import tqdm


def main(argString):
	args = argString.split()
	parser = argparse.ArgumentParser(description='%(prog)s: fetch data and save into database')
	parser.add_argument('command', nargs='?', default='day', help='period choices=[add day] (default: day)')
	ps = parser.parse_args(args)
	if ps.command=='all':
		all()
	else:
		daily()

#		fetch_stock_basics()

def all():
	pass


def daily():
	print('Perform daily operations')
	fetch_day_all()
	print('The daily operations have been completed.') 


def monthly():
	fetch_concept_classified()
	fetch_stock_basics()

def yearly():
	fetch_trade_calendar()


def fetch_trade_calendar():
	print('Fetching trade_calendar... ', end='')
	df = ts.trade_cal()
	df.to_sql('trade_cal', db.conn().connect, if_exists='replace')
	print('is done! And saved data to table [trade_cal] success.')


def fetch_concept_classified():
	print("fetching concept classified data (概念分类)")
	df = ts.get_concept_classified()
	df.to_sql('concept', db.conn().connect, if_exists='replace')
	print("Concept classified data is saved to [concept] table success.")


												  
def fetch_today_all():
	print('Fetching today_all... ')
	df = ts.get_today_all()
	df.to_sql('today_all', db.conn().connect, if_exists='replace')
	print('is done! AND saved data to table [today_all] success.')


def fetch_stock_basics():
	print('Fetching stock_basics... ')
	df = ts.get_stock_basics()
	df.to_sql('stock_basics', db.conn().connect, if_exists='replace')
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

	



def fetch_day_all():
	print('Fetching day_all... ')

#	判断是否为当天数据
	for N in range(10):
		df = ts.get_day_all()
		size = df.shape[0]
		loop = False
		for i in range(3):
			idx = random.randint(0, size-1)
			_df = df.ix[idx]
			sql = "SELECT open, close, high, low FROM kdata WHERE code=? ORDER BY date DESC LIMIT 1"
			res = db.conn().one(sql, [_df.code])
			if not any(res):
				continue
			if res[0] == _df.open and res[1]==_df.price and res[2]==_df.high and res[3]==_df.low:
				loop = True
				break
		
		if not loop:
			break

		if N > 8:
			exit()
		print('网上数据不是最新的，1个小时后，再次下载.')
		time.sleep(3600)


#	处理下载的数据
	df = df.loc[df.open > 0]
	df.to_sql('day_all', db.conn().connect, if_exists='replace')
	codes = list(df.code)  #np.array(df[['code']]).tolist()
	print('is done! And saved data to table [day_all] success.')


#	判断是否append to table [kdata]
	sql = "SELECT max(date) FROM kdata"
	maxDate = db.conn().val(sql) or '2018-01-01'
	today = tdate.today()
	_time  = tdate.time()
	nextTradeDay = tdate.nextTrade(maxDate)

#	数据连续,可一次性下载当天全部交易数据
	if (nextTradeDay == today and _time > '15:50:00') or 1:
		df = df[['code', 'open', 'price', 'high', 'low', 'volume']]
		df = df.set_index('code')
		df.insert(0, 'date', pd.Series([nextTradeDay], index=df.index))
		df.rename(columns={'price':'close'}, inplace=True)
		df.to_sql('kdata', db.conn().connect, if_exists='append')
		print('At the same time, day_all data also saved to table [kdata] success.')

		sql = "INSERT INTO log (operate, result, message) VALUES (?, ?, ?)"
		db.conn().exec(sql, ['fetch_day_all', 'success', 'fetch and saveed the data to tables [day_all, kdata], total=[{}]'.format(len(codes))])

		print('Starting compute moving average... ')
		pbar = tqdm(total=len(codes))
		for code in codes:
			pbar.set_description('[{}]'.format(code))
			sql = "SELECT id, close, volume FROM kdata WHERE code=? ORDER BY date DESC LIMIT 60"
			rdf = db.conn().df(sql, [code]).sort_index(axis=0, ascending=False)
			rdf = fetch.compute_ma(rdf)
			r = rdf.iloc[-1]
			sql = '''UPDATE kdata SET 
				ma5=?, ma10=?, ma20=?, ma30=?, ma60=?,
				va5=?, va10=?, va20=?, va30=?, va60=?
				WHERE id=?'''
			db.conn().exec(sql, [*r[3:].round(2), r.id])
			pbar.update(1)
		pbar.close()
	else:
		print('Save data to table [kdata] failed, Please execute the program at trade day and time > 16:00:00.')



def fetch_k_data(codes):
	print('Fetching data through function named get_k_data(code)... ')
	sql = "SELECT code, max(date) FROM kdata GROUP BY code"
	dates = dict(db.conn().all(sql))
	lastTradeDay = tdate.lastTrade(tdate.today())
	errorCodes = []
	pbar = tqdm(total=len(codes))
	for code in codes:
		pbar.set_description('[{}]'.format(code))
		sDate = dates.get(code, '2017-01-01')
		if sDate < lastTradeDay:
			try:
				df = ts.get_k_data(code, start=sDate)
				df = df.set_index('date')
				df.to_sql('kdata', db.conn().connect, if_exists='append')
			except Exception as e:
				print('[{}] some error raised:'.format(code), e)
				errorCodes.append(code)
		pbar.update(1)
	pbar.close()
	print('The data fetched and saved to table [kdata] success.')





if __name__ == '__main__':
	main(' '.join(sys.argv[1:]))
