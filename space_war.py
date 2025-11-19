import pygame
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Space War")
main_clock = pygame.time.Clock()
main_font = pygame.font.SysFont("Tahoma",20)
end_font = pygame.font.SysFont("Tahoma",60)

COLOR_WHITE = (255,255,255)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_GRAY = (100,100,100)

BACKGROUND_GAME = pygame.transform.scale(pygame.image.load("Background.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))
BACKGROUND_MENU = pygame.transform.scale(pygame.image.load("Firstpage.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))
BACKGROUND_LEVEL = pygame.transform.scale(pygame.image.load("Pagetwo.png"),(SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load("icon_game.png"))

Player_img = pygame.image.load("player.png")
IMG_PLAYER_L = pygame.transform.scale(Player_img,(int(Player_img.get_width()*0.2),int(Player_img.get_height()*0.2)))
IMG_PLAYER_R = pygame.transform.flip(IMG_PLAYER_L,True,False)
IMG_PLAYER_BULLET = pygame.transform.scale(pygame.image.load("bullet_player.png"),(20,40))

IMG_BOSS_R = pygame.transform.scale(pygame.image.load("boss2.png"),(120, 120))
IMG_BOSS_L = pygame.transform.flip(IMG_BOSS_R,True,False)
IMG_BOSS_BULLET = pygame.transform.scale(pygame.image.load("bullet_boss.png"),(30, 30))

pygame.mixer.music.load("song_background.mp3")
pygame.mixer.music.set_volume(0.25)
SOUND_HIT_PLAYER = pygame.mixer.Sound("player_hit.mp3")
SOUND_HIT_BOSS = pygame.mixer.Sound("boss_hit.mp3")
SOUND_WIN = pygame.mixer.Sound("if_win.mp3")
SOUND_LOSE = pygame.mixer.Sound("if_lose.mp3")

current_page = "main_menu"
player_direction = "right"
boss_direction = "right"
boss_phases = ["single","spread","wait"]


btn_start = pygame.Rect(SCREEN_WIDTH//2-100,250,200,50)
btn_quit = pygame.Rect(SCREEN_WIDTH//2-100,320,200,50)
btn_easy = pygame.Rect(SCREEN_WIDTH//2-100,200,200,50)
btn_norm = pygame.Rect(SCREEN_WIDTH//2-100,270,200,50)
btn_hard = pygame.Rect(SCREEN_WIDTH//2-100,340,200,50)
btn_back = pygame.Rect(SCREEN_WIDTH//2-100,410,200,50)
btn_retry = pygame.Rect(SCREEN_WIDTH//2-100,270,200,50)
btn_over_back = pygame.Rect(SCREEN_WIDTH//2-100,340,200,50)
btn_win_back = pygame.Rect(SCREEN_WIDTH//2-100,400,200,50)

is_running = True
while is_running:
    mouse_position = pygame.mouse.get_pos()
    if current_page in ["main_menu","difficulty_menu"]:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    else:
            pygame.mixer.music.stop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_page == "main_menu":
                if btn_start.collidepoint(mouse_position):
                    current_page = "difficulty_menu"
                if btn_quit.collidepoint(mouse_position):
                    is_running = False
            
            elif current_page == "difficulty_menu":
                do_start = False
                if btn_easy.collidepoint(mouse_position): 
                    selected_difficulty = "easy"
                    do_start = True
                if btn_norm.collidepoint(mouse_position):
                    selected_difficulty = "normal"
                    do_start = True
                if btn_hard.collidepoint(mouse_position):
                    selected_difficulty = "hard"
                    do_start = True
                
                if do_start:
                    score = 0
                    bullets_player = []
                    bullets_boss = []
                    
                    if selected_difficulty == "easy":
                        player_hp = 5
                    elif selected_difficulty == "normal":
                        player_hp = 3
                    else: 
                        player_hp = 1

                    player_rect = IMG_PLAYER_L.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT-70))
                    player_cooldown = 0
                    player_speed = 5
                    boss_hp = 50
                    boss_rect = IMG_BOSS_R.get_rect(center=(SCREEN_WIDTH//2,100))
                    boss_speed = 5
                    boss_direction_multiplier = 1
                    boss_phase_index = 0
                    boss_phase = "single"
                    boss_timer = 300
                    boss_cooldown = 0

                    current_page = "game_running"

                if btn_back.collidepoint(mouse_position):
                    current_page = "main_menu"

            elif current_page == "game_over":
                if btn_retry.collidepoint(mouse_position):
                    score = 0
                    bullets_player = []
                    bullets_boss = []
                    if selected_difficulty == "easy":
                        player_hp = 5
                    elif selected_difficulty == "normal":
                        player_hp = 3
                    else:
                        player_hp = 1
                    player_rect = IMG_PLAYER_L.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT-70))
                    player_cooldown = 0
                    player_speed = 5
                    boss_hp = 50
                    boss_rect = IMG_BOSS_R.get_rect(center=(SCREEN_WIDTH//2,100))
                    boss_speed = 5
                    boss_direction_multiplier = 1
                    boss_phase_index = 0
                    boss_phase = "single"
                    boss_direction = "right"
                    boss_timer = 300
                    boss_cooldown = 0
                    current_page = "game_running"
                
                if btn_over_back.collidepoint(mouse_position):
                    current_page = "main_menu"
            
            elif current_page == "win_screen":
                if btn_win_back.collidepoint(mouse_position):
                    current_page = "main_menu"

    if current_page == "main_menu":
        display_surface.blit(BACKGROUND_MENU,(0,0))
    elif current_page == "difficulty_menu":
        display_surface.blit(BACKGROUND_LEVEL,(0,0))
    elif current_page == "game_running":
        display_surface.blit(BACKGROUND_GAME,(0,0))
    elif current_page in ["game_over","win_screen"]:
        display_surface.blit(BACKGROUND_GAME,(0,0))

    if current_page == "main_menu":

        pygame.draw.rect(display_surface,COLOR_GRAY,btn_start)
        text_start = main_font.render("Start",True,COLOR_WHITE)
        display_surface.blit(text_start,(btn_start.centerx - text_start.get_width()//2,btn_start.centery - text_start.get_height()//2))
        
        pygame.draw.rect(display_surface,COLOR_GRAY,btn_quit)
        text_quit = main_font.render("Quit",True,COLOR_WHITE)
        display_surface.blit(text_quit,(btn_quit.centerx - text_quit.get_width()//2,btn_quit.centery - text_quit.get_height()//2))
        
        Name_game = end_font.render("Space War",True,COLOR_WHITE)
        display_surface.blit(Name_game,(SCREEN_WIDTH//2 - Name_game.get_width()//2,100))

    elif current_page == "difficulty_menu":

        Difficulty_text = end_font.render("Select level",True,COLOR_WHITE)
        display_surface.blit(Difficulty_text,(SCREEN_WIDTH//2 - Difficulty_text.get_width()//2,100))

        pygame.draw.rect(display_surface,COLOR_GRAY,btn_easy)
        Easy_btn=main_font.render("Easy",True,COLOR_WHITE)
        display_surface.blit(Easy_btn,(btn_easy.centerx-Easy_btn.get_width()//2,btn_easy.centery-Easy_btn.get_height()//2))

        pygame.draw.rect(display_surface,COLOR_GRAY,btn_norm)
        Normal_btn=main_font.render("Normal",True,COLOR_WHITE)
        display_surface.blit(Normal_btn,(btn_norm.centerx-Normal_btn.get_width()//2,btn_norm.centery-Normal_btn.get_height()//2))

        pygame.draw.rect(display_surface,COLOR_GRAY,btn_hard)
        Hard_btn=main_font.render("Hard",True,COLOR_WHITE)
        display_surface.blit(Hard_btn,(btn_hard.centerx-Hard_btn.get_width()//2,btn_hard.centery-Hard_btn.get_height()//2))

        pygame.draw.rect(display_surface, COLOR_GRAY,btn_back)
        Back_btn=main_font.render("Back",True,COLOR_WHITE)
        display_surface.blit(Back_btn,(btn_back.centerx-Back_btn.get_width()//2,btn_back.centery-Back_btn.get_height()//2))

    elif current_page == "game_running":

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_rect.x -= player_speed
            player_direction = "left"
        elif keys[pygame.K_d]:
            player_rect.x += player_speed
            player_direction = "right"
        
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH
        
        if player_cooldown > 0:
            player_cooldown -= 1
        if keys[pygame.K_SPACE] and player_cooldown == 0:
            player_cooldown = 20

            bullets_player.append({
                "IMG_PLAYER_BULLET": IMG_PLAYER_BULLET,
                "POSITION_PLAYER": IMG_PLAYER_BULLET.get_rect(center=(player_rect.centerx, player_rect.top)),
                "speed_playerbullet_x": 0,
                "speed_playerbullet_y": -10
            })

        boss_rect.x += boss_speed * boss_direction_multiplier
        if boss_rect.right >= SCREEN_WIDTH: 
            boss_direction_multiplier = -1
            boss_direction = "left"
        elif boss_rect.left <= 0:
            boss_direction_multiplier = 1
            boss_direction = "right"
        
        boss_timer -= 1
        if boss_timer <= 0:
            boss_phase_index += 1
            if boss_phase_index >= 3 :
                boss_phase_index = 0
            boss_phase = boss_phases[boss_phase_index]
            if boss_phase == "wait":
                boss_timer = 120
            else:
                boss_timer = 300

        if boss_cooldown > 0:
            boss_cooldown -= 1
        if boss_cooldown == 0 and boss_phase != "wait":
            bullet_boss_x,bullet_boss_y = boss_rect.centerx,boss_rect.bottom
            if boss_phase == "single":
                boss_cooldown = 20
                bullets_boss.append({"IMG_BOSS_BULLET":IMG_BOSS_BULLET,
                                     "POSITION_BOSS": IMG_BOSS_BULLET.get_rect(center=(bullet_boss_x,bullet_boss_y)), 
                                     "speed_bossbullet_x":0,
                                     "speed_bossbullet_y":6
                })
            elif boss_phase == "spread":
                boss_cooldown = 40
                bullets_boss.append({"IMG_BOSS_BULLET": IMG_BOSS_BULLET,
                                     "POSITION_BOSS": IMG_BOSS_BULLET.get_rect(center=(bullet_boss_x,bullet_boss_y)), 
                                     "speed_bossbullet_x":0,
                                     "speed_bossbullet_y":6
                })
                bullets_boss.append({"IMG_BOSS_BULLET": IMG_BOSS_BULLET,
                                     "POSITION_BOSS": IMG_BOSS_BULLET.get_rect(center=(bullet_boss_x,bullet_boss_y)),
                                     "speed_bossbullet_x":-2,
                                     "speed_bossbullet_y":6
                })
                bullets_boss.append({"IMG_BOSS_BULLET": IMG_BOSS_BULLET,
                                     "POSITION_BOSS": IMG_BOSS_BULLET.get_rect(center=(bullet_boss_x,bullet_boss_y)),
                                     "speed_bossbullet_x":2,
                                     "speed_bossbullet_y":6
                })

        for p in bullets_player[:]:
            p["POSITION_PLAYER"].y += p["speed_playerbullet_y"]
            if p["POSITION_PLAYER"].bottom < 0:
                bullets_player.remove(p)
            
        for b in bullets_boss[:]:
            b["POSITION_BOSS"].x += b["speed_bossbullet_x"]
            b["POSITION_BOSS"].y += b["speed_bossbullet_y"]
            if b["POSITION_BOSS"].top > SCREEN_HEIGHT:
                bullets_boss.remove(b)
            
        for b in bullets_boss[:]:
            if player_rect.colliderect(b["POSITION_BOSS"]):
                player_hp -= 1
                SOUND_HIT_PLAYER.play()
                bullets_boss.remove(b)
        
        for p in bullets_player[:]:
            if boss_rect.colliderect(p["POSITION_PLAYER"]):
                boss_hp -= 1
                SOUND_HIT_BOSS.play()
                bullets_player.remove(p)
                if selected_difficulty == "easy" :
                    score += 10
                elif selected_difficulty == "normal" :
                    score += 15
                elif selected_difficulty == "hard" :
                    score += 20


        if player_hp <= 0:
            SOUND_LOSE.play()
            current_page = "game_over"
        if boss_hp <= 0:
            SOUND_WIN.play()
            current_page = "win_screen"


        if player_direction == "left":
            display_surface.blit(IMG_PLAYER_L,player_rect)
        else:
            display_surface.blit(IMG_PLAYER_R,player_rect)
        
        if boss_direction == "left":
            display_surface.blit(IMG_BOSS_L,boss_rect)
        else :
            display_surface.blit(IMG_BOSS_R,boss_rect)

            
        for p in bullets_player:
            display_surface.blit(p["IMG_PLAYER_BULLET"],p["POSITION_PLAYER"])
        for b in bullets_boss:
            display_surface.blit(b["IMG_BOSS_BULLET"],b["POSITION_BOSS"])
        
        text_player_hp = main_font.render(f"Player HP: {player_hp}",True,COLOR_GREEN)
        display_surface.blit(text_player_hp,(SCREEN_WIDTH-120,30)) 

        text_boss_hp = main_font.render(f"Boss HP: {boss_hp}",True,COLOR_RED)
        display_surface.blit(text_boss_hp,(SCREEN_WIDTH-120,60))

        text_score = main_font.render(f"Score: {int(score)}",True,COLOR_WHITE)
        display_surface.blit(text_score,(30, 30))

    elif current_page == "game_over":
        text_lose = end_font.render("You Lose!!!",True,COLOR_RED)
        display_surface.blit(text_lose,(SCREEN_WIDTH//2 - text_lose.get_width()//2,100))
        text_lose_score = main_font.render(f"Score: {int(score)}", True, COLOR_WHITE)
        display_surface.blit(text_lose_score,(SCREEN_WIDTH//2 - text_lose_score.get_width()//2,240))
        
        pygame.draw.rect(display_surface,COLOR_GRAY,btn_retry)
        Retry_btn = main_font.render("Retry",True,COLOR_WHITE)
        display_surface.blit(Retry_btn,(btn_retry.centerx-Retry_btn.get_width()//2,btn_retry.centery-Retry_btn.get_height()//2))

        pygame.draw.rect(display_surface,COLOR_GRAY,btn_over_back)
        back_btn = main_font.render("Back",True,COLOR_WHITE)
        display_surface.blit(back_btn, (btn_over_back.centerx-back_btn.get_width()//2,btn_over_back.centery-back_btn.get_height()//2))

    elif current_page == "win_screen":
        text_victory = end_font.render("Victory!!!",True,COLOR_GREEN)
        display_surface.blit(text_victory,(SCREEN_WIDTH//2 - text_victory.get_width()//2,200))
        text_victory_score= main_font.render(f"Score: {int(score)}",True,COLOR_WHITE)
        display_surface.blit(text_victory_score,(SCREEN_WIDTH//2 - text_victory_score.get_width()//2,350))
        
        pygame.draw.rect(display_surface, COLOR_GRAY, btn_win_back)
        back_btn_win = main_font.render("Back",True,COLOR_WHITE)
        display_surface.blit(back_btn_win,(btn_win_back.centerx-back_btn_win.get_width()//2,btn_win_back.centery-back_btn_win.get_height()//2))

    pygame.display.flip()
    main_clock.tick(60)

pygame.quit()