import pygame

from pprint import pprint

class Renderer:
    def __init__(self, engine):
        self.engine = engine
        self.display = self.engine.display
        self.font = pygame.font.SysFont('courier new', 8)
        self.avg_fps = []

    def show_fps(self, pos=(5, 3)):
        fps = int(self.engine.clock.get_fps())
        self.avg_fps.append(fps)
        text = self.font.render(str(fps), 0, (255, 255, 255))
        self.display.blit(text, pos)

    def draw_quad(self, vertices, color=(255, 255, 255)):
        # ppri<nt(vertices)
        # can_draw = True
        # for vertex in vertices:
            # if vertex[0] < 0:
                # vertex[0] = 0
            # if vertex[0] > 480:
                # vertex[0] = 480
            # if vertex[1] < 0:
                # vertex[1] = 0
            # if vertex[1] > 270:
           #      vertex[1] = 270
            # if vertex[0] > 0 and vertex[0] < 480 and vertex[1] > 0 and vertex[1] < 270:
                # pass
            # else:
                # can_draw = False
        # if can_draw:
            pygame.draw.polygon(self.display, color, vertices, width=1)
