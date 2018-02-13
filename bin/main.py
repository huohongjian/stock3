#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, readline, importlib
import pandas as pd
from libs import cache


def main(argString=''):
	pd.set_option('display.width', 1366)
	sep = os.path.sep								
	dirname = os.path.dirname(os.path.abspath(__file__)) + sep

	cmd = 'main'
	arg = ''
	modCache = {}
	while True:
		I = input('stock-{}> '.format(cmd)).strip()

		if I == '':
			continue
		elif I in ('exit', 'e'):
			if cmd == 'main':
				return
			else:
				cmd = 'main'
				arg = ''
				continue
		elif I in ('cache', 'c', 'list', 'l'):
			cache.codes.list()
			continue
		elif I in ('help', 'h'):
			import help
			help.main(cmd)
			continue
		elif len(I)==6 and I.isdigit():
			import detail
			detail.main(I)
			continue
		elif I[0:6].upper() in ('SELECT', 'INSERT', 'UPDATE'):
			arg = I
		elif I.isdigit():
			arg = 'page:' + I
		elif I in ('n', '>', '.'):
			arg = 'page:+1' 
		elif I in ('p', '<', ','):	
		 	arg = 'page:-1'
		elif (I.startswith('+') or I.startswith('-')) and I[1:].isdigit():
		 	arg = 'page:' + I
#		省略命令
		elif I.split()[0].find(':')>0:
			arg = I
		elif I in ('asc', 'a'):
			arg =  'asc:True'
		elif I in ('desc', 'd'):
			arg = 'asc:False'
		elif I in ('rerender', 'r'):
			pass
		else:
			i = (I + ' ').find(' ')
			_cmd, _arg = I[:i], I[i:].strip()
			if modCache.get(_cmd) is None:
				if os.path.isfile(dirname + _cmd + '.py'):
					modCache[_cmd] = importlib.import_module(_cmd)
				else:
					print('Command error, please input again.')
					continue
			cmd = _cmd
			arg = _arg
	

		if cmd == 'main':
			continue
		else:
			modCache.get(cmd).main(arg)



if __name__ == '__main__':

	print('\n'*3)
	print('1.买涨不买跌，深跌长影是最佳')
	print('2.下跌2%坚决卖')
	print('3.买卖分批次(111223)、有间隔(>5%)')
	print('4.')
	print()
	main()

