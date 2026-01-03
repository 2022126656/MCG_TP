import pygame

from . import configs
from .main_menu import MainMenu
from .arena import SnakeArena
from .pause_menu import PauseMenu
from .confirm_dialog import ConfirmDialog
from .leaderboard_screen import LeaderboardScreen

def main():
	pygame.init()
	configs.init_fonts()
	screen = pygame.display.set_mode((960, 600))
	pygame.display.set_caption("Super Snake")
	clock = pygame.time.Clock()
	menu = MainMenu(screen)
	arena = SnakeArena(screen)
	pause_menu = PauseMenu(screen)
	current_state = "menu"
	running = True
	while running:
		if current_state == "menu":
			confirm_dialog = None
			show_leaderboard = False
			leaderboard_screen = LeaderboardScreen(screen)
			while current_state == "menu" and running:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
						break
					if show_leaderboard:
						action = leaderboard_screen.handle_event(event)
						if action == "menu":
							show_leaderboard = False
						continue
					if confirm_dialog:
						result = confirm_dialog.handle_event(event)
						if result == "yes":
							running = False
							confirm_dialog = None
						elif result == "no":
							confirm_dialog = None
						continue
					action = menu.handle_event(event)
					if action == "play":
						current_state = "arena"
					elif action == "leaderboard":
						leaderboard_screen = LeaderboardScreen(screen)
						show_leaderboard = True
					elif action == "quit":
						confirm_dialog = ConfirmDialog(screen, "Quit the game?")
				if show_leaderboard:
					leaderboard_screen.draw()
				else:
					menu.draw()
				if confirm_dialog:
					confirm_dialog.draw()
				pygame.display.flip()
				clock.tick(60)
		elif current_state == "arena":
			result = arena.run()
			if result == "menu":
				current_state = "menu"
			elif result == "quit":
				running = False
			elif result == "pause":
				paused = True
				confirm_dialog = None
				confirm_action = None
				while paused and running:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							running = False
							paused = False
							break
						if confirm_dialog:
							result = confirm_dialog.handle_event(event)
							if result == "yes":
								if confirm_action == "restart":
									arena.reset()
									paused = False
								elif confirm_action == "menu":
									current_state = "menu"
									paused = False
								elif confirm_action == "quit":
									running = False
									paused = False
								confirm_dialog = None
								confirm_action = None
							elif result == "no":
								confirm_dialog = None
								confirm_action = None
							continue
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_ESCAPE:
								paused = False
							elif event.key == pygame.K_r:
								confirm_dialog = ConfirmDialog(screen, "Restart the game?")
								confirm_action = "restart"
							elif event.key == pygame.K_m:
								confirm_dialog = ConfirmDialog(screen, "Return to main menu?")
								confirm_action = "menu"
							elif event.key == pygame.K_q:
								confirm_dialog = ConfirmDialog(screen, "Quit the game?")
								confirm_action = "quit"
						if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
							mouse_pos = pygame.mouse.get_pos()
							for button in pause_menu.buttons:
								if button.rect.collidepoint(mouse_pos):
									label = button.label.lower()
									if label == "resume":
										paused = False
									elif label == "restart":
										confirm_dialog = ConfirmDialog(screen, "Restart the game?")
										confirm_action = "restart"
									elif label == "menu":
										confirm_dialog = ConfirmDialog(screen, "Return to main menu?")
										confirm_action = "menu"
									elif label == "quit":
										confirm_dialog = ConfirmDialog(screen, "Quit the game?")
										confirm_action = "quit"
					screen.fill((24, 28, 34))
					arena.draw()
					pause_menu.draw()
					if confirm_dialog:
						confirm_dialog.draw()
					pygame.display.flip()
					clock.tick(60)
	pygame.quit()

if __name__ == "__main__":
	main()