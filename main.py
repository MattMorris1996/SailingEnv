import numpy as np
import pygame
import sys

import sailboat
import tileengine

SCALE = 5

class Env:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # window size pixels
        self.window_size = self.win_width, self.win_height = 320 * SCALE, 240 * SCALE

        self.screen = pygame.display.set_mode(self.window_size)

        # World size meters per block
        self.meters_per_block = 100

        self.world = tileengine.TileEngine('../SailingSim/default-world', self.window_size, self.meters_per_block)

        self.boat = sailboat.SailBoat([1600, 1200])

    def reset(self):
        pass

    def step(self):
        """Step function reads agent input observes rewards
        Args:
            rudder_positions:
            sail_position:
        Returns:
            reward:
        """
        self.boat.step(np.array([10, 0]), t=1)
        # ToDo: Collisions
        # ToDo: GoalChecking
        # ToDo: Reward Function

    def render(self, framerate=120):
        """Renders environment"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Render boat onto working surface of the world with correct scale
        self.boat.render(self.world.working_surface, self.world.scale())
        self.world.render(self.screen)

        # Update screen and lock framerate
        self.clock.tick()
        pygame.display.flip()
        self.clock.tick_busy_loop(framerate)


if __name__ == "__main__":
    env = Env()

    while True:
        env.step()
        env.render()
