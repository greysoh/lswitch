import threading
import time

import nxbt

class BetterButton: 
  def __init__(self, is_pro_controller = True, controller_index = 0, nxbt = nxbt.Nxbt()):
    self.nxbt = nxbt
    self.controller_index = controller_index
    
    if is_pro_controller:
      self.ms_to_wait = 1/120
    else:
      self.ms_to_wait = 1/60
    
    self.base_packet = nxbt.create_input_packet()

    # Start send_keys
    threading.Thread(target=self._send_keys).start()
  
  # Epic life hack: The keys are just strings. So, nxbt.Buttons will work 100%
  def key_down(self, key_list = []):
    for key in key_list:
      if key == "L_STICK_PRESS" or key == "R_STICK_PRESS":
        self.base_packet[f"{key[0]}_STICK"]["PRESSED"] = True
      
      self.base_packet[key] = True
  
  def key_up(self, key_list = []):
    for key in key_list:
      if key == "L_STICK_PRESS" or key == "R_STICK_PRESS":
        self.base_packet[f"{key[0]}_STICK"]["PRESSED"] = False
      
      self.base_packet[key] = False

  def tilt_stick(self, stick, side_vertical, side_horizonal):
    self.base_packet[stick]["X_VALUE"] = side_vertical
    self.base_packet[stick]["Y_VALUE"] = side_horizonal
  
  # Am I a real programmer now? (threads)
  def _send_keys(self):
    while True:
      self.nxbt.set_controller_input(self.controller_index, self.base_packet)
      time.sleep(self.ms_to_wait) # I love floating point