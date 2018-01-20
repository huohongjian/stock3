#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

defaultOptions = {
	'sort':	 'code',
	'asc' :  'True',
	'limit': 20,
	'page':  1,
}


def merge(defaultParas, customParas):
	conditions = defaultOptions.copy()
	conditions.update(defaultParas)
	conditions.update(customParas)

	options = {
		'sort':		conditions.pop('sort'),
		'asc':		conditions.pop('asc').lower() not in ('0', 'f', 'false'),
		'limit':	int(conditions.pop('limit')),
		'page':		int(conditions.pop('page'))
	}
	return (conditions, options)


