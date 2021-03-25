import re
import pygame
import os
import numpy as np


class TileEngine:
    def __init__(self, path_dir, size, meters_per_block):

        self.texture_dir_path = path_dir + '/textures'
        self.tiles = np.genfromtxt(path_dir + '/world.csv', delimiter=',')

        self.n_rows, self.n_columns = self.tiles.shape
        self.meter_per_block = meters_per_block

        self.tile_rect_map = [[pygame.Rect(x * 256, y * 256, 256, 256) for x in range(self.n_columns)] for y in
                              range(self.n_rows)]

        self.tile_textures = self._init_tile_dict(path_dir + '/tiles.txt')

        self.collidables_id = set()

        self.render_rect, self.world_surface = self._generate_surface(size)

        self.surface_size = self.world_surface.get_size()

        self.working_surface = pygame.Surface(self.surface_size)

    def scale(self, spherical=True):
        """Returns a world scale function, converting meters into a pixel location"""
        window_width, window_height = self.surface_size
        world_width, world_height = self.n_columns*self.meter_per_block, self.meter_per_block*self.n_rows

        def s_scale(x, y):
            return (x * window_width / world_width) % window_width, (y * window_height / world_height) % window_height

        def scale(x, y):
            return (x * window_width / world_width), (y * window_height / world_height)

        if spherical:
            return s_scale
        else:
            return scale

    def _parse_line(self, string):
        """
        private member function reads an input string, validates it is a correct fill type entry returning
        the fill type information
        Args:
            string: string variable detailing an entry into the tiles.txt file
        Returns
            None: if string is invalid
            tile_id, (fill_type, color|texture_path)
        """
        regex_valid_entry = re.compile('\d,(color|texture):(\s+|)(\(\d+,\d+,\d+\)|.+\.png)')
        match = regex_valid_entry.match(string)
        regex_id = re.compile('\d+,')
        tile_id = int(regex_id.search(string).group()[:-1])

        regex_type = re.compile('(color|texture)')
        fill_type = regex_type.findall(string)[0]

        if fill_type == 'color':
            regex_colors = re.compile('(\d+,|\d+\))')
            color_match = regex_colors.findall(string)
            color = int(color_match[1][:-1]), int(color_match[2][:-1]), int(color_match[3][:-1])
            return tile_id, (fill_type, color)

        if fill_type == 'texture':
            regex_texture_path = re.compile(':.+\.png')
            texture_path_match = regex_texture_path.findall(string)
            texture_path = texture_path_match[0][1:]
            texture = pygame.image.load(os.path.abspath(self.texture_dir_path + '/' + texture_path))
            texture = pygame.transform.scale(texture, (256, 256))
            texture = texture.convert()
            return tile_id, (fill_type, texture)

    def _init_tile_dict(self, path):
        """Reads a txt file with the key value pairs relating the tile_id to the desired texture/colour
            Args:
                path: string variable of path to look up txt file
            Returns:
                success: returns boolean true/false if text file values successfully imported
        """
        tile_textures = {}
        f = open(path, "r")
        for line in f:
            tile_id, fill_data = self._parse_line(str(line))
            tile_textures[tile_id] = fill_data

        return tile_textures

    def get_collidables(self):
        # ToDo:
        """Returns a list of rect objects detailing the location of a collidable tile square
            Returns:
                collidables: a list of rect objects corresponding to the collidable tile squares
        """
        pass

    def _generate_surface(self, size):
        """Generate world surface from world data"""

        world_surface = pygame.Surface((self.n_columns * 256, self.n_rows * 256))

        for y in range(self.n_rows):
            for x in range(self.n_columns):
                tile_id = self.tiles[y][x]
                rect = self.tile_rect_map[y][x]
                fill_type, dat = self.tile_textures[tile_id]
                if fill_type == 'color':
                    color = dat
                    world_surface.fill(color, rect=rect)
                if fill_type == 'texture':
                    texture = dat
                    world_surface.blit(texture, rect)

        width, height = size

        if width > height:
            tile_side_length = height // self.n_rows
            blit_height = height
            blit_width = self.n_columns * tile_side_length
            border_width = (width - blit_width) // 2
            render_rect = pygame.Rect(border_width, 0, blit_width, blit_height)
        else:
            tile_side_length = width // self.n_columns
            blit_width = width
            blit_height = self.n_rows * tile_side_length
            border_height = (height - blit_height) // 2
            render_rect = pygame.Rect(0, border_height, blit_width, blit_height)

        world_surface = pygame.transform.scale(world_surface, render_rect.size)

        return render_rect, world_surface

    def render(self, input_surface: pygame.Surface):
        """Takes a pygame rendering tile squares with the correct texture information
            Args:
                :param input_surface:
            Returns:
                None
        """
        input_surface.blit(self.working_surface, self.render_rect)
        self.working_surface.blit(self.world_surface, self.working_surface.get_rect())
