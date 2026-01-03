import pygame
from . import configs
from .main_menu import MenuButton
class GameOverScreen:
	def __init__(self, screen, score):
		self.screen = screen
		self.score = score
		self.width, self.height = screen.get_size()
		if configs.FONT_MEDIUM is None or configs.TITLE_FONT is None:
			configs.init_fonts()
		self.title_font = configs.TITLE_FONT or pygame.font.SysFont("arial", 72, bold=True)
		self.button_font = configs.FONT_MEDIUM or pygame.font.SysFont("arial", 36)
		button_width, button_height = 220, 60
		center_x = self.width // 2
		top_y = self.height // 2 + 40
		self.show_save_score = True
		self.restart_button = MenuButton(
			pygame.Rect(center_x - button_width // 2, top_y, button_width, button_height),
			"Restart",
			self.button_font,
			base_color=configs.GREEN,
			text_color=configs.WHITE,
			hover_color=configs.DARK_GREEN,
		)
		self.save_score_button = MenuButton(
			pygame.Rect(center_x - button_width // 2, top_y + 80, button_width, button_height),
			"Save Score",
			self.button_font,
			base_color=configs.BLUE,
			text_color=configs.WHITE,
			hover_color=configs.DARK_BLUE,
		)
		self.leaderboard_button = MenuButton(
			pygame.Rect(center_x - button_width // 2, top_y + 80, button_width, button_height),
			"Leaderboard",
			self.button_font,
			base_color=configs.BLUE,
			text_color=configs.WHITE,
			hover_color=configs.DARK_BLUE,
		)
		self.menu_button = MenuButton(
			pygame.Rect(center_x - button_width // 2, top_y + 160, button_width, button_height),
			"Main Menu",
			self.button_font,
			base_color=configs.MAGENTA,
			text_color=configs.WHITE,
			hover_color=configs.DARK_MAGENTA,
		)

	def draw(self):
		self.screen.fill(configs.BLACK)
		over_surface = self.title_font.render("GAME OVER", True, configs.RED)
		over_rect = over_surface.get_rect(center=(self.width // 2, self.height // 2 - 60))
		self.screen.blit(over_surface, over_rect)
		score_surface = self.button_font.render(f"Final Score: {self.score}", True, configs.AMBAR)
		score_rect = score_surface.get_rect(center=(self.width // 2, self.height // 2 + 10))
		self.screen.blit(score_surface, score_rect)
		mouse_pos = pygame.mouse.get_pos()
		if self.show_save_score:
			self.restart_button.draw(self.screen, mouse_pos)
			self.save_score_button.draw(self.screen, mouse_pos)
			self.menu_button.draw(self.screen, mouse_pos)
		else:
			self.restart_button.draw(self.screen, mouse_pos)
			self.leaderboard_button.draw(self.screen, mouse_pos)
			self.menu_button.draw(self.screen, mouse_pos)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.show_save_score:
				if self.restart_button.rect.collidepoint(event.pos):
					return "restart"
				if self.save_score_button.rect.collidepoint(event.pos):
					return "add_leaderboard"
				if self.menu_button.rect.collidepoint(event.pos):
					return "menu"
			else:
				if self.restart_button.rect.collidepoint(event.pos):
					return "restart"
				if self.leaderboard_button.rect.collidepoint(event.pos):
					return "leaderboard"
				if self.menu_button.rect.collidepoint(event.pos):
					return "menu"
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				return "restart"
			elif event.key == pygame.K_m:
				return "menu"
		return None
