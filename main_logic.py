import pygame
import player_logic
import boss_logic
import bullet_logic
import game_utils


WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

BOSS_HP = 50        

# สร้าง Dictionary เก็บค่า HP ของผู้เล่นตามระดับความยาก
PLAYER_HP_SETTINGS = {
    "easy": 5,     
    "medium": 3,   
    "hard": 1      
}


def reset_game(diff):
    # สร้าง List ว่างสำหรับเก็บกระสุนบอส
    boss_bullets = []
    # สร้าง List ว่างสำหรับเก็บกระสุนผู้เล่น
    player_bullets = []
    
    player = player_logic.create_player(PLAYER_HP_SETTINGS[diff], WIDTH, HEIGHT)
    boss = boss_logic.create_boss(BOSS_HP, WIDTH)
    
    return player, boss, player_bullets, boss_bullets

# สร้างฟังก์ชันสำหรับรันเกม 1 เฟรม (เป็นหัวใจหลักของ Logic เกม)
def run_game_frame(screen, player, boss, player_bullets, boss_bullets, my_font, player_img, boss_img):
    
    # (ส่งค่า WIDTH, HEIGHT ไปให้ เพื่อให้ player_logic รู้ขอบเขตจอ)
    new_player_bullets = player_logic.update_player(player, player_img, WIDTH, HEIGHT) 
    # (ส่งค่า WIDTH ไปให้ เพื่อให้ boss_logic รู้ขอบเขตจอ)
    new_boss_bullets = boss_logic.update_boss(boss, boss_img, WIDTH) 
    
    # นำกระสุนใหม่ของผู้เล่นไปรวมกับ List หลัก (p_bullets)
    player_bullets.extend(new_player_bullets)
    # นำกระสุนใหม่ของบอสไปรวมกับ List หลัก (b_bullets)
    boss_bullets.extend(new_boss_bullets)
    
    # วนลูปกระสุนผู้เล่น (ใช้ [:] เพื่อสร้างสำเนา List ทำให้ลบสมาชิกขณะวนลูปได้)
    for p in player_bullets[:]:
        # 🌟 เรียกใช้ฟังก์ชัน update_bullet จากโมดูล bullet_logic
        bullet_logic.update_bullet(p) 
        # ตรวจสอบว่ากระสุนตกขอบจอ (บน, ล่าง, ซ้าย, ขวา) หรือไม่
        if p["rect"].bottom < 0 or p["rect"].top > HEIGHT or p["rect"].left > WIDTH or p["rect"].right < 0:
            # ถ้าตกขอบจอ ให้ลบกระสุนนั้นทิ้ง
            player_bullets.remove(p)
            
    # วนลูปกระสุนบอส (ใช้ [:] เช่นกัน)
    for b in boss_bullets[:]:
        # 🌟 เรียกใช้ฟังก์ชัน update_bullet จากโมดูล bullet_logic
        bullet_logic.update_bullet(b) 
        # ตรวจสอบว่ากระสุนตกขอบจอหรือไม่
        if b["rect"].bottom < 0 or b["rect"].top > HEIGHT or b["rect"].left > WIDTH or b["rect"].right < 0:
            # ถ้าตกขอบจอ ให้ลบกระสุนนั้นทิ้ง
            boss_bullets.remove(b)

    # วนลูปกระสุนบอส (เพื่อเช็คการชนผู้เล่น)
    for b in boss_bullets[:]: 
        # ตรวจสอบว่าสี่เหลี่ยมของผู้เล่น ชนกับ สี่เหลี่ยมของกระสุนบอส หรือไม่
        if player["rect"].colliderect(b["rect"]):
            # 🌟 เรียกใช้ฟังก์ชัน hit_player จากโมดูล player_logic
            player_logic.hit_player(player) 
            # ลบกระสุนนัดนั้นทิ้ง (ป้องกันการโดนซ้ำ)
            boss_bullets.remove(b) 
            
    # วนลูปกระสุนผู้เล่น (เพื่อเช็คการชนบอส)
    for p in player_bullets[:]: 
        # ตรวจสอบว่าสี่เหลี่ยมของบอส ชนกับ สี่เหลี่ยมของกระสุนผู้เล่น หรือไม่
        if boss["rect"].colliderect(p["rect"]):
            # 🌟 เรียกใช้ฟังก์ชัน hit_boss จากโมดูล boss_logic
            boss_logic.hit_boss(boss, 1) 
            # ลบกระสุนนัดนั้นทิ้ง
            player_bullets.remove(p) 
    
    # ตรวจสอบว่าผู้เล่นตายหรือไม่
    if player_logic.is_player_dead(player):
        # ถ้าตาย ให้คืนค่าสถานะ (page) "game_over"
        return "game_over" 
    # ตรวจสอบว่าบอสตายหรือไม่
    if boss_logic.is_boss_dead(boss):
        # ถ้าบอสตาย ให้คืนค่าสถานะ (page) "win_screen"
        return "win_screen"

    player_logic.draw_player(screen, player) 
    # (และส่งค่าสี RED, GREEN ที่ไฟล์นี้เก็บไว้ ไปให้)
    boss_logic.draw_boss(screen, boss, RED, GREEN)   
    
    # วนลูปกระสุนผู้เล่น (เพื่อวาด)
    for p in player_bullets:
        # วาดกระสุนผู้เล่น
        screen.blit(p["image"], p["rect"])
    # วนลูปกระสุนบอส (เพื่อวาด)
    for b in boss_bullets:
        # วาดกระสุนบอส
        screen.blit(b["image"], b["rect"])
        
 
    # เพื่อวาดข้อความแสดง HP ผู้เล่น (ที่มุมบนขวา)
    game_utils.draw_text_utility(screen, my_font, f"HP: {player['hp']}", WIDTH - 100, 30, RED)

    # ถ้าเกมยังไม่จบ (ไม่แพ้/ไม่ชนะ) ให้คืนค่า None
    return None



