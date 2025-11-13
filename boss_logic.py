import pygame 
# นำเข้าฟังก์ชัน create_bullet จากไฟล์ bullet_logic.py
from bullet_logic import create_bullet 


# เลยเก็บไว้ที่นี่ได้
# อัตราการยิงของบอส (ค่า Cooldown เป็นเฟรม)
BOSS_SPAWN_RATE = 20  
# ความเร็วของกระสุนบอส
BOSS_SPEED = 6      
# ระยะเวลาของแต่ละเฟส
PHASE_DURATION = { 
    "single": 300, # เฟสยิงนัดเดียว: 300 เฟรม
    "spread": 300, # เฟสยิงกระจาย: 300 เฟรม
    "wait": 120    # เฟสหยุดพัก: 120 เฟรม
}

def create_boss(hp, width):
    """
    สร้างบอส (คืนค่าเป็น Dictionary)
    รับค่า hp (จาก main.py)
    รับค่า width (จาก main.py) เพื่อกำหนดจุดเกิด
    """
    image = pygame.image.load("boss2.png")
    # ปรับขนาดรูปภาพบอสเป็น 120x120 pixels
    image = pygame.transform.scale(image, (120, 120))


    # เพื่อกำหนดตำแหน่งเริ่มต้น (กึ่งกลางบน)
    rect = image.get_rect(center=(width // 2, 100))
    
    # คืนค่า Dictionary ที่เก็บข้อมูลของบอส
    return {
        "image": image,               # รูปภาพบอส
        "rect": rect,                 # สี่เหลี่ยม (ตำแหน่งและขนาด)
        "speed": 5,                   # ความเร็วในการเคลื่อนที่ (ซ้าย-ขวา)
        "dir": 1,                     # ทิศทางการเคลื่อนที่ (1 = ขวา, -1 = ซ้าย)
        "hp": hp,                     # HP ปัจจุบัน (ที่รับมาจาก main.py)
        "max_hp": hp,                 # HP สูงสุด (สำหรับคำนวณ HP bar)
        "phases": ["single", "spread", "wait"], # List ของเฟสทั้งหมด
        "current_phase_index": 0,     # Index ของเฟสปัจจุบัน
        "current_phase": "single",    # ชื่อของเฟสปัจจุบัน
        "phase_timer": PHASE_DURATION["single"], # ตัวนับเวลาถอยหลัง (ใช้ค่าคงที่ในไฟล์นี้)
        "cd": 0                       # Cooldown การยิง
    }

def update_boss(boss, bullet_img, max_width): 
    """
    อัปเดตบอส (การเคลื่อนที่, การยิง, เปลี่ยนเฟส)
    รับค่า max_width มาจาก main.py เพื่อใช้เช็คขอบจอ
    """
    # เคลื่อนที่บอสในแกน X (ตามความเร็วและทิศทาง dir)
    boss["rect"].x += boss["speed"] * boss["dir"]
    if boss["rect"].left <= 0 or boss["rect"].right >= max_width: 
        boss["dir"] *= -1 # ถ้าชน ให้สลับทิศทาง
        
    # สร้าง List ว่างสำหรับเก็บกระสุนที่บอสยิงในเฟรมนี้
    bullets_fired = []
    # ใช้ค่าคงที่ภายในไฟล์นี้
    rate = BOSS_SPAWN_RATE 
    speed = BOSS_SPEED    

    # ลดเวลาของเฟสปัจจุบันลง 1
    boss["phase_timer"] -= 1
    # ถ้าเวลาของเฟสปัจจุบันหมดลง (น้อยกว่าหรือเท่ากับ 0)
    if boss["phase_timer"] <= 0:
        # เปลี่ยน Index ของเฟส (เช่น (0+1)%3 = 1, (1+1)%3 = 2, (2+1)%3 = 0)
        boss["current_phase_index"] = (boss["current_phase_index"] + 1) % len(boss["phases"])
        # อัปเดตชื่อเฟสปัจจุบัน
        boss["current_phase"] = boss["phases"][boss["current_phase_index"]]
        # ตั้งเวลาเฟสใหม่ (ใช้ค่าคงที่ภายในไฟล์นี้)
        boss["phase_timer"] = PHASE_DURATION[boss["current_phase"]] 
        boss["cd"] = 0 # รีเซ็ต Cooldown การยิง
        
    # ถ้า Cooldown การยิงยังเหลือ (มากกว่า 0)
    if boss["cd"] > 0:
        boss["cd"] -= 1 # ลดค่า Cooldown ลง 1 (นับถอยหลัง)
    
    # ถ้า Cooldown เป็น 0 และ เฟสปัจจุบันไม่ใช่ "wait" (เฟสพัก)
    if boss["cd"] == 0 and boss["current_phase"] != "wait":
        # กำหนดตำแหน่งยิง (แกน X คือกึ่งกลางบอส, แกน Y คือด้านล่างของบอส)
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
    รับค่า red_color, green_color มาจาก main.py (เพราะไฟล์นี้ไม่รู้จักสี)
    """
    # สร้างสี่เหลี่ยมสำหรับพื้นหลัง HP Bar (อยู่เหนือบอส 20 pixels)
    hp_bar = pygame.Rect(boss["rect"].left, boss["rect"].top - 20, boss["rect"].width, 15)
    # 🌟 วาดพื้นหลัง HP Bar (ใช้ red_color ที่รับเข้ามา)
    pygame.draw.rect(surface, red_color, hp_bar)
    
    # ตรวจสอบว่าบอสยังมี HP เหลือ (มากกว่า 0)
    if boss["hp"] > 0:
        # คำนวณความกว้างของ HP Bar ปัจจุบัน (เทียบสัดส่วน HP)
        hp_width = (boss["hp"] / boss["max_hp"]) * boss["rect"].width
        # สร้างสี่เหลี่ยมสำหรับ HP Bar ปัจจุบัน
        cur_hp_bar = pygame.Rect(boss["rect"].left, boss["rect"].top - 20, hp_width, 15)
        # 🌟 วาด HP Bar ปัจจุบัน (ใช้ green_color ที่รับเข้ามา)
        pygame.draw.rect(surface, green_color, cur_hp_bar)
    
    # วาดรูปบอส
    surface.blit(boss["image"], boss["rect"])

def hit_boss(boss, dmg):
    """
    ฟังก์ชันเมื่อบอสโดนโจมตี
    """
    boss["hp"] -= dmg # ลด HP บอส (ตามความเสียหาย dmg)

def is_boss_dead(boss):
    """
    ฟังก์ชันตรวจสอบว่าบอสตายหรือยัง
    """
    # คืนค่า True ถ้า HP น้อยกว่าหรือเท่ากับ 0
    return boss["hp"] <= 0