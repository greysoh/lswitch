import pygame
import nxbt

from config import macro_kdl_path

from libs.macro_agent import MacroAgentFromFile
from libs.better_button import BetterButton

# Start PyGame
(width, height) = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("LSwitch Desktop Mode")

# Start the NXBT Service
nx = nxbt.Nxbt()

controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
print("Waiting for connection(s)...")

nx.wait_for_connection(controller_index)

print("NXBT Connected")
print("Initializing components...")

bb = BetterButton(True, controller_index, nx)
val_conv_btn = [bb.key_up, bb.key_down]

ma = MacroAgentFromFile(macro_kdl_path)

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYDOWN:
      print("TODO")