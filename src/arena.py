import pygame
import random
from . import configs
from .game_over import GameOverScreen
from .confirm_dialog import ConfirmDialog
from .leaderboard_input import LeaderboardInput

class SnakeArena:
	def play_music(self, track):
		try:
			pygame.mixer.music.stop()
			pygame.mixer.music.load(track)
			pygame.mixer.music.play(-1)
		except Exception:
			pass
	def __init__(self, screen, cols=16, rows=16, cell=30):
		self.screen = screen
		self.screen_width, self.screen_height = screen.get_size()
		self.cols = cols
		self.rows = rows
		self.cell = cell
		self.arena_width = self.cols * self.cell
		self.arena_height = self.rows * self.cell
		self.offset_x = (self.screen_width - self.arena_width) // 2
		self.offset_y = (self.screen_height - self.arena_height) // 2

	def reset(self):
		mid_x = self.cols // 2
		mid_y = self.rows // 2
		self.snake = [
			[mid_x, mid_y],
			[mid_x - 1, mid_y],
			[mid_x - 2, mid_y],
		]
		self.direction = pygame.Vector2(1, 0)
		self.score = 0
		self.spawn_food()

	def spawn_food(self):
		self.food = [
			random.randint(0, self.cols - 1),
			random.randint(0, self.rows - 1),
		]
		if any(part[0] == self.food[0] and part[1] == self.food[1] for part in self.snake):
			self.spawn_food()

	def move_snake(self):
		head = [self.snake[0][0] + int(self.direction.x), self.snake[0][1] + int(self.direction.y)]
		head[0] %= self.cols
		head[1] %= self.rows
		self.snake.insert(0, head)
		if head in self.snake[1:]:
			return True
		if head[0] == self.food[0] and head[1] == self.food[1]:
			self.score += 10
			self.spawn_food()
		else:
			self.snake.pop()
		return False

	def draw(self):
		self.screen.fill(configs.GRAY)
		arena_rect = pygame.Rect(self.offset_x, self.offset_y, self.arena_width, self.arena_height)
		for gx in range(self.cols):
			for gy in range(self.rows):
				color = configs.BEGE if (gx + gy) % 2 == 0 else configs.BROWN
				px = self.offset_x + gx * self.cell
				py = self.offset_y + gy * self.cell
				pygame.draw.rect(self.screen, color, (px, py, self.cell, self.cell))
		pygame.draw.rect(self.screen, configs.GRAY, arena_rect, 2)
		for x in range(self.cols + 1):
			start = (self.offset_x + x * self.cell, self.offset_y)
			end = (self.offset_x + x * self.cell, self.offset_y + self.arena_height)
			pygame.draw.line(self.screen, configs.BLACK, start, end, 1)
		for y in range(self.rows + 1):
			start = (self.offset_x, self.offset_y + y * self.cell)
			end = (self.offset_x + self.arena_width, self.offset_y + y * self.cell)
			pygame.draw.line(self.screen, configs.BLACK, start, end, 1)
		if hasattr(self, "food"):
			food_px = (self.offset_x + self.food[0] * self.cell, self.offset_y + self.food[1] * self.cell)
			pygame.draw.rect(self.screen, configs.RED, (food_px[0], food_px[1], self.cell, self.cell))
		if hasattr(self, "snake"):
			for gx, gy in self.snake:
				px = self.offset_x + gx * self.cell
				py = self.offset_y + gy * self.cell
				pygame.draw.rect(self.screen, configs.DARK_GREEN, (px, py, self.cell, self.cell))
		if hasattr(configs, "FONT_MEDIUM") and configs.FONT_MEDIUM:
			font = configs.FONT_MEDIUM
		else:
			font = pygame.font.SysFont("arial", 36)
		current_score = getattr(self, 'score', 0)
		high_score = 0
		try:
			with open("src/leaderboard.txt", "r") as f:
				for line in f:
					if ":" in line:
						_, score = line.strip().split(":", 1)
						try:
							score_val = int(score)
							if score_val > high_score:
								high_score = score_val
						except ValueError:
							continue
		except FileNotFoundError:
			pass
		if current_score > high_score and current_score > 0:
			label = f"High Score: {current_score}"
		else:
			label = f"Score: {current_score}"
		score_surface = font.render(label, True, configs.AMBAR)
		self.screen.blit(score_surface, (20, 20))

	def run(self):
		clock = pygame.time.Clock()
		self.reset()
		running = True
		game_over_screen = None
		confirm_dialog = None
		confirm_action = None
		leaderboard_input = None
		leaderboard_saved = False
		while running:
			if not game_over_screen:
				last_direction = None
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						return "quit"
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							return "pause"
						if event.key == pygame.K_UP and self.direction.y == 0:
							last_direction = pygame.Vector2(0, -1)
						elif event.key == pygame.K_DOWN and self.direction.y == 0:
							last_direction = pygame.Vector2(0, 1)
						elif event.key == pygame.K_LEFT and self.direction.x == 0:
							last_direction = pygame.Vector2(-1, 0)
						elif event.key == pygame.K_RIGHT and self.direction.x == 0:
							last_direction = pygame.Vector2(1, 0)
				if last_direction is not None:
					self.direction = last_direction
				collision = self.move_snake()
				if collision:
					game_over_screen = GameOverScreen(self.screen, self.score)
					leaderboard_input = None
					leaderboard_saved = False
					while True:
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								return "quit"
							if leaderboard_input:
								name = leaderboard_input.handle_event(event)
								if leaderboard_input.done and name:
									with open("src/leaderboard.txt", "a") as f:
										f.write(f"{name}:{self.score}\n")
									leaderboard_saved = True
									leaderboard_input = None
									if hasattr(game_over_screen, 'show_save_score'):
										game_over_screen.show_save_score = False
								elif leaderboard_input.done:
									leaderboard_input = None
								continue
							action = game_over_screen.handle_event(event)
							if action == "restart":
								self.reset()
								game_over_screen = None
								break
							elif action == "menu":
								return "menu"
							elif action == "leaderboard":
								from .leaderboard_screen import LeaderboardScreen
								leaderboard_screen = LeaderboardScreen(self.screen)
								self.play_music("music/leaderboard_theme.mp3")
								viewing = True
								while viewing:
									for lbevent in pygame.event.get():
										if lbevent.type == pygame.QUIT:
											return "quit"
										lbaction = leaderboard_screen.handle_event(lbevent)
										if lbaction == "menu":
											viewing = False
											self.play_music("music/game_over_theme.mp3")
									leaderboard_screen.draw()
									pygame.display.flip()
									clock.tick(24)
							elif action == "add_leaderboard" and not leaderboard_input and not leaderboard_saved:
								self.play_music("music/leaderboard_theme.mp3")
								leaderboard_input = LeaderboardInput(self.screen, self.score)
						if game_over_screen is None:
							break
						game_over_screen.draw()
						if leaderboard_input:
							leaderboard_input.draw()
						pygame.display.flip()
						clock.tick(24)
					continue
				self.draw()
				pygame.display.flip()
				min_fps = 10
				max_fps = 24
				dynamic_fps = min(max_fps, min_fps + self.score // 50)
				clock.tick(dynamic_fps)
			else:
				skip_frame = False
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						return "quit"
					if leaderboard_input:
						name = leaderboard_input.handle_event(event)
						if leaderboard_input.done and name:
							with open("src/leaderboard.txt", "a") as f:
								f.write(f"{name}:{self.score}\n")
							leaderboard_saved = True
							leaderboard_input = None
						elif leaderboard_input.done:
							leaderboard_input = None
						continue
					if confirm_dialog:
						result = confirm_dialog.handle_event(event)
						if result == "yes":
							if confirm_action == "restart":
								self.reset()
								game_over_screen = None
								leaderboard_saved = False
								confirm_dialog = None
								confirm_action = None
								skip_frame = True
								break
							elif confirm_action == "menu":
								return "menu"
							confirm_dialog = None
							confirm_action = None
						elif result == "no":
							confirm_dialog = None
							confirm_action = None
						continue
					action = game_over_screen.handle_event(event)
					if action == "restart":
						confirm_dialog = ConfirmDialog(self.screen, "Restart the game?")
						confirm_action = "restart"
					elif action == "menu":
						confirm_dialog = ConfirmDialog(self.screen, "Return to main menu?")
						confirm_action = "menu"
					elif action == "add_leaderboard" and not leaderboard_input and not leaderboard_saved:
						self.play_music("music/leaderboard_theme.mp3")
						leaderboard_input = LeaderboardInput(self.screen, self.score)
				if skip_frame or game_over_screen is None:
					continue
				game_over_screen.draw()
				if leaderboard_input:
					leaderboard_input.draw()