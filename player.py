import pygame
from bullet import Bullet

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player:
    
    def __init__(self):
        
        
        scale = 0.2
        
        path_left = "player_left.png" 

        self.img_left = pygame.image.load(path_left)
        
        self.img_left = pygame.transform.scale(self.img_left,(int(self.img_left.get_width()*scale),int(self.img_left.get_height()*scale)))
        self.img_right = pygame.transform.flip(self.img_left, True, False)
        
        self.hp = 3 
        self.iv = False 
        self.iv_timer = 0 
        self.cd = 0 

        self.dash = False
        self.dash_time = 0
        self.dash_cd = 0
        
        self.speed = 5 
        self.direction = "right" 
        
        self.image = self.img_right 
        self.rect = self.image.get_rect(
            center=(800 // 2, 600 - 70) 
        )

    def set_hp(self, hp):
        self.hp = hp

    def update(self,keys):
        
        bullets_fired = []
        
        SPEED = self.speed
        if not self.dash and keys[pygame.K_r] and self.dash_cd == 0 :
            self.dash = True
            self.dash_time = 20
            self.dash_cd = 40
        
        if self.dash :
            SPEED = self.speed * 2 
            self.dash_time -= 1
            if self.dash_time <= 0 :
                self.dash = False

        if self.dash_cd > 0 :
            self.dash_cd -= 1

        if keys[pygame.K_a]:
            self.rect.x -= SPEED
            self.direction = "left"
        elif keys[pygame.K_d]:
            self.rect.x += SPEED
            self.direction = "right"
        elif keys[pygame.K_w]:
            self.rect.y -= SPEED
        elif keys[pygame.K_s]:
            self.rect.y += SPEED
            
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 800: self.rect.right = 800
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 600: self.rect.bottom = 600
            
        if self.iv:
            self.iv_timer -= 1
            if self.iv_timer <= 0:
                self.iv = False
                
        if self.cd > 0:
            self.cd -= 1
            
        if keys[pygame.K_SPACE] and self.cd == 0:
            self.cd = 20 
            x = self.rect.centerx
            y = self.rect.top
            b = Bullet(x, y, 0, -10, GREEN, 10, 20) 
            bullets_fired.append(b)

        return bullets_fired 

    def draw(self, surface):
        
        
        if self.direction == "left":
            surface.blit(self.img_left, self.rect)
        else:
            surface.blit(self.img_right, self.rect)

    def hit(self):
        if not self.iv:
            self.hp -= 1
            self.iv = True
            self.iv_timer = 120 
            return True 
        return False 

    def is_dead(self):
        return self.hp <= 0