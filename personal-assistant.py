####
# Personal Assistant Bot v.2
#
# @Author: Ausome1
####

import keyboard
import sys
import threading
import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser
import os
import urllib.parse
import random
import yaml
from neuralintents import BasicAssistant
from datetime import datetime

class Assistant:
	def __init__(self):
		self.multi_command_mode = False
		self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

		with open("config.yaml", "r") as f:
			self.config = yaml.load(f, Loader=yaml.FullLoader)

		self.recognizer = sr.Recognizer()
		self.speaker = pyttsx3.init()
		self.speaker.setProperty("rate", 150)
		voices = self.speaker.getProperty('voices')
		self.speaker.setProperty('voice', voices[self.config['voice']].id)

		# The keys mustmatch the tags in the intent.json file.
		self.assistant = BasicAssistant("intents.json", model_name="intent_model", method_mappings={	
			"open_cmd_prompt": self._open_cmd_prompt,
			"powershell": self._open_powershell,
			"firefox": self._open_firefox,
			"chrome": self._open_chrome,
			"weather": self._show_weather,
			"play_music": self._play_music,
			"screenshot": self._take_a_screenshot,
			"feelings": self._feelings,
			"timer": self._open_timer,
			"multi_command": self._enter_multi_command_mode,
			"exit_multi_command": self._exit_multi_command_mode,
			"shut_down": self._shut_down
		})
		
		if os.path.exists('intent_model.keras'):
		    self.assistant.load_model()
		else:
		    self.assistant.fit_model(epochs=50)
		    self.assistant.save_model()

		self.root = tk.Tk()
		self.root.title(self.config["botname"])
		self.root.background = "grey"
		self.gui = tk.Label(text="👽", font=(self.config["font"], 180, "bold"), bg="grey", fg="black")
		self.gui.pack()

		server_thread = threading.Thread(target=self._run_assistant)
		server_thread.daemon = True
		server_thread.start()

		self.root.mainloop()

	def _run_assistant(self):
		while True:
			try:
				with sr.Microphone() as source:
					self.recognizer.adjust_for_ambient_noise(source)
					
					if not self.multi_command_mode:
						print("Listening for you to call on me to assist you...")
						command = self._listen_for_command(source)

					if self.multi_command_mode or (command is not None and self._trigger(command)):
						self._greeting()
						command = self._listen_for_command(source)

						if command is not None:
							response = self.assistant.process_input(command)
							if response is not None:
								self._respond(response)

						if not self.multi_command_mode:
							self.gui.config(fg="black")
			except Exception as e:
				self.gui.config(fg="red")
				self._respond("You done messed up A A Ron.")
				print(e)
				continue

	def _trigger(self, command):
		trigger = (f"hey {self.config['botname']}").lower()
		if (trigger in command):
			return True
		return False

	def _hotkey(self):
		try:
			if self.config["hotkey_trigger"]["enabled"]:
				if not keyboard.is_pressed(self.config["hotkey_trigger"]["key"]):
					return False
			return True
		except Exception as e:
			print(e)

	def _listen_for_command(self, source):
		if self._hotkey():	
			audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=8)
			try:
				command = self.recognizer.recognize_google(audio)
				print(f"You said: {command}")
				return command.lower()
			except sr.UnknownValueError:
				print("Could not understand audio. Please try again.")
				return None
			except sr.RequestError:
				print("Unable to access the Google Speech Recognition API.")
				return None

	def _respond(self, command):
		self.speaker.say(command)
		self.speaker.runAndWait()

	def _greeting(self):
		responses = ["How May I Be Of Assistance?", "What Can I Do For You?", "How May I Assist You?"]
		print("Listening for command...")
		response = random.choice(responses)
		self.gui.config(fg="green")					
		self._respond(random.choice(responses))

	def _shut_down(self):
		self._respond("Shutting down.")
		self.speaker.stop()
		self.root.destroy()
		sys.exit(0)

	def _open_cmd_prompt(self):
		os.system('start cmd')

	def _open_powershell(self):
		os.system('start powershell')

	def _open_firefox(self):
		os.system("start firefox")

	def _open_chrome(self):
		os.system("start chrome")

	def _show_weather(self):
		self._respond("What city do you want the weather for?")

		with sr.Microphone() as source:
			self.recognizer.adjust_for_ambient_noise(source)
			command = self._listen_for_command(source)

			if command is not None:
				self._respond(f"Showing you the weather for {command}")
				city = urllib.parse.quote(command)
				os.system(f"start /max cmd /k curl wttr.in/{city}")

	def _play_music(self):
		availableMusic = ["coding", "jazz", "dio"]
		availableMusic[-1] = f"and {availableMusic[-1]}"
		self._respond(f"The music I have available to play is {','.join(availableMusic)}.")
		validChoice = False

		while not validChoice:
			with sr.Microphone() as source:
				self.recognizer.adjust_for_ambient_noise(source)
				command = self._listen_for_command(source)

				if any(c in command for c in ['coding']):
					webbrowser.open("https://www.youtube.com/watch?v=ZcG2tmRxh_c&autoplay=1")
					validChoice = True
				elif any(c in command for c in ['jazz']):
					webbrowser.open("https://www.youtube.com/watch?v=6UMHt6Yr2bo&autoplay=1")
					validChoice = True
				elif any(c in command for c in ['dio']):
					webbrowser.open("https://www.youtube.com/watch?v=rjCBV6o_DSE&list=PLBzBwYhHpqLIOsFEV9k-X2N9G3GJPoPpQ&autoplay=1")
					validChoice = True
				else:
					availableMusic[-1] = f"and {availableMusic[-1]}"
					self._respond(f"I can't play that choice. Please choose again. The music I have available to play is {','.join(availableMusic)}.")

	def _list_commands(self):
		pass

	def _take_a_screenshot(self):
		pyautogui.screenshot(f"{self.desktop}/screenshot_" + str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".png")

	def _feelings(self):
		os.system("start chrome https://www.youtube.com/watch?v=QDia3e12czc&autoplay=1")

	def _open_timer(self):
		os.system("start ms-clock:")

	def _enter_multi_command_mode(self):
		print("Entering multi-command mode")
		self.multi_command_mode = True

	def _exit_multi_command_mode(self):
		print("Exiting multi-command mode")
		self.multi_command_mode = False

if __name__ == "__main__":
	Assistant()