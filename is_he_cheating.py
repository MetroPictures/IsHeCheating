import random, os, json, logging
from sys import argv, exit
from time import time, sleep

from core.api import MPServerAPI
from core.vars import DEFAULT_TELEPHONE_GPIO

class IsHeCheating(MPServerAPI):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.gpio_mappings = DEFAULT_TELEPHONE_GPIO
		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def run_script(self):
		super(IsHeCheating, self).run_script()

if __name__ == "__main__":
	res = False
	ihc = IsHeCheating()

	if argv[1] in ['--stop', '--restart']:
		res = ihc.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = ihc.start()

	exit(0 if res else -1)

