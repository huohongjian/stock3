#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass
from colorama import init, Fore, Back, Style
# ----------- colorama ----------
# https://pypi.python.org/pypi/colorama
# Fore/Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
# init(autoreset=True)  


def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: the detail info of buy stock saved into database')
	parser.add_argument('code', nargs="*", help='stock code')
	parser.add_argument('-m', '--message', default='', help='extra message')
	ps = parser.parse_args(args)

	# example:
	for color in ['RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN']:
		print(Style.BRIGHT)
		print(getattr(Fore, color), 'The fore color will be', color, Style.RESET_ALL)	
		print(getattr(Back, color), 'The back color will be', color)
		print(Style.RESET_ALL)


if __name__ == '__main__':
	main(sys.argv[1:])

