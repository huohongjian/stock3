#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22


class LinkedDict():

	def __init__(self, maxLength=10):
		self.maxLength = maxLength
		self.length = 0
		self.buffer = {}
		self.head = None
		self.last = None


	def clear(self):
		self.buffer = {}


	def size(self):
		return self.length


	def has(self, key):
		return key in self.buffer


	def isHead(self, key):
		return key == self.head


	def isLast(self, key):
		return key == self.last


	def remove(self, key):
		if self.has(key):
			prevKey = self.buffer.get(key).get('prev')
			nextKey = self.buffer.get(key).get('next')
			if self.isHead(key):
				self.head = nextKey
				self.buffer[nextKey]['prev'] = None
			elif self.isLast(key):
				self.last = prevKey
				self.buffer[prevKey]['next'] = None
			else:
				self.buff[prevKey]['next'] = nextKey
				self.buff[nextKey]['prev'] = prevKey

			del self.buffer[key]
			self.length -= 1


	def add(self, key, data): 
		if self.length > self.maxLength:
			self.remove(self.head)

		node = {
			'data': data,
			'prev': self.last,
			'next': None,
		}
		if self.head is None:
			self.head = key
		else:
			self.buffer[self.last]['next'] = key
		
		self.last = key
		self.buffer[key] = node
		self.length += 1


	def get(self, key):
		if self.has(key):
			node = self.buffer[key]
			if not self.isLast(key):
				prevKey = node.get('prev')
				nextKey = node.get('next')
				if self.isHead(key):
					self.head = nextKey
					self.buffer[nextKey]['prev'] = None
				else:
					self.buffer[prevKey]['next'] = nextKey
					self.buffer[nextKey]['prev'] = prevKey

				self.buffer[self.last]['next'] = key
				node['prev'] = self.last
				node['next'] = None
				self.last = key
			print('get from cache')
			return node.get('data')


	def getHead(self):
		return self.get(self.head)


	def getLast(self):
		return self.get(self.last)
