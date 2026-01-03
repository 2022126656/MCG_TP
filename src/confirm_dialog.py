import pygame
from . import configs
class ConfirmDialog:
	def __init__(self, screen, message):
		self.screen = screen
		self.message = message
		self.width, self.height = screen.get_size()
		if configs.FONT_MEDIUM is None:
			configs.init_fonts()
		self.font = configs.FONT_MEDIUM or pygame.font.SysFont("arial", 36)
		self.button_font = pygame.font.SysFont("arial", 28)
		button_width, button_height = 120, 50
		center_x = self.width // 2
		center_y = self.height // 2 + 40
		self.buttons = [
			pygame.Rect(center_x - button_width - 20, center_y, button_width, button_height),
			pygame.Rect(center_x + 20, center_y, button_width, button_height)
		]

	def draw(self):
		overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 180))
		self.screen.blit(overlay, (0, 0))
		box_rect = pygame.Rect(self.width//2 - 220, self.height//2 - 80, 440, 180)
		pygame.draw.rect(self.screen, configs.GRAY, box_rect, border_radius=12)
		pygame.draw.rect(self.screen, configs.LIGHT_GRAY, box_rect, 4, border_radius=12)
		msg_surface = self.font.render(self.message, True, configs.WHITE)
		msg_rect = msg_surface.get_rect(center=(self.width//2, self.height//2 - 20))
		self.screen.blit(msg_surface, msg_rect)
		labels = ["Yes", "No"]
		for i, rect in enumerate(self.buttons):
			color = configs.GREEN if i == 0 else configs.RED
			pygame.draw.rect(self.screen, color, rect, border_radius=8)
			label_surface = self.button_font.render(labels[i], True, configs.WHITE)
			label_rect = label_surface.get_rect(center=rect.center)
			self.screen.blit(label_surface, label_rect)

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			for i, rect in enumerate(self.buttons):
				if rect.collidepoint(event.pos):
					return "yes" if i == 0 else "no"
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_y:
				return "yes"
			elif event.key == pygame.K_n:
				return "no"
		return None
