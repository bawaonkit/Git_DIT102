import pygame, sys  # โมดูล sys ใช้สำหรับ สั่งออกจากโปรแกรมหรือเข้าถึงค่าจากระบบ
pygame.init()

WIDTH, HEIGHT = 720, 640
Full_sereen = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(Full_sereen, pygame.RESIZABLE | pygame.SCALED)
# pygame.RESIZABLE = อนุญาตให้ปรับขนาดหน้าต่างได้
# pygame.SCALED = ปรับสเกลภาพให้คมชัดเมื่อขยายหน้าต่าง
pygame.display.set_caption("เลือกระดับความยาก")

# สี (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (160, 160, 160)
GREEN = (100, 200, 100)
YELLOW = (240, 220, 100)
RED = (220, 100, 100)

FONT = pygame.font.SysFont(None, 36)
SMALL = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()  # ควบคุมความเร็วของลูปเกม (FPS)


# สร้างและวาดปุ่ม
class Button:
    def __init__(self, rect, text, color, hover_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface, mouse_pos):
        is_hover = self.rect.collidepoint(mouse_pos)
        fill = self.hover_color if is_hover else self.color
        pygame.draw.rect(surface, fill, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        # render text
        txt = FONT.render(self.text, True, BLACK)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)
        return is_hover


# สร้างปุ่ม 3 ปุ่ม
btn_width, btn_height = 300, 56
gap = 12
start_y = (HEIGHT - (3 * btn_height + 2 * gap)) // 2

buttons = [
    Button(((WIDTH - btn_width) // 2, start_y + i * (btn_height + gap), btn_width, btn_height),
           text, color, DARK_GRAY)
    for i, (text, color) in enumerate([
        ("(Easy)", GREEN),
        ("(Medium)", YELLOW),
        ("(Hard)", RED),
    ])
]


def draw_header():
    title = FONT.render("Level", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 48))
    SCREEN.blit(title, title_rect)


def main():
    selected = None
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # ปิดหน้าต่างโปรแกรม
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # ตรวจสอบว่าคลิกปุ่มใด
                for b in buttons:
                    if b.rect.collidepoint(event.pos):
                        selected = b.text
                        print("ผู้ใช้เลือก:", selected)
                        # ที่นี่สามารถเรียกฟังก์ชันอื่น / ส่งค่าไปยังเกมหลัก ฯลฯ
                        pygame.time.delay(250)
                        pygame.quit()
                        return selected

        SCREEN.fill(WHITE)
        draw_header()
        for b in buttons:
            b.draw(SCREEN, mouse_pos)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    choice = main()
    # ถ้าต้องการใช้ค่าในโปรแกรมต่อ:
    # print("ระดับที่ได้ไปใช้ต่อ:", choice)