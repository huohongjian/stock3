#!/usr/bin/env python
# -*- coding:utf-8

import os
import importlib


def main():
	dirname = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
	while True:
		INPUT = input('stock> ').strip()
		if INPUT == '':
			continue
		if INPUT in ['exit', 'e']:
			exit()

		i = INPUT.find(' ')
		if i==-1:
			command = INPUT
			arg = ''
		else:
			command = INPUT[0:i]
			arg = INPUT[i+1:]
		
		filename = dirname + command + '.py'
		if os.path.isfile(filename):
			mod = importlib.import_module(command)
			if hasattr(mod, 'main'):
				mod.main(arg.split())
		else:
			print('Command error, please input again.', 'No {} file'.format(filename))


if __name__ == '__main__':

	main()

