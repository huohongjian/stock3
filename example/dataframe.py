#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
import pandas as pd


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: the detail info of buy stock saved into database')
	parser.add_argument('code', nargs="*", help='stock code')
	parser.add_argument('-m', '--message', default='', help='extra message')
	ps = parser.parse_args(args)

	dict = [[11,12,13,14], [21,22,23,24]]
	dict = [{'c1':10, 'c2':100}, {'c1':11, 'c2':110}, {'c1':12, 'c2':120}]
	df = pd.DataFrame(dict)
	print(df)

	for idx in df.index:
		df.loc[idx, 'c2'] = idx + 500
		print(idx, df.loc[idx].values)	



if __name__ == '__main__':
	main(sys.argv[1:])

