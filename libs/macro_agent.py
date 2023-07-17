import kdl

class MacroAgent:
  def __init__(self, str):
    self.keybinding_cache = []
    self.macro_cache = []

    self.doc = kdl.parse(str)

    self._build_keybinding_cache()
    self._build_macro_cache()
  
  def get_keybinding(self, key_to_search):
    desktop_binding_cache_search = [x for x in self.keybinding_cache if x["key"] == key_to_search]
   
    if len(desktop_binding_cache_search) != 0:
      return desktop_binding_cache_search[0]["value"]
  
  def get_macro(self, type, key):
    macros_cache_search = [x for x in self.macro_cache if x["mode"] == type and x["key"] == key]

    if len(macros_cache_search) != 0:
      return macros_cache_search[0]["macro_items"]
  
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

                break
            
              case "sleep":
                macro_items.append({
                  "type": "sleep",
                  "time": arguments["duration"]
                })
              
              case "key_down":
                macro_items.append({
                  "type": "key_down",
                  "key": arguments["key"]
                })
              
              case "key_up":
                macro_items.append({
                  "type": "key_up",
                  "key": arguments["key"]
                })

          self.macro_cache.append({
            "mode": type,
            "key": key,
            "macro_items": macro_items
          })

  KEYBOARD = "keyboard"
  CONTROLLER = "controller"

class MacroAgentFromFile(MacroAgent):
  def __init__(self, file_path):
    with open(file_path) as f:
      super().__init__(f.read())