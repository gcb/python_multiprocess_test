#!/usr/bin/env python
import sys
import multiprocessing as MP
from time import sleep

PY3 = sys.version_info[0] == 3


class GCBTestNET():
	def __init__(self, mpq_output=None, mpq_input=None):
		""" assing the main multiprocess queue handler. """
		self.mpq_input = mpq_input
		self.mpq_output = mpq_output
		self.check_queue()

	def check_queue(self):
		""" check the main multiprocess message queue for network actions """
		# TODO check the queue
		sleep(0.1)
		self.check_queue()
