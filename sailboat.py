import pygame
import numpy as np


class SailBoat(object):
    """Handles Boat Position and Physics"""

    def __init__(self, position):
        """Currently takes a starting position of two numbers and initialises boat physics properties

        Args:
            position (:obj list of two ints): x, y position of starting position

        """

        # ToDo: Linear Scale Function
        #   currently world units is in pixels, which creates problems when scale of world is changed

        self.position = np.array(position, dtype=np.float64)

        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)

        self.angular_acceleration = 0
        self.angular_velocity = 0

        self.rudder_range = 90
        self.rudder_angle = 0

        self.sail_angle = -5
        self.heading_angle = 0

        self.mass = 10

    def step(self, wind_force, t=1):
        """Step function takes a force on the boat due to wind vector, and updates the boats physics properties
        based on the time step t
        """

        # ToDo: Improve Physics
        #   Much of the values are fudged

        # Calculate the force acting on the boat along the angle of its heading
        forward_force_angle_rads = np.radians(self.heading_angle)
        forward_force_unit_vector = np.array([np.cos(forward_force_angle_rads), np.sin(forward_force_angle_rads)])

        # Project force onto unit vector of heading to obtain the motion of the boat
        forward_force = np.dot(forward_force_unit_vector, wind_force) * forward_force_unit_vector

        # Update linear physics properties
        self.acceleration = forward_force / self.mass - self.velocity * 0.5
        self.velocity += self.acceleration * t
        self.position += self.velocity * t

        # Update angular physics properties
        self.angular_acceleration = self.rudder_angle - self.angular_velocity
        self.angular_velocity += self.angular_acceleration * t
        self.heading_angle += self.angular_velocity * t

    def render(self, world_surface: pygame.Surface, linear_scale):
        """Takes a python surface and renders the current state of the boat, depicting direction of travel,
        sail angle and rudder angle

        Args:
            world_surface (:obj pygame.Surface): surface of world
            :param linear_scale:
            :param world_surface:

        """
        # ToDo:
        #  Update this entire function so its not such a hack
        #  Likely more elegant with sprite sheets

        width, height = world_surface.get_size()

        # boat_size roughly 30x smaller
        boat_size = boat_width, boat_height = height / 30, height / 30

        boat_surface_rect = pygame.Rect(0, 0, boat_size[0], boat_size[1])

        boat_surface_rect.center = linear_scale(self.position[0], self.position[1])

        boat_pivot = boat_surface_rect.center

        boat_fill_rect = pygame.Rect(0, 0, boat_size[0] // 2, boat_size[1])

        boat_fill_rect.center = boat_size[0] // 2, boat_size[1] // 2

        boat_surface = pygame.Surface(boat_size)
        boat_surface.fill((112, 82, 0), rect=boat_fill_rect)

        fill_rect = pygame.Rect(0, 0, boat_width, boat_height // 4)
        fill_rect.center = boat_fill_rect.center
        sail_surface = pygame.Surface(boat_size)
        sail_surface.fill((160, 160, 228), rect=fill_rect)

        boat_surface = pygame.transform.rotozoom(boat_surface, 90 - self.heading_angle, 1)
        rotated_boat_surface_rect = boat_surface.get_rect(center=boat_pivot)

        sail_surface = pygame.transform.rotozoom(sail_surface, 90 - self.heading_angle, 1)
        sail_surface = pygame.transform.rotozoom(sail_surface, 90 - self.sail_angle, 1)
        sail_surface_rect = boat_surface.get_rect(center=boat_pivot)

        sail_surface.set_colorkey((0, 0, 0))
        sail_surface.convert_alpha()

        boat_surface.set_colorkey((0, 0, 0))
        boat_surface.convert_alpha()

        world_surface.blit(boat_surface, rotated_boat_surface_rect)
        world_surface.blit(sail_surface, sail_surface_rect)
