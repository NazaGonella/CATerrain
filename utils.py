import numpy as np
import pygame
from enum import IntEnum

#BLACK      = (0, 0, 255)
#WHITE     = (0, 255, 0)
WATER = (40, 92, 196)
GRASS = (89, 193, 53)
WHITE2    = ( 100, 255, 200 )
DARK_BLUE = (   0,   0,  200 )
RED       = ( 255,   0,   0 )
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)

class TerrainType(IntEnum):
    R         = 0
    G         = 1
    B         = 2
    WATER     = 3
    GRASS     = 4

class NoiseGenerator:
    @staticmethod
    def generate_noise(width : int, height : int, density : float = 0.5, border : int = 0) -> np.ndarray:
        _density = density
        if _density < 0.0:
            _density = 0.0
        elif _density > 1.0:
            _density = 1.0
        noise = np.random.choice([1, 0], (width, height), p=[_density, 1 - _density])
        return noise

class CanvasUtils:

    colors_by_terrain_type : dict[TerrainType, tuple[int, int, int]] = {
        TerrainType.R     : (255,   0,   0),
        TerrainType.G     : (  0, 255,   0),
        TerrainType.B     : (  0,   0,   255),
        TerrainType.WATER : ( 40,  92, 196),
        TerrainType.GRASS : ( 89, 193,  53),
    }

    @staticmethod
    def convert_from_array(array : np.ndarray, surface : pygame.Surface):
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                #color = colors[array[i][j]]
                color = CanvasUtils.colors_by_terrain_type.get(array[i][j], (255, 255, 255))
                surface.set_at((i, j), color)
    
    @staticmethod
    def animate_from_array(array_snapshots : list[np.ndarray], surface : pygame.Surface):
        for snapshot in array_snapshots:
            CanvasUtils.convert_from_array(snapshot, surface)

    @staticmethod
    def _get_neighbors(array : np.ndarray, i : int, j : int, _range : int = 1, normalized : bool = False, pattern : str = "") -> list[TerrainType]:  
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
                    case "von_neumann":
                        if abs(dx) + abs(dy) > _range:
                            continue
                    case "euclidean":
                        if np.hypot(dx, dy) > _range:
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
    def _get_neighbors_positions(array : np.ndarray, i : int, j : int, _range : int = 1, normalized : bool = False, pattern : str = "") -> list[tuple[int, int]]:  
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
                    case "von_neumann":
                        if abs(dx) + abs(dy) > _range:
                            continue
                    case "euclidean":
                        if np.hypot(dx, dy) > _range:
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
    
    @staticmethod
    def _get_neighbors_offset(_range : int = 1, normalized : bool = False, pattern : str = "") -> list:  
        neighbors_offset = []
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
                    case "von_neumann":
                        if abs(dx) + abs(dy) > _range:
                            continue
                    case "euclidean":
                        if np.hypot(dx, dy) > _range:
                            continue
                    case _:
                        pass
                if normalized:
                    if np.linalg.norm([dx, dy]) > _range:
                        continue
                # ni = (i + (dx)) % array.shape[0]
                # nj = (j + (dy)) % array.shape[1]
                # neighbors.append((ni, nj))
                neighbors_offset.append((dx, dy))
        return neighbors_offset

    def has_neighbor_of_type(array : np.ndarray, pos : tuple[int,int], terrain_type : bool, _range : int = 1, normalized : bool = False) -> bool:
        for n in CanvasUtils._get_neighbors(array, pos[0], pos[1], _range, normalized):
            if n == terrain_type:
                return True
        return False

class CanvasAnimator:
    pass