import constants
import polygon_clipper
import pygame
import pygame.gfxdraw


from time import time_ns
from pygame.draw import polygon as draw_polygon
from matrix import Mat4
from pprint import pprint
from pygame import Vector3
from models import CubeData


def z_sort(quad):
    quad = quad[0]
    return sum([v[0].z for v in quad]) / len(quad)

'''
1. backface culling in clip space or in object space
2. depth sorting
'''

class Pipeline:
    def __init__(self, world):
        self.world = world
        self.setup_projection_matrix()

        self.main_matrix = world.camera.get_view_matrix().mat4_dot(self.projection_matrix)

        self.world_vertex_cache = {}
        self.clip_vertex_cache = {}
        self.sorted_polygons = []
        self.not_visible = []
        self.texture = pygame.image.load('floor.png')
        self.texture.convert()

    def setup_projection_matrix(self):
        aspect_ratio = self.world.engine.height / self.world.engine.width
        far_near_difference = constants.FAR_PLANE - constants.NEAR_PLANE

        self.projection_matrix = Mat4(
            [
              [constants.FOV_COT * aspect_ratio, 0, 0, 0],
              [0, constants.FOV_COT, 0, 0],
              [0, 0, (constants.FAR_PLANE - constants.NEAR_PLANE) / far_near_difference, 1],
              [0, 0, -(2 * constants.FAR_PLANE * constants.NEAR_PLANE) / far_near_difference, 0]
            ]
                )

    def set_light(self, light_pos):
        self.light_pos = Vector3(light_pos)
        self.light_pos.normalize_ip()

    def calculate_light_value(self, normal_index):
        normal = CubeData.NORMALS[normal_index]
        dot_value = self.light_pos.dot(normal)
        return 225 / abs(dot_value + 2.4)

    def send(self, mesh):
        for quad, normal_index in mesh:
            self.quad_matrix_multiply(quad, normal_index)
        self.sort_polygons()

    def quad_matrix_multiply(self, quad, normal_index):
        transformed_quad = []
        for vertex in quad:
            cache_index = tuple(vertex)
            if cache_index not in self.world_vertex_cache:
                self.world_vertex_cache[cache_index] = self.view_matrix.vec_dot(vertex)
            transformed_quad.append(self.world_vertex_cache[cache_index])
        self.backface_cull(transformed_quad, normal_index)

    def backface_cull(self, quad, normal_index):
        v0 = quad[0][0]
        line1 = quad[1][0] - v0
        line2 = quad[2][0] - v0

        normal = line1.cross(line2)

        if normal.dot(v0) <= 0:
            self.projection_transformation(quad, normal_index)

    def projection_transformation(self, quad, normal_index):
        transformed_quad = []
        for vertex in quad:
            cache_index = tuple(vertex[0])
            if cache_index not in self.clip_vertex_cache:
                self.clip_vertex_cache[cache_index] = self.projection_matrix.vec_dot2(vertex)
            transformed_quad.append(self.clip_vertex_cache[cache_index])
        self.clip_quad(transformed_quad, normal_index)


    def clip_quad(self, quad, normal_index):
        # make one function call
        clipped = polygon_clipper.clip_polygon(quad, 0)
        clipped = polygon_clipper.clip_polygon(clipped, 1)
        clipped = polygon_clipper.clip_polygon(clipped, 2)
        if clipped:  # is empty?
            self.sorted_polygons.append((clipped, normal_index))

    def sort_polygons(self):
        self.sorted_polygons.sort(key=z_sort, reverse=True)
        for polygon, normal_index in self.sorted_polygons:
            light_value = self.calculate_light_value(normal_index)
            color = (light_value, ) * 3
            self.rasterize_polygon(polygon, color)

    def rasterize_polygon(self, polygon, color=(255, 255, 255)):
        screen_polygon = []
        for vertex in polygon:
            w = vertex[1]
            if w == 0:
                w = 0.00001
            ndc_vec = vertex[0] / w  # normalize device coordinates
            screen_point = [(ndc_vec.x + 1) * 240, (ndc_vec.y + 1) * 135]
            screen_polygon.append(screen_point)
        # draw_polygon(self.world.engine.display, color, screen_polygon, width=4)
        draw_polygon(self.world.engine.display, color, screen_polygon, width=0)

    def update(self):
        self.world_vertex_cache.clear()
        self.clip_vertex_cache.clear()
        self.sorted_polygons.clear()
        self.not_visible.clear()

        self.view_matrix = self.world.camera.get_view_matrix()