# เริ่มต้นการทำงานของ pygame
pygame.init()
# สร้างหน้าจอเกมตามขนาด (WIDTH, HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# ตั้งชื่อหน้าต่างเกม (Window Title)
pygame.display.set_caption("My Game (Prototype - Bullets)")

my_font = pygame.font.SysFont("Tahoma", 40)

# --- โหลดรูปภาพทั้งหมด ---

BACKGROUND_IMAGE = pygame.image.load("Background.png")
# ปรับขนาดรูปพื้นหลังให้พอดีจอ (WIDTH, HEIGHT)
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
    

MENU_BACKGROUND_IMAGE = pygame.image.load("Firstpage.png")
DIFFICULTY_MENU_IMAGE = pygame.image.load("Pagetwo.png")
# ปรับขนาดรูปพื้นหลังหน้าให้พอดีจอ
MENU_BACKGROUND_IMAGE = pygame.transform.scale(MENU_BACKGROUND_IMAGE, (WIDTH, HEIGHT))
DIFFICULTY_MENU_IMAGE = pygame.image.load("Pagetwo.png")
# ปรับขนาดรูปพื้นหลังหน้า 2 ให้พอดีจอ
DIFFICULTY_MENU_IMAGE = pygame.transform.scale(DIFFICULTY_MENU_IMAGE, (WIDTH, HEIGHT))
p_bullet_img_orig = pygame.image.load("bullet_player.png")
PLAYER_BULLET_IMG = pygame.transform.scale(p_bullet_img_orig, (20, 40)) 
b_bullet_img_orig = pygame.image.load("bullet_boss.png")
BOSS_BULLET_IMG = pygame.transform.scale(b_bullet_img_orig, (30, 30)) 
# --- จบการโหลดรูปภาพ ---


# กำหนดสถานะ (หน้า) เริ่มต้นของเกม
page = "main_menu" 
# กำหนดค่าความยากเริ่มต้น
diff = "easy" 

# สร้างตัวแปรผู้เล่น (เริ่มต้นเป็น None คือยังไม่สร้าง Object)
player = None
# สร้างตัวแปรบอส (เริ่มต้นเป็น None)
boss = None
# สร้าง List กระสุนบอส (ว่าง)
b_bullets = []
# สร้าง List กระสุนผู้เล่น (ว่าง)
p_bullets = []

# สร้างฟังก์ชันย่อ (wrapper) สำหรับ draw_text_utility (ให้เรียกใช้ง่ายขึ้น)
def draw_text(text, x, y, color=WHITE):
    # 🌟 เรียกใช้ฟังก์ชัน draw_text_utility จากโมดูล game_utils
    game_utils.draw_text_utility(screen, my_font, text, x, y, color)
    

