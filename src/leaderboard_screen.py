import pygame
from . import configs
from .main_menu import MenuButton

class LeaderboardScreen:
	def __init__(self, screen):
		self.screen = screen
		self.width, self.height = screen.get_size()
		if configs.FONT_MEDIUM is None or configs.TITLE_FONT is None:
			configs.init_fonts()
		self.title_font = configs.TITLE_FONT or pygame.font.SysFont("arial", 72, bold=True)
		self.font = configs.FONT_MEDIUM or pygame.font.SysFont("arial", 36)
		self.small_font = pygame.font.SysFont("arial", 28)
		button_width, button_height = 220, 60
		center_x = self.width // 2
		self.back_button = MenuButton(
			pygame.Rect(center_x - button_width // 2, self.height - 100, button_width, button_height),
			"Main Menu",
			self.font,
			base_color=configs.MAGENTA,
			text_color=configs.WHITE,
			hover_color=configs.DARK_MAGENTA,
		)
		self.scores = self.load_scores()

	def load_scores(self):
		try:
			with open("src/leaderboard.txt", "r") as f:
				lines = f.readlines()
			entries = []
			for line in lines:
				if ":" in line:
					name, score = line.strip().split(":", 1)
					try:
						entries.append((name, int(score)))
					except ValueError:
						continue
			entries.sort(key=lambda x: x[1], reverse=True)
			return entries[:10]
		except FileNotFoundError:
			return []

	def draw(self):
		self.screen.fill((24, 28, 34))
		title_surface = self.title_font.render("Leaderboard", True, configs.AMBAR)
		title_rect = title_surface.get_rect(center=(self.width // 2, 80))
		self.screen.blit(title_surface, title_rect)
		y = 160
		for idx, (name, score) in enumerate(self.scores, 1):
			entry = f"{idx}. {name} - {score}"
			entry_surface = self.small_font.render(entry, True, configs.WHITE)
			entry_rect = entry_surface.get_rect(center=(self.width // 2, y))
			self.screen.blit(entry_surface, entry_rect)
			y += 40
		if not self.scores:
			no_scores = self.small_font.render("No scores yet.", True, configs.LIGHT_GRAY)
			no_scores_rect = no_scores.get_rect(center=(self.width // 2, y))
			self.screen.blit(no_scores, no_scores_rect)
		self.back_button.draw(self.screen)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.back_button.rect.collidepoint(event.pos):
				return "menu"
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_m:
				return "menu"
		return None
def display_leaderboard():
	print("Displaying leaderboard...")

def update_leaderboard():
	print("Updating leaderboard...")
