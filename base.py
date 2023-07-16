import nxbt

# Start the NXBT service
nx = nxbt.Nxbt()

# Create a Pro Controller and wait for it to connect
controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
print("Waiting for connection(s)...")

nx.wait_for_connection(controller_index)
nx.press_buttons(controller_index, [nxbt.Buttons.B])

print("Connected")