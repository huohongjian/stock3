#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

#import os, sys, time, argparse, getpass, datetime
#from libs.Sqlite import Sqlite as db
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from libs import tdate
#from libs import fetch
#import pandas as pd
#import numpy as np
from tqdm import tqdm
#from libs import common as co
#from libs import view

from libs.Sqlite import Sqlite as db
import tushare as ts
import threading
import time
from concurrent import futures
from queue import Queue

end = object()

print('start..........')
s = time.time()
q = Queue()

sql = "select code from day_all limit 100"
res = db.conn().all(sql)
codes = [r[0] for r in res]



def test():
	print('this is a function')
	for i in range(100):	
		print(i)
		r = q.get()
		print(r)
		if r == 'hhj':
			print('hhj')
			break

pbar = tqdm(total=len(codes))
def getData(code):
	df = ts.get_k_data(code=code)
	hd = df.head(1)
	q.put(hd)
	pbar.update(1)
	return hd

#t = threading.Thread(target=test)
#t.setDaemon(True)
#t.start()


with futures.ThreadPoolExecutor(4) as executor:
#	executor.submit(test)
	for code in codes:
		future = executor.submit(getData, code)
#		q.put(future.result())
#		pbar.update(1)
#	i = 0
#	for future in executor.map(getData, codes):
#		i +=1
#		print(q.qsize(), i, '-'*20)
#		pass

pbar.close()
print(time.time() - s)
#q.put(end)
print('size', q.qsize())
#while not q.empty():
#	df = q.get()
#	print(df.head(1))

print()
print(time.time() - s)

exit()






result = []

def worker(n):
	print('worker', n)
	time.sleep(1)


def get(code):	
	df = ts.get_k_data(code, start='2017-01-01')
	result.append(df)
	print(len(result), code)


def begin():
	for code in codes:
		t = threading.Thread(target=get, args=(code,))
		t.start()
	t.join()


def begin1():
	for code in codes:
		get(code)


if __name__ == '__main__':
	print('start...')
	start = time.time()
	pool = []
	for code in codes:
		t = threading.Thread(target=get, args=(code,))
		pool.append(t)

	for t in pool:
		t.start()

#	for t in pool:
#		t.join()
	
	print('finished:', time.time() - start)
	print(len(result))
