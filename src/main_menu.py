import pygame
from . import configs



class MenuButton:
    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        font: pygame.font.Font,
        base_color=configs.GRAY,
        text_color=configs.WHITE,
        hover_color=None,
    ):
        self.rect = rect
        self.label = label
        self.font = font
        self.base_color = pygame.Color(base_color)
        self.text_color = pygame.Color(text_color)
        if hover_color is None:
            self.hover_color = pygame.Color(
                min(255, self.base_color.r + 20),
                min(255, self.base_color.g + 20),
                min(255, self.base_color.b + 20),
            )
        else:
            self.hover_color = pygame.Color(hover_color)

    def draw(self, surface: pygame.Surface, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surface = self.font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class MainMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()
        if configs.FONT_MEDIUM is None or configs.TITLE_FONT is None:
            configs.init_fonts()
        self.title_font = configs.TITLE_FONT or pygame.font.SysFont("arial", 72, bold=True)
        self.button_font = configs.FONT_MEDIUM or pygame.font.SysFont("arial", 36)
        button_width, button_height = 220, 60
        center_x = self.width // 2
        top_y = self.height // 2 - button_height
        self.buttons = [
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y, button_width, button_height),
                "Play",
                self.button_font,
                base_color=configs.GREEN,
                text_color=configs.WHITE,
                hover_color=configs.DARK_GREEN,
            ),
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y + 80, button_width, button_height),
                "Options",
                self.button_font,
                base_color=configs.BLUE,
                text_color=configs.WHITE,
                hover_color=configs.DARK_BLUE,
            ),
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y + 160, button_width, button_height),
                "Leaderboard",
                self.button_font,
                base_color=configs.MAGENTA,
                text_color=configs.WHITE,
                hover_color=configs.DARK_MAGENTA,
            ),
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y + 240, button_width, button_height),
                "Quit",
                self.button_font,
                base_color=configs.RED,
                text_color=configs.WHITE,
                hover_color=configs.DARK_RED,
            ),
        ]

    def draw(self):
        self.screen.fill((24, 28, 34))
        title_surface = self.title_font.render("Super Snake", True, configs.WHITE)
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 140))
        self.screen.blit(title_surface, title_rect)
        subtitle_font = pygame.font.SysFont("arial", 20)
        subtitle_surface = subtitle_font.render("Main Menu", True, configs.LIGHT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(subtitle_surface, subtitle_rect)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    return button.label.lower()
        return None

def run_main_menu_demo():
	pygame.init()
	configs.init_fonts()
	screen = pygame.display.set_mode((960, 600))
	pygame.display.set_caption("Main Menu Prototype")
	clock = pygame.time.Clock()
	menu = MainMenu(screen)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			else:
				action = menu.handle_event(event)
				if action == "quit":
					running = False
		menu.draw()
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()

if __name__ == "__main__":
	run_main_menu_demo()
