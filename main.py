import pygame
import numpy as np
import time

pygame.init()

SEED = 42
np.random.seed(42)
LAST_STATE = np.random.get_state()

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
LOW_RES_WIDTH, LOW_RES_HEIGHT = 200, 200
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

# BLACK     = (   0,   0,   0 )
# WHITE     = ( 255, 255, 255 )
BLACK      = (0, 0, 255)
WHITE     = (0, 255, 0)
DARK_BLUE = (   3,   5,  54 )
RED       = ( 255,   0,   0 )
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)

window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), WINDOW_SURFACE )
pygame.display.set_caption("CA")

canvas = pygame.Surface( ( LOW_RES_WIDTH, LOW_RES_HEIGHT ) )
canvas.fill( DARK_BLUE )

class CanvasUtils:
    @staticmethod
    def convert_from_array(array : np.ndarray, surface : pygame.Surface):
        colors = {0 : WHITE, 1 : BLACK, 2 : RED, 3 : GREEN, 4 : BLUE}
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                # color = WHITE if array[i][j] == 0 else BLACK
                color = colors[array[i][j]]
                surface.set_at((i, j), color)
    
    @staticmethod
    def _get_neighbors(array, i, j, _range : int = 1, moore : bool = True) -> list:
        neighbors = []
        if moore:
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r in range(1, _range + 1):
            for x, y in dirs:
                if x == 0 and y == 0:
                    continue
                ni = (i + (x * r)) % array.shape[0]
                nj = (j + (y * r)) % array.shape[1]
                neighbors.append(array[ni][nj])
        return neighbors


class NoiseGenerator:
    @staticmethod
    def generate_noise(density : float = 0.5) -> np.ndarray:
        _density = density
        if _density < 0.0:
            _density = 0.0
        elif _density > 1.0:
            _density = 1.0
        noise = np.random.choice([1, 0], (LOW_RES_WIDTH, LOW_RES_HEIGHT), p=[_density, 1 - _density])
        return noise

class CAiterator:
    def __init__(self):
        pass

    def iterate(self, array : np.ndarray):
        new_array = np.zeros_like(array)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                new_array[i][j] = self._apply_rule(array, i, j)
        return new_array

    def _apply_rule(self, array, i, j):
        _range = 2
        _rule = 8
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range)
        if sum(neighbors) > _rule:
            return 1
        return 0

class MapPainter:
    def __init__(self):
        pass

    def paint_isle(self, map : np.ndarray, i : int, j : int, color : int):
        queue = [(i, j)]
        while len(queue) > 0:
            i, j = queue.pop(0)
            map[i][j] = color
            neighbors = CanvasUtils._get_neighbors(map, i, j)
            for n in neighbors:
                if map[n] == 0 and n not in queue:
                    queue.append(n)

    def paint(self, map : np.ndarray):
        for i in range(map.shape[0]):
            for j in range(map.shape[1]):
                if map[i][j] == 0:
                    self.paint_isle(map, i, j, np.random.choice([2, 3, 4]))

def _start_loop():
    clock = pygame.time.Clock()
    running = True

    map = NoiseGenerator.generate_noise()
    map_painter = MapPainter()
    CanvasUtils.convert_from_array(map, canvas)

    current_noise_density = 0.5
    current_iteration = 0
    last_state = LAST_STATE

    ca_iterator = CAiterator()

    while running:
        for event in pygame.event.get():
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE ):
                # print("Current density: ", current_noise_density)
                last_state = np.random.get_state()
                map = NoiseGenerator.generate_noise(current_noise_density)
                for _ in range(current_iteration):
                    map = ca_iterator.iterate(map)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_UP ):
                current_noise_density += 0.01
                print("Current density: ", current_noise_density)
                np.random.set_state(last_state)
                map = NoiseGenerator.generate_noise(current_noise_density)
                for _ in range(current_iteration):
                    map = ca_iterator.iterate(map)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN ):
                current_noise_density -= 0.01
                print("Current density: ", current_noise_density)
                np.random.set_state(last_state)
                map = NoiseGenerator.generate_noise(current_noise_density)
                for _ in range(current_iteration):
                    map = ca_iterator.iterate(map)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                map = ca_iterator.iterate(map)
                current_iteration+=1
                print("Current Iteration: ", current_iteration)
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                print("Reset CA")
                np.random.set_state(last_state)
                map = NoiseGenerator.generate_noise(current_noise_density)
                current_iteration = 0
                CanvasUtils.convert_from_array(map, canvas)
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_c):
                start_time = time.perf_counter()
                map_painter.paint(map)
                print("Painting took: ", time.perf_counter() - start_time)
                start_time = time.perf_counter()
                CanvasUtils.convert_from_array(map, canvas)
                print("Converting took: ", time.perf_counter() - start_time)
            
            if ( event.type == pygame.QUIT ):
                running = False

        window.blit( pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), ( 0, 0 ) )
        pygame.display.flip()

        # Clamp FPS
        clock.tick_busy_loop(60)

_start_loop()
pygame.quit()