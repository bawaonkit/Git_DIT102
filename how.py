import pygame

pygame.init()

# 🖥️ ตั้งค่าหน้าจอ
SCREEN_W, SCREEN_H = 720, 640
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Ninja Move")
 #ตั้งค่า fps
clock = pygame.time.Clock()
# ขนาดตัวละครปรับเอง
scale = 0.5

# ภาพเดินซ้ายขวา
player_left = pygame.image.load("player_left.png").convert_alpha() 
player_left = pygame.transform.scale(player_left,(int(player_left.get_width()*scale),int(player_left.get_height()*scale)))
player_right = pygame.transform.flip(player_left, True, False)  # กลับด้านให้หันขวา
#dash ซ้าย ขวา
player_dash_right = pygame.image.load("player_dash_right.png").convert_alpha()
player_dash_right = pygame.transform.scale(player_dash_right,(int(player_dash_right.get_width()*scale),int(player_dash_right.get_height()*scale)))
player_dash_left = pygame.transform.flip(player_dash_right, True, False)  # กลับด้านให้หันขวา
#dash ขึ้น ลง
player_dash_up_down = pygame.image.load("Screenshot_2025-10-28_132314-removebg-preview.png").convert_alpha()
player_dash_up_down = pygame.transform.scale(player_dash_up_down,(int(player_dash_up_down.get_width()*scale),int(player_dash_up_down.get_height()*scale)))

# ตำแหน่งเริ่มต้น
player_x = (SCREEN_W - player_left.get_width()) // 2
player_y = SCREEN_H - 20  
player_speed = 5
# ทิศทางเริ่มต้น
direction = "right" 
dash_is = False
dash_time = 0
dash_direction = None
last_moved = "right"

WHITE = (255,255,255)

#วนลูปหลัก
running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 :
            if not dash_is :
                dash_is = True
                dash_time = 12
                if keys[pygame.K_a] :
                    dash_direction = "left"
                elif keys[pygame.K_d] :
                    dash_direction = "right"
                elif keys[pygame.K_w] :
                    dash_direction = "up"
                elif keys[pygame.K_s] :
                    dash_direction = "down"
                else :
                    dash_direction = last_moved

    #การเคลื่อนไหว
    if not dash_is :
        if keys[pygame.K_a] :
            player_x -= player_speed
            direction = "left"
            last_moved = "left"
        elif keys[pygame.K_d] :
            player_x += player_speed
            direction = "right"
            last_moved = "right"
        elif keys[pygame.K_w] :
            player_y -= player_speed
            direction = "up"
            last_moved = "up"
        elif keys[pygame.K_s] :
            player_y += player_speed
            direction = "down"
            last_moved = "down"

# ถ้ากดเมาส์ขวา  เร่งความเร็ว
    if dash_is :
        dash_time -= 1 
        if  dash_direction == "left" and player_x > 0 :
            player_x -= player_speed *2
        elif  dash_direction == "right" and player_x < SCREEN_W - player_left.get_width():
            player_x += player_speed *2
        elif  dash_direction == "up" and player_y > 0 :
            player_y -= player_speed *2
        elif  dash_direction == "down" and player_y < SCREEN_H - player_left.get_height() :
            player_y += player_speed *2
        if dash_time <= 0 :
            dash_is = False
            dash_direction = None
#กันตกขอบจอ
    player_x = max(0, min(player_x, SCREEN_W - player_left.get_width()))
    player_y = max(0, min(player_y, SCREEN_H - player_left.get_height()))


#วาดตัวละครเมื่อเคลื่อนไหว
    if dash_is :
        if dash_direction == "left" :
            screen.blit(player_dash_left,(player_x,player_y))
        elif dash_direction == "right" :
            screen.blit(player_dash_right,(player_x,player_y))
        elif dash_direction == "up" or dash_direction == "down" :
            screen.blit(player_dash_up_down,(player_x,player_y))
    else :
        if direction == "left":
            screen.blit(player_left, (player_x, player_y))
        else:
            screen.blit(player_right, (player_x, player_y))
    #ใส่ fps
    clock.tick(60)
    pygame.display.flip()
pygame.quit()