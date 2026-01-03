import pygame
from . import configs
from .main_menu import MenuButton

class PauseMenu:
	def __init__(self, screen: pygame.Surface):
		self.screen = screen
		self.width, self.height = screen.get_size()
		if configs.FONT_MEDIUM is None or configs.TITLE_FONT is None:
			configs.init_fonts()
		self.title_font = configs.TITLE_FONT or pygame.font.SysFont("arial", 72, bold=True)
		self.button_font = configs.FONT_MEDIUM or pygame.font.SysFont("arial", 36)
		button_width, button_height = 220, 60
		center_x = self.width // 2
		top_y = self.height // 2 - 20
		self.buttons = [
			MenuButton(
				pygame.Rect(center_x - button_width // 2, top_y, button_width, button_height),
				"Resume",
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
				"Restart",
				self.button_font,
				base_color=configs.MAGENTA,
				text_color=configs.WHITE,
				hover_color=configs.DARK_MAGENTA,
			),
			MenuButton(
				pygame.Rect(center_x - button_width // 2, top_y + 240, button_width, button_height),
				"Menu",
				self.button_font,
				base_color=configs.RED,
				text_color=configs.WHITE,
				hover_color=configs.DARK_RED,
			),
		]

	def draw(self):
		mouse_pos = pygame.mouse.get_pos()
		title_surface = self.title_font.render("PAUSED", True, configs.AMBAR)
		title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
		self.screen.blit(title_surface, title_rect)
		for button in self.buttons:
			button.draw(self.screen, mouse_pos)

