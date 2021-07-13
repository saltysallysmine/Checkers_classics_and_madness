import os
import pygame

white_man = None
black_man = None
white_king = None
black_king = None
sign_to_checker = None


def __load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_all_checkers():
    global white_man, black_man, white_king, black_king, sign_to_checker

    colorkey = -1
    white_man = __load_image('Checker_1.png', colorkey)
    black_man = __load_image('Checker_2.png', colorkey)
    white_king = __load_image('Checker_3.png', colorkey)
    black_king = __load_image('Checker_4.png', colorkey)

    sign_to_checker = {
        1: white_man, 2: black_man, 3: white_king, 4: black_king
    }


def render_checker(screen, piece_sign, cell_size, cur_cell_x, cur_cell_y):
    global white_man, black_man, white_king, black_king, sign_to_checker

    piece_img = sign_to_checker[piece_sign]
    piece_img = pygame.transform.scale(piece_img, (cell_size - 8, cell_size - 8))

    screen.blit(piece_img, (cur_cell_x + 4, cur_cell_y + 4))
