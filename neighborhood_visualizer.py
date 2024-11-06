import pygame
import numpy as np
import time

from utils import CanvasUtils
from utils import NoiseGenerator
from cellular_automata import CAiterator

pygame.init()

SEED = 42
np.random.seed(42)
LAST_STATE = np.random.get_state()

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
LOW_RES_WIDTH, LOW_RES_HEIGHT = 100, 100
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), WINDOW_SURFACE )
pygame.display.set_caption("CA")

canvas = pygame.Surface( ( LOW_RES_WIDTH, LOW_RES_HEIGHT ) )
canvas.fill( (0, 0, 50) )


def _start_loop():
    clock = pygame.time.Clock()
    running = True
    
    map = np.ones((LOW_RES_WIDTH, LOW_RES_HEIGHT))

    i_center = LOW_RES_WIDTH // 2
    j_center = LOW_RES_HEIGHT // 2

    # map[i_center][j_center] = 4

    neighbors : list = CanvasUtils._get_neighbors_positions(map, i_center, j_center, 7, pattern="interlined", normalized=False)
    for n in neighbors:
        map[n] = 0
    CanvasUtils.convert_from_array(map, canvas)

    while running:
        for event in pygame.event.get():
            if ( event.type == pygame.QUIT ):
                running = False

        window.blit( pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), ( 0, 0 ) )
        pygame.display.flip()

        # Clamp FPS
        clock.tick_busy_loop(60)

_start_loop()
pygame.quit()