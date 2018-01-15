#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass, datetime
from libs.Sqlite import Sqlite as db
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs import tdate
import pandas as pd
import numpy as np
from tqdm import tqdm

df1 = pd.DataFrame([['001', 11], ['002', 2]], columns=['code', 'price'])
print(df1)

df2 = pd.DataFrame([['001', 1], ['003', 3]], columns=['code', 'price'])
print(df2)

df3 = pd.merge(df1, df2)
print(df3)


'''
sql = "select code, date, open, close, high, low from kdata where code in ('600300', '300347') and date>'2017-06-30' order by date"

df = pd.read_sql(sql, db.conn().connect)
print(df.groupby(['code'])['close'].max())

start = time.time()
sql = "select code from kdata group by code"
res = db.conn().all(sql)
codes = [x[0] for x in res]
print(time.time() - start)


start = time.time()
sql = "select distinct code from kdata"
res = db.conn().all(sql)
codes = [x[0] for x in res]
print(time.time() - start)

pbar = tqdm(total=len(codes))
for code in codes:
	pbar.set_description('[{}]'.format(code))
	sql = "select id, close from kdata where code=?"
	df = db.conn().df(sql, [code])
	df['ma5'] = df.close.rolling(window=5).mean()
	df['ma10'] = df.close.rolling(window=10).mean()
	df['ma20'] = df.close.rolling(window=20).mean()
	df['ma30'] = df.close.rolling(window=30).mean()
	df['ma60'] = df.close.rolling(window=60).mean()
	pbar.update(1)
pbar.close()
'''

