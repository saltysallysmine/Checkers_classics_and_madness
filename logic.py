# Current desk state
# 0 - empty, 1 - white man, 2 - black man, 3 - white king, 4 - black king
desk = []
SIDE_LENGTH = 8
white_move = True
raise_message = 'No errors'
# move_vectors = [(-2, -2), (-2, 2), (2, 2), (2, -2)]
move_vectors = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
N_VECTORS = len(move_vectors)


def set_desk(desk_scheme, white_move_first=True):
    global desk, SIDE_LENGTH, white_move
    desk = desk_scheme
    SIDE_LENGTH = len(desk)

    white_move = white_move_first


def convert_coords_to_vector(coords_from, coords_to):
    from_i, from_j = coords_from
    to_i, to_j = coords_to

    if from_i == to_i or from_j == to_j:
        return None

    dif_i, dif_j = to_i - from_i, to_j - from_j

    if abs(dif_i) != abs(dif_j):
        return None

    # vector 0, 4, 8
    if dif_i < 0 and dif_j < 0:
        return (abs(dif_i) - 1) * 4
    # 1, 5, 9
    if dif_i < 0 and dif_j > 0:
        return (abs(dif_i) - 1) * 4 + 1
    # 2, 6, 10
    if dif_i > 0 and dif_j > 0:
        return (abs(dif_i) - 1) * 4 + 2
    # 3, 7, 11
    if dif_i > 0 and dif_j < 0:
        return (abs(dif_i) - 1) * 4 + 3


def valid_cell(cell):
    return 0 <= cell[0] < SIDE_LENGTH and 0 <= cell[1] < SIDE_LENGTH


def is_back_move(start, vector):
    return vector[0] > 0 and desk[start[0]][start[1]] == 1 or vector[0] < 0 and desk[start[0]][start[1]] == 2


def dist(start, to):
    current_pos = move_dest(start, to)[-1]
    ans = 0
    while valid_cell(current_pos):
        ans += 1
        current_pos = move_dest(current_pos, to)[-1]
    return ans


# Eat destination
def eat_dest(start, to):
    cells = move_dest(start, to + N_VECTORS * (dist(start, to) - 1))
    for i in cells:
        if is_enemy(desk[start[0]][start[1]], desk[i[0]][i[1]]) == 'enemy':
            return i
    return None


# Move destination
def move_dest(start, to):
    return [(start[0] + i * move_vectors[to % N_VECTORS][0], start[1] + i * move_vectors[to % N_VECTORS][1])
            for i in range(1, to // N_VECTORS + 2)]


# Check if can move
def can_move(start, to):
    global desk
    if desk[start[0]][start[1]] in (1, 2) and (to >= N_VECTORS or is_back_move(start, move_vectors[to % N_VECTORS])):
        return False
    dests = move_dest(start, to)
    for dest in dests:
        if not (0 <= dest[0] < SIDE_LENGTH and 0 <= dest[1] < SIDE_LENGTH):
            return False
        if desk[dest[0]][dest[1]]:
            return False
    return True


# Check if can eat
def can_eat(start, to):
    global desk
    if desk[start[0]][start[1]] in (1, 2) and to >= N_VECTORS:
        return False
    dest = move_dest(start, to)[-1]
    eat = eat_dest(start, to % N_VECTORS)
    if not eat:
        return False
    after_eat = move_dest(eat, to % N_VECTORS)[-1]
    if not (0 <= after_eat[0] < SIDE_LENGTH and 0 <= after_eat[1] < SIDE_LENGTH and dest == eat):
        return False
    piece_1 = desk[start[0]][start[1]]
    piece_2 = desk[eat[0]][eat[1]]
    piece_3 = desk[after_eat[0]][after_eat[1]]
    return is_enemy(piece_1, piece_2) == 'enemy' and not piece_3


# Check piece relations
def is_enemy(piece_1, piece_2):
    if not piece_1 or not piece_2:
        return 'empty'
    if piece_1 % 2 == piece_2 % 2:
        return 'friend'
    return 'enemy'


def king_transform(cell):
    if desk[cell[0]][cell[1]] == 1 and cell[0] == 0 or desk[cell[0]][cell[1]] == 2 and cell[0] == SIDE_LENGTH - 1:
        desk[cell[0]][cell[1]] += 2
        return True
    return False


def end_move():
    global white_move
    white_move = not white_move


def move(start, to):
    global desk
    piece = desk[start[0]][start[1]]
    dest = move_dest(start, to)[-1]
    after_dest = move_dest(dest, to % N_VECTORS)[-1]
    if not piece:
        print('Empty cell')
        return False
    if (piece - white_move) % 2 == 1:
        print('Wrong color')
        return False
    if can_eat(start, to):
        desk[start[0]][start[1]] = 0
        desk[dest[0]][dest[1]] = 0
        desk[after_dest[0]][after_dest[1]] = piece
        king_transform(after_dest)
        if moves(after_dest)[1] == 'idle':
            end_move()
        print('Ate')
        return True
    if can_move(start, to):
        if is_back_move(start, move_vectors[to % 4]) and piece in [1, 2]:
            print('Cannot go backwards')
            return False
        desk[start[0]][start[1]] = 0
        desk[dest[0]][dest[1]] = piece
        king_transform(dest)
        end_move()
        print('Moved')
        return True
    print('Cannot go there')
    return False


# All possible current moves from given start
def moves(start):
    piece = desk[start[0]][start[1]]
    if piece == 0:
        return [], 'idle'
    if (piece + white_move) % 2 == 1:
        return [], 'idle'
    move_variants = []
    eat_variants = []
    if desk[start[0]][start[1]] in [1, 2]:
        for to in range(N_VECTORS):
            if can_move(start, to):
                move_variants.append(move_dest(start, to)[-1])
            elif can_eat(start, to):
                eat_variants.append(eat_dest(start, to))
    else:
        for to in range(N_VECTORS * SIDE_LENGTH):
            if can_move(start, to):
                move_variants.append(move_dest(start, to)[-1])
            elif can_eat(start, to):
                eat_variants.append(eat_dest(start, to % N_VECTORS))
    if eat_variants:
        return eat_variants, 'eat'
    return move_variants, 'idle'


if __name__ == '__main__':
    board_scheme = [
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 3, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
    ]
    set_desk(board_scheme)

    print(moves((5, 2)))

    for i in desk:
        print(i)