#ปุ่ม Start
start_btn = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
#ปุ่ม Quit
quit_btn = pygame.Rect(WIDTH // 2 - 100, 320, 200, 50)
# Back (หน้า Win)
win_back_btn = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
#ปุ่ม Easy
easy_btn = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
#ปุ่ม Medium
medium_btn = pygame.Rect(WIDTH // 2 - 100, 270, 200, 50)
#ปุ่ม Hard
hard_btn = pygame.Rect(WIDTH // 2 - 100, 340, 200, 50)
#ปุ่ม Back (หน้า Difficulty)
diff_back_btn = pygame.Rect(WIDTH // 2 - 100, 410, 200, 50)
#ปุ่ม Retry (หน้า Game Over)
retry_btn = pygame.Rect(WIDTH // 2 - 100, 270, 200, 50)
#ปุ่ม Back (หน้า Game Over)
game_over_back_btn = pygame.Rect(WIDTH // 2 - 100, 340, 200, 50)



# สร้าง Object Clock สำหรับควบคุม Framerate (FPS)
clock = pygame.time.Clock()
running = True

while running:
    # อ่านตำแหน่งของเมาส์ในเฟรมนี้
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # ตรวจสอบว่า Event คือการคลิกเมาส์
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 

                if page == "main_menu":
                    # ตรวจสอบว่าคลิก (mouse_pos) โดนปุ่ม Start (start_btn) หรือไม่
                    if start_btn.collidepoint(mouse_pos):
                        # ถ้าใช่ ให้เปลี่ยนสถานะ (page) ไปหน้า "difficulty_menu"
                        page = "difficulty_menu" 
                    if quit_btn.collidepoint(mouse_pos): 
                        # ถ้าใช่ ให้ออกจาก Game Loop
                        running = False
                
                # หรือถ้าอยู่ที่หน้า "difficulty_menu"
                elif page == "difficulty_menu":
                    # ตรวจสอบว่าคลิกโดนปุ่ม Easy
                    if easy_btn.collidepoint(mouse_pos):
                        # ตั้งค่าความยากเป็น "easy"
                        diff = "easy"
                        # เรียกฟังก์ชันรีเซ็ตเกม (เริ่มเกมใหม่ด้วยความยากนี้)
                        player, boss, p_bullets, b_bullets = reset_game(diff)
                        # เปลี่ยนสถานะไปหน้า "game_running"
                        page = "game_running"
                    # ตรวจสอบว่าคลิกโดนปุ่ม Medium
                    if medium_btn.collidepoint(mouse_pos):
                        # ตั้งค่าความยากเป็น "medium"
                        diff = "medium"
                        # เรียกฟังก์ชันรีเซ็ตเกม
                        player, boss, p_bullets, b_bullets = reset_game(diff)
                        # เปลี่ยนสถานะไปหน้า "game_running"
                        page = "game_running"
                    # ตรวจสอบว่าคลิกโดนปุ่ม Hard
                    if hard_btn.collidepoint(mouse_pos):
                        # ตั้งค่าความยากเป็น "hard"
                        diff = "hard"
                        # เรียกฟังก์ชันรีเซ็ตเกม
                        player, boss, p_bullets, b_bullets = reset_game(diff)
                        # เปลี่ยนสถานะไปหน้า "game_running"
                        page = "game_running"
                    # ตรวจสอบว่าคลิกโดนปุ่ม Back
                    if diff_back_btn.collidepoint(mouse_pos):
                        # กลับไปหน้าเมนูหลัก
                        page = "main_menu"

                # หรือถ้าอยู่ที่หน้า "win_screen"
                elif page == "win_screen":
                    # ตรวจสอบว่าคลิกโดนปุ่ม Back
                    if win_back_btn.collidepoint(mouse_pos): 
                        # กลับไปหน้าเมนูหลัก
                        page = "main_menu"

                # หรือถ้าอยู่ที่หน้า "game_over"
                elif page == "game_over":
                    # ตรวจสอบว่าคลิกโดนปุ่ม Retry
                    if retry_btn.collidepoint(mouse_pos):
                        player, boss, p_bullets, b_bullets = reset_game(diff)
                        # เปลี่ยนสถานะไปหน้า "game_running"
                        page = "game_running"
                    # ตรวจสอบว่าคลิกโดนปุ่ม Back
                    if game_over_back_btn.collidepoint(mouse_pos):
                        # กลับไปหน้าเมนูหลัก
                        page = "main_menu"



    if page == "main_menu":
        # วาดพื้นหลังเมนู
        screen.blit(MENU_BACKGROUND_IMAGE, (0, 0))
    # หรือถ้าอยู่ที่หน้าเลือกความยาก
    elif page == "difficulty_menu":
        # วาดพื้นหลังหน้าเลือกความยาก
        screen.blit(DIFFICULTY_MENU_IMAGE, (0, 0))
    # หรือถ้ากำลังเล่นเกม (และโหลดรูป BACKGROUND_IMAGE สำเร็จ)
    elif page == "game_running" and BACKGROUND_IMAGE:
        # วาดพื้นหลังตอนเล่นเกม
        screen.blit(BACKGROUND_IMAGE, (0, 0))
    # กรณีหน้าอื่นๆ (เช่น win, game_over)
    else:
        # เติมหน้าจอด้วยสีดำ
        screen.fill(BLACK)
    # --- จบการวาดพื้นหลัง ---

    # --- ส่วนการวาด (ตามสถานะ page) ---
    # (วาดทับพื้นหลัง)
    # ถ้าอยู่ที่หน้า "main_menu"
    if page == "main_menu":
        # วาดชื่อเกม
        draw_text("My Game", WIDTH // 2, 100) 
        # วาดปุ่ม Start (สี่เหลี่ยมสีเทา) และ ข้อความ "Start" บนปุ่ม
        pygame.draw.rect(screen, GRAY, start_btn); draw_text("Start", start_btn.centerx, start_btn.centery)
        # วาดปุ่ม Quit และ ข้อความ "Quit" บนปุ่ม
        pygame.draw.rect(screen, GRAY, quit_btn); draw_text("Quit", quit_btn.centerx, quit_btn.centery)

    # หรือถ้าอยู่ที่หน้า "difficulty_menu"
    elif page == "difficulty_menu":
        # วาดหัวข้อ "Select Difficulty"
        draw_text("Select Difficulty", WIDTH // 2, 100)
        # วาดคำอธิบาย
        draw_text("Difficulty only affects Player HP", WIDTH // 2, 150) 
        # วาดปุ่ม Easy และข้อความ
        pygame.draw.rect(screen, GRAY, easy_btn); draw_text("Easy (5 HP)", easy_btn.centerx, easy_btn.centery)
        # วาดปุ่ม Medium และข้อความ
        pygame.draw.rect(screen, GRAY, medium_btn); draw_text("Medium (3 HP)", medium_btn.centerx, medium_btn.centery)
        # วาดปุ่ม Hard และข้อความ
        pygame.draw.rect(screen, GRAY, hard_btn); draw_text("Hard (1 HP)", hard_btn.centerx, hard_btn.centery)
        # วาดปุ่ม Back และข้อความ
        pygame.draw.rect(screen, GRAY, diff_back_btn); draw_text("Back", diff_back_btn.centerx, diff_back_btn.centery)

    # หรือถ้าอยู่ที่หน้า "game_running"
    elif page == "game_running":
        # เรียกฟังก์ชันรันเกม 1 เฟรม (อัปเดต logic + วาด)
        # และรับสถานะถัดไป (None, "game_over", หรือ "win_screen")
        next_page = run_game_frame(screen, player, boss, p_bullets, b_bullets, my_font, PLAYER_BULLET_IMG, BOSS_BULLET_IMG) 
        
        # ตรวจสอบว่าเกมจบหรือไม่ (ถ้า next_page ไม่ใช่ None)
        if next_page: 
            # อัปเดตสถานะของเกม (เปลี่ยน page)
            page = next_page

    # หรือถ้าอยู่ที่หน้า "win_screen"
    elif page == "win_screen":
        # วาดข้อความแสดงความยินดี (สีเขียว)
        draw_text("ชนะละ!", WIDTH // 2, 200, GREEN) 
        # วาดข้อความขอบคุณ
        draw_text("ขอบคุณที่เล่น", WIDTH // 2, 300)
        # วาดปุ่ม Back
        pygame.draw.rect(screen, GRAY, win_back_btn)
        # วาดข้อความบนปุ่ม Back
        draw_text("กลับ", win_back_btn.centerx, win_back_btn.centery)

    # หรือถ้าอยู่ที่หน้า "game_over"
    elif page == "game_over":
        # วาดข้อความแสดงการแพ้ (สีแดง)
        draw_text("แพ้แล้ว...", WIDTH // 2, 100, RED) 
        # วาดข้อความชวนเล่นใหม่
        draw_text("สู้ใหม่อีกครั้ง?", WIDTH // 2, 200)
        # วาดปุ่ม Retry และข้อความ
        pygame.draw.rect(screen, GRAY, retry_btn); draw_text("สู้อีกครั้ง", retry_btn.centerx, retry_btn.centery)
        # วาดปุ่ม Back และข้อความ
        pygame.draw.rect(screen, GRAY, game_over_back_btn); draw_text("กลับ", game_over_back_btn.centerx, game_over_back_btn.centery)


    # อัปเดตการเปลี่ยนแปลงทั้งหมดลงบนหน้าจอจริง (สำคัญมาก)
    pygame.display.flip()
    # ควบคุมให้ Game Loop ทำงานไม่เกิน 60 เฟรมต่อวินาที (FPS)
    clock.tick(60) 

# จบการทำงานของ pygame (หลังจากหลุดจาก while loop)
pygame.quit()