import pygame

from Main_Menu import MainMenu
from Pause_Menu import PauseMenu


def run_demo():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    pygame.display.set_caption("Menu Visual Prototype")
    clock = pygame.time.Clock()

    main_menu = MainMenu(screen)
    pause_menu = PauseMenu(screen)

    showing_main_menu = True
    paused = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not showing_main_menu:
                    paused = not paused
                elif event.key == pygame.K_SPACE and showing_main_menu:
                    showing_main_menu = False

        if showing_main_menu:
            main_menu.draw()
        else:
            screen.fill((26, 46, 56))
            game_font = pygame.font.SysFont("arial", 24)
            instructions = [
                "In-game placeholder view.",
                "Press ESC to toggle the pause menu overlay.",
                "Press the window close button to exit.",
            ]
            for i, line in enumerate(instructions):
                text_surface = game_font.render(line, True, (220, 220, 220))
                screen.blit(text_surface, (32, 32 + i * 32))

            if paused:
                pause_menu.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_demo()
