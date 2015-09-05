#!/usr/bin/env python
import sys
import multiprocessing as MP

DEBUG_MULTI_PROCESS = True
DEBUG_TK = True

PY3 = sys.version_info[0] == 3
if PY3:
	import tkinter as tk
	#from tkinter import ttk
else:
	import Tkinter as tk
	#import ttk
	#tk.ttk = ttk #make it like py3. and hope hell won't freeze


class GCBTestUI():
	def __init__(self, mpq_output=None, mpq_input=None):
		""" assing the main multiprocess queue handler. start Tk flow """
		self.mpq_input = mpq_input
		self.mpq_output = mpq_output
		self.tk_root = tk.Tk()
		if( self.mpq_input is not None ):
			self.check_queue()
		# if queue is none, it means we are in testing mode...
		self.tk_root.mainloop()

	def check_queue(self):
		""" check the main multiprocess message queue for actions """
		if not self.mpq_input.empty(): #work around retarded Queue vs multiprocess namespace for exceptions
			msg = self.mpq_input.get(0) # todo handle a list in case we have arguments. or maybe another queue for data?
			# Check contents of message and do what it says
			if DEBUG_MULTI_PROCESS:
				print( 'UI: ', msg )
			#
			if msg == 'draw A':
				self._draw_A()
			#
		else:
			pass
		#
		if DEBUG_MULTI_PROCESS:
			print("UI check")
		#
		return self.tk_root.after(100, self.check_queue) # UI changes can wait .5 sec to be checked

	# every _draw_X method should wipe out the tk_root of anything and then start adding
	# its own widgets to draw the expected window
	def _draw_A(self):
		""" draw widgets for window A """
		if DEBUG_TK:
			print( 'UI: TK: drawing window A' )
		self.A_frm_base = tk.Frame(self.tk_root);
		self.A_frm_base.pack()
		self.A_txt_hi = tk.Label(self.A_frm_base, text='hello world')
		self.A_txt_hi.pack()
		self.A_btn_quit = tk.Button(self.A_frm_base, text='quit', command=self.send_quit)
		self.A_btn_quit.pack()
	
	def send_quit(self):
		self.mpq_output.put('UI quit')


# handy testing mode to test the several _draw_X methods.
if __name__ == '__main__':
	x = GCBTestUI();
	x._draw_A()
