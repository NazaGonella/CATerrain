import numpy as np
import random
from utils import CanvasUtils, TerrainType

class VoronoiSimulation:

    clean_map : np.ndarray = []
    map : np.ndarray = []
    map_snapshots : list[np.ndarray] = []

    seeds : list[tuple[tuple[int, int], TerrainType]] = []
    def __init__(self, map : np.ndarray):
        self.clean_map = map.copy()
        self.map = map.copy()
        self.map_snapshots = [map.copy()]
    
    def add_random_points(self, base_terrain_type : TerrainType, density : float = 0.005) -> None:
        new_map : np.ndarray = self.clean_map.copy()
        noise = np.random.choice([TerrainType.R, TerrainType.G, TerrainType.B, base_terrain_type], (new_map.shape[0], new_map.shape[1]), p=[density / 3, density / 3, density / 3, 1 - density])
        self.seeds.clear()
        for i in range(new_map.shape[0]):
            for j in range(new_map.shape[1]):
                if new_map[i][j] == base_terrain_type:
                    new_map[i][j] = noise[i][j]
                    if noise[i][j] != base_terrain_type:
                        self.seeds.append(((i, j), noise[i][j]))
                
        self.map = new_map
    
    def add_seeds(self, base_terrain_type : TerrainType, biomes : list[TerrainType] = [TerrainType.R, TerrainType.G, TerrainType.B], biome_distribution : list[int] = []) -> None:
        """Adds seed points to map array with the given biomes / terrain types
        Args:
        base_terrain_type -- Terrain Type where the seeds will be placed.
        biomes -- terrain type of the seed points.
        biome_distribution -- how many seed per biome (Must be same size as biomes) | default = [1, ...], (one seed per biome)
        """
        if len(biome_distribution) == 0:
            for _ in biomes:
                biome_distribution.append(1)
        if len(biome_distribution) != len(biomes):
            raise ValueError("Size of distribution is not the same as the number of biomes")
        new_map : np.ndarray = self.clean_map.copy()
        self.seeds.clear()
        for b_index in range(len(biomes)):
            for i in range(biome_distribution[b_index]):
                for t in range(500): # number of tries
                    x : int = np.random.randint(0, new_map.shape[0])
                    y : int = np.random.randint(0, new_map.shape[1])
                    if new_map[x][y] == base_terrain_type:
                        new_map[x][y] = biomes[b_index]
                        self.seeds.append(((x, y), biomes[b_index]))
                        self.map_snapshots.append(new_map.copy())
                        break
        self.map = new_map
    
    def hard_tessellate(self, base_terrain_type : TerrainType) -> None:
        new_map : np.ndarray = self.map.copy()
        for i in range(new_map.shape[0]):
            for j in range(new_map.shape[1]):
                if new_map[i][j] == base_terrain_type:
                    closest_point : tuple[int, TerrainType] = (-1, base_terrain_type)
                    for point in self.seeds:
                        a : np.ndarray = np.array([i,j])
                        b : np.ndarray = point[0]
                        distance : float = (np.linalg.norm(a-b)) ** 2
                        if closest_point[0] == -1 or closest_point[0] >= distance:
                            closest_point = (distance, point[1])
                    new_map[i][j] = closest_point[1]
        self.map = new_map

    def organic_tessellate(self, base_terrain_type : TerrainType) -> None:
        new_map : np.ndarray = self.map.copy()

        biomes = {p[1] for p in self.seeds}
        biomes_uncolored_neighbors: dict[TerrainType, set[tuple[int, int]]] = {b : set() for b in biomes}
        biome_distribution : dict[TerrainType, int] = {}

        for pos, biome in self.seeds:
            biome_distribution[biome] = 0 

        for pos, biome in self.seeds:
            for n in CanvasUtils._get_neighbors_positions(new_map, pos[0], pos[1], normalized=True):
                if new_map[n[0]][n[1]] == base_terrain_type:
                    biomes_uncolored_neighbors[biome].add(n)
            biome_distribution[biome] += 1
        
        changed_terrain : bool = False
        for _ in range(10000): # Number of tries
            for biome in biomes:
                for d in range(biome_distribution[biome]):
                    if len(biomes_uncolored_neighbors[biome]) > 0:
                        chosen_neighbor : tuple[int, int] = random.choice(list(biomes_uncolored_neighbors[biome]))
                        for n in CanvasUtils._get_neighbors_positions(new_map, chosen_neighbor[0], chosen_neighbor[1], normalized=True):
                            if new_map[n[0]][n[1]] == base_terrain_type:
                                biomes_uncolored_neighbors[biome].add(n)
                        biomes_uncolored_neighbors[biome].remove(chosen_neighbor)
                        new_map[chosen_neighbor[0]][chosen_neighbor[1]] = biome
                        self.map_snapshots.append(new_map.copy())
                        changed_terrain = True
            if changed_terrain == False:
                break
        

        self.map = new_map

    def get_map_with_points(self) -> np.ndarray:
        return self.map

    def get_map_snapshots(self) -> list[np.ndarray]:
        return self.map_snapshots