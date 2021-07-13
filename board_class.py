import logic_10_07 as logic
import pygame
import checkers_image
from constants import *
from board_cell_class import BoardCell


def set_scheme(board_scheme=None):
    if board_scheme is None:
        board_scheme = [
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 4, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 3, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
        ]
    logic.set_desk(board_scheme)


class Board:
    def __init__(self, board_width, board_height):
        self.cell_size = 50

        self.width = board_width
        self.height = board_height

        self.left = 100
        self.top = 100

        # rows and lines names
        self.lines_names = {}
        for i in range(1, 11):
            self.lines_names[i - 1] = str(i)

        self.rows_names = {}
        for i in range(65, 75):
            self.rows_names[i - 65] = chr(i)

        self.board = list()
        self.board_map = list()
        self.board_filling()

        self.last_highlighted_cell_cords = None

        self.clicked_cell = None

        self.captured_cells = []

        self.grabbed_piece = None

        self.mouse = None

        checkers_image.load_all_checkers()

    def board_filling(self):
        for line in range(self.height):
            cells_line = list()
            for cell in range(self.width):
                cur_cell = BoardCell()
                cells_line.append(cur_cell)

            self.board.append(cells_line)

    def set_view(self, left, top, cell_size, central=False):
        self.cell_size = cell_size

        self.left = left
        self.top = top

        if central:
            self.left -= self.width * self.cell_size // 2
            self.top -= self.height * self.cell_size // 2

    def set_mouse(self, mouse):
        self.mouse = mouse

    def get_cell(self, mouse_pos):
        mouse_is_on_board = \
            0 < mouse_pos[0] - self.left < self.cell_size * self.width and \
            0 < mouse_pos[1] - self.top < self.cell_size * self.height

        if mouse_is_on_board:
            clicked_cell_i = (mouse_pos[1] - self.top) // self.cell_size
            clicked_cell_j = (mouse_pos[0] - self.left) // self.cell_size

            return clicked_cell_i, clicked_cell_j

    def get_cell_cords_from_cell(self, cell_coords):
        i, j = cell_coords
        return self.left + j * self.cell_size, \
               self.top + i * self.cell_size

    def on_click(self, cell_coords):
        # cleaning last free for capture cells
        for cur_i, cur_j in self.captured_cells:
            self.board[cur_i][cur_j].set_captured_status(False)
        self.captured_cells.clear()

        # highlight new free for capture cells
        i, j = cell_coords
        self.board[i][j].set_captured_status(True)
        self.captured_cells.append(cell_coords)

        if logic.desk[i][j]:

            self.grab_piece(cell_coords)

            possible_moves = logic.moves(cell_coords)
            print(possible_moves)
            for move in possible_moves[0]:
                cur_i, cur_j = move

                self.board[cur_i][cur_j].set_captured_status(True)

                self.captured_cells.append(move)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def cell_highlighting(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        # the last focused cell update
        if self.last_highlighted_cell_cords is not None:
            reset_i, reset_j = self.last_highlighted_cell_cords
            self.board[reset_i][reset_j].set_focused_status(False)

        self.last_highlighted_cell_cords = cell

        # the currently focused cell update
        if cell is not None:
            self.board[cell[0]][cell[1]].set_focused_status(True)

    def grab_piece(self, cell_coords):
        self.grabbed_piece = cell_coords

    def release_piece(self):
        to_cell = self.get_cell(self.mouse.get_pos())
        from_cell = self.grabbed_piece

        if to_cell is not None and from_cell is not None:
            vector = logic.convert_coords_to_vector(from_cell, to_cell)
            if vector is not None:
                motion = logic.move(from_cell, vector)
                if motion:
                    for cell_i, cell_j in self.captured_cells:
                        self.board[cell_i][cell_j].set_captured_status(False)

                    self.captured_cells.clear()

        self.grabbed_piece = None

    def render_coordinates(self, screen):
        def rendering_symbol(symbol_number, symbol_x, symbol_y, rows=True):
            if rows:
                symbol = self.rows_names[symbol_number]
            else:
                symbol = self.lines_names[symbol_number]

            font = pygame.font.Font(None, self.cell_size)
            text = font.render(symbol, True, pygame.Color(TEXT_COLOR))
            text_rect = text.get_rect(center=(symbol_x + self.cell_size // 2,
                                              symbol_y + self.cell_size // 2))
            screen.blit(text, text_rect)

        # rendering rows names
        cur_x = self.left
        cur_y = self.top + self.cell_size * self.height
        for i in range(self.width):
            rendering_symbol(i, cur_x, cur_y)
            cur_x += self.cell_size

        # rendering lines names
        cur_x = self.left - self.cell_size
        cur_y = self.top
        for i in range(self.height - 1, -1, -1):
            rendering_symbol(i, cur_x, cur_y, rows=False)
            cur_y += self.cell_size

    def render_cells_and_pieces(self, screen):
        for i in range(self.height):
            cur_cell_x = self.left
            cur_cell_y = self.top + i * self.cell_size

            for j in range(self.width):
                self.board[i][j].render(screen, self.cell_size, cur_cell_x, cur_cell_y)

                piece_sign = logic.desk[i][j]
                if piece_sign != 0 and (i, j) != self.grabbed_piece:
                    checkers_image.render_checker(
                        screen, piece_sign, self.cell_size, cur_cell_x, cur_cell_y
                    )

                cur_cell_x += self.cell_size

    def render_grabbed_piece(self, screen):
        if self.grabbed_piece:
            i, j = self.grabbed_piece
            piece_sign = logic.desk[i][j]

            mouse_pos = self.mouse.get_pos()
            cur_i, cur_j = mouse_pos
            cur_i, cur_j = cur_i - self.cell_size // 2, cur_j - self.cell_size // 2

            # cur_i, cur_j = self.get_cell_cords_from_cell(self.get_cell(mouse_pos))

            checkers_image.render_checker(
                screen, piece_sign, self.cell_size, cur_i, cur_j
            )

    def render(self, screen):
        self.render_coordinates(screen)
        self.render_cells_and_pieces(screen)
        self.render_grabbed_piece(screen)
