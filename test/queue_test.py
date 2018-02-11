#/usr/bin/env python


import queue
import threading
import time
import random


q = queue.Queue(0)
NUM_WORKERS = 3


class MyThread(threading.Thread):

	def __init__(self, input, worktype):
		self._jobq = input
		self._work_type = worktype
		threading.Thread.__init__(self)

	def run(self):
		while True:
			if self._jobq.qsize() > 0:
				self._process_job(self._jobq.get(), self._work_type)
			else:break


	def _process_job(self, job, worktype):
		doJob(job, worktype)


def doJob(job, worktype):
	time.sleep(random.random() * 3)
	print('doing', job, 'worktype', worktype)


if __name__ == '__main__':
	print('begin...')
	for i in range(NUM_WORKERS * 2):
		q.put(i)

	print('job qsize:', q.qsize())

	for x in range(NUM_WORKERS):
		MyThread(q, x).start()
