import threading
import time
import os

import kdl

class MacroAgent:
  def __init__(self, str_data, is_file):
    self.keybinding_cache = []
    self.macro_cache = []

    self.str_base = str_data # fixme: betterer?

    if is_file:
      with open(str_data) as f:
        self.file_path = str_data
        self.str_base = f.read()    
      
      self.file_timestamp_current = os.path.getmtime(str_data)
      threading.Thread(target=self._file_background_update_daemon).start()

    self.doc = kdl.parse(self.str_base)

    self._build_keybinding_cache()
    self._build_macro_cache()
  
  def get_keybinding(self, key_to_search):
    desktop_binding_cache_search = [x for x in self.keybinding_cache if x["key"] == key_to_search]
   
    if len(desktop_binding_cache_search) != 0:
      return desktop_binding_cache_search[0]["value"]
    
  def get_keybind_list(self):
    return self.keybinding_cache
  
  def get_macro(self, type, key):
    macros_cache_search = [x for x in self.macro_cache if x["mode"] == type and x["key"] == key]

    if len(macros_cache_search) != 0:
      return macros_cache_search[0]["macro_items"]
    
  def execute_macro(self, macro, bb):
    threading.Thread(target=self._execute_macro, args=(macro,), kwargs={"bb":bb}).start()
  
  def _execute_macro(self, macro, bb):
    for macro_button in macro:
      match macro_button["type"]:
        case "key_down":
          bb.key_down([macro_button["key"]])
        
        case "sleep":
          time.sleep(macro_button["time"])
        
        case "key_up":
          bb.key_up([macro_button["key"]])
    
  def _file_background_update_daemon(self):
    while True:
      time.sleep(0.5)

      modified_time = os.path.getmtime(self.file_path)
      if modified_time != self.file_timestamp_current:
        try:
          self.file_timestamp_current = modified_time
          print("File modified, beginning macro rebuild process...")

          # FIXME: There is no locks, so, if you time inputs right some macros will drop.
          self.doc = kdl.parse(self.file_path)

          self._build_keybinding_cache()
          self._build_macro_cache()

          print("Finished successfully.")
        except Exception as e:
          print(e)
  
  def _build_keybinding_cache(self):
    # FIXME: Maybe instead of clearing the keybinding cache each run, we check if we already have it?
    self.keybinding_cache.clear()

    desktop_bindings_lists = [x for x in self.doc.nodes if x.name == "desktop_bindings"]

    for desktop_list in desktop_bindings_lists:
      for binding in desktop_list.nodes:
        gen_binding_info = {
          "key": None,
          "value": None,
        }

        arguments = list(binding.props.items())

        for key, value in arguments:
          if key == "key":
            gen_binding_info["key"] = value
          elif key == "button":
            gen_binding_info["value"] = value
        
        self.keybinding_cache.append(gen_binding_info)
  
  def _build_macro_cache(self):
    # FIXME: Maybe instead of clearing the keybinding cache each run, we check if we already have it?
    self.macro_cache.clear()

    for type in [self.KEYBOARD, self.CONTROLLER]:
      macros_lists = [x for x in self.doc.nodes if x.name == "macros"]

      for node in macros_lists:
        mode_lists = [x for x in node.nodes if x.name == type]

        for mode_items in mode_lists:
          for macros in mode_items.nodes:
            key = macros.name
  
            time_scale = 1 
            macro_items = []

            for macro_key in macros.nodes:
              arguments_tuple = tuple(macro_key.props.items())
              arguments = dict((x, y) for x, y in arguments_tuple)

              match macro_key.name:
                case "press":
                  duration = arguments["duration"]
                  key_arg = arguments["key"]

                  if len(arguments) > 2:
                    time_scale = arguments["timeScale"]
                    if time_scale == "ms":
                      duration = duration / 1000
                
                  macro_items.append({
                    "type": "key_down",
                    "key": key_arg
                  })

                  macro_items.append({
                    "type": "sleep",
                    "time": duration
                  })

                  macro_items.append({
                    "type": "key_up",
                    "key": key_arg
                  })
  
                  continue
            
                case "sleep":
                  macro_items.append({
                    "type": "sleep",
                    "time": arguments["duration"]
                  })

                  continue
              
                case "key_down":
                  macro_items.append({
                    "type": "key_down",
                    "key": arguments["key"]
                  })

                  continue
              
                case "key_up":
                  macro_items.append({
                    "type": "key_up",
                    "key": arguments["key"]
                  })

                  continue

            self.macro_cache.append({
              "mode": type,
              "key": key,
              "macro_items": macro_items
            })
    
  KEYBOARD = "keyboard"
  CONTROLLER = "controller"