from utils import CanvasUtils, TerrainType
import numpy as np

class CAiterator:
    def __init__(self):
        pass

    def iterate(self, rule : int, array : np.ndarray):
        new_array = np.zeros_like(array)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                new_array[i][j] = Rules.apply_rule(rule, array, i, j)
        return new_array

class Rules:
    @staticmethod
    def apply_rule(rule_index : int, array : np.ndarray, i : int, j : int) -> int:
        if rule_index == 1:
            return Rules._rule_01(array, i, j)
        elif rule_index == 2:
            return Rules._rule_02(array, i, j)
        elif rule_index == 3:
            return Rules._rule_03(array, i, j)
        elif rule_index == 4:
            return Rules._rule_04(array, i, j)
        elif rule_index == 5:
            return Rules._rule_05(array, i, j)
        elif rule_index == 6:
            return Rules._rule_06(array, i, j)
        elif rule_index == 7:
            return Rules._rule_07(array, i, j)
        elif rule_index == 8:
            return Rules._rule_08(array, i, j)
        elif rule_index == 9:
            return Rules._rule_09(array, i, j)
        return Rules._rule_01(array, i, j)

    # bug? considers deep water land
    def _rule_01(array, i, j) -> int:
        _range = 2
        _rule = 8
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range, pattern="cross_fractal")
        neighbors_2 : list = CanvasUtils._get_neighbors(array, i, j, _range + 1, normalized=True, pattern="interlined")
        land_ammount : int = len([n for n in neighbors if n != 0])
        water_ammount = len([n for n in neighbors_2 if n == 0])
        
        if water_ammount == len(neighbors_2):
            return 3
        if land_ammount > _rule:
            return 1
        return 0
    
    # like rule_01 but fixed
    def _rule_02(array, i, j) -> int:
        _range = 2
        _rule = 8
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range, pattern="cross_fractal")
        neighbors_2 : list = CanvasUtils._get_neighbors(array, i, j, _range + 1, normalized=True, pattern="interlined")
        land_ammount : int = len([n for n in neighbors if n != 0 and n != 3])
        water_ammount = len([n for n in neighbors_2 if n == 0])
        
        if water_ammount == len(neighbors_2):
            return 3
        if land_ammount > _rule:
            return 1
        return 0
    
    def _rule_03(array, i, j) -> int:
        _range = 2
        _rule = 8
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range, pattern="cross_fractal")
        neighbors_2 : list = CanvasUtils._get_neighbors(array, i, j, _range + 1, normalized=True, pattern="interlined")
        neighbors_3 : list = CanvasUtils._get_neighbors(array, i, j, 1, normalized=True, pattern="")
        land_ammount : int = len([n for n in neighbors if n != 0 and n != 3])
        water_ammount = len([n for n in neighbors_2 if n == 0])
        land_ammount_2 : int = len([n for n in neighbors_3 if n != 0 and n != 3])
        
        if land_ammount_2 >= 3:
            return 1
        if water_ammount == len(neighbors_2):
            return 1
        if land_ammount > _rule:
            return 1
        return 0
    
    def _rule_04(array, i, j) -> int:
        _range = 2
        _rule = 13
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range)
        land_ammount : int = len([n for n in neighbors if n != 0])
        if land_ammount >= _rule:
            return 1
        return 0
    
    def _rule_05(array, i, j) -> int:
        _range = 2
        _rule = 8
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range, pattern="cross_fractal")
        neighbors_2 : list = CanvasUtils._get_neighbors(array, i, j, _range + 1, normalized=True, pattern="interlined")
        neighbors_3 : list = CanvasUtils._get_neighbors(array, i, j, 1, normalized=True, pattern="")
        land_ammount : int = len([n for n in neighbors if n != 0 and n != 3])
        water_ammount = len([n for n in neighbors_2 if n == 0])
        land_ammount_2 : int = len([n for n in neighbors_3 if n != 0 and n != 3])
        
        if land_ammount_2 >= 3:
            return 1
        if water_ammount == len(neighbors_2):
            return 1
        if land_ammount > _rule:
            return 1
        return 0

    def _rule_06(array, i, j) -> int:
        _range = 1
        _rule = 4
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range)
        land_ammount : int = len([n for n in neighbors if n != 0 and n != 3])
        
        if land_ammount > _rule:
            return 1
        return 0
    
    def _rule_07(array, i, j) -> int:
        _range = 2
        _rule = 10
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range)
        land_ammount : int = len([n for n in neighbors if n != 0 and n != 3])
        
        if land_ammount > _rule:
            return 1
        return 0
    
    def _rule_08(array, i, j) -> int:
        #_range = 2
        #_rule = 8
        # neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range, normalized=True)
        _range = 2
        _rule = 9
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range)
        land_ammount : int = len([n for n in neighbors if n != 0 and n != 3])
        
        if land_ammount > _rule:
            return TerrainType.GRASS
        return TerrainType.WATER

    def _rule_09(array, i, j) -> int:
        #_range = 2
        #_rule = 8
        # neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range, normalized=True)
        if array[i][j] == TerrainType.WATER or array[i][j] == TerrainType.G:
            return array[i][j]
        _range = 1
        _rule = 4
        neighbors : list = CanvasUtils._get_neighbors(array, i, j, _range)
        land_ammount : int = len([n for n in neighbors if array[i][j] == n])
        land_type_count : dict[TerrainType, int] = {}
        for n in neighbors:
            if n == array[i][j]:
                continue
            land_type_count[n] = 0
        for n in neighbors:
            if n == array[i][j]:
                continue
            land_type_count[n] += 1
        
        if land_ammount > _rule or len(land_type_count) == 0:
            return array[i][j]
        return max(land_type_count, key=land_type_count.get)