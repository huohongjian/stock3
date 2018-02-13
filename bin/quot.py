#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import pandas as pd
from libs.Sqlite import Sqlite as db
from libs import cache, parameter, dataFrame
import time, easyquotation
from colorama import Fore, Back, Style

sqls = {}
filt = {}
disp = {}

def main(argString=''):

	COLORS = ['YELLOW', 'MAGENTA', 'CYAN', 'RED', 'GREEN', 'BLUE'] * 3
	header = '{:>3} {:^8} {:^6} {:>6} {:>6} {:>5}  {:>6} {:>6} {:>6} {:>6}'.format(
			 'NO','time','code','price','pc ','pcr','valume','amount','bid','ask')
	pattern = '{:>3} {:^8} {:^6} {:>6.2f} {:>6.2f} {:>5.1%} {:>6.0f} {:>6.0f} {:>6.2f} {:>6.2f}'

	
	codes = ['600300', '002339']
	colors = {}
	i = 0
	for code in codes:
		colors[code] = COLORS[i]
		i += 1

	quot = easyquotation.use('sina')
	pre = {}

	print('Starting monitor:', str(codes))
	i = 0
	while True:
		res = quot.stocks(codes)

		for k, v in res.items():
			p = pre.get(k, {})
			times 	= v.get('time')
			price 	= v.get('now')
			pc		= price - v.get('close', 0)
			pcr		= pc / v.get('close', 1)
			volume 	= (v.get('turnover') - p.get('turnover', 0)) / 100
			amount 	= (v.get('volume') - p.get('volume', 0)) / 10000
			bid		= v.get('buy')
			ask		= v.get('sell')
			if volume>10 or amount>10:
				i += 1
				if i%10 == 1:
					print(Back.BLUE, header, '', Style.RESET_ALL)
				print(getattr(Fore, colors.get(k)), pattern.format(i, times, k, price, pc, pcr, volume, amount, bid, ask), Style.RESET_ALL)
#				print('\a')
				if i%5 == 0:
					print()

		pre = res
		time.sleep(6)




if __name__ == '__main__':
	main()
