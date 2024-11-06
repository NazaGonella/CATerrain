import numpy as np
import pygame

# BLACK     = (   0,   0,   0 )
# WHITE     = ( 255, 255, 255 )
BLACK      = (0, 0, 255)
WHITE     = (0, 255, 0)
WHITE2    = ( 100, 255, 200 )
# WHITE2    = ( 255,   0,   0 )
DARK_BLUE = (   0,   0,  200 )
RED       = ( 255,   0,   0 )
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)

class NoiseGenerator:
    @staticmethod
    def generate_noise(width : int, height : int, density : float = 0.5) -> np.ndarray:
        _density = density
        if _density < 0.0:
            _density = 0.0
        elif _density > 1.0:
            _density = 1.0
        noise = np.random.choice([1, 0], (width, height), p=[_density, 1 - _density])
        return noise

class CanvasUtils:
    @staticmethod
    def convert_from_array(array : np.ndarray, surface : pygame.Surface):
        colors = {0 : BLACK, 1 : WHITE, 2 : WHITE2, 3 : DARK_BLUE, 4 : BLUE}
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                color = colors[array[i][j]]
                surface.set_at((i, j), color)

    @staticmethod
    def _get_neighbors(array : np.ndarray, i : int, j : int, _range : int = 1, normalized : bool = False, pattern : str = "") -> list:  
        neighbors = []
        for dx in range(-_range, _range + 1):
            for dy in range(-_range, _range + 1):
                if dx == 0 and dy == 0:
                    continue
                match pattern:
                    case "interlined":
                        if (dx + dy) % 2 == 0:
                            continue
                    case "cross_fractal":
                        if (dx % (max([abs(dx), abs(dy)])) != 0 or dy % (max([abs(dx), abs(dy)])) != 0):
                            continue
                    case _:
                        pass
                ni = (i + (dx)) % array.shape[0]
                nj = (j + (dy)) % array.shape[1]
                if normalized:
                    if np.linalg.norm([dx, dy]) > _range:
                        continue
                neighbors.append(array[ni][nj])
        return neighbors
    
    @staticmethod
    def _get_neighbors_positions(array : np.ndarray, i : int, j : int, _range : int = 1, normalized : bool = False, pattern : str = "") -> list:  
        neighbors = []
        for dx in range(-_range, _range + 1):
            for dy in range(-_range, _range + 1):
                if dx == 0 and dy == 0:
                    continue
                match pattern:
                    case "interlined":
                        if (dx + dy) % 2 == 0:
                            continue
                    case "cross_fractal":
                        if (dx % (max([abs(dx), abs(dy)])) != 0 or dy % (max([abs(dx), abs(dy)])) != 0):
                            continue
                    case _:
                        pass
                ni = (i + (dx)) % array.shape[0]
                nj = (j + (dy)) % array.shape[1]
                if normalized:
                    if np.linalg.norm([dx, dy]) > _range:
                        continue
                neighbors.append((ni, nj))
        return neighbors