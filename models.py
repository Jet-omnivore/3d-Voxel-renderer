from enum import Enum
from pygame import Vector3

class BlockType(Enum):
    ''' add uint8 '''
    GRASS = 0


class Voxel:

    block_type: BlockType = BlockType.GRASS
    active: bool = True
    neighbours:int = 0

    def is_active(self):
        return self.active

    def set_active(self, active):
        self.active = active


class CubeData:
    NORMALS = [
                Vector3([-1, 0, 0]),
                Vector3([1, 0, 0]),
                Vector3([0, -1, 0]),
                Vector3([0, 1, 0]),
                Vector3([0, 0, -1]),
                Vector3([0, 0, 1])
            ]
