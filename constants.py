from collections import namedtuple

BORDERS_COLOR = 'black'

#  = (176, 196, 222)  # 'white'
# FOCUSED_CELL_COLOR = (175, 218, 252)

BACKGROUND_COLOR = None
UNFOCUSED_CELL_COLOR = None
FOCUSED_CELL_COLOR = None
FREE_FOR_CAPTURE_COLOR = None
TEXT_COLOR = None

BUTTON_COLOR = (160, 214, 180)
FOCUSED_BUTTON_COLOR = (113, 188, 120)
PUSHED_BUTTON_COLOR = (181, 101, 167)
INACTIVE_CELL_COLOR = 'grey'

Theme = namedtuple(
    'Theme',
    [
        'BACKGROUND_COLOR',
        'UNFOCUSED_CELL_COLOR',
        'FOCUSED_CELL_COLOR',
        'FREE_FOR_CAPTURE_COLOR',
        'TEXT_COLOR',
        'BUTTON_COLOR',
        'FOCUSED_BUTTON_COLOR',
        'PUSHED_BUTTON_COLOR'
    ]
)

standard = Theme(
    BACKGROUND_COLOR='white',
    UNFOCUSED_CELL_COLOR='#34C6CD',
    FOCUSED_CELL_COLOR='#01939A',
    FREE_FOR_CAPTURE_COLOR='#1D7074',
    TEXT_COLOR='#059CC0',

    BUTTON_COLOR=(160, 214, 180),
    FOCUSED_BUTTON_COLOR=(113, 188, 120),
    PUSHED_BUTTON_COLOR=(181, 101, 167)
)

sea_of_cerenity = Theme(
    BACKGROUND_COLOR='white',
    UNFOCUSED_CELL_COLOR='#6AF2F0',
    FOCUSED_CELL_COLOR='#04D4F0',
    FREE_FOR_CAPTURE_COLOR='#059DC0',
    TEXT_COLOR='#059DC0',

    BUTTON_COLOR=(160, 214, 180),
    FOCUSED_BUTTON_COLOR=(113, 188, 120),
    PUSHED_BUTTON_COLOR=(181, 101, 167)
)

themes = {
    'standard': standard,
    'sea of cerenity': sea_of_cerenity
}


def change_theme(theme_name='standard'):
    if theme_name not in themes:
        theme_name = 'standard'

    global BACKGROUND_COLOR, UNFOCUSED_CELL_COLOR, FOCUSED_CELL_COLOR, \
        FREE_FOR_CAPTURE_COLOR, TEXT_COLOR

    theme = themes[theme_name]

    BACKGROUND_COLOR = theme.BACKGROUND_COLOR
    UNFOCUSED_CELL_COLOR = theme.UNFOCUSED_CELL_COLOR
    FOCUSED_CELL_COLOR = theme.FOCUSED_CELL_COLOR
    FREE_FOR_CAPTURE_COLOR = theme.FREE_FOR_CAPTURE_COLOR
    TEXT_COLOR = theme.TEXT_COLOR


change_theme()
