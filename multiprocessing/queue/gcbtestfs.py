#!/usr/bin/env python
import sys
import multiprocessing as MP
from time import sleep

DEBUG_MULTI_PROCESS=True

PY3 = sys.version_info[0] == 3


class GCBTestFS():
	def __init__(self, mpq_output=None, mpq_input=None):
		""" assing the main multiprocess queue handler. """
		self.mpq_input = mpq_input
		self.mpq_output = mpq_output
		if mpq_output is not None:
			self.check_queue()
		# if arg is none, means we are in test

	def check_queue(self):
		""" check the main multiprocess message queue for local filesystem actions """
		# TODO check the queue
		if not self.mpq_input.empty(): #work around retarded Queue vs multiprocess namespace for exceptions
			msg = self.mpq_input.get(0) # todo handle a list in case we have arguments. or maybe another queue for data?
			# Check contents of message and do what it says
			if DEBUG_MULTI_PROCESS:
				print( 'FS: ', msg )
			#
			if msg == 'test 1':
				x = self.primes()
				self.mpq_output.put(['test 1 done', x]);
			#
			if msg == 'test 2':
				x = self.primes()
				self.mpq_output.put(['test 2 done', x]);
		else:
			pass
		#
		if DEBUG_MULTI_PROCESS:
			print( 'FS: check' )
		#
		sleep(.1)
		return self.check_queue()
	
	def primes(self):
		ret = []
		for p in range(2, 50000):
			for i in range(2, p):
				if p % i == 0:
					break
				#
			else:
				ret.append(p)
			#
		#
		#return ret
		return p

# handy test entry point
if __name__ == '__main__':
	x = GCBTestFS()
	print( x.primes() )
