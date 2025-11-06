import pygame
import random
from player import Player 
from boss import Boss     
from bullet import Bullet 
import game 

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

DIFFICULTIES = {"easy": {"spawn_rate": 30, "speed": 4, "name": "ง่าย"}}
BOSS_HP = {"easy": 50,}
PLAYER_HP = {"easy": 5}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game (Prototype)")

my_font = pygame.font.SysFont("Tahoma", 40)

page = "main_menu" 
char = 1 

player = None
boss = None
b_bullets = []
p_bullets = []

def draw_text(text, x, y, color=WHITE):
    text_obj = my_font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)
    
start_btn = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
quit_btn = pygame.Rect(WIDTH // 2 - 100, 320, 200, 50)
win_back_btn = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)

clock = pygame.time.Clock()
running = True

while running:
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                
                if page == "main_menu":
                    if start_btn.collidepoint(mouse_pos):
                        char = 1
                        diff = "easy"                        
                        player, boss, p_bullets, b_bullets = game.reset_game(char, diff, PLAYER_HP, BOSS_HP)
                        
                        page = "game_running"
                        
                    if quit_btn.collidepoint(mouse_pos): 
                        running = False
                
                elif page == "win_screen":
                    if win_back_btn.collidepoint(mouse_pos): 
                        page = "main_menu"

    screen.fill(BLACK) 
    
    if page == "main_menu":
        draw_text("My Game", WIDTH // 2, 100) 
        pygame.draw.rect(screen, GRAY, start_btn); draw_text("Start", start_btn.centerx, start_btn.centery)
        pygame.draw.rect(screen, GRAY, quit_btn); draw_text("Quit", quit_btn.centerx, quit_btn.centery)

    elif page == "game_running":
        
        diff_settings = DIFFICULTIES[diff]
        next_page = game.run_game_frame(screen, player, boss, p_bullets, b_bullets, diff_settings, WIDTH, HEIGHT, RED, my_font)
        
        if next_page: 
            page = next_page

    elif page == "win_screen":
        draw_text("ชนะละ!", WIDTH // 2, 200, GREEN) 
        draw_text("ขอบคุณที่เล่น", WIDTH // 2, 300)
        pygame.draw.rect(screen, GRAY, win_back_btn)
        draw_text("กลับ", win_back_btn.centerx, win_back_btn.centery)

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()