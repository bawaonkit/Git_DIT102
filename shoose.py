import pygame, sys
pygame.init()

WIDTH, HEIGHT = 720, 640
DEFAULT_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(DEFAULT_SIZE, pygame.RESIZABLE | pygame.SCALED) 
pygame.display.set_caption("Mini Bullet Hell")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 80, 80)
BLUE = (80, 180, 255)
GREEN = (80, 255, 80)
DARK_GREEN = (50, 150, 50)
DARK_GRAY = (50, 50, 50)

CHARACTER_COLORS = {
    "Red": RED,
    "Blue": BLUE,
    "Green": DARK_GREEN,
}

font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 60)

def draw_text(txt, x, y, color=WHITE, used_font=font):
    text_surface = used_font.render(txt, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color


    def draw(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        text_surface = font.render(self.text, True, (0,0,0))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def character_selection():
    char_size = 100
    gap = 60
    start_x = (WIDTH - ((char_size + gap) * len(CHARACTER_COLORS) - gap)) // 2
    y_pos = HEIGHT // 2 - 50

    buttons = []
    for i, (name, color) in enumerate(CHARACTER_COLORS.items()):
        x = start_x + (i * (char_size + gap))
        buttons.append(Button(x, y_pos, char_size, char_size, name, color, WHITE))

    running = True
    while running:
        screen.fill(DARK_GRAY)
        draw_text("SELECT YOUR CHARACTER", WIDTH // 2, HEIGHT // 4, WHITE, large_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            for b in buttons:
                if b.is_clicked(event):
                    print(f"Selected: {b.text}")

        for b in buttons:
            b.draw()

        pygame.display.flip()
        clock.tick(60)


character_selection()
