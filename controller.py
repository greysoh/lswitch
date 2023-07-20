import math
import time
import sys
sys.path.insert(0, "./libs/Gamepad")

import Gamepad
import nxbt

from config import gamepad_type, gamepad_id, macro_kdl_path
from libs.xb_like_conversion import convert_xb_trigger
from libs.macro_agent import MacroAgentFromFile
from libs.better_button import BetterButton

# Start the NXBT service
nx = nxbt.Nxbt()

# Create a Pro Controller and wait for it to connect
controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
print("Waiting for connection(s)...")

nx.wait_for_connection(controller_index)
 
print("NXBT Connected")
print("Checking controller status...")

if not Gamepad.available(gamepad_id):
  print('Please connect your gamepad.')
  while not Gamepad.available():
    time.sleep(1.0)

print("Connected.")
gamepad = gamepad_type(gamepad_id)

print("Initializing components...")

bb = BetterButton(True, controller_index, nx)
val_conv_btn = [bb.key_up, bb.key_down]

ma = MacroAgentFromFile(macro_kdl_path)

# FIXME: CLEAN UP THIS SHIT
def A_button(value):
  val_conv_btn[value]([nxbt.Buttons.A])

def B_button(value):
  val_conv_btn[value]([nxbt.Buttons.B])

def X_button(value):
  val_conv_btn[value]([nxbt.Buttons.X])

def Y_button(value):
  val_conv_btn[value]([nxbt.Buttons.Y])

def HOME_button(value):
  val_conv_btn[value]([nxbt.Buttons.HOME])

def SHARE_button(value):
  val_conv_btn[value]([nxbt.Buttons.MINUS])

def MENU_button(value):
  val_conv_btn[value]([nxbt.Buttons.PLUS])

def LASB_button(value):
  val_conv_btn[value]([nxbt.Buttons.L_STICK_PRESS])

def RASB_button(value):
  val_conv_btn[value]([nxbt.Buttons.R_STICK_PRESS])

def LB_button(value):
  val_conv_btn[value]([nxbt.Buttons.L])

def RB_button(value):
  val_conv_btn[value]([nxbt.Buttons.R])

def DPADY_trigger(value):
  if value == -1:
    bb.key_down([nxbt.Buttons.DPAD_UP])
  elif value == 1:
    bb.key_down([nxbt.Buttons.DPAD_DOWN])
  elif value == 0:
    bb.key_up([nxbt.Buttons.DPAD_UP, nxbt.Buttons.DPAD_DOWN])

def DPADX_trigger(value):
  if value == -1:
    bb.key_down([nxbt.Buttons.DPAD_LEFT])
  elif value == 1:
    bb.key_down([nxbt.Buttons.DPAD_RIGHT])
  elif value == 0:
    bb.key_up([nxbt.Buttons.DPAD_LEFT, nxbt.Buttons.DPAD_RIGHT])

def LT_trigger(value):
  better_value = convert_xb_trigger(value)

  if better_value > 35:
    bb.key_down([nxbt.Buttons.ZL])
  elif better_value < 34:
    bb.key_up([nxbt.Buttons.ZL])

def RT_trigger(value):
  better_value = convert_xb_trigger(value)

  if better_value > 35:
    bb.key_down([nxbt.Buttons.ZR])
  elif better_value < 34:
    bb.key_up([nxbt.Buttons.ZR])
    
def LASX_trigger(value):
  better_value = math.floor(value*100)
  bb.tilt_stick(nxbt.Sticks.LEFT_STICK, better_value, None)

def LASY_trigger(value):
  better_value = math.floor(value*100)
  bb.tilt_stick(nxbt.Sticks.LEFT_STICK, None, -better_value)

def RASX_trigger(value):
  better_value = math.floor(value*100)
  print("rasx: " + str(better_value))
  
  bb.tilt_stick(nxbt.Sticks.RIGHT_STICK, better_value, None)

def RASY_trigger(value):
  better_value = math.floor(value*100)
  print("rasy: " + str(better_value))
  
  bb.tilt_stick(nxbt.Sticks.RIGHT_STICK, None, -better_value)

# magic time.
gamepad.startBackgroundUpdates()

gamepad.addButtonChangedHandler("A", A_button)
gamepad.addButtonChangedHandler("B", B_button)
gamepad.addButtonChangedHandler("X", X_button)
gamepad.addButtonChangedHandler("Y", Y_button)
gamepad.addButtonChangedHandler("HOME", HOME_button)
gamepad.addButtonChangedHandler("SHARE", SHARE_button)
gamepad.addButtonChangedHandler("MENU", MENU_button)
gamepad.addButtonChangedHandler("LASB", LASB_button)
gamepad.addButtonChangedHandler("RASB", RASB_button)
gamepad.addButtonChangedHandler("LB", LB_button)
gamepad.addButtonChangedHandler("RB", RB_button)

gamepad.addAxisMovedHandler("DPAD -Y", DPADY_trigger)
gamepad.addAxisMovedHandler("DPAD -X", DPADX_trigger)
gamepad.addAxisMovedHandler("LT", LT_trigger)
gamepad.addAxisMovedHandler("RT", RT_trigger)
gamepad.addAxisMovedHandler("LAS -X", LASX_trigger)
gamepad.addAxisMovedHandler("LAS -Y", LASY_trigger)
gamepad.addAxisMovedHandler("RAS -X", RASX_trigger)
gamepad.addAxisMovedHandler("RAS -Y", RASY_trigger)

#    if macro and value:
#      ma.execute_macro(macro, bb)
#      continue

print("Initialized.")