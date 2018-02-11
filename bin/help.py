#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05


HELPS = {}
HELPS['main'] = '''
commands:                       [main]
-----------------------------------------------
 jbm       基本面        *qsx    趋势线
 ycx       阳穿线        *ljb    量价比
 qsx       趋势线        *mmp    买卖盘
 xyx       下影线
 '''


HELPS['jbm'] = '''
parameters:                     [jbm]
----------------------------------------
 pe          市盈率
 pb          市净率
 esp         每股收益
 bvps        每股净资产
 industry    所属行业
 area        所属地区
 totals      总股本(亿)
 outstanding 流通股本(亿)
 gpr         毛利率(%)
 npr         净利率(%)
 holders     股东人数'''


HELPS['ycx'] = '''
parameters:                      [ycx]
----------------------------------------------------------
 ma          移动平均线    日线穿过的平均线，可多选
 date        日期          默认值为最新日期'''


HELPS['qsx'] = '''
parameters:
----------------------------------------------------------
 n             进行趋势分析的最大日线数量
 nlow          最低价出现的日期距今的自然天数区间
 grow          最新价相对于最低价增长的区间
 lhr           最低价相对于最高价比值的区间'''


def main(argString='main'):
	print(HELPS.get(argString))


terms = {
	'ndays':	['360',		'日线数量'],
	'nlow':		['0,30',	'最低'],
	'grow':		['',		''],
}
