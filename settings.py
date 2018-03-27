import os

TITLE = "Spirit Weaver"
WIDTH = 1024
HEIGHT = 768
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SS = (0, 117, 117)

UP = [(72 * i, 0, 72, 96) for i in [1, 2, 1, 0]]
RIGHT = [(72 * i, 96, 72, 96) for i in [1, 2, 1, 0]]
DOWN = [(72 * i, 192, 72, 96) for i in [1, 2, 1, 0]]
LEFT = [(72 * i, 288, 72, 96) for i in [1, 2, 1, 0]]

SIDEWALK_MID = (544, 1360, 64, 64)

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_SPEED = 200

# set up assets
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")
characters_folder = os.path.join(assets_folder, "characters")
audio_folder = os.path.join(assets_folder, "audio")
map_folder = os.path.join(assets_folder, "map")