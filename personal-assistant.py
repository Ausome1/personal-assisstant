####
# Personal Assistant Bot
#
# @Author: Ausome1
####

import speech_recognition as sr
import pyautogui
import webbrowser
from datetime import datetime
import pyttsx3
import os
import urllib.parse
import random

WHAT_SHOULD_I_CALL_YOU = "Master"
BOT_NAME = "Jeannie"
VOICE = 1 # 0 for male, 1 for female

listOfCommands = {
	"cancelcommand" : ["cancel", "cancel request", "cancel command"],
	"weather" : ["show weather", "weather report", "show me the weather", "show weather report", "show me the weather report"],
	"screenshot" : ["take screenshot", "take a screenshot"],
	"availablecommands" : ["help", "available commands", "list of commands"],
	"checkmarx1" : ["open check marks one"],
	"checkmarx" : ["open check marks"],
	"commandprompt" : ["open command prompt"],
	"powershell" : ["open powershell"],
	"firefox" : ["open firefox"],
	"chrome" : ["open chrome"],
	"mood" : ["how are you feeling"],
	"closeapp" : ["exit", "go to sleep", "shut down"],
	"timer" : ["set timer"],
	"multicommandmode" : ["red alert"],
	"exitmulticommandmode" : ["all clear"],
	"music" : ["play music"]
};

availableMusic = ["coding", "jazz", "dio"]

CommandMode = False;
MultiCommandMode = False;
ListeningForWeatherCity = False;
ListeningForMusic = False

def listen_for_command():
	global CommandMode
	global MultiCommandMode
	global ListeningForWeatherCity
	global ListeningForMusic

	recognizer = sr.Recognizer()

	with sr.Microphone() as source:
		if ListeningForWeatherCity:
			print("Listening for city weather choice...")
		elif ListeningForMusic:
			print("Listening for music choice...")
		elif MultiCommandMode:
			print("Listening for multi commands...")
		elif CommandMode:
			print("Listening for command...")
		else:
			print("Listening for you to call on me to assist you...")
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)

	try:
		command = recognizer.recognize_google(audio)
		print("You said:", command)
		return command.lower()
	except sr.UnknownValueError:
		print("Could not understand audio. Please try again.")
		return None
	except sr.RequestError:
		print("Unable to access the Google Speech Recognition API.")
		return None

def respond(response_text):
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[VOICE].id)
	engine.say(response_text)
	engine.runAndWait()

def main():
	global CommandMode
	global MultiCommandMode
	global ListeningForWeatherCity
	global ListeningForMusic

	while True:
		command = listen_for_command()
		trigger = (f"hey {BOT_NAME}").lower();

		if CommandMode == False and (command and trigger in command):
			responses = ["How May I Be Of Assistance?", "Is There Something I Can Do For You?", "What Can I Do For You?", 
						 "How May I Assist You?", "Would You Like Me To Help You With Something?"]
			respond(random.choice(responses))
			CommandMode = True
		elif (MultiCommandMode or CommandMode) and command:
			### Cancel Commands ###
			if any(c in command for c in listOfCommands['cancelcommand']):
				respond("OK, I'll go back to what I was doing.")
				CommandMode = False;
				MultiCommandMode = False;
				ListeningForWeatherCity = False;
				ListeningForMusic = False

			### Show Weather ###
			elif ListeningForWeatherCity:
				respond(f"Showing you the weather for {command}")
				ListeningForWeatherCity = False
				city = urllib.parse.quote(command)
				os.system(f"start /max cmd /k curl wttr.in/{city}")
			elif any(c in command for c in listOfCommands['weather']):
				respond("What city do you want the weather for?")
				ListeningForWeatherCity = True

			### Play Music ###
			elif ListeningForMusic:
				validChoice = True			

				if any(c in command for c in ['coding']):
					webbrowser.open("https://www.youtube.com/watch?v=ZcG2tmRxh_c&autoplay=1")
				elif any(c in command for c in ['jazz']):
					webbrowser.open("https://www.youtube.com/watch?v=6UMHt6Yr2bo&autoplay=1")
				elif any(c in command for c in ['dio']):
					webbrowser.open("https://www.youtube.com/watch?v=rjCBV6o_DSE&autoplay=1")
				else:
					availableMusic[-1] = f"and {availableMusic[-1]}"
					respond(f"I don't know what to do with your choice. Please choose again. Music available. {','.join(availableMusic)}.")
					validChoice = False

				if (validChoice):
					ListeningForMusic = False
			elif any(c in command for c in listOfCommands['music']):
				availableMusic[-1] = f"and {availableMusic[-1]}"
				respond(f"The music available is {','.join(availableMusic)}.")
				ListeningForMusic = True

			### List Commands ###
			elif any(c in command for c in listOfCommands['availablecommands']):
				respond("Let me get you a list of the commands I know.")
				knownCommands = ""
				desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
				for key, value in listOfCommands.items():
				 	for val in value:
				 		knownCommands += val+'\n'
				with open(f"{desktop}/commands.txt", "w") as f:
				  	f.write(knownCommands)
				os.system(f"notepad {desktop}/commands.txt")

			### Take a Screenshot ###
			elif any(c in command for c in listOfCommands['screenshot']):
				pyautogui.screenshot("screenshot_" + str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".png")
				respond("I took a screenshot for you.")

			### Open CMD Prompt ###
			elif any(c in command for c in listOfCommands['commandprompt']):
				respond("Opening a command window for you.")
				os.system('start cmd')

			### Open Powershell Window ###
			elif any(c in command for c in listOfCommands['powershell']):
				respond("Opening powershell for you.")
				os.system('start powershell')

			### Open Firefox ###
			elif any(c in command for c in listOfCommands['firefox']):
				respond("Opening Firefox for you.")
				os.system("start firefox")

			### Open Chrome ###
			elif any(c in command for c in listOfCommands['chrome']):
				respond("Opening Chrome for you.")
				os.system("start chrome")

			### How is your assisstant feeling? ###
			elif any(c in command for c in listOfCommands['mood']):
				respond("Let me show you how I'm feeling.")
				os.system("start chrome https://www.youtube.com/watch?v=QDia3e12czc&autoplay=1")

			### Close the personal assisstant ###
			elif any(c in command for c in listOfCommands['closeapp']):
				respond("Goodbye, " + WHAT_SHOULD_I_CALL_YOU)
				break

			### Open a Timer ###
			elif any(c in command for c in listOfCommands['timer']):
				respond("Let me get you a timer.")
				os.system("start ms-clock:")

			### Enter Multi-Command Mode ###
			elif any (c in command for c in listOfCommands['multicommandmode']):
				respond("Entering multi command mode.")
				MultiCommandMode = True

			### Exit Multi-Command Mode ###
			elif any (c in command for c in listOfCommands['exitmulticommandmode']):
				respond("Exiting multi command mode")
				MultiCommandMode = False

			### Rut Roh Raggy, assistant doesn't know that command. ###
			else:
				respond("Sorry, I'm not sure how to handle that command.")

			if not MultiCommandMode and not any([ListeningForWeatherCity, ListeningForMusic]):
				CommandMode = False

if __name__ == "__main__":
	respond("Hello " + WHAT_SHOULD_I_CALL_YOU + ", how can I assist you today?")
	main()