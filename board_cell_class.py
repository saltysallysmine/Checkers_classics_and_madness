import pygame
from constants import *


class BoardCell:
    def __init__(self):
        self.color = None

        self.unfocused_color = None
        self.focused_color = None
        self.free_for_capture_color = None

        self.focused = False
        self.captured = False

        self.set_cell_color()

    def set_cell_color(self):
        # cur_focused_color = pygame.Color(FOCUSED_CELL_COLOR)
        # cur_capture_color = pygame.Color(UNFOCUSED_CELL_COLOR)
        #
        # hsv = pygame.Color(self.unfocused_color).hsva
        # if hsv[2] + 10 < 100:
        #     cur_focused_color.hsva = (hsv[0], hsv[1], hsv[2] + 10, hsv[3])
        #     cur_capture_color.hsva = (hsv[0], (hsv[1] + 40) % 100, hsv[2], hsv[3])
        # else:
        #     cur_focused_color.hsva = ((hsv[0] + 10) % 360, hsv[1], hsv[2], hsv[3])
        #     cur_capture_color.hsva = ((hsv[0] + 40) % 360, hsv[1], hsv[2], hsv[3])
        #
        # self.focused_color = tuple(cur_focused_color)
        # self.free_for_capture_color = tuple(cur_capture_color)
        self.color = UNFOCUSED_CELL_COLOR

        self.unfocused_color = UNFOCUSED_CELL_COLOR
        self.focused_color = FOCUSED_CELL_COLOR
        self.free_for_capture_color = FREE_FOR_CAPTURE_COLOR

    def get_cell_color(self):
        return self.color

    def set_focused_status(self, status):
        self.focused = status

        if not self.captured:
            if self.focused:
                self.color = self.focused_color
            else:
                self.color = self.unfocused_color

    def set_captured_status(self, status):
        self.captured = status

        if self.captured:
            self.color = self.free_for_capture_color
        else:
            if self.focused:
                self.color = self.focused_color
            else:
                self.color = self.unfocused_color

    def render(self, screen, cell_size, cur_cell_x, cur_cell_y):
        cur_color = BORDERS_COLOR
        pygame.draw.rect(
            screen, pygame.Color(cur_color),
            (cur_cell_x, cur_cell_y, cell_size, cell_size),
            3  # , border_radius=8
        )

        cur_color = self.color
        pygame.draw.rect(
            screen, pygame.Color(cur_color),
            (cur_cell_x + 3, cur_cell_y + 3,
             cell_size - 6, cell_size - 6),
            0  # , border_radius=5
        )
