# LSwitch
LSwitch is a 2 (counting 3 for debug apps) program suite of Switch tools:
1. `controller.py` - Controller converts any controller into a Switch Pro controller
2. `debug-ctrl.py` - Lets you view the incoming inputs of your controller
3. `desktop.py` - Lets you play switch games like a PC (wip)  
  
LSwitch currently supports Linux only. 
## Installation
You must be running Linux with Bluetooth set up using `BlueZ`.  
  
Then, run these commands:
```bash
# 0. If you haven't already, install the packages:
git clone https://github.com/greysoh/lswitch.git
# 1. Install pip packages | FIXME: better way to do this?
cat requirements.txt | xargs sudo pip install --break-system-packages
# 2. Copy the base configurations
cp config.default.py config.py
cp config.default.kdl config.kdl
# 3. Edit the base configurations to your needs. Remove the default macros unless you need them, and maybe add your own?
$EDITOR config.py
$EDITOR config.kdl
# 4. Start as root!
sudo python controller.py # or whatever you want...
```
## Python config usage
### `use_nintendo_layout`
Instead of using `ABXY`, it maps it to `BAYX` in that order. If set to false, it disables this.
#### For PS controllers
`ABXY` maps to Cross, Circle, Triangle, and Square in that order.  
  
So, if you turn on `use_nintendo_layout`, `ABXY` would map to Circle, Cross, Square, and Triangle.
### `gamepad_type`
Gamepad is the modified gamepad library originally at [this Git link](https://github.com/piborg/gamepad).  
You must specify a controller in line `gamepad_type`
  
We officially support these following controllers:
* PS4 (`Gamepad.PS4`)
* PS5 (`Gamepad.PS5`)
* Series S/X (`Gamepad.XboxSeries`)

Gamepad has support for these additional controllers (but WE don't as they are untested/not converted):
* PS3 (`Gamepad.PS3`)
* Xbox 360 (`Gamepad.Xbox360`)
* Xbox One (`Gamepad.XboxONE`)
* Steam Controller (`Gamepad.Steam`)
* ModMyPi Wireless Gamepad (`Gamepad.MMP1251`)
* WaveShare PI GameHat (`Gamepad.GameHat`)
* ipega PG-9099 (`Gamepad.PG9099`)
  
But none of these are officially validated/unified to work with our code.
### `gamepad_id`
This is used in the gamepad library mentioned above.  
  
This is the number that corresponds to the joystick API at `/dev/input/jsX`. Use the number that corresponds to your controller by trial and error and using `debug-ctrl.py`.
### `macro_kdl_path`
KDL is a Cuddly Document Language. This was chosen for simplicity. `macro_kdl_path` is the path to that file.
## Macro (KDL) docs
### `macors.keyboard`
TODO. not complete (code wise)
### `macros.controller`
The first entry (ex. `A {}`) maps to the button on YOUR controller, and not the nintendo keys.  
There are currently 4 commands:
* `press`: Toggles a key for a given time. key=`Nintendo key, ex. ZL, ZR` duration=`Time to sleep. Defaults to being in seconds.` timeScale=`Changes the scale of duration. Options are: "ms" to change it to milliseconds [OPTIONAL]`
* `key_down`: Presses a key down. key=`Nintendo key, ex. ZL, ZR`
* `sleep`: Sleeps for a given time in milliseconds. duration=`Duration in seconds`
* `key_down`: Releases a key. key=`Nintendo key, ex. ZL, ZR`  
  
Here are a full list of controller keys (based on Series S/X code in `Gampead`):
```py
self.axisNames = {
    0: 'LAS -X', #Left Analog Stick Left/Right (GOOD)
    1: 'LAS -Y', #Left Analog Stick Up/Down (GOOD)
    4: 'RAS -Y', #Right Analog Stick Left/Right (GOOD)
    3: 'RAS -X', #Right Analog Stick Up/Down (GOOD)
    5: 'RT', #Right Trigger (GOOD)
    2: 'LT', #Left Trigger (GOOD)
    6: 'DPAD -X', #D-Pad Left/Right (GOOD)
    7: 'DPAD -Y' #D-Pad Up/Down (GOOD)
}
self.buttonNames = {
    0:  'A', #A Button (GOOD)
    1:  'B', #B Button (GOOD)
    2:  'X', #X Button (GOOD)
    3:  'Y', #Y Button (GOOD)
    4:  'LB', #Left Bumper (GOOD)
    5:  'RB', #Right Bumper (GOOD)
    11: 'START', #Hamburger Button (GOOD)
    8: 'HOME', #XBOX Button (GOOD)
    9: 'LASB', #Left Analog Stick button (GOOD)
    10: 'RASB', #Right Analog Stick button (GOOD)

    6: 'SHARE',
    7: 'MENU'
}
```
Here are a full list of Nintendo keys (based on NXBT code):
```py
DIRECT_INPUT_PACKET = {
    # Sticks
    "L_STICK_PRESS": False,
    "R_STICK_PRESS": False,
    # Dpad
    "DPAD_UP": False,
    "DPAD_LEFT": False,
    "DPAD_RIGHT": False,
    "DPAD_DOWN": False,
    # Triggers
    "L": False,
    "ZL": False,
    "R": False,
    "ZR": False,
    # Joy-Con Specific Buttons
    "JCL_SR": False,
    "JCL_SL": False,
    "JCR_SR": False,
    "JCR_SL": False,
    # Meta buttons
    "PLUS": False,
    "MINUS": False,
    "HOME": False,
    "CAPTURE": False,
    # Buttons
    "Y": False,
    "X": False,
    "B": False,
    "A": False
}
```
### `desktop_bindings`
TODO. not complete (code wise)