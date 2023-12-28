STRING_XML = """
<canvas pySize="500x500" pyBackground="(80, 80, 80)">
<label> hello there! </label>
</canvas>
"""

DICT_CLASSES = {
    "label": {
        "bgc": [200, 120, 120],
        "tc": [100, 100, 240]
    }
}

import sys
import pygame
from pygame_xml_gui.src.UserInterface import UserInterface

ui = UserInterface()
ui.set_pos((300, 300))
ui.set_classes_from_dict(DICT_CLASSES)
ui.set_structure_from_string(STRING_XML)
ui.initialize()

screen = pygame.display.set_mode((600, 600))
fpsclock = pygame.time.Clock()
fps = 60

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    ui.update(events)
    screen.fill((0,0,0))
    ui.draw(screen)
    
    pygame.display.flip()
    fpsclock.tick(fps)