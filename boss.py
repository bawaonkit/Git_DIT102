# boss.py

import pygame
from bullet import Bullet 

# สี
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


PHASE_DURATION = {
    "single": 300,
    "spread": 300, 
    "wait": 120    
}

class Boss:
    
    def __init__(self):
        
        
        self.image = pygame.image.load("boss2.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (120, 120)) 
        self.rect = self.image.get_rect(
            center=(800 // 2, 100) 
        )
        
        self.speed = 5
        self.dir = 1 
        
        self.hp = 100
        self.max_hp = 100
        
        self.phases = ["single", "spread", "wait"]
        self.current_phase_index = 0
        self.current_phase = self.phases[self.current_phase_index]
        
        self.phase_timer = PHASE_DURATION[self.current_phase]
        self.cd = 0
        
    def set_hp(self, hp):
        self.hp = hp
        self.max_hp = hp
        
    def hit(self, dmg):
        self.hp -= dmg

    def is_dead(self):
        return self.hp <= 0
    
    def update(self, diff_settings):
        
        self.rect.x += self.speed * self.dir
        if self.rect.left <= 0 or self.rect.right >= 800: 
            self.dir *= -1
            
        bullets_fired = []
        
        rate = diff_settings["spawn_rate"]
        speed = diff_settings["speed"]


        self.phase_timer -= 1
        
        if self.phase_timer <= 0:
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phases)
            self.current_phase = self.phases[self.current_phase_index]
            
            self.phase_timer = PHASE_DURATION[self.current_phase]
            
            self.cd = 0 
            
        if self.cd > 0:
            self.cd -= 1
        
        if self.cd == 0 and self.current_phase != "wait":
            
            if self.current_phase == "single":
                self.cd = rate 
                x, y = self.rect.centerx, self.rect.bottom
                bullets_fired.append(Bullet(x, y, 0, speed, WHITE, 20, 20))
                
            elif self.current_phase == "spread":
                self.cd = rate * 2
                x, y = self.rect.centerx, self.rect.bottom
                bullets_fired.append(Bullet(x, y, 0, speed, WHITE, 20, 20)) 
                bullets_fired.append(Bullet(x, y, -2, speed, WHITE, 20, 20)) 
                bullets_fired.append(Bullet(x, y, 2, speed, WHITE, 20, 20)) 
        
        return bullets_fired 

    def draw(self, surface):

        hp_bar = pygame.Rect(self.rect.left, self.rect.top - 20, self.rect.width, 15)
        pygame.draw.rect(surface, RED, hp_bar)
        
        if self.hp > 0:
            hp_width = (self.hp / self.max_hp) * self.rect.width
            cur_hp_bar = pygame.Rect(self.rect.left, self.rect.top - 20, hp_width, 15)
            pygame.draw.rect(surface, GREEN, cur_hp_bar)
        
        surface.blit(self.image, self.rect)