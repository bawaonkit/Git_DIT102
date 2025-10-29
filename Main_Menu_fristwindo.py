import pygame
import sys
pygame.init()

# กำหนดขนาดหน้าจอ
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 640
FULLSCREEN = ((SCREEN_WIDTH , SCREEN_HEIGHT))
SCREEN = pygame.display.set_mode(FULLSCREEN , pygame.RESIZABLE|pygame.SCALED) 
pygame.display.set_caption("Main Menu Game")

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)

# กำหนดฟอนต์
# Pygame จะใช้ฟอนต์ดีฟอลต์หากหาฟอนต์ที่ระบุไม่พบ
try:
    FONT = pygame.font.Font(None, 74) # None คือใช้ฟอนต์ดีฟอลต์ของ Pygame
    SMALL_FONT = pygame.font.Font(None, 50)
except:
    FONT = pygame.font.SysFont("arial", 74)
    SMALL_FONT = pygame.font.SysFont("arial", 50)


# 2. ฟังก์ชันวาดข้อความและปุ่ม

def draw_text(text, font, color, surface, x, y):
    """วาดข้อความบนหน้าจอ"""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_button(msg, x, y, w, h, inactive_color, active_color, action=None):
    """สร้างปุ่มที่สามารถคลิกได้"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # ตรวจสอบว่าเมาส์อยู่เหนือปุ่มหรือไม่
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(SCREEN, active_color, (x, y, w, h))
        
        # ตรวจสอบการคลิก
        if click[0] == 1 and action is not None:
            if action == "play":
                # ฟังก์ชันที่จะถูกเรียกเมื่อกด 'เล่น'
                print("--- เข้าสู่เกม! (Start Game) ---")
                # ในเกมจริงคุณจะเปลี่ยนไปหน้าเล่นเกม (Game Loop)
                game_loop()
            elif action == "quit":
                # ฟังก์ชันที่จะถูกเรียกเมื่อกด 'ออก'
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(SCREEN, inactive_color, (x, y, w, h))

    # วาดข้อความบนปุ่ม
    text_surface = SMALL_FONT.render(msg, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    SCREEN.blit(text_surface, text_rect)

# 3. โครงสร้าง Game State (สถานะเกม)

def game_loop():
    """จำลองหน้าจอหลักของเกม เมื่อผู้เล่นกด 'เล่น'"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # กด ESC เพื่อกลับเมนู
                    return # ออกจาก game_loop กลับไปที่ main_menu

        SCREEN.fill(WHITE)
        draw_text('YOU ARE PLAYING!', FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text('Press ESC to return to menu', SMALL_FONT, WHITE, SCREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
        
        pygame.display.update()
    
    # หากออกจาก loop นี้ (เช่น กด X) ก็ปิดเกม
    pygame.quit()
    sys.exit()


def main_menu():
    """หน้าจอเมนูหลัก"""
    menu_running = True
    
    while menu_running:
        # รับ Event (เช่น การคลิก, การกดปุ่ม)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # วาดพื้นหลัง สีของพื้อหลัง
        SCREEN.fill(WHITE)
        
        # 1. ชื่อเกม
        draw_text('Bullet Hell', FONT, BLACK, SCREEN, SCREEN_WIDTH // 2, 100)
        
        # 2. ปุ่ม 'เล่น' (START GAME)
        # ตำแหน่ง (x, y, กว้าง, สูง)
        button_x = SCREEN_WIDTH // 2 - 100
        button_y_play = SCREEN_HEIGHT // 2
        draw_button('Play Game', button_x, button_y_play, 200, 50, GREEN, BRIGHT_GREEN, "play")
        
        # 3. ปุ่ม 'ออก' (QUIT GAME)
        button_y_quit = button_y_play + 70
        draw_button('QUIT', button_x, button_y_quit, 200, 50, RED, BRIGHT_RED, "quit")
        
        # อัพเดตหน้าจอ
        pygame.display.update()


# 4. เริ่มการทำงาน
if __name__ == '__main__':
    main_menu()