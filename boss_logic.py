# -------------------
# ไฟล์: boss_logic.py
# -------------------
import pygame # นำเข้า pygame
from bullet_logic import create_bullet # นำเข้าฟังก์ชันสร้างกระสุน

# 🌟 ค่าคงที่เหล่านี้ใช้เฉพาะในไฟล์นี้ (ไม่ทำให้เกิด Circular Import)
# เลยเก็บไว้ที่นี่ได้
BOSS_SPAWN_RATE = 20 # อัตราการยิงของบอส (ค่า Cooldown เป็นเฟรม)
BOSS_SPEED = 6       # ความเร็วของกระสุนบอส
PHASE_DURATION = { # ระยะเวลาของแต่ละเฟส
    "single": 300,
    "spread": 300, 
    "wait": 120    
}

def create_boss(hp, width):
    """
    สร้างบอส
    รับค่า hp (จาก main.py)
    รับค่า width (จาก main.py) เพื่อกำหนดจุดเกิด
    """
    # โหลดรูปภาพบอส (ใช้ .convert_alpha() เพื่อรองรับความโปร่งใส)
    image = pygame.image.load("boss2.png").convert_alpha()
    # ปรับขนาดรูปภาพบอสเป็น 120x120 pixels
    image = pygame.transform.scale(image, (120, 120))

    # 🌟 สร้างสี่เหลี่ยม (rect) โดยใช้ width ที่รับมาจาก main.py
    rect = image.get_rect(center=(width // 2, 100))
    
    # คืนค่า Dictionary ที่เก็บข้อมูลของบอส
    return {
        "image": image, "rect": rect, "speed": 5, "dir": 1,
        "hp": hp, "max_hp": hp,
        "phases": ["single", "spread", "wait"],
        "current_phase_index": 0,
        "current_phase": "single",
        "phase_timer": PHASE_DURATION["single"], # ใช้ค่าคงที่ภายในไฟล์นี้
        "cd": 0 
    }

def update_boss(boss, bullet_img, max_width): 
    """
    อัปเดตบอส (การเคลื่อนที่, การยิง, เปลี่ยนเฟส)
    รับค่า max_width มาจาก main.py เพื่อเช็คขอบจอ
    """
    # เคลื่อนที่บอสในแกน X (ตามความเร็วและทิศทาง dir)
    boss["rect"].x += boss["speed"] * boss["dir"]
    # 🌟 ตรวจสอบว่าบอสชนขอบจอซ้าย หรือ ขวา หรือไม่ (ใช้ max_width ที่รับเข้ามา)
    if boss["rect"].left <= 0 or boss["rect"].right >= max_width: 
        boss["dir"] *= -1 # ถ้าชน ให้สลับทิศทาง
        
    # สร้าง List ว่างสำหรับเก็บกระสุนที่บอสยิงในเฟรมนี้
    bullets_fired = []
    # ใช้ค่าคงที่ภายในไฟล์นี้
    rate = BOSS_SPAWN_RATE 
    speed = BOSS_SPEED    

    # ลดเวลาของเฟสปัจจุบันลง 1
    boss["phase_timer"] -= 1
    # ถ้าเวลาของเฟสปัจจุบันหมดลง
    if boss["phase_timer"] <= 0:
        # เปลี่ยน Index ของเฟส (วนลูป)
        boss["current_phase_index"] = (boss["current_phase_index"] + 1) % len(boss["phases"])
        # อัปเดตชื่อเฟสปัจจุบัน
        boss["current_phase"] = boss["phases"][boss["current_phase_index"]]
        # ตั้งเวลาเฟสใหม่ (ใช้ค่าคงที่ภายในไฟล์นี้)
        boss["phase_timer"] = PHASE_DURATION[boss["current_phase"]] 
        boss["cd"] = 0 # รีเซ็ต Cooldown การยิง
        
    # ถ้า Cooldown การยิงยังเหลือ
    if boss["cd"] > 0:
        boss["cd"] -= 1 # ลดค่า Cooldown ลง 1
    
    # ถ้า Cooldown เป็น 0 และ เฟสปัจจุบันไม่ใช่ "wait"
    if boss["cd"] == 0 and boss["current_phase"] != "wait":
        # กำหนดตำแหน่งยิง
        x, y = boss["rect"].centerx, boss["rect"].bottom
        
        # ถ้าเป็นเฟส "single"
        if boss["current_phase"] == "single":
            boss["cd"] = rate # ตั้ง Cooldown
            bullets_fired.append(create_bullet(x, y, 0, speed, bullet_img)) # สร้างกระสุน 1 นัด
            
        # หรือถ้าเป็นเฟส "spread"
        elif boss["current_phase"] == "spread":
            boss["cd"] = rate * 2 # ตั้ง Cooldown (นานขึ้น 2 เท่า)
            bullets_fired.append(create_bullet(x, y, 0, speed, bullet_img)) # นัดที่ 1 (ตรง)
            bullets_fired.append(create_bullet(x, y, -2, speed, bullet_img)) # นัดที่ 2 (เฉียงซ้าย)
            bullets_fired.append(create_bullet(x, y, 2, speed, bullet_img)) # นัดที่ 3 (เฉียงขวา)
    
    # คืนค่า List กระสุนที่บอสยิงในเฟรมนี้
    return bullets_fired 

def draw_boss(surface, boss, red_color, green_color):
    """
    วาดบอส และ HP Bar
    รับค่า red_color, green_color มาจาก main.py
    """
    # สร้างสี่เหลี่ยมสำหรับพื้นหลัง HP Bar (สีแดง)
    hp_bar = pygame.Rect(boss["rect"].left, boss["rect"].top - 20, boss["rect"].width, 15)
    # 🌟 วาดพื้นหลัง HP Bar (ใช้ red_color ที่รับเข้ามา)
    pygame.draw.rect(surface, red_color, hp_bar)
    
    # ตรวจสอบว่าบอสยังมี HP เหลือ
    if boss["hp"] > 0:
        # คำนวณความกว้างของ HP Bar ปัจจุบัน
        hp_width = (boss["hp"] / boss["max_hp"]) * boss["rect"].width
        # สร้างสี่เหลี่ยมสำหรับ HP Bar ปัจจุบัน
        cur_hp_bar = pygame.Rect(boss["rect"].left, boss["rect"].top - 20, hp_width, 15)
        # 🌟 วาด HP Bar ปัจจุบัน (ใช้ green_color ที่รับเข้ามา)
        pygame.draw.rect(surface, green_color, cur_hp_bar)
    
    # วาดรูปบอส
    surface.blit(boss["image"], boss["rect"])

def hit_boss(boss, dmg):
    """
    เมื่อบอสโดนโจมตี
    """
    boss["hp"] -= dmg # ลด HP บอส

def is_boss_dead(boss):
    """
    ตรวจสอบว่าบอสตายหรือยัง
    """
    return boss["hp"] <= 0 # คืนค่า True ถ้า HP น้อยกว่าหรือเท่ากับ 0