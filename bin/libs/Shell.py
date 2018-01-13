#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Shell:

	def __init__(self, login=None):
		self.login = login
	
	def exit(self, comms=[], paras={}):
		exit()
	
	def buy(self, comms, paras):
		from libs import trade
		trade.buy(comms, paras, self.login)

	def sale(self, comms, paras):
		from libs import trade
		trade.sale(comms, paras, self.login)

	def show(self, comms, paras):
		from libs import trade
		trade.show(comms, paras, self.login)

	def help(self, comms, paras):
		print('''
buy code price volumns [-d date] [-m message]
show [code] [-d start_date, end_date]
		''')

