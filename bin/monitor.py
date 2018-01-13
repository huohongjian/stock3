#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import time, sys, argparse, getpass
from libs.Sqlite import Sqlite as db
from datetime import date

def main(args):
	parser = argparse.ArgumentParser(description='%(prog)s: monitor stocks and setup monitor condition')
	parser.add_argument('command',nargs='?', default='monitor', help='operation command')
	parser.add_argument('code',   nargs='?', default='000000', help='stock code')
	parser.add_argument('volume', nargs='?', default=0, type=int, help='stock code')
	parser.add_argument('amount', nargs='?', default=0, type=float, help='stock code')
	parser.add_argument('-u', '--user', default=getpass.getuser(), help='default: system login')
	parser.add_argument('-c', '--codes',nargs='*', help='monitor stock codes list')
	parser.add_argument('-m', '--message', default='', help='extra message')

	try:
		ps = parser.parse_args(args)
		{
			'monitor'	: monitor,
			'show'		: show,
			'add'		: add,
			'remove'	: remove,
			'usage'		: usage
		}.get(ps.command, monitor)(ps)

	except Exception as e:
		print('Some error raised.', e)


def usage(ps):
	print('Usage:')
	print('  monitor [-u user] [-c codes]:       monitoring user\'s stocks indicted by -c')
	print('  monitor add code volume [amount]:   add or renew the monitor condition of stock')
	print('  monitor remove code:                remove the monitor condition of stock')


def show(ps):
	sql = "SELECT * FROM monitor WHERE user=?"
	for r in db.conn().all(sql, [ps.user]):
		print(r)


def add(ps):
	sql = "INSERT OR REPLACE INTO monitor(id, user, date, code, volume, amount, message) VALUES (\
		   (SELECT id FROM monitor WHERE user=? AND code=?), ?, ?, ?, ?, ?, ?)"
	db.conn().exec(sql, [ps.user, ps.code, ps.user, date.today(), ps.code, ps.volume, ps.amount, ps.message])
	print('Add stock monitor info successed.')


def remove(ps):
	sql = "DELETE FROM monitor WHERE user=? AND code=?"
	db.conn().exec(sql, [ps.user, ps.code])
	print('code=[{}] stock is deleted success.')


def monitor(ps):
	import tushare as ts
	from libs.Sqlite import Sqlite as db
	from colorama import Fore, Back, Style
	COLORS = ['YELLOW', 'MAGENTA', 'CYAN', 'RED', 'GREEN', 'BLUE'] * 3
	header = '{:>3} {:^8} {:^6} {:>6} {:>6} {:>5}  {:>6} {:>6} {:>6} {:>6}'.format(
			 'NO','time','code','price','pc ','pcr','valume','amount','bid','ask')
	pattern = '{:>3} {:^8} {:^6} {:>6.2f} {:>6.2f} {:>5.1f}% {:>6.0f} {:>6.0f} {:>6.2f} {:>6.2f}'


	sql = "SELECT code, volume, amount FROM monitor WHERE user=?"
	res = db.conn().all(sql, [ps.user])
	print('Monitoring:', str(res))

	i, I, codes, stock = 0, 0, [], {}
	for code, volume, amount in res:
		codes.append(code)
		stock[code] = {'volume':volume, 'amount':amount, 'color':COLORS[I], 'lastVolume':0, 'lastAmount':0}
		I+=1
	
	while True:
		time.sleep(6)
		t = time.strftime("%H:%M:%S")
		if (t<'09:28:00' or (t>'11:32:00' and t<'12:58:00') or t>'15:02:00'):
			time.sleep(54)
			continue

		try:
			df = ts.get_realtime_quotes(codes)
		except:
			continue

		for r in df.values:
			open, pre_close, price, high, low, bid, ask = float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[6]), float(r[7])
			volume, amount = float(r[8])/100, float(r[9])/10000
#			b1_v, b2_v, b3_v, b4_v, b5_v = r[10], r[12], r[14], r[16], r[18]
#			b1_p, b2_p, b3_p, b4_p, b5_p = r[11], r[13], r[15], r[17], r[19]
#			a1_v, a2_v, a3_v, a4_v, a5_v = r[20], r[22], r[24], r[26], r[28]
#			a1_p, a2_p, a3_p, a4_p, a5_p = r[21], r[23], r[25], r[27], r[29]
			date, times, code = str(r[30]), str(r[31]), str(r[32])

			vc = volume - stock[code]['lastVolume']
			ac = amount - stock[code]['lastAmount']
			stock[code]['lastVolume'] = volume
			stock[code]['lastAmount'] = amount
			pc  = price - pre_close
			pcr = pc / pre_close * 100
			if vc > stock[code]['volume'] and ac > stock[code]['amount']:
				i += 1
				if i%10 == 1:
					print(Back.BLUE, header, '', Style.RESET_ALL)
				print(getattr(Fore, stock[code]['color']), pattern.format(i, times, code, price, pc, pcr, vc, ac, bid, ask), Style.RESET_ALL)
#				print('\a')
				if i%5 == 0:
					print()



if __name__ == '__main__':
	main(sys.argv[1:])
