import sys

import pygame

import constants
from board_class import Board, BACKGROUND_COLOR, set_scheme
from buttons_classes import Button

from checkers_image import render_checker


def terminate():
    pygame.quit()
    sys.exit()


def render_title(screen):
    font = pygame.font.Font(None, 120)
    title_text = font.render('Checkers', True, pygame.Color(constants.TEXT_COLOR))
    title_text_rect = title_text.get_rect(center=(center_w, center_h - 150))
    screen.blit(title_text, title_text_rect)


def menu_stage_logic(event_list, menu_buttons, screen):
    # we need to remake this and remove using of 'global'
    global menu_stage

    play, wild_madness_squared, exit = menu_buttons

    for event in event_list:
        if event.type == pygame.QUIT:
            terminate()

        if event.type == pygame.MOUSEMOTION:
            for button in menu_buttons:
                button.get_motion(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play.is_focused(event.pos):
                play.set_pushed_color()
                board_scheme = [
                    [0, 2, 0, 2, 0, 2, 0, 2],
                    [2, 0, 2, 0, 2, 0, 2, 0],
                    [0, 2, 0, 2, 0, 2, 0, 2],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                ]
                set_scheme(board_scheme)
                menu_stage = False
            if wild_madness_squared.is_focused(event.pos):
                wild_madness_squared.set_pushed_color()
                board_scheme = [
                    [0, 4, 0, 4, 0, 4, 0, 4],
                    [4, 0, 4, 0, 4, 0, 4, 0],
                    [0, 4, 0, 4, 0, 4, 0, 4],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [3, 0, 3, 0, 3, 0, 3, 0],
                    [0, 3, 0, 3, 0, 3, 0, 3],
                    [3, 0, 3, 0, 3, 0, 3, 0],
                ]
                set_scheme(board_scheme)
                menu_stage = False

            if exit.is_focused(event.pos):
                exit_button.set_pushed_color()
                terminate()

        if event.type == pygame.MOUSEBUTTONUP:
            for button in menu_buttons:
                if button.is_button_pushed(event.pos):
                    button.button_unpushed(event.pos)

    for button in menu_buttons:
        button.render(screen)

    render_title(screen)
    # render_checker(screen, 1, 150, center_w - 250, center_h - 400)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Checkers')

    info_object = pygame.display.Info()
    size = width, height = info_object.current_w, info_object.current_h
    center_w, center_h = width // 2, height // 2
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    board = Board(8, 8)
    board.set_view(center_w, center_h, 90, central=True)
    board.set_mouse(pygame.mouse)

    constants.change_theme('sea of cerenity')

    start_game_button = Button((center_w, center_h + 50), (500, 50), "Play")
    start_game_button.head_is_center()
    wild_madness_squared = Button((center_w, center_h + 150), (500, 50), "Wild Madness Squared")
    wild_madness_squared.head_is_center()
    exit_button = Button((center_w, center_h + 250), (500, 50), "Exit")
    exit_button.head_is_center()
    menu_buttons = [start_game_button, wild_madness_squared, exit_button]

    # fps
    fps = 60
    clock = pygame.time.Clock()

    running = True
    menu_stage = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        event_list = pygame.event.get()

        if menu_stage:
            menu_stage_logic(event_list, menu_buttons, screen)

        if not menu_stage:
            for event in event_list:
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.MOUSEMOTION:
                    board.cell_highlighting(event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    board.release_piece()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_stage = True
            board.render(screen)

        pygame.display.flip()

        clock.tick()
