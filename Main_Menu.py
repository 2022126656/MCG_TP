import pygame


class MenuButton:
    def __init__(self, rect: pygame.Rect, label: str, font: pygame.font.Font):
        self.rect = rect
        self.label = label
        self.font = font

    def draw(self, surface: pygame.Surface, base_color: pygame.Color, text_color: pygame.Color):
        pygame.draw.rect(surface, base_color, self.rect, border_radius=8)
        text_surface = self.font.render(self.label, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class MainMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.button_font = pygame.font.SysFont("arial", 28)

        button_width, button_height = 220, 60
        center_x = self.width // 2
        top_y = self.height // 2 - button_height

        self.buttons = [
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y, button_width, button_height),
                "Play",
                self.button_font,
            ),
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y + 80, button_width, button_height),
                "Options",
                self.button_font,
            ),
            MenuButton(
                pygame.Rect(center_x - button_width // 2, top_y + 160, button_width, button_height),
                "Quit",
                self.button_font,
            ),
        ]

    def draw(self):
        self.screen.fill((24, 28, 34))

        title_surface = self.title_font.render("My Game", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 140))
        self.screen.blit(title_surface, title_rect)

        subtitle_font = pygame.font.SysFont("arial", 20)
        subtitle_surface = subtitle_font.render("Main Menu", True, (180, 180, 180))
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(subtitle_surface, subtitle_rect)

        for button in self.buttons:
            button.draw(self.screen, base_color=pygame.Color(70, 82, 95), text_color=pygame.Color(255, 255, 255))


def run_main_menu_demo():
    pygame.init()
    screen = pygame.display.set_mode((960, 600))
    pygame.display.set_caption("Main Menu Prototype")
    clock = pygame.time.Clock()
    menu = MainMenu(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        menu.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run_main_menu_demo()
