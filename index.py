import time
import sys

user_dir = sys.argv[1]
sys.path.insert(0, f"{user_dir}/Gamepad")

import Gamepad
import nxbt

import xb_like_conversion
import better_button

# Start the gamepad service
gamepadType = Gamepad.XboxSeries # close enough :3
gamepad_id = 1

# Start the NXBT service
nx = nxbt.Nxbt()

# Create a Pro Controller and wait for it to connect
controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
print("Waiting for connection(s)...")

nx.wait_for_connection(controller_index)
nx.press_buttons(controller_index, [nxbt.Buttons.B])

print("NXBT Connected")
print("Checking controller status...")

if not Gamepad.available(gamepad_id):
  print('Please connect your gamepad.')
  while not Gamepad.available():
    time.sleep(1.0)

print("Connected.")
gamepad = gamepadType(gamepad_id)

print("Initializing 'better_button'... (thanks, et al.)")
bb = better_button.BetterButton(True, controller_index, nx)

# FIXME(?): We using pulling! So FUCK OFF.
# FIXME: This is also kinda flawed. Afaik NXBT doesn't have "hold down til I say so" support.



while gamepad.isConnected():
  eventType, control, value = gamepad.getNextEvent()

  if eventType == "BUTTON":
    print("BUTTON BITCH ASS: " + str(control))
    match control:
      case "A":
        if value:
          bb.key_down([nxbt.Buttons.A])
        else:
          bb.key_up([nxbt.Buttons.A])
      
      case "B":
        if value:
          bb.key_down([nxbt.Buttons.B])
        else:
          bb.key_up([nxbt.Buttons.B])
      
      case "X":
        if value:
          bb.key_down([nxbt.Buttons.X])
        else:
          bb.key_up([nxbt.Buttons.X])
      
      case "Y":
        if value:
          bb.key_down([nxbt.Buttons.Y])
        else:
          bb.key_up([nxbt.Buttons.Y])

      case "LT":
        if value:
          bb.key_down([nxbt.Buttons.L])
        else:
          bb.key_up([nxbt.Buttons.L])

      case "RT":
        if value:
          bb.key_down([nxbt.Buttons.R])
        else:
          bb.key_up([nxbt.Buttons.R])
      
      case "HOME":
        if value:
          bb.key_down([nxbt.Buttons.HOME])
        else:
          bb.key_up([nxbt.Buttons.HOME])

      case "SHARE":
        if value:
          bb.key_down([nxbt.Buttons.MINUS])
        else:
          bb.key_up([nxbt.Buttons.MINUS])
      
      case "MENU":
        if value:
          bb.key_down([nxbt.Buttons.PLUS])
        else:
          bb.key_up([nxbt.Buttons.PLUS])

      case "LASB":
        if value:
          bb.key_down([nxbt.Buttons.L_STICK_PRESS])
        else:
          bb.key_up([nxbt.Buttons.L_STICK_PRESS])

      case "RASB":
        if value:
          bb.key_down([nxbt.Buttons.R_STICK_PRESS])
        else:
          bb.key_up([nxbt.Buttons.R_STICK_PRESS])

      case "LB":
        if value:
          bb.key_down([nxbt.Buttons.L])
        else:
          bb.key_up([nxbt.Buttons.L])

      case "RB":
        if value:
          bb.key_down([nxbt.Buttons.R])
        else:
          bb.key_up([nxbt.Buttons.R])
              
  elif eventType == "AXIS":
    # TODO: implement
    print('YO BITCH ASS: ' + str(control))
    
    match control:
      case "DPAD -Y":
        if value == -1:
          bb.key_down([nxbt.Buttons.DPAD_UP])
        elif value == 1:
          bb.key_down([nxbt.Buttons.DPAD_DOWN])
        elif value == 0:
          bb.key_up([nxbt.Buttons.DPAD_UP, nxbt.Buttons.DPAD_DOWN])
      
      case "DPAD -X":
        if value == -1:
          bb.key_down([nxbt.Buttons.DPAD_LEFT])
        elif value == 1:
          bb.key_down([nxbt.Buttons.DPAD_RIGHT])
        elif value == 0:
          bb.key_up([nxbt.Buttons.DPAD_LEFT, nxbt.Buttons.DPAD_RIGHT])

      case "LT":
        better_value = xb_like_conversion.convert_xb_trigger(value)

        if better_value > 35:
          bb.key_down([nxbt.Buttons.ZL])
        elif better_value < 34:
          bb.key_up([nxbt.Buttons.ZL])
      
      case "RT":
        better_value = xb_like_conversion.convert_xb_trigger(value)

        if better_value > 35:
          bb.key_down([nxbt.Buttons.ZR])
        elif better_value < 34:
          bb.key_up([nxbt.Buttons.ZR])
    
      case "LAS -X":
        print("TODO")

      case "LAS -Y":
        print("TODO")
      
      case "RAS -X":
        print("TODO")
      
      case "RAS -Y":
        print("TODO")