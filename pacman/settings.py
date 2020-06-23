import pathlib
from pygame.math import Vector2 as vec

# info écran
WIDTH = 560
HEIGHT = 620
FPS = 60
# couleur
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 255, 0)


ROWS = 30
COLS = 28

TEXT_SIZE = 16
FONT = "arial black"


FOLDER_PATH = str(pathlib.Path(__file__).parent.absolute())