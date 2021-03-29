import numpy as np
import pygame
import sys

import sailboat
import tileengine
import wind_effect

SCALE = 4


class Env:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # window size pixels
        self.window_size = self.win_width, self.win_height = 350 * SCALE, 200 * SCALE

        self.screen = pygame.display.set_mode(self.window_size)

        # World size meters per block
        self.meters_per_block = 1

        self.world = tileengine.TileEngine('../SailingSim/default-world', self.window_size, self.meters_per_block)

        self.boat = sailboat.SailBoat([1600, 1200])

    def reset(self):
        pass

    def step(self, rudder_position=None, sail_position=None):
        """Step function reads agent input observes rewards
        Args:
            :param sail_position:
            :param rudder_position:
        Returns:
            state: ?
            reward:
            terminal:
        """
        reward = 0
        terminal = False

        # Step through boat physics at time t
        self.boat.step(np.array([10, 0]), t=1 / 120)

        boat_hit_box = self.boat.boat_hit_box(self.world.world_size)

        collision_boxes = self.world.hit_boxes
        hit_index = boat_hit_box.collidelist(collision_boxes)
        if hit_index > 0:
            self.boat.position = np.array([1600, 1200], dtype=np.float64)
            self.boat.reset()
            reward = -100

        goal_boxes = self.world.goal_boxes
        goal_hit_index = boat_hit_box.collidelist(goal_boxes)
        if goal_hit_index > 0:
            self.boat.position = np.array([1600, 1200], dtype=np.float64)
            self.boat.reset()
            reward = 100
            terminal = True

        # ToDo: Vision
        #   How will agent avoid obstacles ? is returning the pixel surface sufficient ?

        state = None

        return state, reward, terminal

    def render(self, framerate=250):
        """Renders environment"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Render boat onto working surface of the world with correct scale
        self.boat.render(self.world.working_surface, self.world.scale(spherical=True))
        self.world.render(self.screen)

        print(self.clock.get_fps())

        # Update screen and lock framerate
        self.clock.tick()
        pygame.display.flip()
        self.clock.tick_busy_loop(framerate)


if __name__ == "__main__":
    env = Env()

    while True:
        state, reward, terminal = env.step()
        env.render()
        if terminal:
            break
