#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05


HELPS = {}
HELPS['commands'] = {
	'jbm':		'基本面',
	'my':		'我的',
}
HELPS['terms'] = {
	'pe':		'市盈率',
	'pb':		'市净率',
	'esp':		'每股收益',
	'bvps':		'每股净资产',
	'industry':	'所属行业',
	'area':		'所属地区',
	'totals':	'总股本(亿)',
	'outstanding':	'流通股本(亿)',
	'gpr':		'毛利率(%)',
	'npr':		'净利率(%)',
	'holders':	'股东人数',

}
def main(paraString):
	for k, v in HELPS.items():
		print('\n' + k + '\n' + '-'*50)
		printHelp(v)

def printHelp(values):
	for k, v in values.items():
		print(' {:15} {}'.format(k, v))


