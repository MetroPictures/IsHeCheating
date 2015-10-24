import re, os, json, logging
from sys import argv, exit
from time import time, sleep

from core.api import MPServerAPI
from core.video_pad import MPVideoPad
from core.vars import UNPLAYABLE_FILES, BASE_DIR

ENTER_KEY = 4
CONTROL_KEY = 5

class IsHeCheating(MPServerAPI, MPVideoPad):
	def __init__(self):
		MPServerAPI.__init__(self)

		self.audio_routes = []

		def sort_by_num(file_name):
			return [int(n) if n.isdigit() else n for n in re.split('(\d+)', file_name)]

		for r, _, files in os.walk(os.path.join(self.conf['media_dir'], "prompts")):
			files = [f for f in files if f not in UNPLAYABLE_FILES]
			files.sort(key=sort_by_num)

			for i, prompt in enumerate(files):
				if re.match(r'\d+\.Question.*\.wav$', prompt) or prompt == "1.IsHeCheatingMenu.wav":
					self.audio_routes.append({
						'wav' : os.path.join(r, prompt),
						'gather' : xrange(6) if i != 13 else [CONTROL_KEY, ENTER_KEY]
					})
			
			break

		print self.audio_routes

		self.conf['d_files']['vid'] = {
			'log' : self.conf['d_files']['module']['log'],
			'pid' : os.path.join(BASE_DIR, ".monitor", "video_pad.pid.txt")
		}

		MPVideoPad.__init__(self)

		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def route_next(self, route_idx=0):
		route = self.audio_routes[route_idx]

		choice = self.gather(route['wav'], route['gather'])
		if route_idx != len(self.audio_routes) - 1:
			return self.route_next(route_idx=(route_idx + 1))

		else:
			if choice == CONTROL_KEY:
				terminus = "15. YesAdviceEnd.wav"
			elif choice == ENTER_KEY:
				terminus = "16. NoAdviceEnd.wav"

			return self.say(terminus)

		return False

	def press(self, key):
		logging.debug("(press overridden.)")

		try:
			return self.route_next()
		except Exception as e:
			logging.error("Could not play next route (%d)" % int(key))

		return False

	def run_script(self):
		super(IsHeCheating, self).run_script()
		self.play_video("VID_20140815_143633.mp4")
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

