#!/usr/bin/env python

import sys
import multiprocessing as MP
import gcbtestui
import gcbtestfs
import gcbtestnet
from time import sleep

DEBUG_MULTI_PROCESS=True

PY3 = sys.version_info[0] == 3
#if PY3:
#	from io import StringIO
#	import configparser as cfg
#else:
#	from StringIO import StringIO
#	import ConfigParser as cfg

class GCBTest():
	# mpq_main - the main queue of the program. this is what the controller (here) will use to know what is going on
	def __init__(self):
		self.mpq_main = MP.Queue() # where we, the controller, receive messages
		self.mpq_ui = MP.Queue() # messages to the children...
		self.mpq_fs = MP.Queue()
		self.mpq_net = MP.Queue()
		self.mpt_ui = MP.Process( target=gcbtestui.GCBTestUI, args=(self.mpq_main, self.mpq_ui) )#all processes will share the main queue
		self.mpt_ui.start();
		# TODO should we also call .join() here to not have memory leaks?
		self.mpt_fs = MP.Process( target=gcbtestfs.GCBTestFS, args=(self.mpq_main, self.mpq_fs) )
		self.mpt_fs.start();
		self.mpt_net = MP.Process( target=gcbtestnet.GCBTestNET, args=(self.mpq_main, self.mpq_net) )
		self.mpt_net.start();
		# when all is started up, kick our main loop
		return self.check_queue()

	x = 1
	def check_queue(self):
		self.x += 1
		if self.x == 5:
			self.mpq_ui.put('draw A')
		#
		if self.x == 10:
			self.mpq_fs.put('test 1')
			self.mpq_fs.put('test 2')
		#
		if DEBUG_MULTI_PROCESS:
			print( 'CONTROL: check' )
		if not self.mpq_main.empty(): #work around retarded Queue vs multiprocess namespace for exceptions
			msg = self.mpq_main.get(0) # todo handle a list in case we have arguments. or maybe another queue for data?
			# Check contents of message and do what it says
			if DEBUG_MULTI_PROCESS:
				print( 'CONTROL: ', msg )
			if msg == 'UI quit':
				self.do_polite_quit()
		else:
			pass
		#
		# TODO: check if all threads are still up
		sleep(.5)
		return self.check_queue()
	
	def do_polite_quit(self):
		# TODO: be polite
		self.mpt_ui.terminate()
		self.mpt_fs.terminate()
		self.mpt_net.terminate()
		sys.exit()


if __name__ == '__main__':
        theclass = GCBTest()
