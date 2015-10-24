import re, os, json, logging
from sys import argv, exit
from time import time, sleep

from core.api import MPServerAPI
from core.video_pad import MPVideoPad
from core.vars import UNPLAYABLE_FILES, BASE_DIR, DEFAULT_TELEPHONE_GPIO

ENTER_KEY = 4
CONTROL_KEY = 5

ANY_BUTTON = [3, 5, 10, 11]

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
						'gather' : [CONTROL_KEY, ENTER_KEY] if i not in ANY_BUTTON else DEFAULT_TELEPHONE_GPIO
					})
			
			break

		self.conf['d_files']['vid'] = {
			'log' : self.conf['d_files']['module']['log'],
			'pid' : os.path.join(BASE_DIR, ".monitor", "video_pad.pid.txt")
		}

		MPVideoPad.__init__(self)

		logging.basicConfig(filename=self.conf['d_files']['module']['log'], level=logging.DEBUG)

	def route_next(self, route_idx=0):
		route = self.audio_routes[route_idx]

		choice = self.prompt(route['wav'], release_keys=route['gather'])
		if route_idx != len(self.audio_routes) - 1:
			return self.route_next(route_idx=(route_idx + 1))

		else:
			if choice == CONTROL_KEY:
				terminus = "15.YesAdviceEnd.wav"
			elif choice == ENTER_KEY:
				terminus = "16.NoAdviceEnd.wav"

			return self.say(os.path.join(self.conf['media_dir'], "prompts", terminus))

		return False

	def reset_for_call(self):
		super(IsHeCheating, self).reset_for_call()

		for video_mapping in self.video_mappings:
			self.db.delete("video_%s" % video_mapping.index)

	def on_hang_up(self):
		self.stop_video_pad()
		return super(IsHeCheating, self).on_hang_up()

	def run_script(self):
		super(IsHeCheating, self).run_script()
		self.play_video("is_he_cheating.mp4", with_extras={"loop" : ""})
		self.route_next()

if __name__ == "__main__":
	res = False
	ihc = IsHeCheating()

	if argv[1] in ['--stop', '--restart']:
		res = ihc.stop()
		sleep(5)

	if argv[1] in ['--start', '--restart']:
		res = ihc.start()

	exit(0 if res else -1)

