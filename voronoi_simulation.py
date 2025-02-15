import numpy as np
import random
from utils import CanvasUtils, TerrainType

class VoronoiSimulation:

    clean_map : np.ndarray = []
    map : np.ndarray = []
    density : float = 0.05

    points : list[tuple[tuple[int, int], TerrainType]] = []

    def __init__(self, map : np.ndarray, density : float = 0.05):
        self.clean_map = map.copy()
        self.map = map.copy()
        self.density = density
    
    def add_random_points(self, terrain_type : TerrainType) -> None:
        new_map : np.ndarray = self.clean_map.copy()
        noise = np.random.choice([TerrainType.R, TerrainType.G, TerrainType.B, terrain_type], (new_map.shape[0], new_map.shape[1]), p=[self.density / 3, self.density / 3, self.density / 3, 1 - self.density])
        self.points.clear()
        for i in range(new_map.shape[0]):
            for j in range(new_map.shape[1]):
                if new_map[i][j] == terrain_type:
                    new_map[i][j] = noise[i][j]
                    if noise[i][j] != terrain_type:
                        self.points.append(((i, j), noise[i][j]))
        self.map = new_map
        #print(self.points)
    
    def add_points(self, terrain_type : TerrainType, biomes : list[TerrainType] = [TerrainType.R, TerrainType.G, TerrainType.B]) -> None:
        new_map : np.ndarray = self.clean_map.copy()
        self.points.clear()
        for b in biomes:
            multiplier : float = 2 if b == TerrainType.G else 1
            for i in range(2 * multiplier):
                for t in range(500): # number of tries
                    x : int = np.random.randint(0, new_map.shape[0])
                    y : int = np.random.randint(0, new_map.shape[1])
                    if new_map[x][y] == terrain_type:
                        new_map[x][y] = b
                        self.points.append(((x, y), b))
                        break
        self.map = new_map
    
    def hard_tessellate(self, terrain_type : TerrainType) -> None:
        new_map : np.ndarray = self.map.copy()
        for i in range(new_map.shape[0]):
            for j in range(new_map.shape[1]):
                if new_map[i][j] == terrain_type:
                    closest_point : tuple[int, TerrainType] = (-1, terrain_type)
                    for point in self.points:
                        a : np.ndarray = np.array([i,j])
                        b : np.ndarray = point[0]
                        distance : float = (np.linalg.norm(a-b)) ** 2
                        if closest_point[0] == -1 or closest_point[0] >= distance:
                            closest_point = (distance, point[1])
                    new_map[i][j] = closest_point[1]
        self.map = new_map
    
    def organic_tessellate(self, terrain_type : TerrainType) -> None:
        new_map : np.ndarray = self.map.copy()
        colored_points : dict[tuple[int, int], TerrainType] = {}
        for p in self.points:
            colored_points[p[0]] = p[1]
        changed_color : bool = False
        for y in range(100):
            _colored_points : dict[tuple[int, int], TerrainType] = colored_points.copy()
            for colored_point, biome in _colored_points.items():
                neighbors : list[tuple[int, int]] = CanvasUtils._get_neighbors_positions(new_map, colored_point[0], colored_point[1], 1, True)
                chosen_neighbor : tuple[int, int] = neighbors[np.random.randint(0, len(neighbors))]
                if new_map[chosen_neighbor[0]][chosen_neighbor[1]] != terrain_type:
                    continue
                new_map[chosen_neighbor[0]][chosen_neighbor[1]] = biome
                colored_points[(chosen_neighbor[0], chosen_neighbor[1])] = biome
                changed_color = True
            if changed_color == False:
                break
            changed_color = False
        self.map = new_map

    def organic_tessellate_fast(self, terrain_type : TerrainType) -> None:
        new_map : np.ndarray = self.map.copy()

        biomes = {p[1] for p in self.points}
        biomes_uncolored_neighbors: dict[TerrainType, set[tuple[int, int]]] = {b : set() for b in biomes}

        for pos, biome in self.points:
            for n in CanvasUtils._get_neighbors_positions(new_map, pos[0], pos[1], normalized=True):
                if new_map[n[0]][n[1]] == terrain_type:
                    biomes_uncolored_neighbors[biome].add(n)
        
        for _ in range(10000):
            for biome in biomes:
                if len(biomes_uncolored_neighbors[biome]) > 0:
                    chosen_neighbor : tuple[int, int] = random.choice(list(biomes_uncolored_neighbors[biome]))
                    for n in CanvasUtils._get_neighbors_positions(new_map, chosen_neighbor[0], chosen_neighbor[1], normalized=True):
                        if new_map[n[0]][n[1]] == terrain_type:
                            biomes_uncolored_neighbors[biome].add(n)
                    biomes_uncolored_neighbors[biome].remove(chosen_neighbor)
                    new_map[chosen_neighbor[0]][chosen_neighbor[1]] = biome
        

        self.map = new_map

    def get_map_with_points(self) -> np.ndarray:
        return self.map