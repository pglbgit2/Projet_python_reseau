import os
import sys

sys.path.insert(0, '..')
# Add the parent directory to the PYTHONPATH


import pygame as pg
import sys

import pygame as pg
from View.camera import *
from View.settings import *
import Model.logique as l
import Model.matrice as m
import View.game as g


class Map:

    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.matrixNature = [
            [10058, 10054, 10061, 10060, 10055, 10055, 10060, 0, 10036, 10032, 30152, 30172, 30121, 30121, 30121, 30121,
             30131, 0, 0, 0, 0, 0, 10055, 10057, 10054, 10058, 10060, 10042, 10047, 10036, 10032, 10052, 10061, 10058,
             10060, 10043, 0, 0, 0, 10033],
            [10058, 10058, 10058, 10060, 10051, 10060, 10054, 10053, 10052, 10052, 10052, 30154, 30172, 30121, 30121,
             30121, 30170, 30133, 30133, 30133, 30144, 0, 0, 10032, 10031, 10054, 10045, 10047, 10036, 10055, 0, 10036,
             10060, 10061, 10054, 10057, 10031, 0, 0, 10033],
            [10057, 10059, 10061, 10059, 10049, 10059, 10057, 10042, 10047, 10036, 10036, 10052, 30153, 30141, 30142,
             30143, 30172, 30121, 30121, 30121, 30129, 0, 10056, 10057, 10054, 10055, 10060, 10036, 10036, 10032, 10036,
             10061, 10042, 10043, 10047, 10052, 10052, 10031, 0, 10033],
            [10057, 10061, 10060, 10036, 10055, 10054, 10052, 10052, 10038, 10033, 10053, 10061, 10044, 10054, 10045,
             10060, 30154, 30143, 30172, 30121, 30170, 30144, 0, 10032, 10036, 10042, 10047, 10043, 10031, 10045, 10054,
             10056, 10057, 10050, 10055, 10031, 10031, 10040, 10040, 10033],
            [10050, 10032, 10036, 10055, 10058, 10058, 10059, 10060, 10061, 10044, 10043, 10045, 0, 10031, 0, 10052,
             10051, 0, 30154, 30172, 30121, 30170, 30147, 0, 10036, 10036, 10032, 10031, 10040, 0, 0, 0, 10061, 10060,
             10057, 10055, 10054, 10056, 10057, 0],
            [10054, 10051, 10052, 10053, 10057, 10055, 10061, 10033, 10033, 10038, 10053, 10042, 10040, 10036, 10035,
             10057, 10045, 0, 0, 30152, 30172, 30121, 30170, 30133, 30144, 10036, 10047, 10045, 10032, 10036, 10043,
             10042, 10047, 10055, 10056, 10057, 10060, 10061, 10040, 10032],
            [10054, 10051, 10052, 10047, 10040, 10055, 10042, 10036, 10038, 10036, 10042, 10045, 10036, 10036, 10032,
             10040, 10037, 10038, 10033, 0, 30154, 30172, 30121, 30121, 30170, 30133, 30135, 30133, 30133, 30146, 0, 0,
             10031, 10032, 0, 10055, 10043, 10058, 10057, 10045],
            [10056, 10060, 10054, 10052, 10053, 10057, 10055, 10042, 10036, 10061, 10045, 10042, 10036, 10042, 0, 10032,
             10057, 10036, 10040, 0, 0, 30152, 30172, 30121, 30121, 30121, 30121, 30121, 30121, 30170, 30144, 0, 10060,
             10059, 10052, 10053, 10043, 10047, 10032, 10049],
            [10050, 10040, 10055, 10061, 10055, 10045, 0, 10038, 10040, 10036, 10032, 10036, 10042, 10044, 0, 0, 10032,
             10057, 10040, 10040, 10040, 0, 30154, 30172, 30121, 30121, 30121, 30121, 30121, 30121, 30170, 30146, 0,
             10045, 10054, 10055, 10036, 10031, 10040, 10051],
            [10055, 10060, 10056, 10054, 10037, 10061, 10044, 10044, 10044, 10042, 10036, 10036, 10040, 10044, 0, 0, 0,
             0, 10057, 10037, 10040, 10032, 0, 30152, 30172, 30121, 30121, 30121, 30121, 30121, 30121, 30129, 0, 30151,
             30145, 0, 10056, 10060, 10031, 10036],
            [10060, 10055, 10060, 10056, 10054, 10042, 10052, 10040, 10053, 10055, 10040, 10037, 10041, 10044, 0, 0, 0,
             0, 0, 0, 10037, 10035, 10032, 0, 30152, 30172, 30121, 30121, 30121, 30121, 30121, 30170, 30133, 30171,
             30129, 0, 10032, 10040, 10036, 10036],
            [10061, 10041, 10041, 10041, 10036, 10036, 10036, 0, 0, 10033, 10032, 10033, 10047, 10043, 0, 10057, 0, 0,
             0, 10040, 10040, 10040, 0, 0, 0, 30152, 30141, 30143, 30142, 30141, 30172, 30121, 30121, 30121, 30170,
             30147, 10031, 10032, 10036, 10037],
            [10055, 10038, 10034, 10037, 10053, 10040, 0, 0, 10036, 10034, 10036, 10045, 10045, 10038, 10035, 10037,
             10055, 10045, 0, 0, 10038, 10037, 10040, 10032, 10034, 10033, 10034, 10036, 10038, 10040, 30152, 30140,
             30172, 30121, 30121, 30170, 30146, 10036, 30165, 10040],
            [10058, 10036, 10034, 10036, 10035, 0, 0, 0, 10042, 10036, 10061, 10045, 10042, 10045, 10047, 10036, 10032,
             10057, 10045, 0, 0, 10052, 10038, 10038, 10032, 10055, 10061, 10043, 10045, 0, 0, 0, 30153, 30143, 30172,
             30121, 30170, 30135, 30174, 30134],
            [10055, 10032, 10036, 10042, 0, 0, 0, 0, 0, 10044, 10045, 10042, 10045, 10047, 10036, 10032, 10061, 10055,
             10034, 10037, 0, 10042, 10045, 10047, 10038, 10032, 10057, 10045, 10045, 10036, 0, 0, 10045, 10054, 30154,
             30143, 30172, 30121, 30121, 30121],
            [10052, 10035, 10034, 10041, 10042, 0, 0, 0, 0, 0, 10061, 10045, 10042, 10045, 10047, 10036, 10032, 10057,
             10045, 10045, 10036, 0, 10042, 10045, 10045, 10040, 10032, 10057, 10045, 10045, 10036, 0, 0, 10045, 10054,
             10040, 30154, 30143, 30172, 30121],
            [10052, 10038, 10038, 10036, 10036, 10034, 0, 0, 0, 0, 0, 10045, 10045, 10036, 0, 0, 10045, 10054, 10040, 0,
             0, 10055, 10054, 10051, 10052, 10045, 10040, 10055, 10042, 10036, 10061, 10045, 10042, 10045, 10036, 0,
             10042, 10045, 30154, 30142],
            [0, 0, 10034, 10036, 10032, 10036, 10045, 0, 0, 0, 0, 0, 10034, 10036, 10032, 10036, 0, 10036, 0, 0, 10045,
             10054, 10040, 0, 0, 10055, 10044, 10041, 10052, 10053, 10057, 10055, 10042, 10036, 0, 0, 0, 0, 0, 10054],
            [0, 0, 0, 0, 0, 10044, 10034, 10040, 0, 0, 0, 0, 0, 0, 0, 10057, 10055, 10042, 10036, 0, 0, 0, 0, 0, 10054,
             10036, 10045, 10047, 10042, 10032, 10057, 10045, 10045, 10036, 0, 10042, 10045, 10047, 10036, 10032],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 10036, 10033, 10033, 10033, 10036, 10036, 10040, 10036, 0, 10036, 10040, 0, 0, 0, 0, 0, 0,
             0, 10033, 0, 0, 10033, 10036, 10041, 10041, 10034, 10036, 10036, 10037, 10033, 10033, 10032, 0, 0, 10034],
            [30146, 0, 0, 10033, 10047, 10053, 10040, 10042, 10053, 10044, 10034, 10034, 10034, 10031, 10036, 0, 0, 0,
             0, 10054, 10033, 10035, 10035, 10037, 10040, 10049, 10046, 10044, 10038, 10037, 10045, 10043, 10035, 10040,
             10042, 10044, 10040, 10040, 10033, 10031],
            [30170, 30144, 0, 0, 10036, 10040, 10040, 10040, 10042, 10033, 0, 0, 0, 10052, 0, 0, 0, 0, 0, 10033, 10036,
             30139, 10041, 10038, 10042, 10035, 10047, 10044, 10044, 10044, 10043, 10042, 10041, 10050, 10040, 0, 10047,
             0, 10040, 10044],
            [30121, 30170, 30147, 0, 0, 10053, 10036, 10036, 10047, 10047, 0, 0, 0, 0, 10047, 0, 10037, 10037, 10037,
             10037, 10033, 10035, 10042, 10042, 10042, 10042, 10043, 10045, 10050, 10060, 10060, 10049, 10061, 10040,
             10054, 10046, 10050, 0, 10053, 10060],
            [30141, 30172, 30170, 30135, 30147, 0, 0, 10040, 10040, 10050, 0, 0, 0, 0, 0, 0, 0, 20378, 10054, 10041,
             10042, 10043, 10044, 10045, 10044, 10043, 10042, 10041, 10040, 10040, 39, 10038, 10037, 10037, 10038,
             10042, 10044, 10037, 10060, 10054],
            [0, 30152, 30172, 30121, 30131, 0, 0, 10036, 10042, 10043, 10044, 0, 0, 0, 20384, 0, 0, 20383, 20371, 10035,
             20377, 0, 0, 0, 0, 10037, 10053, 10053, 10038, 10038, 10053, 10035, 0, 0, 10037, 10050, 10060, 10040,
             10054, 10055],
            [10033, 0, 30152, 30172, 30170, 30133, 30147, 0, 0, 10052, 10053, 0, 0, 0, 0, 0, 0, 10043, 20372, 20372, 0,
             10040, 10037, 10038, 0, 10038, 0, 10053, 10053, 10054, 10045, 10044, 10046, 10047, 10058, 10060, 10044,
             10042, 10054, 10054],
            [10030, 10033, 10037, 30139, 30121, 30121, 30131, 0, 0, 10040, 0, 0, 20379, 20372, 0, 0, 0, 10044, 10033, 0,
             0, 0, 20381, 10033, 0, 0, 10053, 10037, 10037, 10036, 10056, 10060, 10040, 10050, 0, 0, 10038, 10034,
             10054, 10046],
            [0, 10037, 10044, 30152, 30172, 30121, 30170, 30144, 10036, 0, 0, 0, 0, 20378, 0, 0, 10033, 10037, 10044,
             10036, 0, 0, 0, 0, 20380, 10033, 0, 0, 10038, 10053, 0, 10035, 10034, 10034, 10036, 10036, 10040, 10050,
             10042, 10038],
            [10043, 10038, 10036, 10044, 30152, 30172, 30121, 30170, 30146, 0, 0, 0, 0, 20381, 10037, 10036, 10056,
             10060, 10060, 10042, 0, 10035, 0, 0, 0, 20378, 0, 0, 0, 10034, 10047, 10042, 10044, 10040, 10050, 10060,
             10059, 10058, 10036, 10038],
            [10042, 10040, 10052, 10033, 0, 30138, 30121, 30121, 30170, 30144, 20374, 0, 0, 0, 10035, 10044, 10042,
             10038, 10034, 10043, 0, 10045, 0, 0, 0, 20381, 20374, 0, 0, 0, 0, 10036, 10038, 10040, 10037, 10036, 0, 0,
             10047, 10053],
            [10047, 10036, 10036, 10036, 0, 30154, 30172, 30121, 30121, 30129, 0, 0, 0, 20380, 10040, 10060, 10050,
             10055, 10061, 10034, 10040, 10042, 10041, 0, 0, 0, 20372, 20374, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10033],
            [10037, 10047, 0, 0, 0, 20371, 30152, 30172, 30121, 30170, 30145, 10033, 10060, 10042, 10043, 10058, 10047,
             10061, 10061, 10061, 10059, 10056, 10059, 0, 0, 0, 20381, 20372, 20377, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [10036, 0, 20374, 0, 0, 0, 20371, 30152, 30140, 30172, 30170, 30144, 10043, 10059, 10042, 10046, 10046,
             10046, 10042, 0, 10050, 10043, 0, 10054, 10055, 20378, 0, 0, 20382, 20375, 0, 20371, 0, 0, 20372, 0, 0, 0,
             20372, 20372],
            [20372, 20372, 20374, 20371, 20371, 20377, 20374, 0, 0, 30137, 30121, 30170, 30133, 30144, 10033, 10044,
             10040, 10042, 10041, 10041, 10041, 10058, 10060, 10058, 10034, 10044, 0, 0, 0, 0, 0, 0, 0, 0, 20378, 0, 0,
             0, 0, 0],
            [20374, 20374, 20374, 20374, 20371, 20375, 20377, 20374, 0, 30138, 30121, 30121, 30121, 30131, 10053, 10036,
             10040, 10042, 10044, 10043, 10035, 10057, 10042, 10060, 10043, 10050, 10061, 10061, 20375, 20378, 20378,
             20376, 20375, 0, 20371, 20377, 20376, 20375, 20374, 20372],
            [20374, 20377, 20374, 20372, 20372, 20376, 20372, 0, 0, 30139, 30121, 30121, 30121, 30131, 0, 10040, 10036,
             0, 10052, 10047, 10036, 0, 0, 10031, 10045, 10040, 10053, 0, 0, 0, 0, 0, 20377, 20372, 20372, 20374, 20372,
             20371, 20371, 20372]
        ]

        # self.perlin_scale = grid_length_x/2
        self.overlay = ""
        self.grass_tiles = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.map = None
        self.create_map()
        self.map_walkeur = None

    def draw_mini(self, screen, camera):

        # pg.draw.rect(screen, BLACK, (pg.display.Info().current_w - 500, pg.display.Info().current_h - 100, 144.3, 111))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                # render_pos = self.map[x][y]["render_pos"]
                # tile = self.map[x][y]["tile"]
                tile1 = m.Mat_batiment[y][x].id
                # minimap
                minimap_offset = [83, 90]
                render_pos_mini = self.map[x][y]["render_pos_mini"]

                # WATER
                if tile1 == 1:
                    """pg.draw.circle(screen, BLUE, (
                        render_pos_mini[0] + pg.display.Info().current_w - 130 + minimap_offset[0],
                        render_pos_mini[1] + pg.display.Info().current_h - 1040 + minimap_offset[1]), 2)
                    """
                    pg.draw.circle(screen, BLUE, (
                        render_pos_mini[0] + pg.display.Info().current_w - minimap_offset[0],
                        render_pos_mini[1] + minimap_offset[1]), 2)

                # ROCK
                elif tile1 == 2:
                    pg.draw.circle(screen, GREY, (
                        render_pos_mini[0] + pg.display.Info().current_w - minimap_offset[0],
                        render_pos_mini[1] + minimap_offset[1]), 2)

                # TREE
                elif tile1 == 3:
                    pg.draw.circle(screen, GREEN, (
                        render_pos_mini[0] + pg.display.Info().current_w - minimap_offset[0],
                        render_pos_mini[1] + minimap_offset[1]), 2)

                elif tile1 == 5:
                    pg.draw.circle(screen, RED, (
                        render_pos_mini[0] + pg.display.Info().current_w - minimap_offset[0],
                        render_pos_mini[1] + minimap_offset[1]), 2)

                elif tile1 not in (666, 0):
                    pg.draw.circle(screen, ORANGE, (
                        render_pos_mini[0] + pg.display.Info().current_w - minimap_offset[0],
                        render_pos_mini[1] + minimap_offset[1]), 2)

                mini = self.map[x][y]["iso_poly_mini"]
                mini = [(x + pg.display.Info().current_w - minimap_offset[0], y + minimap_offset[1]) for x, y
                        in mini]
                pg.draw.polygon(screen, YELLOW, mini, 2)
                pg.draw.rect(screen, RED, (
                pg.display.Info().current_w - 153.5 - camera.scroll_mini.x, 65 + camera.scroll_mini.y, 26, 20), 1)
                # pg.draw.circle(screen, RED, (1382.5 + 13 - camera.scroll_mini.x, 59.5 + 10 + camera.scroll_mini.y), 5)

    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))
        self.overlay = l.get_overlay()

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.map[y][x]["render_pos"]
                if self.overlay == "":

                    if m.Mat_batiment[x][y].id_bat == 55 and m.Mat_batiment[x][y].curEmployees == l.m.Mat_batiment[x][y].neededEmployees:
                        m.Mat_batiment[x][y].texture = "security_occupied"
                    elif m.Mat_batiment[x][y].id_bat == 81 and l.m.Mat_batiment[x][y].curEmployees == l.m.Mat_batiment[x][y].neededEmployees:
                        m.Mat_batiment[x][y].texture = "engineer_occupied"
                    elif m.Mat_batiment[x][y].id_bat == 555 and m.Mat_fire[x][y] == 1:
                        m.Mat_batiment[x][y].texture = "ruine_in_fire"
                    elif m.Mat_batiment[x][y].id_bat == 555 and m.Mat_fire[x][y] == 0:
                        m.Mat_batiment[x][y].texture = "ruine"

                    if m.Mat_batiment[x][y].pos_x + m.Mat_batiment[x][y].nbr_cases - 1 == y and \
                       m.Mat_batiment[x][y].pos_y + m.Mat_batiment[x][y].nbr_cases - 1 == x:
                        tile = m.Mat_batiment[x][y].texture
                    else:
                        tile = "block"

                    if tile != "":
                        if tile in sizedbuildings_2:
                            screen.blit(self.tiles[tile],
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 - TILE_SIZE + camera.scroll.x,
                                         render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                        elif tile in sizedbuildings_3:
                            screen.blit(self.tiles[tile],
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 - TILE_SIZE * 2 + camera.scroll.x,
                                         render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                        else:
                            screen.blit(self.tiles[tile],
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                         render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                elif self.overlay == "fire":

                    risk = l.get_fire_level(y, x)

                    if risk >= 24:  # WORST : need Pin-Pon asap
                        tile = "red"
                    elif 24 > risk >= 18:
                        tile = "orange"
                    elif 18 > risk >= 12:
                        tile = "yellow"
                    elif 12 > risk >= 6:
                        tile = "green"
                    elif 6 > risk >= 0:  # BEST : disable smoke detectors
                        tile = "blue"

                    elif m.Mat_batiment[x][y].id_bat == 55:
                        if m.Mat_batiment[x][y].curEmployees == l.m.Mat_batiment[x][y].neededEmployees:
                            tile = "security_occupied"
                        else:
                            tile = "security"

                    elif m.Mat_batiment[x][y].id_bat == 555 and m.Mat_fire[x][y] == 1:
                        m.Mat_batiment[x][y].texture = "ruine_in_fire"
                        tile = "ruine_in_fire"

                    elif m.Mat_batiment[x][y].id_bat == 555 and m.Mat_fire[x][y] == 0:
                        m.Mat_batiment[x][y].texture = "ruine"
                        tile = "ruine"

                    elif m.Mat_batiment[x][y].id_bat in (1, 2, 3, 5, 666, 116, 115):
                        tile = m.Mat_batiment[x][y].texture

                    else:
                        tile = ""

                    if tile != "":
                        if tile in sizedbuildings_2:
                            screen.blit(self.tiles[tile],
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 - TILE_SIZE + camera.scroll.x,
                                         render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                        elif tile in sizedbuildings_3:
                            screen.blit(self.tiles[tile],
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 - TILE_SIZE * 2 + camera.scroll.x,
                                         render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                        else:
                            screen.blit(self.tiles[tile],
                                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                         render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                elif self.overlay == "bat":

                    risk = l.get_eff_level(y, x)

                    if risk >= 24:  # WORST : need a dispenser here
                        tile = "red"
                    elif 24 > risk >= 18:
                        tile = "orange"
                    elif 18 > risk >= 12:
                        tile = "yellow"
                    elif 12 > risk >= 6:
                        tile = "green"
                    elif 6 > risk >= 0:  # BEST : No spy around
                        tile = "blue"

                    elif m.Mat_batiment[x][y].id_bat == 81:
                        if l.m.Mat_batiment[x][y].curEmployees == l.m.Mat_batiment[x][y].neededEmployees:
                            tile = "engineer_occupied"
                        else:
                            tile = "engineer"

                    elif m.Mat_batiment[x][y].id_bat == 555:
                        tile = "ruine"

                    elif m.Mat_batiment[x][y].id_bat in (1, 2, 3, 5, 666, 116, 115):
                        tile = m.Mat_batiment[x][y].texture

                    else:
                        tile = ""

                    if tile != "":
                        if tile in sizedbuildings_2:
                             screen.blit(self.tiles[tile],
                                             (render_pos[
                                                 0] + self.grass_tiles.get_width() / 2 - TILE_SIZE + camera.scroll.x,
                                             render_pos[1] - (
                                                         self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                        elif tile in sizedbuildings_3:
                            screen.blit(self.tiles[tile],
                                            (render_pos[
                                                 0] + self.grass_tiles.get_width() / 2 - TILE_SIZE * 2 + camera.scroll.x,
                                             render_pos[1] - (
                                                         self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                        else:
                            screen.blit(self.tiles[tile],
                                            (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                             render_pos[1] - (
                                                         self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                elif self.overlay == "water":
                    if l.get_water(y, x):

                        if m.Mat_batiment[x][y].id_bat in (10, 11, 12):
                            tile = "house_watered"
                        else:
                            tile = "watered"

                    elif not l.get_water(y, x):
                        tile = "unwatered"

                    else:
                        tile = ""

                        # Water services

                    if m.Mat_batiment[x][y].id_bat == 92:
                        tile = "well"

                    elif m.Mat_batiment[x][y].id_bat == 91:
                        tile = "fountain_full"

                    elif m.Mat_batiment[x][y].id_bat == 9100:
                        tile = "fountain_full"

                    elif m.Mat_batiment[x][y].id_bat == 90:
                        tile = "reservoir_empty"

                    elif m.Mat_batiment[x][y].id_bat == 9000:
                        tile = "reservoir_full"

                    if tile != "":
                        screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     render_pos[1] - (
                                             self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    
                if l.getWalker(y, x).name != 'no Walker':  # Vérifier si un/des walkeur/s est/sont sur la case actuelle
                    tile = self.grid_to_walkeur(y, x, l.getWalker(y, x))
                    if tile != "":
                        screen.blit(self.tiles[tile], (
                        render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                        render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

    def create_map(self):

        map = []

        for grid_x in range(self.grid_length_x):
            map.append([])
            for grid_y in range(self.grid_length_y):
                map_tile = self.grid_to_map(grid_x, grid_y)
                map[grid_x].append(map_tile)
                render_pos = map_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))
        self.map = map

    def grid_to_map(self, grid_x, grid_y):

        self.overlay = l.get_overlay()

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        rect_mini_map = [
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            ((grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP), grid_y * TILE_SIZE_MINI_MAP),
            ((grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP), (grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP)),
            (grid_x * TILE_SIZE_MINI_MAP, (grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP))
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        iso_poly_mini = [self.cart_to_iso(x, y) for x, y in rect_mini_map]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        minx_mini = min([x for x, y in iso_poly_mini])
        miny_mini = min([y for x, y in iso_poly_mini])

        if m.Mat_batiment[grid_y][grid_x] == 666:
            tile = ""

        if m.Mat_batiment[grid_y][grid_x].id == 3:  # TREES
            if self.matrixNature[grid_x][grid_y] == 10033:
                m.Mat_batiment[grid_y][grid_x].texture = "tree33"
            elif self.matrixNature[grid_x][grid_y] == 10030:
                m.Mat_batiment[grid_y][grid_x].texture = "tree30"
            elif self.matrixNature[grid_x][grid_y] == 10037:
                m.Mat_batiment[grid_y][grid_x].texture = "tree37"
            elif self.matrixNature[grid_x][grid_y] == 10058:
                m.Mat_batiment[grid_y][grid_x].texture = "tree58"
            elif self.matrixNature[grid_x][grid_y] == 10056:
                m.Mat_batiment[grid_y][grid_x].texture = "tree56"
            elif self.matrixNature[grid_x][grid_y] == 10054:
                m.Mat_batiment[grid_y][grid_x].texture = "tree54"
            elif self.matrixNature[grid_x][grid_y] == 10061:
                m.Mat_batiment[grid_y][grid_x].texture = "tree61"
            elif self.matrixNature[grid_x][grid_y] == 10060:
                m.Mat_batiment[grid_y][grid_x].texture = "tree60"
            elif self.matrixNature[grid_x][grid_y] == 10055:
                m.Mat_batiment[grid_y][grid_x].texture = "tree55"
            elif self.matrixNature[grid_x][grid_y] == 10051:
                m.Mat_batiment[grid_y][grid_x].texture = "tree51"
            elif self.matrixNature[grid_x][grid_y] == 10041:
                m.Mat_batiment[grid_y][grid_x].texture = "tree41"
            elif self.matrixNature[grid_x][grid_y] == 10057:
                m.Mat_batiment[grid_y][grid_x].texture = "tree57"
            elif self.matrixNature[grid_x][grid_y] == 10031:
                m.Mat_batiment[grid_y][grid_x].texture = "tree31"
            elif self.matrixNature[grid_x][grid_y] == 10032:
                m.Mat_batiment[grid_y][grid_x].texture = "tree32"
            elif self.matrixNature[grid_x][grid_y] == 10035:
                m.Mat_batiment[grid_y][grid_x].texture = "tree35"
            elif self.matrixNature[grid_x][grid_y] == 10052:
                m.Mat_batiment[grid_y][grid_x].texture = "tree52"
            elif self.matrixNature[grid_x][grid_y] == 10053:
                m.Mat_batiment[grid_y][grid_x].texture = "tree53"
            elif self.matrixNature[grid_x][grid_y] == 10059:
                m.Mat_batiment[grid_y][grid_x].texture = "tree59"
            elif self.matrixNature[grid_x][grid_y] == 10049:
                m.Mat_batiment[grid_y][grid_x].texture = "tree49"
            elif self.matrixNature[grid_x][grid_y] == 10046:
                m.Mat_batiment[grid_y][grid_x].texture = "tree46"
            elif self.matrixNature[grid_x][grid_y] == 10050:
                m.Mat_batiment[grid_y][grid_x].texture = "tree50"
            elif self.matrixNature[grid_x][grid_y] == 10036:
                m.Mat_batiment[grid_y][grid_x].texture = "tree36"
            elif self.matrixNature[grid_x][grid_y] == 10034:
                m.Mat_batiment[grid_y][grid_x].texture = "tree34"
            elif self.matrixNature[grid_x][grid_y] == 10038:
                m.Mat_batiment[grid_y][grid_x].texture = "tree38"
            elif self.matrixNature[grid_x][grid_y] == 10042:
                m.Mat_batiment[grid_y][grid_x].texture = "tree42"
            elif self.matrixNature[grid_x][grid_y] == 10047:
                m.Mat_batiment[grid_y][grid_x].texture = "tree47"
            elif self.matrixNature[grid_x][grid_y] == 10045:
                m.Mat_batiment[grid_y][grid_x].texture = "tree45"
            elif self.matrixNature[grid_x][grid_y] == 10043:
                m.Mat_batiment[grid_y][grid_x].texture = "tree43"
            elif self.matrixNature[grid_x][grid_y] == 10040:
                m.Mat_batiment[grid_y][grid_x].texture = "tree40"
            elif self.matrixNature[grid_x][grid_y] == 10044:
                m.Mat_batiment[grid_y][grid_x].texture = "tree44"
            else:
                m.Mat_batiment[grid_y][grid_x].texture = ""

        elif m.Mat_batiment[grid_y][grid_x] == 115:
            m.Mat_batiment[grid_y][grid_x].texture = "direction1"
        elif m.Mat_batiment[grid_y][grid_x] == 116:
            m.Mat_batiment[grid_y][grid_x].texture = "direction2"

        elif m.Mat_batiment[grid_y][grid_x].id == 2:  # ROCKS
            if self.matrixNature[grid_x][grid_y] == 20384:
                m.Mat_batiment[grid_y][grid_x].texture = "rock1"
            elif self.matrixNature[grid_x][grid_y] == 20376:
                m.Mat_batiment[grid_y][grid_x].texture = "rock2"
            elif self.matrixNature[grid_x][grid_y] == 20372:
                m.Mat_batiment[grid_y][grid_x].texture = "rock3"
            elif self.matrixNature[grid_x][grid_y] == 20374:
                m.Mat_batiment[grid_y][grid_x].texture = "rock4"
            elif self.matrixNature[grid_x][grid_y] == 20377:
                m.Mat_batiment[grid_y][grid_x].texture = "rock5"
            elif self.matrixNature[grid_x][grid_y] == 20371:
                m.Mat_batiment[grid_y][grid_x].texture = "rock6"
            elif self.matrixNature[grid_x][grid_y] == 20380:
                m.Mat_batiment[grid_y][grid_x].texture = "rock7"
            elif self.matrixNature[grid_x][grid_y] == 20381:
                m.Mat_batiment[grid_y][grid_x].texture = "rock8"
            elif self.matrixNature[grid_x][grid_y] == 20379:
                m.Mat_batiment[grid_y][grid_x].texture = "rock9"
            elif self.matrixNature[grid_x][grid_y] == 20378:
                m.Mat_batiment[grid_y][grid_x].texture = "rock10"
            elif self.matrixNature[grid_x][grid_y] == 20383:
                m.Mat_batiment[grid_y][grid_x].texture = "rock11"
            elif self.matrixNature[grid_x][grid_y] == 20382:
                m.Mat_batiment[grid_y][grid_x].texture = "rock12"
            elif self.matrixNature[grid_x][grid_y] == 20375:
                m.Mat_batiment[grid_y][grid_x].texture = "rock13"
            elif self.matrixNature[grid_x][grid_y] == 20300:
                m.Mat_batiment[grid_y][grid_x].texture = "rock300"
            else:
                m.Mat_batiment[grid_y][grid_x].texture = ""

        elif m.Mat_batiment[grid_y][grid_x].id == 1:  # WATER
            if self.matrixNature[grid_x][grid_y] == 30152:
                m.Mat_batiment[grid_y][grid_x].texture = "water1"
            elif self.matrixNature[grid_x][grid_y] == 30121:
                m.Mat_batiment[grid_y][grid_x].texture = "water"
            elif self.matrixNature[grid_x][grid_y] == 30153:
                m.Mat_batiment[grid_y][grid_x].texture = "water2"
            elif self.matrixNature[grid_x][grid_y] == 30154:
                m.Mat_batiment[grid_y][grid_x].texture = "water4"
            elif self.matrixNature[grid_x][grid_y] == 30172:
                m.Mat_batiment[grid_y][grid_x].texture = "water3"
            elif self.matrixNature[grid_x][grid_y] == 30131:
                m.Mat_batiment[grid_y][grid_x].texture = "water5"
            elif self.matrixNature[grid_x][grid_y] == 30141:
                m.Mat_batiment[grid_y][grid_x].texture = "water6"
            elif self.matrixNature[grid_x][grid_y] == 30142:
                m.Mat_batiment[grid_y][grid_x].texture = "water7"
            elif self.matrixNature[grid_x][grid_y] == 30143:
                m.Mat_batiment[grid_y][grid_x].texture = "water8"
            elif self.matrixNature[grid_x][grid_y] == 30170:
                m.Mat_batiment[grid_y][grid_x].texture = "water9"
            elif self.matrixNature[grid_x][grid_y] == 30135:
                m.Mat_batiment[grid_y][grid_x].texture = "water10"
            elif self.matrixNature[grid_x][grid_y] == 30133:
                m.Mat_batiment[grid_y][grid_x].texture = "water11"
            elif self.matrixNature[grid_x][grid_y] == 30144:
                m.Mat_batiment[grid_y][grid_x].texture = "water12"
            elif self.matrixNature[grid_x][grid_y] == 30129:
                m.Mat_batiment[grid_y][grid_x].texture = "water13"
            elif self.matrixNature[grid_x][grid_y] == 30147:
                m.Mat_batiment[grid_y][grid_x].texture = "water14"
            elif self.matrixNature[grid_x][grid_y] == 30146:
                m.Mat_batiment[grid_y][grid_x].texture = "water15"
            elif self.matrixNature[grid_x][grid_y] == 30140:
                m.Mat_batiment[grid_y][grid_x].texture = "water16"
            elif self.matrixNature[grid_x][grid_y] == 30151:
                m.Mat_batiment[grid_y][grid_x].texture = "water17"
            elif self.matrixNature[grid_x][grid_y] == 30171:
                m.Mat_batiment[grid_y][grid_x].texture = "water18"
            elif self.matrixNature[grid_x][grid_y] == 30145:
                m.Mat_batiment[grid_y][grid_x].texture = "water19"
            elif self.matrixNature[grid_x][grid_y] == 30165:
                m.Mat_batiment[grid_y][grid_x].texture = "water20"
            elif self.matrixNature[grid_x][grid_y] == 30174:
                m.Mat_batiment[grid_y][grid_x].texture = "water21"
            elif self.matrixNature[grid_x][grid_y] == 30134:
                m.Mat_batiment[grid_y][grid_x].texture = "water22"
            elif self.matrixNature[grid_x][grid_y] == 30156:
                m.Mat_batiment[grid_y][grid_x].texture = "water23"
            elif self.matrixNature[grid_x][grid_y] == 30139:
                m.Mat_batiment[grid_y][grid_x].texture = "water24"
            elif self.matrixNature[grid_x][grid_y] == 30138:
                m.Mat_batiment[grid_y][grid_x].texture = "water25"
            elif self.matrixNature[grid_x][grid_y] == 30137:
                m.Mat_batiment[grid_y][grid_x].texture = "water26"
            else:
                m.Mat_batiment[grid_y][grid_x].texture = ""
        """
        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) != 5:
            tile = "roadYL"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) != 5:
            tile = "roadXL_captop"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) != 5:
            tile = "roadXL_capbottom"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,6) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 4) != 5:
            tile = "roadXL"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y,6) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 4) != 5:
            tile = "roadYL_capright"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,6) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 4) != 5:
            tile = "roadYL_capleft"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) != 5:
            tile = "roadXL_teeright"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5:
            tile = "roadXL_teeleft"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5:
            tile = "roadYL_teetop"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5:
            tile = "roadYL_teebottom"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5:
            tile = "roadcurv_lefttobottom"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5:
            tile = "roadcurv_lefttotop"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) != 5:
            tile = "roadcurv_righttotop"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) != 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) != 5:
            tile = "roadcurv_righttobottom"

        elif self.matrix[grid_x][grid_y] == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y,4) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5 and self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5:
            tile = "road_quad"


        elif self.matrix[grid_x][grid_y] == 5 and not any([self.get_neighbor(self.matrix, grid_x, grid_y, 0) == 5,
                                                            self.get_neighbor(self.matrix, grid_x, grid_y, 3) == 5,
                                                           self.get_neighbor(self.matrix, grid_x, grid_y, 4) == 5,
                                                           self.get_neighbor(self.matrix, grid_x, grid_y, 6) == 5]):

            tile = "roadYL_capright"
        
        else : 
            tile = ""

        if self.overlay == "":

            #HOUSING

            if self.matrix[grid_x][grid_y] == 7:
                tile = "post_sign"

            elif self.matrix[grid_x][grid_y] == 10:
                tile = "houselvl0"

            elif self.matrix[grid_x][grid_y] == 11:
                tile = "houselvl1"

            elif self.matrix[grid_x][grid_y] == 12:
                tile = "houselvl2"

            elif self.matrix[grid_x][grid_y] == 13:
                tile = "houselvl3"

            #Service publique
            if self.matrix[grid_x][grid_y] == 55:
                if l.m.Mat_batiment[grid_y][grid_x].curEmployees == l.m.Mat_batiment[grid_y][grid_x].neededEmployees:
                    tile = "security_occupied"
                else:
                    tile = "security"

            elif self.matrix[grid_x][grid_y] == 81:
                if l.m.Mat_batiment[grid_y][grid_x].curEmployees == l.m.Mat_batiment[grid_y][grid_x].neededEmployees:
                    tile = "engineer_occupied"
                else:
                    tile = "engineer"

            #Commerce

            elif self.matrix[grid_x][grid_y] == 70:
                tile = "market"

            elif self.matrix[grid_x][grid_y] == 71:
                tile = "granary"

            elif self.matrix[grid_x][grid_y] == 72:
                tile = "warehouse"

            elif self.matrix[grid_x][grid_y] == 100:
                tile = "farm"

            #Water services

            elif self.matrix[grid_x][grid_y] == 92:
                tile = "well"

            elif self.matrix[grid_x][grid_y] == 91:
                tile = "fountain_full"

            elif self.matrix[grid_x][grid_y] == 9100:
                tile = "fountain_full"

            elif self.matrix[grid_x][grid_y] == 90:
                tile = "reservoir_empty"

            elif self.matrix[grid_x][grid_y] == 9000:
                tile = "reservoir_full"

            #TEMPLE

            elif self.matrix[grid_x][grid_y] == 60:
                tile = "temple_farming"
            elif self.matrix[grid_x][grid_y] == 61:
                tile = "temple_shipping"
            elif self.matrix[grid_x][grid_y] == 62:
                tile = "temple_commerce"
            elif self.matrix[grid_x][grid_y] == 63:
                tile = "temple_war"
            elif self.matrix[grid_x][grid_y] == 64:
                tile = "temple_love"

            #Aléa

            elif self.matrix[grid_x][grid_y] == 555:
                tile = "ruine"
            elif l.m.Mat_fire[grid_y][grid_x] == 1:
                tile = "ruine_in_fire"


        elif self.overlay == "water":

            if l.get_water(grid_x, grid_y):

                if self.matrix[grid_x][grid_y] in (10, 11, 12):
                    tile = "house_watered"
                else:
                    tile = "watered"

            elif not l.get_water(grid_x, grid_y):
                tile = "unwatered"

            else:
                tile = ""

            # Water services

            if self.matrix[grid_x][grid_y] == 92:
                tile = "well"

            elif self.matrix[grid_x][grid_y] == 91:
                tile = "fountain_full"

            elif self.matrix[grid_x][grid_y] == 9100:
                tile = "fountain_full"

            elif self.matrix[grid_x][grid_y] == 90:
                tile = "reservoir_empty"

            elif self.matrix[grid_x][grid_y] == 9000:
                tile = "reservoir_full"

        elif self.overlay == "fire":

            risk = l.get_fire_level(grid_x, grid_y)

            if risk >= 24: #WORST : need Pin-Pon asap
                tile = "red"
            elif 24 > risk >= 18:
                tile = "orange"
            elif 18 > risk >= 12:
                tile = "yellow"
            elif 12 > risk >= 6:
                tile = "green"
            elif 6 > risk >= 0: #BEST : disable smoke detectors
                tile = "blue"

            if self.matrix[grid_x][grid_y] == 55:
                if l.m.Mat_batiment[grid_y][grid_x].curEmployees == l.m.Mat_batiment[grid_y][grid_x].neededEmployees:
                    tile = "security_occupied"
                else:
                    tile = "security"

            elif self.matrix[grid_x][grid_y] == 555 and l.m.Mat_fire[grid_y][grid_x] == 1:
                tile = "ruine_in_fire"

            elif self.matrix[grid_x][grid_y] == 555 and l.m.Mat_fire[grid_y][grid_x] == 0:
                tile = "ruine"

        elif self.overlay == "bat":

            risk = l.get_eff_level(grid_x, grid_y)

            if risk >= 24:  # WORST : need a dispenser here
                tile = "red"
            elif 24 > risk >= 18:
                tile = "orange"
            elif 18 > risk >= 12:
                tile = "yellow"
            elif 12 > risk >= 6:
                tile = "green"
            elif 6 > risk >= 0:  # BEST : No spy around
                tile = "blue"

            if self.matrix[grid_x][grid_y] == 81:
                if l.m.Mat_batiment[grid_y][grid_x].curEmployees == l.m.Mat_batiment[grid_y][grid_x].neededEmployees:
                    tile = "engineer_occupied"
                else:
                    tile = "engineer"

            elif self.matrix[grid_x][grid_y] == 555:
                tile = "ruine"
        """

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "cart_rect_mini_map": rect_mini_map,
            "iso_poly": iso_poly,
            "iso_poly_mini": iso_poly_mini,
            "render_pos": [minx, miny],
            "render_pos_mini": [minx_mini, miny_mini],
        }

        return out

    def grid_to_walkeur(self, grid_x, grid_y, walker):

        self.overlay = l.get_overlay()

        if walker.name != "no Walker":

            Mov_x = walker.x - walker.prev_x  # +1 -1 0
            Mov_y = walker.y - walker.prev_y  # +1 -1 0

            if Mov_x == 0 and Mov_y == 1:
                temp = 3
            elif Mov_x == 0 and Mov_y == -1:
                temp = 0
            elif Mov_x == 1 and Mov_y == 0:
                temp = 1
            elif Mov_x == -1 and Mov_y == 0:
                temp = 2
            else:
                temp = 0

            if self.overlay == "":  # AKA map d'eau, map de feu ou map de risque d'effondrement

                if (walker.name == "Priest"):
                    tile = "priest" + str(temp)

                elif (walker.name == "Delivery_Guy"):
                    tile = "random" + str(temp)

                elif (walker.name == "Engineer"):
                    tile = "engineer" + str(temp)

                elif (walker.name == "Prefect"):
                    tile = "prefet" + str(temp)

                elif (walker.name == "Food_Guy"):
                    tile = "foodguy" + str(temp)

                elif (walker.name == "Immigrant"):
                    tile = "random" + str(temp)

                elif (walker.name == "Recruteur"):
                    tile = "random" + str(temp)

                else:
                    tile = ""

            elif (self.overlay == "fire"):  # OVERLAY FIRE
                if (walker.name == "Prefect"):
                    tile = "prefet" + str(temp)
                else:
                    tile = ""  # NE PAS AFFICHER LES AUTRES WALKERS

            elif (self.overlay == "bat"):  # OVERLAY BAT
                if (walker.name == "Engineer"):
                    tile = "engineer" + str(temp)
                else:
                    tile = ""  # NE PAS AFFICHER LES AUTRES WALKERS

            elif (self.overlay == "water"):
                tile = ""

            else:
                tile = ""

        else:
            tile = ""

        return tile

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def load_images(self):

        # NATURE

        block = pg.image.load(path_to_Nature + "/Land1a_00255.png").convert_alpha()
        tree33 = pg.image.load(path_to_Nature + "/Land1a_00033.png").convert_alpha()
        tree30 = pg.image.load(path_to_Nature + "/Land1a_00030.png").convert_alpha()
        tree37 = pg.image.load(path_to_Nature + "/Land1a_00037.png").convert_alpha()
        tree54 = pg.image.load(path_to_Nature + "/Land1a_00054.png").convert_alpha()
        tree58 = pg.image.load(path_to_Nature + "/Land1a_00058.png").convert_alpha()
        tree51 = pg.image.load(path_to_Nature + "/Land1a_00051.png").convert_alpha()
        tree55 = pg.image.load(path_to_Nature + "/Land1a_00055.png").convert_alpha()
        tree61 = pg.image.load(path_to_Nature + "/Land1a_00061.png").convert_alpha()
        tree60 = pg.image.load(path_to_Nature + "/Land1a_00060.png").convert_alpha()
        tree57 = pg.image.load(path_to_Nature + "/Land1a_00057.png").convert_alpha()
        tree46 = pg.image.load(path_to_Nature + "/Land1a_00046.png").convert_alpha()
        tree41 = pg.image.load(path_to_Nature + "/Land1a_00041.png").convert_alpha()
        tree31 = pg.image.load(path_to_Nature + "/Land1a_00031.png").convert_alpha()
        tree32 = pg.image.load(path_to_Nature + "/Land1a_00032.png").convert_alpha()
        tree34 = pg.image.load(path_to_Nature + "/Land1a_00034.png").convert_alpha()
        tree35 = pg.image.load(path_to_Nature + "/Land1a_00035.png").convert_alpha()
        tree36 = pg.image.load(path_to_Nature + "/Land1a_00036.png").convert_alpha()
        tree38 = pg.image.load(path_to_Nature + "/Land1a_00038.png").convert_alpha()
        tree42 = pg.image.load(path_to_Nature + "/Land1a_00042.png").convert_alpha()
        tree45 = pg.image.load(path_to_Nature + "/Land1a_00045.png").convert_alpha()
        tree47 = pg.image.load(path_to_Nature + "/Land1a_00047.png").convert_alpha()
        tree52 = pg.image.load(path_to_Nature + "/Land1a_00052.png").convert_alpha()
        tree53 = pg.image.load(path_to_Nature + "/Land1a_00053.png").convert_alpha()
        tree59 = pg.image.load(path_to_Nature + "/Land1a_00059.png").convert_alpha()
        tree49 = pg.image.load(path_to_Nature + "/Land1a_00049.png").convert_alpha()
        tree50 = pg.image.load(path_to_Nature + "/Land1a_00050.png").convert_alpha()
        tree56 = pg.image.load(path_to_Nature + "/Land1a_00056.png").convert_alpha()
        tree43 = pg.image.load(path_to_Nature + "/Land1a_00043.png").convert_alpha()
        tree40 = pg.image.load(path_to_Nature + "/Land1a_00040.png").convert_alpha()
        tree44 = pg.image.load(path_to_Nature + "/Land1a_00044.png").convert_alpha()
        tree46 = pg.image.load(path_to_Nature + "/Land1a_00046.png").convert_alpha()
        rock1 = pg.image.load(path_to_Nature + "/Land3a_00084.png").convert_alpha()
        rock2 = pg.image.load(path_to_Nature + "/Land3a_00076.png").convert_alpha()
        rock3 = pg.image.load(path_to_Nature + "/Land3a_00072.png").convert_alpha()
        rock4 = pg.image.load(path_to_Nature + "/Land3a_00074.png").convert_alpha()
        rock5 = pg.image.load(path_to_Nature + "/Land3a_00077.png").convert_alpha()
        rock6 = pg.image.load(path_to_Nature + "/Land3a_00071.png").convert_alpha()
        rock7 = pg.image.load(path_to_Nature + "/Land3a_00080.png").convert_alpha()
        rock8 = pg.image.load(path_to_Nature + "/Land3a_00081.png").convert_alpha()
        rock9 = pg.image.load(path_to_Nature + "/Land3a_00079.png").convert_alpha()
        rock10 = pg.image.load(path_to_Nature + "/Land3a_00078.png").convert_alpha()
        rock11 = pg.image.load(path_to_Nature + "/Land3a_00083.png").convert_alpha()
        rock12 = pg.image.load(path_to_Nature + "/Land3a_00082.png").convert_alpha()
        rock13 = pg.image.load(path_to_Nature + "/Land3a_00075.png").convert_alpha()
        direction1 = pg.image.load(path_to_Nature + "/Land3a_00089.png").convert_alpha()
        direction2 = pg.image.load(path_to_Nature + "/Land3a_00087.png").convert_alpha()
        water = pg.image.load(path_to_Nature + "/Land1a_00121.png").convert_alpha()
        water1 = pg.image.load(path_to_Nature + "/Land1a_00152.png").convert_alpha()
        water2 = pg.image.load(path_to_Nature + "/Land1a_00153.png").convert_alpha()
        water3 = pg.image.load(path_to_Nature + "/Land1a_00172.png").convert_alpha()
        water4 = pg.image.load(path_to_Nature + "/Land1a_00154.png").convert_alpha()
        water5 = pg.image.load(path_to_Nature + "/Land1a_00131.png").convert_alpha()
        water6 = pg.image.load(path_to_Nature + "/Land1a_00141.png").convert_alpha()
        water7 = pg.image.load(path_to_Nature + "/Land1a_00142.png").convert_alpha()
        water8 = pg.image.load(path_to_Nature + "/Land1a_00143.png").convert_alpha()
        water9 = pg.image.load(path_to_Nature + "/Land1a_00170.png").convert_alpha()
        water10 = pg.image.load(path_to_Nature + "/Land1a_00135.png").convert_alpha()
        water11 = pg.image.load(path_to_Nature + "/Land1a_00133.png").convert_alpha()
        water12 = pg.image.load(path_to_Nature + "/Land1a_00144.png").convert_alpha()
        water13 = pg.image.load(path_to_Nature + "/Land1a_00129.png").convert_alpha()
        water14 = pg.image.load(path_to_Nature + "/Land1a_00147.png").convert_alpha()
        water15 = pg.image.load(path_to_Nature + "/Land1a_00146.png").convert_alpha()
        water16 = pg.image.load(path_to_Nature + "/Land1a_00140.png").convert_alpha()
        water17 = pg.image.load(path_to_Nature + "/Land1a_00151.png").convert_alpha()
        water18 = pg.image.load(path_to_Nature + "/Land1a_00171.png").convert_alpha()
        water19 = pg.image.load(path_to_Nature + "/Land1a_00145.png").convert_alpha()
        water20 = pg.image.load(path_to_Nature + "/Land1a_00165.png").convert_alpha()
        water21 = pg.image.load(path_to_Nature + "/Land1a_00174.png").convert_alpha()
        water22 = pg.image.load(path_to_Nature + "/Land1a_00134.png").convert_alpha()
        water23 = pg.image.load(path_to_Nature + "/Land1a_00156.png").convert_alpha()
        water24 = pg.image.load(path_to_Nature + "/Land1a_00139.png").convert_alpha()
        water25 = pg.image.load(path_to_Nature + "/Land1a_00138.png").convert_alpha()
        water26 = pg.image.load(path_to_Nature + "/Land1a_00137.png").convert_alpha()
        rock300 = pg.image.load(path_to_Nature + "/Land1a_00300.png").convert_alpha()

        # ROADS

        road0 = pg.image.load(path_to_Nature + "/Land2a_00093.png").convert_alpha()  # Road YL
        road1 = pg.image.load(path_to_Nature + "/Land2a_00094.png").convert_alpha()  # Road XL
        road2 = pg.image.load(path_to_Nature + "/Land2a_00095.png").convert_alpha()  # Road YL
        road3 = pg.image.load(path_to_Nature + "/Land2a_00096.png").convert_alpha()  # Road XL
        road4 = pg.image.load(path_to_Nature + "/Land2a_00097.png").convert_alpha()
        road5 = pg.image.load(path_to_Nature + "/Land2a_00098.png").convert_alpha()
        road6 = pg.image.load(path_to_Nature + "/Land2a_00099.png").convert_alpha()
        road7 = pg.image.load(path_to_Nature + "/Land2a_00100.png").convert_alpha()
        road8 = pg.image.load(path_to_Nature + "/Land2a_00101.png").convert_alpha()
        road9 = pg.image.load(path_to_Nature + "/Land2a_00102.png").convert_alpha()
        road10 = pg.image.load(path_to_Nature + "/Land2a_00103.png").convert_alpha()
        road11 = pg.image.load(path_to_Nature + "/Land2a_00104.png").convert_alpha()
        road12 = pg.image.load(path_to_Nature + "/Land2a_00105.png").convert_alpha()
        road13 = pg.image.load(path_to_Nature + "/Land2a_00106.png").convert_alpha()
        road14 = pg.image.load(path_to_Nature + "/Land2a_00107.png").convert_alpha()
        road15 = pg.image.load(path_to_Nature + "/Land2a_00108.png").convert_alpha()
        road16 = pg.image.load(path_to_Nature + "/Land2a_00109.png").convert_alpha()
        road17 = pg.image.load(path_to_Nature + "/Land2a_00110.png").convert_alpha()

        # HOUSING

        post_sign = pg.image.load(path_to_House + "/Housng1a_00045.png").convert_alpha()
        houselvl0 = pg.image.load(path_to_House + "/Housng1a_00001.png").convert_alpha()
        houselvl0_0 = pg.image.load(path_to_House + "/Housng1a_00002.png").convert_alpha()
        houselvl0_1 = pg.image.load(path_to_House + "/Housng1a_00003.png").convert_alpha()
        houselvl0_2 = pg.image.load(path_to_House + "/Housng1a_00004.png").convert_alpha()
        bighouselvl0 = pg.image.load(path_to_House + "/Housng1a_00006.png").convert_alpha()
        houselvl1 = pg.image.load(path_to_House + "/Housng1a_00007.png").convert_alpha()
        houselvl1_0 = pg.image.load(path_to_House + "/Housng1a_00008.png").convert_alpha()
        houselvl1_1 = pg.image.load(path_to_House + "/Housng1a_00009.png").convert_alpha()
        houselvl1_2 = pg.image.load(path_to_House + "/Housng1a_00010.png").convert_alpha()
        bighouselvl1 = pg.image.load(path_to_House + "/Housng1a_00012.png").convert_alpha()
        houselvl2 = pg.image.load(path_to_House + "/Housng1a_00013.png").convert_alpha()
        houselvl2_0 = pg.image.load(path_to_House + "/Housng1a_00014.png").convert_alpha()
        houselvl2_1 = pg.image.load(path_to_House + "/Housng1a_00015.png").convert_alpha()
        houselvl2_2 = pg.image.load(path_to_House + "/Housng1a_00016.png").convert_alpha()
        bighouselvl2 = pg.image.load(path_to_House + "/Housng1a_00017.png").convert_alpha()
        houselvl3 = pg.image.load(path_to_House + "/Housng1a_00021.png").convert_alpha()
        bighouselvl3 = pg.image.load(path_to_House + "/Housng1a_00023.png").convert_alpha()

        # Warehouses and Market and Commerce

        warehouse = pg.image.load(path_to_Utilities + "/Warehouse.png").convert_alpha()
        granary = pg.image.load(path_to_Utilities + "/Grange.png").convert_alpha()
        granary_0 = pg.image.load(path_to_Utilities + "/Grange_0.png").convert_alpha()
        granary_1 = pg.image.load(path_to_Utilities + "/Grange_1.png").convert_alpha()
        market = pg.image.load(path_to_Utilities + "/Marche.png").convert_alpha()
        farm = pg.image.load(path_to_Utilities + "/farm.png").convert_alpha()

        # Service Publique/Fonctionnaires

        security = pg.image.load(path_to_Utilities + "/Security.png").convert_alpha()
        security_occupied = pg.image.load(path_to_Utilities + "/Security_occupied.png").convert_alpha()
        engineer = pg.image.load(path_to_Utilities + "/Engineer_post.png").convert_alpha()
        engineer_occupied = pg.image.load(path_to_Utilities + "/Engineer_post_occupied.png").convert_alpha()

        # Aléas

        ruine = pg.image.load(path_to_Utilities + "/Ruine.png").convert_alpha()
        ruine_in_fire = pg.image.load(path_to_Utilities + "/Ruine_en_feu.png").convert_alpha()

        # Water

        well = pg.image.load(path_to_Utilities + "/Puit.png").convert_alpha()
        fountain_empty = pg.image.load(path_to_Utilities + "/Fontaine_vide.png").convert_alpha()
        fountain_full = pg.image.load(path_to_Utilities + "/Fontaine_pleine.png").convert_alpha()
        reservoir_empty = pg.image.load(path_to_Utilities + "/Reservoir_vide.png").convert_alpha()
        reservoir_full = pg.image.load(path_to_Utilities + "/Reservoir_plein.png").convert_alpha()

        # Temples

        temple_farming = pg.image.load(path_to_Utilities + "/temple_FARMING.png").convert_alpha()
        temple_love = pg.image.load(path_to_Utilities + "/temple_LOVE.png").convert_alpha()
        temple_shipping = pg.image.load(path_to_Utilities + "/temple_SHIPPING.png").convert_alpha()
        temple_war = pg.image.load(path_to_Utilities + "/temple_WAR.png").convert_alpha()
        temple_commerce = pg.image.load(path_to_Utilities + "/temple_COMMERCE.png").convert_alpha()

        # Overlays

        red = pg.image.load(path_to_Utilities + "/Land2a_00043.png").convert_alpha()
        orange = pg.image.load(path_to_Utilities + "/Land2a_00041.png").convert_alpha()
        yellow = pg.image.load(path_to_Utilities + "/Land2a_00038.png").convert_alpha()  # MEDIUM
        green = pg.image.load(path_to_Utilities + "/Land2a_00036.png").convert_alpha()
        blue = pg.image.load(path_to_Utilities + "/Land2a_00034.png").convert_alpha()

        watered = pg.image.load(path_to_Utilities + "/EAU.png").convert_alpha()
        house_watered = pg.image.load(path_to_Utilities + "/EAU2.png").convert_alpha()
        unwatered = pg.image.load(path_to_Utilities + "/PAS_EAU.png").convert_alpha()

        case = pg.image.load(path_to_Utilities + "/case.png").convert_alpha()

        # Walkers

        priest0 = pg.image.load(path_to_Walkers + "/priest0.png").convert_alpha()
        priest1 = pg.image.load(path_to_Walkers + "/priest1.png").convert_alpha()
        priest2 = pg.image.load(path_to_Walkers + "/priest2.png").convert_alpha()
        priest3 = pg.image.load(path_to_Walkers + "/priest3.png").convert_alpha()

        engineer0 = pg.image.load(path_to_Walkers + "/Engineer0.png").convert_alpha()
        engineer1 = pg.image.load(path_to_Walkers + "/Engineer1.png").convert_alpha()
        engineer2 = pg.image.load(path_to_Walkers + "/Engineer2.png").convert_alpha()
        engineer3 = pg.image.load(path_to_Walkers + "/Engineer3.png").convert_alpha()

        prefet0 = pg.image.load(path_to_Walkers + "/Prefet0.png").convert_alpha()
        prefet1 = pg.image.load(path_to_Walkers + "/Prefet1.png").convert_alpha()
        prefet2 = pg.image.load(path_to_Walkers + "/Prefet2.png").convert_alpha()
        prefet3 = pg.image.load(path_to_Walkers + "/Prefet3.png").convert_alpha()

        foodguy0 = pg.image.load(path_to_Walkers + "/food_guy0.png").convert_alpha()
        foodguy1 = pg.image.load(path_to_Walkers + "/food_guy1.png").convert_alpha()
        foodguy2 = pg.image.load(path_to_Walkers + "/food_guy2.png").convert_alpha()
        foodguy3 = pg.image.load(path_to_Walkers + "/food_guy3.png").convert_alpha()

        random0 = pg.image.load(path_to_Walkers + "/Random0.png").convert_alpha()
        random1 = pg.image.load(path_to_Walkers + "/Random1.png").convert_alpha()
        random2 = pg.image.load(path_to_Walkers + "/Random2.png").convert_alpha()
        random3 = pg.image.load(path_to_Walkers + "/Random3.png").convert_alpha()

        return {"block": block,
                "tree33": tree33, "tree51": tree51, "tree55": tree55, "tree54": tree54, "tree36": tree36,
                "tree60": tree60, "tree61": tree61, "tree57": tree57, "tree56": tree56, "tree58": tree58,
                "tree31": tree31, "tree52": tree52, "tree59": tree59, "tree49": tree49, "tree50": tree50,
                "tree32": tree32, "tree53": tree53, "tree42": tree42, "tree47": tree47, "tree45": tree45,
                "tree43": tree43, "tree40": tree40, "tree30": tree30, "tree37": tree37, "tree44": tree44,
                "tree38": tree38, "tree35": tree35, "tree34": tree34, "tree46": tree46, "tree41": tree41,
                "rock1": rock1, "rock2": rock2, "rock3": rock3, "rock4": rock4, "rock5": rock5, "rock6": rock6,
                "rock7": rock7, "rock8": rock8, "rock9": rock9, "rock10": rock10, "rock11": rock11, "rock12": rock12,
                "rock13": rock13, "rock300": rock300,
                "water": water, "water1": water1, "water2": water2, "water3": water3, "water4": water4,
                "water5": water5, "water6": water6, "water7": water7, "water8": water8, "water9": water9,
                "water10": water10, "water11": water11, "water12": water12, "water13": water13, "water14": water14,
                "water15": water15, "water16": water16, "water17": water17, "water18": water18, "water19": water19,
                "water20": water20, "water21": water21, "water22": water22, "water23": water23, "water24": water24,
                "water25": water25, "water26": water26,
                "road0": road0,
                "road1": road1, "road2": road2, "road3": road3, "road4": road4, "road5": road5,
                "road6": road6, "road7": road7, "road8": road8, "road9": road9, "road10": road10,
                "road11": road11, "road12": road12, "road13": road13, "road14": road14, "road15": road15,
                "road16": road16, "road17": road17,
                "direction1": direction1, "direction2": direction2,
                "post_sign": post_sign,
                "houselvl0": houselvl0, "houselvl0_0": houselvl0_0, "houselvl0_1": houselvl0_1, "houselvl0_2": houselvl0_2,
                "houselvl1": houselvl1, "houselvl1_0": houselvl1_0, "houselvl1_1": houselvl1_1, "houselvl1_2": houselvl1_2,
                "houselvl2": houselvl2, "houselvl2_0": houselvl2_0, "houselvl2_1": houselvl2_1, "houselvl2_2": houselvl2_2,
                "houselvl3": houselvl3,
                "warehouse": warehouse,
                "granary": granary, "granary_0": granary_0, "granary_1": granary_1,
                "market": market, "farm": farm,
                "security": security, "security_occupied": security_occupied, "engineer": engineer,
                "engineer_occupied": engineer_occupied, "ruine": ruine, "ruine_in_fire": ruine_in_fire,
                "well": well, "fountain_empty": fountain_empty, "fountain_full": fountain_full,
                "reservoir_empty": reservoir_empty, "reservoir_full": reservoir_full,
                "temple_farming": temple_farming, "temple_love": temple_love, "temple_shipping": temple_shipping,
                "temple_war": temple_war, "temple_commerce": temple_commerce,
                "priest0": priest0, "priest1": priest1, "priest2": priest2, "priest3": priest3,
                "engineer0": engineer0, "engineer1": engineer1, "engineer2": engineer2, "engineer3": engineer3,
                "prefet0": prefet0, "prefet1": prefet1, "prefet2": prefet2, "prefet3": prefet3,
                "foodguy0": foodguy0, "foodguy1": foodguy1, "foodguy2": foodguy2, "foodguy3": foodguy3,
                "random0": random0, "random1": random1, "random2": random2, "random3": random3,
                "red": red, "orange": orange, "yellow": yellow, "green": green, "blue": blue,
                "watered": watered, "unwatered": unwatered, "house_watered": house_watered, "case": case

                }

    def get_neighbor(self, grid, coorX, coorY, who=4):

        max = 40 - 1

        if coorX == 0:
            if coorY == 0:  # case (0,0)
                if who == 6:  # BOTTOM NEIGHBOR
                    return grid[coorX][coorY + 1]
                elif who == 5:  # BOTTOM LEFT NEIGHBOR
                    return grid[coorX + 1][coorY + 1]
                elif who == 3:  # LEFT NEIGHBOR
                    return grid[coorX + 1][coorY]
                else:  # Error : unknown neighbor = return self
                    return grid[coorX][coorY]
            elif coorY == max:  # case (0,max)
                if who == 3:  # LEFT NEIGHBOR
                    return grid[coorX + 1][coorY]
                elif who == 1:  # TOP LEFT NEIGHBOR
                    return grid[coorX + 1][coorY - 1]
                elif who == 0:  # TOP NEIGHBOR
                    return grid[coorX][coorY - 1]
                else:  # Error : unknown neighbor = return self
                    return grid[coorX][coorY]
            else:  # case (0,y)
                if who == 6:  # BOTTOM NEIGHBOR
                    return grid[coorX][coorY + 1]
                if who == 5:  # BOTTOM LEFT NEIGHBOR
                    return grid[coorX + 1][coorY + 1]
                if who == 3:  # LEFT NEIGHBOR
                    return grid[coorX + 1][coorY]
                if who == 1:  # TOP LEFT NEIGHBOR
                    return grid[coorX + 1][coorY - 1]
                if who == 0:  # TOP NEIGHBOR
                    return grid[coorX][coorY - 1]
                else:  # Error : unknown neighbor = return self
                    return grid[coorX][coorY]

        elif coorX == max:
            if coorY == 0:  # case (max,0)
                if who == 4:  # RIGHT NEIGHBOR
                    return grid[coorX - 1][coorY]
                elif who == 7:  # BOTTOM RIGHT NEIGHBOR
                    return grid[coorX - 1][coorY + 1]
                elif who == 6:  # BOTTOM NEIGHBOR
                    return grid[coorX][coorY + 1]
                else:  # Error : unknown neighbor = return self
                    return grid[coorX][coorY]
            elif coorY == max:  # case(max,max)
                if who == 0:  # TOP NEIGHBOR
                    return grid[coorX][coorY - 1]
                elif who == 2:  # TOP LEFT NEIGHBOR
                    return grid[coorX - 1][coorY - 1]
                elif who == 4:  # RIGHT NEIGHBOR
                    return grid[coorX - 1][coorY]
                else:  # Error : unknown neighbor = return self
                    return grid[coorX][coorY]
            else:  # case(max,y)
                if who == 0:  # TOP NEIGHBOR
                    return grid[coorX][coorY - 1]
                elif who == 2:  # TOP LEFT NEIGHBOR
                    return grid[coorX - 1][coorY - 1]
                elif who == 4:  # RIGHT NEIGHBOR
                    return grid[coorX - 1][coorY]
                elif who == 7:  # BOTTOM RIGHT NEIGHBOR
                    return grid[coorX - 1][coorY + 1]
                elif who == 6:  # BOTTOM NEIGHBOR
                    return grid[coorX][coorY + 1]
                else:  # Error : unknown neighbor = return self
                    return grid[coorX][coorY]

        elif coorY == 0:  # case (x,0)
            if who == 3:  # LEFT NEIGHBOR
                return grid[coorX + 1][coorY]
            elif who == 4:  # RIGHT NEIGHBOR
                return grid[coorX - 1][coorY]
            elif who == 5:  # BOTTOM LEFT NEIGHBOR
                return grid[coorX + 1][coorY + 1]
            elif who == 6:  # BOTTOM NEIGHBOR
                return grid[coorX][coorY + 1]
            elif who == 7:  # BOTTOM RIGHT NEIGHBOR
                return grid[coorX - 1][coorY + 1]
            else:  # Error : unknown neighbor = return self
                return grid[coorX][coorY]

        elif coorY == max:  # case (x,max)
            if who == 3:  # LEFT NEIGHBOR
                return grid[coorX + 1][coorY]
            elif who == 1:  # TOP LEFT NEIGHBOR
                return grid[coorX + 1][coorY - 1]
            elif who == 0:  # TOP NEIGHBOR
                return grid[coorX][coorY - 1]
            elif who == 2:  # TOP RIGHT NEIGHBOR
                return grid[coorX - 1][coorY - 1]
            elif who == 4:  # RIGHT NEIGHBOR
                return grid[coorX - 1][coorY]
            else:  # Error : unknown neighbor = return self
                return grid[coorX][coorY]


        else:  # case(x,y) normal use
            if who == 0:  # TOP NEIGHBOR
                return grid[coorX][coorY - 1]
            elif who == 1:  # TOP LEFT NEIGHBOR
                return grid[coorX + 1][coorY - 1]
            elif who == 2:  # TOP RIGHT NEIGHBOR
                return grid[coorX - 1][coorY - 1]
            elif who == 3:  # LEFT NEIGHBOR
                return grid[coorX + 1][coorY]
            elif who == 4:  # RIGHT NEIGHBOR
                return grid[coorX - 1][coorY]
            elif who == 5:  # BOTTOM LEFT NEIGHBOR
                return grid[coorX + 1][coorY + 1]
            elif who == 6:  # BOTTOM NEIGHBOR
                return grid[coorX][coorY + 1]
            elif who == 7:  # BOTTOM RIGHT NEIGHBOR
                return grid[coorX - 1][coorY + 1]
            else:
                return grid[coorX][coorY]
