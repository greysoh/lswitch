import pygame
import nxbt

import libs.better_button as better_button

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
print("Initializing 'better_button'...")
bb = better_button.BetterButton(True, controller_index, nx)
val_conv_btn = [bb.key_up, bb.key_down]

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False