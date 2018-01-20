#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import re, os, sys, time, argparse, getpass, readline, importlib
from libs.Sqlite import Sqlite as db
from libs import common as co


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: Execute Structured Query Language')
	parser.add_argument('commands', nargs='*', default='jbm', help='Execute filename [command.py]')
	ps = parser.parse_args(args)

	sep = os.path.sep								
	dirname = os.path.dirname(os.path.abspath(__file__))\
			+ sep + 'libs' + sep + 'select' + sep

	cmd = ''
	params = {}
	modCache = {}
	while True:
		I = input('stock-ss> ').strip()
		I = re.sub('\s*:\s*', ':', I)
		I = re.sub('\s*,\s*', ',', I)

		if I == '':
			continue
		elif I in ('exit', 'e'):
			return
#		删除缓存的参数
		elif I.startswith('-'):
			key = I[1:].strip()
			if key in params.get(cmd):
				params[cmd].pop(key)
			continue
		elif I in ('h'):
			I = 'help'
		elif I.isdigit():
			I = cmd + ' page:' + I
		elif I in ('n', '>', '.'):
		 	I = cmd + ' page:' + str(int(params.get(cmd,{}).get('page',1)) + 1)
		elif I in ('p', '<', ','):	
		 	I = cmd + ' page:' + str(int(params.get(cmd,{}).get('page',2)) - 1)
		elif I.startswith('-') and I[1:].isdigit():
		 	I = cmd + ' page:' + str(int(params.get(cmd,{}).get('page',2)) - int(I[1:]))
#		省略命令
		elif I.split()[0].find(':')>0:
			I = cmd + ' ' + I
		elif I in ('asc', 'a'):
			I = cmd + ' asc:True'
		elif I in ('desc', 'd'):
			I = cmd + ' asc:False'
		elif I in ('r'):
			I = cmd


		i = (I + ' ').find(' ')
		cmd, paraString = I[:i], I[i:]
		if params.get(cmd) is None:
			params[cmd] = {}
		params[cmd].update(parseParameter(paraString))
			
		if modCache.get(cmd) is None:
			if os.path.isfile(dirname + cmd + '.py'):
				modCache[cmd] = importlib.import_module('libs.select.' + cmd)
			else:
				print('Command error, please input again.', 'No {}.py file'.format(cmd))
				continue

		modCache.get(cmd).main(params.get(cmd))



def parseParameter(paraString):
	args = paraString.split()	
	options = {}
	for a in args:
		i = a.find(':')
		if i>0:
			options[a[:i]] = a[i+1:]
	return options





if __name__ == '__main__':
	main(sys.argv[1:])

