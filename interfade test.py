import sys
import pygame
from pygame import mixer

# กำหนดขนาดหน้าต่าง
WIDTH, HEIGHT = 720, 640
FPS = 60

# สี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Start Screen Example')
clock = pygame.time.Clock()

# ฟอนต์ไม่ถูกใจค่อยเปลี่ยนทีหลังได้
title_font = pygame.font.SysFont('arial', 64, bold=True)
menu_font = pygame.font.SysFont('arial', 28)
small_font = pygame.font.SysFont('arial', 18)

# ปุ่ม
class Button:
    def __init__(self, rect, text, font, bg=GRAY, fg=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg
        self.fg = fg
        self.hover = False

    def draw(self, surf):
        color = tuple(min(255, c + 30) for c in self.bg) if self.hover else self.bg
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, BLACK, self.rect, 2, border_radius=10)
        txt = self.font.render(self.text, True, self.fg)
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# สร้างปุ่ม
btn_w, btn_h = 240, 54
play_btn = Button(((WIDTH-btn_w)//2, 250, btn_w, btn_h), 'Play', menu_font, bg=(28,130,196))

# ตำแหน่งโลโก้
logo_y = 120
logo_dir = 1
logo_range = 8
logo_speed = 40

# Fade control
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0,0,0))
fade_alpha = 255
fading_in = True
fading_out = False
fade_speed = 300


#main menu loop
running = True
while running:
    dt = clock.tick(FPS) / 1000
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                fading_out = True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                fading_out = True
            if event.key == pygame.K_ESCAPE:
                running = False

    #อัพเดตปุ่ม
    play_btn.update(mouse_pos)
   

    #พื้นหลัง
    screen.fill((10, 12, 23))

    #โลโก้/ชื่อเกม
    title_surf = title_font.render('Bullet Hell', True, (240,240,240))
    title_rect = title_surf.get_rect(center=(WIDTH//2, int(logo_y)))

    # เงาตรงโลโก้
    shadow = title_font.render('My Awesome Game', True, (10,10,10))
    shadow_rect = shadow.get_rect(center=(WIDTH//2 + 4, int(logo_y) + 4))
    screen.blit(shadow, shadow_rect)
    screen.blit(title_surf, title_rect)

    #เขียนคำด้านล่างใต้ชื่อเกม
    subtitle = small_font.render('Press Enter or click Play to start', True, (180,180,180))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, int(logo_y)+50)))

    # วาดปุ่ม
    play_btn.draw(screen)

    #แถบแสงขยับบนปุ่ม
    glow_rect = pygame.Rect(play_btn.rect.x - 2, play_btn.rect.y - 2, play_btn.rect.width + 4, play_btn.rect.height + 4)
    #วงแหวนตรงปุ่ม
    if play_btn.hover:
        pygame.draw.rect(screen, (255,255,255), glow_rect, 3, border_radius=12)

    # Fade in
    if fading_in:
        fade_alpha -= fade_speed * dt
        if fade_alpha <= 0:
            fade_alpha = 0
            fading_in = False
        fade_surface.set_alpha(int(fade_alpha))
        screen.blit(fade_surface, (0,0))

    # Fade out
    if fading_out:
        fade_alpha += fade_speed * dt
        if fade_alpha >= 255:
            fade_alpha = 255
            running = False
        fade_surface.set_alpha(int(fade_alpha))
        screen.blit(fade_surface, (0,0))
    pygame.display.flip()
pygame.quit()
sys.exit()
#เอาตัวเกมมาใส่หรือตกแต่งอะไรเพิ่มค่อยคุยกันอีกทีนะ