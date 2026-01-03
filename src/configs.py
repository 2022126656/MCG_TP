import pygame

FONT_MEDIUM = None
TITLE_FONT = None

def init_fonts():
    if not pygame.font.get_init():
        pygame.font.init()
    global FONT_MEDIUM, TITLE_FONT
    FONT_MEDIUM = pygame.font.SysFont("arial", 36)
    TITLE_FONT = pygame.font.SysFont("arial", 72, bold=True)

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (70, 70, 70)
LIGHT_GRAY  = (150, 150, 150)

GREEN       = (0, 200, 0)
DARK_GREEN  = (0, 150, 0)

RED         = (200, 0, 0)
DARK_RED    = (150, 0, 0)

BLUE        = (50, 120, 255)
DARK_BLUE   = (30, 90, 200)

YELLOW      = (230, 230, 0)

MAGENTA     = (255, 0, 255)
DARK_MAGENTA= (200, 0, 200)

BEGE = (240, 235, 220)
BEGE_ESCURO = (235, 225, 200)

BROWN = (150, 75, 0)

AMBAR = (255, 191, 0)
