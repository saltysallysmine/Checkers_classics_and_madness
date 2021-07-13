import pygame
from constants import *


class Button:
    def __init__(self, head, btn_size, text):
        self.head = self.head_x, self.head_y = head
        self.size = self.width, self.height = btn_size
        self.text = text
        self.btn_color = BUTTON_COLOR
        self.border_color = BORDERS_COLOR
        self.is_active = True
        self.auto_size_change()

    def render(self, screen):
        # button
        pygame.draw.rect(screen, pygame.Color(self.border_color),
                         (self.head, self.size), 3, border_radius=10)

        pygame.draw.rect(screen, pygame.Color(self.btn_color),
                         (self.head_x + 3, self.head_y + 3,
                          self.width - 6, self.height - 6), 0,
                         border_radius=5)

        # text
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, True, pygame.Color(TEXT_COLOR))
        text_rect = text.get_rect(center=(self.head_x + self.width // 2,
                                          self.head_y + self.height // 2))
        screen.blit(text, text_rect)

    def auto_size_change(self):
        # text rectangle
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, True, pygame.Color(TEXT_COLOR))
        text_rect = text.get_rect(center=(self.head_x + self.width // 2,
                                          self.head_y + self.height // 2))
        # compare the values of size
        self.width = max(self.width, text_rect.size[0] + 20)
        self.height = max(self.height, text_rect.size[1] + 20)
        self.size = (self.width, self.height)

    def set_head_pos(self, head):
        self.head = self.head_x, self.head_y = head

    def head_is_center(self, hd_is_cen=True):
        if hd_is_cen:
            self.head_x -= self.width // 2
            self.head_y -= self.height // 2
        else:
            self.head_x += self.width // 2
            self.head_y += self.height // 2
        self.head = self.head_x, self.head_y

    def set_active(self, active):
        self.is_active = active
        self.btn_color = INACTIVE_CELL_COLOR

    def is_focused(self, cur_pos):
        return 0 < cur_pos[0] - self.head_x < self.width \
               and 0 < cur_pos[1] - self.head_y < self.height

    def get_motion(self, cur_pos):
        if self.is_active:
            if self.is_focused(cur_pos):
                self.btn_color = FOCUSED_BUTTON_COLOR
            else:
                self.btn_color = BUTTON_COLOR

    def set_pushed_color(self):
        self.btn_color = PUSHED_BUTTON_COLOR

    def is_button_pushed(self, cur_pos):
        return self.is_focused(cur_pos)

    def button_unpushed(self, cur_pos):
        if self.is_focused(cur_pos) and self.is_active:
            self.btn_color = FOCUSED_BUTTON_COLOR
