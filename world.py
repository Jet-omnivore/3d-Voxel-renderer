from graphics_pipeline import Pipeline

from pygame import Vector3 as vec3
from random import randint
from models import Voxel
from renderer import Renderer
from camera import Camera
from chunk_sys import ChunkSys
from pprint import pprint


def z_sort(quad):
    vertices_count = len(quad[0])
    return sum((quad[0][i][0].w for i in range(vertices_count))) / vertices_count


def clip(quad):
    for vertex in quad:
        if vertex[0].z < 1:
            return False
    return True


class World:

    def __init__(self, engine):
        self.engine = engine

        self.renderer = Renderer(self.engine)
        self.camera = Camera()
        self.chunks = ChunkSys()

        n = 20
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    if y == 0 and randint(0, 3) <= 2:
                        self.chunks.add_block([x, y, z], Voxel())
                    elif y > 0:
                        self.chunks.add_block([x, y, z], Voxel())

        self.mesh = []  # self.chunks.greedy_mesh((0, 0, 0))
        # for chunk_pos in self.chunks.chunks:
            # self.mesh += self.chunks.greedy_mesh(chunk_pos)

        self.chunks.update_mesh_buffer()

        self.pipeline = Pipeline(self)
        self.pipeline.set_light([110 , 129480123,123988993])


    def update(self):
        self.update_objects()
        self.camera.update()

    def render(self):
        self.renderer.show_fps()

    def update_objects(self):
        self.mesh.clear()
        for mesh in self.chunks.mesh_buffer:
            self.mesh.extend(self.chunks.mesh_buffer[mesh])
        self.pipeline.update()
        self.pipeline.send(self.mesh)
