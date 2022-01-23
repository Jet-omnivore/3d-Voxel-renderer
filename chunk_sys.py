import json
import random

from models import Voxel
from pygame import Vector3


class ChunkSys:
    __slots__ = ['chunk_size', 'chunks', 'voxel_data']

    def __init__(self, chunk_size=8):
        self.chunk_size = chunk_size
        self.chunks = {}

    def load_voxel_data(self, path):
        with open(path) as f:
            data = f.read()
            voxel_data = json.loads(data)

            for i, vertex in enumerate(voxel_data['vertices']):
                voxel_data['vertices'][i] = array(vertex)
            self.voxel_data = voxel_data

    def generate_chunk(self, chunk_pos):
        index = tuple(chunk_pos)
        self.chunks[index] = {}
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                for z in range(self.chunk_size):
                    block_pos = (x + chunk_pos[0],
                                 y + chunk_pos[1],
                                 z + chunk_pos[2])
                    self.add_block(block_pos, Voxel())

    def pos_to_chunk_scale(self, pos):
        return (
                int(pos[0] // self.chunk_size),
                int(pos[1] // self.chunk_size),
                int(pos[2] // self.chunk_size)
                )

    def neighbours_to_number(self, neighbours):
        return sum([x * (2 ** i) for i, x in enumerate(neighbours) if x])

    def number_to_neighbours(self, number):
        neighbours = [int(digit) for digit in bin(number)[2:][::-1]]
        neighbours += [0] * (6 - len(neighbours))
        return neighbours

    def add_block(self, pos, block):
        chunk_pos = self.pos_to_chunk_scale(pos)
        if chunk_pos not in self.chunks:
            self.chunks[tuple(chunk_pos)] = {}

        x, y, z = pos
        chunk_area = self.chunks[chunk_pos]
        if x in chunk_area:
            if y in chunk_area[x]:
                chunk_area[x][y][z] = block
            else:
                chunk_area[x][y] = {z: block}
        else:
            chunk_area[x] = {y: {z: block}}


    def update_block(self, block_pos):
        block = self.get_block(block_pos)
        if block is not None:
            neighbours = self.get_neighbours(block_pos)
            if all(neighbours):
                block.active = False
            block.neighbours = self.neighbours_to_number(neighbours)
            block_pos = array([*block_pos, 0])

    def update_chunk(self, chunk_pos):
        if chunk_pos not in self.chunks:
            return False

        chunk_area = self.chunks[chunk_pos]
        for x in chunk_area:
            for y in chunk_area[x]:
                for z in chunk_area[x][y]:
                    block = chunk_area[x][y][z]
                    pos = [x, y, z]

                    neighbours = self.get_neighbours(pos)
                    if all(neighbours):
                        block.active = False

                    block.neighbours = self.neighbours_to_number(neighbours)

    def update_all_chunks(self):
        for chunk_pos in self.chunks:
            self.update_chunk(chunk_pos)

    def get_block(self, pos):
        chunk_pos = self.pos_to_chunk_scale(pos)
        if chunk_pos not in self.chunks:
            return None
        x, y, z = pos
        try:
            block = self.chunks[chunk_pos][x][y][z]
        except KeyError:
            return None
        return block

    def get_quads(self, block, block_pos):
        neighbours = self.number_to_neighbours(block.neighbours)
        #  range(6) -> [0, 1, 2, 3, 4, 5] -> quads_index
        iterator = enumerate(range(6))
        quads = [self.voxel_data['all_quads'][x] for i, x in iterator if not neighbours[i]]
        return [[block_pos + self.voxel_data['vertices'][i] for i in x] for x in quads]

    def get_neighbours(self, block_pos):
        x, y, z = block_pos
        neighbours = [
                 [x, y, z - 1],  # front
                 [x + 1, y, z],  # right
                 [x, y, z + 1],  # back
                 [x - 1, y, z],  # left
                 [x, y + 1, z],  # down
                 [x, y - 1, z],  # up
                 ]
        neighbours_lst = [1 if self.get_block(n) else 0 for n in neighbours]
        return neighbours_lst

    def get_neighbours_pos(self, block_pos):
        x, y, z = block_pos
        neighbours = [
                 [x, y, z - 1],  # front
                 [x + 1, y, z],  # right
                 [x, y, z + 1],  # back
                 [x - 1, y, z],  # left
                 [x, y + 1, z],  # down
                 [x, y - 1, z],  # up
                 ]
        return list(filter(self.get_block, neighbours))

    def get_chunk(self, chunk_pos):
        if chunk_pos not in self.chunks:
            return False
        chunk = self.chunks[chunk_pos]
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        for x in chunk:
            for y in chunk[x]:
                for z in chunk[x][y]:
                    data = (x, y, z, 0), chunk[x][y][z]
                    if data[1].is_active:
                        yield data, color

    def get_visible_chunks(self, camera_pos):

        for x in range(3):
            for y in range(3):
                for z in range(3):
                    chunk_pos = (x, y, z)
                    yield self.get_chunk(chunk_pos)

    def get_block_in_chunk(self, chunk_pos, block_pos):
        chunk_pos = tuple(chunk_pos)
        if chunk_pos not in self.chunks:
            return None
        x, y, z = block_pos
        try:
            block = self.chunks[chunk_pos][x][y][z]
        except KeyError:
            return None
        return block

    def get_quad_normal_index(self, axis, mask):
        return (axis << 1) + max(mask, 0)

    def greedy_mesh(self, chunk_pos):

        chunk_pos = Vector3(chunk_pos)
        quads = []
        dims = [self.chunk_size] * 3
        block_offset = chunk_pos * self.chunk_size

        for axis in range(3):
            axis1 = (axis + 1) % 3
            axis2 = (axis + 2) % 3

            direction = Vector3([0, 0, 0])
            pos = Vector3([0, 0, 0])
            mask = [0] * dims[axis1] * (dims[axis2])
            direction[axis] = 1

            pos[axis] = -1
            while pos[axis] < dims[axis]:
                n = 0
                for pos[axis2] in range(dims[axis2]):
                    for pos[axis1] in range(dims[axis1]):
                        block1, block2 = False, False
                        block_pos = pos + block_offset
                        if self.get_block(block_pos):
                            block1 = True  # pos[axis] >= 0
                        if self.get_block(block_pos + direction):
                            block2 = True  # pos[axis] < dims[axis]
                        if block1 is block2:
                            mask[n] = 0
                        elif block1:
                            mask[n] = 1
                        else:
                            mask[n] = -1
                        # mask[n] = block1 ^ block2
                        n += 1

                pos[axis] += 1
                n = 0
                for j in range(dims[axis2]):
                    i = 0
                    while i < dims[axis1]:
                        current_mask = mask[n]
                        if current_mask:
                            w = 1
                            while (i + w) < dims[axis1] and mask[n + w] == current_mask:
                                w += 1

                            done = False
                            h = 1
                            while (h + j) < dims[axis2]:
                                for k in range(w):
                                    if not (mask[n + k + h * dims[axis1]] == current_mask):
                                        done = True
                                        break
                                if done:
                                    break
                                h += 1

                            offset = Vector3(block_offset)
                            offset[axis1] += i
                            offset[axis2] += j
                            offset[axis] += pos[axis]
                            pos[axis1] = i
                            pos[axis2] = j
                            du = Vector3(0)
                            dv = Vector3(0)

                            if current_mask > 0:
                                du[axis1] = w
                                dv[axis2] = h
                            else:
                                du[axis2] = h
                                dv[axis1] = w

                            normal_index = self.get_quad_normal_index(axis, current_mask)

                            quads.append([
                                [
                                    offset,
                                    offset + du,
                                    offset + du + dv,
                                    offset + dv
                                    ],
                                normal_index
                                ])

                            for a in range(h):
                                for b in range(w):
                                    mask[n + b + a * dims[axis1]] = False

                            i += w
                            n += w
                        else:
                            i += 1
                            n += 1

        return quads
