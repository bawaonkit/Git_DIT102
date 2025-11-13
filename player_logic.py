import pygame
from bullet_logic import create_bullet

def create_player(hp, width, height):
    scale = 0.2
    img_left = pygame.image.load("player_left.png")
    img_left = pygame.transform.scale(img_left, (int(img_left.get_width() * scale), int(img_left.get_height() * scale)))
    img_right = pygame.transform.flip(img_left, True, False)
    #สร้างสี่เหลี่ยม (rect) โดยใช้ width, height ที่รับมาจาก main.py
    rect = img_left.get_rect(center=(width // 2, height - 70))
    return {
        "img_left": img_left,     
        "img_right": img_right,   
        "hp": hp,                 
        "cd": 0,                  
        "speed": 5,              
        "direction": "right",     
        "image": img_right,       
        "rect": rect              
    }

def update_player(player, bullet_img, max_width, max_height):
    bullets_fired = []
    keys = pygame.key.get_pressed()
    SPEED = player["speed"] * 2 if keys[pygame.K_r] else player["speed"]
    if keys[pygame.K_a]:
        player["rect"].x -= SPEED 
        player["direction"] = "left" 
    elif keys[pygame.K_d]:
        player["rect"].x += SPEED 
        player["direction"] = "right" 
    elif keys[pygame.K_w]:
        player["rect"].y -= SPEED 
    elif keys[pygame.K_s]:
        player["rect"].y += SPEED 
        
    #ตรวจสอบขอบจอ: โดยใช้ max_width, max_height ที่รับเข้ามา
    if player["rect"].left < 0: player["rect"].left = 0
    if player["rect"].right > max_width: player["rect"].right = max_width
    if player["rect"].top < 0: player["rect"].top = 0
    if player["rect"].bottom > max_height: player["rect"].bottom = max_height
    if player["cd"] > 0:
        player["cd"] -= 1 
    if keys[pygame.K_SPACE] and player["cd"] == 0:
        player["cd"] = 20 
        x = player["rect"].centerx 
        y = player["rect"].top 
        b = create_bullet(x, y, 0, -10, bullet_img) 
        bullets_fired.append(b) 
    return bullets_fired 

def draw_player(surface, player):
    if player["direction"] == "left":
        surface.blit(player["img_left"], player["rect"])
    else:
        surface.blit(player["img_right"], player["rect"])

def hit_player(player):
    player["hp"] -= 1 
    return True 

def is_player_dead(player):
    return player["hp"] <= 0