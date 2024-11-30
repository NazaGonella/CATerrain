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
# canvas.fill( DARK_BLUE )


def _start_loop():
    clock = pygame.time.Clock()
    running = True

    map = NoiseGenerator.generate_noise(LOW_RES_WIDTH, LOW_RES_HEIGHT)
    CanvasUtils.convert_from_array(map, canvas)

    current_rule = 5
    current_noise_density = 0.5
    current_iteration = 0
    last_state = LAST_STATE

    ca_iterator = CAiterator()

    while running:
        for event in pygame.event.get():
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE ):
                last_state = np.random.get_state()
                map = NoiseGenerator.generate_noise(LOW_RES_WIDTH, LOW_RES_HEIGHT, density=current_noise_density)
                for _ in range(current_iteration):
                    map = ca_iterator.iterate(current_rule, map)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_UP ):
                current_noise_density += 0.01
                print("Current density: ", current_noise_density)
                np.random.set_state(last_state)
                map = NoiseGenerator.generate_noise(LOW_RES_WIDTH, LOW_RES_HEIGHT, density=current_noise_density)
                for _ in range(current_iteration):
                    map = ca_iterator.iterate(current_rule, map)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN ):
                current_noise_density -= 0.01
                print("Current density: ", current_noise_density)
                np.random.set_state(last_state)
                map = NoiseGenerator.generate_noise(LOW_RES_WIDTH, LOW_RES_HEIGHT, density=current_noise_density)
                for _ in range(current_iteration):
                    map = ca_iterator.iterate(current_rule, map)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                map = ca_iterator.iterate(current_rule, map)
                current_iteration+=1
                print("Current Iteration: ", current_iteration)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                print("Reset CA")
                np.random.set_state(last_state)
                map = NoiseGenerator.generate_noise(LOW_RES_WIDTH, LOW_RES_HEIGHT, density=current_noise_density)
                current_iteration = 0
                CanvasUtils.convert_from_array(map, canvas)
            
            if ( event.type == pygame.QUIT ):
                running = False

        window.blit( pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), ( 0, 0 ) )
        pygame.display.flip()

        # Clamp FPS
        clock.tick_busy_loop(60)

_start_loop()
pygame.quit()