import pygame
import numpy as np


class wind_effect(object):
    def __init__(self, surface_size):

        self.wind_velocity = [20,20]
        self.wind_position = [0,0]

        self.surface_size = self.width, self.height = surface_size[0], surface_size[1],

        self.spacing = self.width // 15

        self.particles = [pygame.Rect(i*self.spacing, 0, 1, self.height) for i in range(20)]

        self.wind_surface = pygame.Surface(self.surface_size)
        self.wind_surface.fill((255, 0, 255))
        self.working_surface = self.wind_surface.copy()

        for rect in self.particles:
            self.wind_surface.fill((255, 255, 255), rect=rect)

    def render(self, world_surface: pygame.Surface, linear_scale):
        self.working_surface = self.wind_surface.copy()

        for i in range(40):
            new_rect = pygame.Rect(self.width, i*self.height//10, self.width, self.height//10)
            new_rect.center = linear_scale(self.wind_position[0], self.wind_position[1] + i*self.height//10)
            self.working_surface.fill((255, 0, 255), rect=new_rect)
            self.working_surface.set_colorkey((255, 0, 255))
            self.working_surface.convert_alpha()

        c = world_surface.get_rect().center

        self.working_surface = pygame.transform.rotate(self.working_surface, 0)

        rect = self.working_surface.get_rect(center=c)

        world_surface.blit(self.working_surface, rect)

        self.wind_position[1] += self.wind_velocity[1]



