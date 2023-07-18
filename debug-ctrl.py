import time

from config import gamepad_type, gamepad_id
import sys
sys.path.insert(0, "./libs/Gamepad")

import Gamepad

print("Checking controller status...")

if not Gamepad.available(gamepad_id):
  print('Please connect your gamepad.')
  while not Gamepad.available():
    time.sleep(1.0)

print("Connected.")
gamepad = gamepad_type(gamepad_id)

while gamepad.isConnected():
  eventType, control, value = gamepad.getNextEvent()

  print(f"{eventType}: {str(control)} = {str(value)}")