import sys
sys.path.insert(0, "./Gamepad")

import Gamepad

# Start the gamepad service
gamepadType = Gamepad.XboxSeries # close enough :3
gamepad_id = 1

print("Checking controller status...")

if not Gamepad.available(gamepad_id):
  print('Please connect your gamepad.')
  while not Gamepad.available():
    time.sleep(1.0)

print("Connected.")
gamepad = gamepadType(gamepad_id)

while gamepad.isConnected():
  eventType, control, value = gamepad.getNextEvent()

  print(f"{eventType}: {str(control)} = {str(value)}")