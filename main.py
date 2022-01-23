import pygame
import sys
import cProfile

from pygame.locals import K_ESCAPE, QUIT, KEYDOWN, K_x
from world import World


class Engine:
    def __init__(self):
        pygame.init()

        self.width, self.height = 480, 270
        self.window = pygame.display.set_mode((960, 540))
        self.display = pygame.Surface((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.world = World(self)

        pygame.mouse.set_visible(0)
        pygame.event.set_grab(True)

    def render(self):
        self.world.render()
        pygame.transform.scale(self.display, (960, 540), self.window)
        pygame.display.update()

    def update_events(self):
        for event in pygame.event.get():
            if event.type== QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    print(sum(self.world.renderer.avg_fps) / len(self.world.renderer.avg_fps))
                    pygame.quit()
                    sys.exit()

    def update(self):
        self.world.update()
        self.update_events()
        self.clock.tick(120)

    def run(self):
        while True:
            self.render()
            self.display.fill((0, 0, 0))
            self.update()


if __name__ == "__main__":
    Engine().run()
    # cProfile.run('Engine().world.update()')
