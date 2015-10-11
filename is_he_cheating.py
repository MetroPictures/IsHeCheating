import random, os, json, logging
from sys import argv, exit
from time import time, sleep

from core.api import MPServerAPI
from core.vars import DEFAULT_TELEPHONE_GPIO

KEY_MAP = {
	'demo_main_menu' : [
		(3, 'demo_first_choice'),
		(4, 'demo_second_choice'),
		(5, 'demo_third_choice')
	],
	'demo_first_choice' : [
		(3, 'demo_fourth_choice'),
		(4, 'demo_main_menu')
	],
	'demo_second_choice' : [
		(3, 'demo_main_menu'),
		(4, 'demo_fourth_choice')
	],
	'demo_third_choice' : [
		(3, 'demo_main_menu'),
		(4, 'demo_fourth_choice')
	],
	'demo_fourth_choice' : [
		(3, 'demo_main_menu')
	]
}

class IsHeCheating(MPServerAPI):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.gpio_mappings = DEFAULT_TELEPHONE_GPIO
		self.key_mappings = KEY_MAP

		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def run_script(self):
		super(IsHeCheating, self).run_script()
		self.route_loop('demo_main_menu')

if __name__ == "__main__":
	res = False
	ihc = IsHeCheating()

	if argv[1] in ['--stop', '--restart']:
		res = ihc.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = ihc.start()

	exit(0 if res else -1)

