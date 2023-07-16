import time
import sys

sys.path.insert(0, "./Gamepad")

import Gamepad
import nxbt

from config import gamepad_type, gamepad_id, use_nintendo_layout
import xb_like_conversion
import better_button

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
gamepad = gamepad_type(gamepad_id)

print("Initializing 'better_button'... (thanks, et al.)")
bb = better_button.BetterButton(True, controller_index, nx)

val_conv_btn = [bb.key_up, bb.key_down]

# NOT A FIXME: Pulling doesn't have any noticeable impact on performance on my machine.
while gamepad.isConnected():
  eventType, control, value = gamepad.getNextEvent()

  if eventType == "BUTTON":
    match control:
      case "A":
        val_conv_btn[value]([nxbt.Buttons.A])
      
      case "B":
        val_conv_btn[value]([nxbt.Buttons.B])
      
      case "X":
        val_conv_btn[value]([nxbt.Buttons.X])
      
      case "Y":
        val_conv_btn[value]([nxbt.Buttons.Y])

      # FIXME: WHAT is this used for?
      case "LT":
        val_conv_btn[value]([nxbt.Buttons.L])

      case "RT":
        val_conv_btn[value]([nxbt.Buttons.R])
      
      case "HOME":
        val_conv_btn[value]([nxbt.Buttons.HOME])
      
      case "SHARE":
        val_conv_btn[value]([nxbt.Buttons.MINUS])
      
      case "MENU":
        val_conv_btn[value]([nxbt.Buttons.PLUS])

      case "LASB":
        val_conv_btn[value]([nxbt.Buttons.L_STICK_PRESS])

      case "RASB":
        val_conv_btn[value]([nxbt.Buttons.R_STICK_PRESS])

      case "LB":
        val_conv_btn[value]([nxbt.Buttons.L])

      case "RB":
        val_conv_btn[value]([nxbt.Buttons.R])
              
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