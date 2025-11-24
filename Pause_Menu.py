import pygame


class PauseMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("arial", 26)

        button_width, button_height = 200, 54
        center_x = self.width // 2
        top_y = self.height // 2 - 40

        self.buttons = [
            ("Resume", pygame.Rect(center_x - button_width // 2, top_y, button_width, button_height)),
            ("Restart", pygame.Rect(center_x - button_width // 2, top_y + 70, button_width, button_height)),
            ("Quit", pygame.Rect(center_x - button_width // 2, top_y + 140, button_width, button_height)),
        ]

    def draw(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title_surface = self.title_font.render("Paused", True, (240, 240, 240))
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 120))
        self.screen.blit(title_surface, title_rect)

        for label, rect in self.buttons:
            pygame.draw.rect(self.screen, pygame.Color(90, 90, 110), rect, border_radius=10)
            text_surface = self.button_font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)


def run_pause_menu_demo():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    pygame.display.set_caption("Pause Menu Prototype")
    clock = pygame.time.Clock()
    menu = PauseMenu(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 32, 36))
        menu.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_pause_menu_demo()
