#bullet_logic.py
import pygame 

def create_bullet(x, y, speed_x, speed_y, image_surface):
    
    image = image_surface 
    # สร้างสี่เหลี่ยม (rect) ให้กระสุน และกำหนดจุดกึ่งกลาง (center)
    rect = image.get_rect(center=(x, y))
    # คืนค่า Dictionary ที่เก็บข้อมูลของกระสุน
    return {
        "image": image,     
        "rect": rect,       
        "speed_x": speed_x, 
        "speed_y": speed_y  
    }

def update_bullet(bullet):
    """
    อัปเดตตำแหน่งกระสุน (เลื่อนกระสุน)
    """
    # อัปเดตตำแหน่งแกน X (บวกด้วยความเร็วแกน X)
    bullet["rect"].x += bullet["speed_x"]
    # อัปเดตตำแหน่งแกน Y (บวกด้วยความเร็วแกน Y)
    bullet["rect"].y += bullet["speed_y"]
