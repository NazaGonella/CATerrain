import pygame
import numpy as np
import time

from utils import CanvasUtils, NoiseGenerator, TerrainType, BiomeDetector
from cellular_automata import CAiterator
from voronoi_simulation import VoronoiSimulation

pygame.init()

SEED = 42
BORDER_SIZE = 1
np.random.seed(42)
LAST_STATE = np.random.get_state()

WINDOW_WIDTH, WINDOW_HEIGHT = 100*10, 60*10
LOW_RES_WIDTH, LOW_RES_HEIGHT = 100, 60
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), WINDOW_SURFACE )
pygame.display.set_caption("CA")

canvas = pygame.Surface( ( LOW_RES_WIDTH, LOW_RES_HEIGHT ) )


def _start_loop():
    clock = pygame.time.Clock()
    running = True
    is_animated = False
    skip_frame : int = 8

    last_state = LAST_STATE

    np.random.seed()

    map, map_snapshots = _generate_map()
    curr_snapshot : int = 0

    #start_time = time.perf_counter()
    biome_detector : BiomeDetector = BiomeDetector(map)
    #print(time.perf_counter() - start_time)

    while running:
        for event in pygame.event.get():
            if ( event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE ):
                last_state = LAST_STATE
                map, map_snapshots = _generate_map()
                biome_detector = BiomeDetector(map)
                curr_snapshot = 0
            
            if ( event.type == pygame.QUIT ):
                running = False

        if is_animated:
            if len(map_snapshots) > curr_snapshot and curr_snapshot != -1:
                CanvasUtils.convert_from_array(map_snapshots[curr_snapshot], canvas)
                curr_snapshot += skip_frame
            elif len(map_snapshots) < curr_snapshot and curr_snapshot < len(map_snapshots) + skip_frame:
                curr_snapshot = -1
                CanvasUtils.convert_from_array(map_snapshots[curr_snapshot], canvas)
        else:
            CanvasUtils.convert_from_array(map, canvas)

        window.blit( pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), ( 0, 0 ) )
        pygame.display.flip()

        # Clamp FPS
        clock.tick_busy_loop(60)

def _create_border(map : np.ndarray, border_size : int) -> np.ndarray:
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            map[i][j] = TerrainType.WATER if i < border_size or i >= map.shape[0] - border_size or j < border_size or j >= map.shape[1] - border_size else map[i][j]

def _generate_map() -> np.ndarray:
    current_rule = 8
    current_noise_density = 0.42
    current_iteration = 3

    ca_iterator = CAiterator()
    map = NoiseGenerator.generate_noise(LOW_RES_WIDTH, LOW_RES_HEIGHT, density=current_noise_density)
    _create_border(map, BORDER_SIZE)
    for _ in range(current_iteration):
        map = ca_iterator.iterate(current_rule, map)
    _create_border(map, BORDER_SIZE)

    clean_map = map.copy()

    for _ in range(100):
        map = clean_map.copy()
        voronoi_density : float = 0.003
        voronoi : VoronoiSimulation = VoronoiSimulation(map)
        voronoi.add_seeds(base_terrain_type=TerrainType.GRASS, biome_distribution=[1, 3, 1])
        voronoi.organic_tessellate(base_terrain_type=TerrainType.GRASS)
        voronoi.hard_tessellate(base_terrain_type=TerrainType.GRASS)
        map = voronoi.get_map_with_points()
        snapshots = voronoi.get_map_snapshots()
        biome_detector : BiomeDetector = BiomeDetector(map)
        if not biome_detector.are_biomes_colliding(TerrainType.R, TerrainType.B):
            break
    for _ in range(1):
        map = ca_iterator.iterate(9, map)
    return map, snapshots

_start_loop()
pygame.quit()