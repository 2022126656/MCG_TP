import pygame
from . import configs

class LeaderboardInput:
	def __init__(self, screen, score):
		self.screen = screen
		self.score = score
		self.width, self.height = screen.get_size()
		if configs.FONT_MEDIUM is None:
			configs.init_fonts()
		self.font = configs.FONT_MEDIUM or pygame.font.SysFont("arial", 36)
		self.input_font = pygame.font.SysFont("arial", 32)
		self.input_box = pygame.Rect(self.width//2 - 120, self.height//2, 240, 50)
		self.color_inactive = configs.LIGHT_GRAY
		self.color_active = configs.AMBAR
		self.color = self.color_inactive
		self.active = False
		self.text = ""
		self.done = False
		self.save_button = pygame.Rect(self.width//2 - 60, self.height//2 + 70, 120, 50)

	def draw(self):
		overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 180))
		self.screen.blit(overlay, (0, 0))
		box_rect = pygame.Rect(self.width//2 - 220, self.height//2 - 100, 440, 220)
		pygame.draw.rect(self.screen, configs.GRAY, box_rect, border_radius=12)
		pygame.draw.rect(self.screen, configs.LIGHT_GRAY, box_rect, 4, border_radius=12)
		score_surface = self.input_font.render(f"Score: {self.score}", True, configs.AMBAR)
		score_rect = score_surface.get_rect(center=(self.width//2, self.height//2 - 70))
		self.screen.blit(score_surface, score_rect)
		prompt = self.font.render("Enter your name:", True, configs.WHITE)
		prompt_rect = prompt.get_rect(center=(self.width//2, self.height//2 - 30))
		self.screen.blit(prompt, prompt_rect)
		pygame.draw.rect(self.screen, self.color, self.input_box, 2, border_radius=8)
		txt_surface = self.input_font.render(self.text, True, configs.WHITE)
		self.screen.blit(txt_surface, (self.input_box.x+10, self.input_box.y+10))
		pygame.draw.rect(self.screen, configs.GREEN, self.save_button, border_radius=8)
		save_label = self.input_font.render("Save", True, configs.WHITE)
		save_rect = save_label.get_rect(center=self.save_button.center)
		self.screen.blit(save_label, save_rect)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.input_box.collidepoint(event.pos):
				self.active = True
				self.color = self.color_active
			else:
				self.active = False
				self.color = self.color_inactive
			if self.save_button.collidepoint(event.pos):
				self.done = True
				return self.text.strip()
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					self.done = True
					return self.text.strip()
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				elif len(self.text) < 16 and event.unicode.isprintable():
					self.text += event.unicode
		return None