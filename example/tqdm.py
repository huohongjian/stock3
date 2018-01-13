#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
from libs.Sqlite import Sqlite as db
from datetime import date

import pandas as pd
import numpy as np
from tqdm import tqdm, trange


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: the detail info of buy stock saved into database')
	parser.add_argument('code', nargs='?', help='stock code')

	print('\nuse in tqdm(range(100))')
	for i in tqdm(range(100)):
		time.sleep(0.01)


	print('\nuse in trange(100)')
	for i in trange(100):
		time.sleep(0.01)


	print('\nuse in list')
	pbar = tqdm(['a', 'b', 'c', 'd', 'e', 'f'])
	for char in pbar:
		time.sleep(0.1)
		pbar.set_description('Processing %s' % char)
						

	print('\nuse with')
	with tqdm(total=100) as pbar:
		for i in range(10):
			pbar.update(10)
		

	print('\nuse update and close()')
	pbar = tqdm(total=300)
	for i in range(10):
		pbar.update(10)
	pbar.close()



	print('\nuse in pandas')
	df = pd.DataFrame(np.random.randint(0, 100, (10000000,6)))
	tqdm.pandas(desc='my bar!')
	df.progress_apply(lambda x: x**2)


	print('\nuse in 3 loop')
	for i in trange(10, desc='1st loop'):
		for j in trange(5, desc='2nd loop'):
			for k in trange(30, desc='3nd loop'):
				time.sleep(0.01)



if __name__ == '__main__':
	main(sys.argv[1:])

