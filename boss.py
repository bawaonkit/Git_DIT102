# boss.py

import pygame
import random
import config
from bullet import Bullet # Import คลาส Bullet

class Boss(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((100, 50))
        self.image.fill(config.RED)
        self.rect = self.image.get_rect(
            center=(config.SCREEN_WIDTH // 2, 75)
        )
        
        self.speed = config.BOSS_SPEED
        self.direction = 1 
        
        self.attack_pattern = "wait"
        self.pattern_timer = 120 
        self.bullet_timer = 0
        
        self.hp = 100
        self.max_hp = 100
        
    def set_hp(self, hp):
        """ตั้งค่า HP เริ่มต้น (เรียกจาก main.py)"""
        self.hp = hp
        self.max_hp = hp
        
    def get_hit(self, damage):
        """ฟังก์ชันเมื่อบอสโดนยิง"""
        self.hp -= damage
        print(f"Boss hit! HP left: {self.hp}")

    def is_dead(self):
        """เช็คว่าบอสตายหรือยัง"""
        return self.hp <= 0
    
    def update(self, diff_settings):
        """อัปเดตบอส และคืนค่า 'list ของกระสุนที่ยิงใหม่'"""
        
        # 1. ย้ายบอส
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= config.SCREEN_WIDTH:
            self.direction *= -1
            
        bullets_to_fire = []
        spawn_rate = diff_settings["spawn_rate"]
        base_speed = diff_settings["speed"]

        # 3. จัดการ Pattern
        self.pattern_timer -= 1
        if self.pattern_timer <= 0:
            self.attack_pattern = random.choice(["wait", "single", "spread"])
            self.bullet_timer = 0 
            
            if self.attack_pattern == "wait":
                self.pattern_timer = random.randint(60, 120) 
            elif self.attack_pattern == "single":
                self.pattern_timer = random.randint(120, 180) 
            elif self.attack_pattern == "spread":
                self.pattern_timer = random.randint(180, 240)
                
        # 4. ยิงกระสุน
        self.bullet_timer += 1
        
        if self.attack_pattern == "single":
            if self.bullet_timer >= spawn_rate:
                self.bullet_timer = 0
                x, y = self.rect.centerx, self.rect.bottom
                bullets_to_fire.append(Bullet(x, y, 0, base_speed, config.WHITE, 20, 20))
                
        elif self.attack_pattern == "spread":
            if self.bullet_timer >= spawn_rate * 2:
                self.bullet_timer = 0
                x, y = self.rect.centerx, self.rect.bottom
                bullets_to_fire.append(Bullet(x, y, 0, base_speed, config.WHITE, 20, 20))
                bullets_to_fire.append(Bullet(x, y, -2, base_speed, config.WHITE, 20, 20))
                bullets_to_fire.append(Bullet(x, y, 2, base_speed, config.WHITE, 20, 20))
        
        return bullets_to_fire

    def draw(self, surface):
        """วาดบอส และแถบ HP"""
        
        # 1. วาดแถบ HP
        bg_bar_rect = pygame.Rect(self.rect.left, self.rect.top - 20, self.rect.width, 15)
        pygame.draw.rect(surface, config.RED, bg_bar_rect)
        
        if self.hp > 0:
            current_hp_width = (self.hp / self.max_hp) * self.rect.width
            health_bar_rect = pygame.Rect(self.rect.left, self.rect.top - 20, current_hp_width, 15)
            pygame.draw.rect(surface, config.GREEN, health_bar_rect)
        
        # 2. วาดตัวบอส
        surface.blit(self.image, self.rect)