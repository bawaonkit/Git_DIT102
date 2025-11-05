from player import Player
from boss import Boss


def reset_game(char, diff, PLAYER_HP, BOSS_HP):
    
    b_bullets = []
    p_bullets = []
    
    player = Player(char)
    player.set_hp(PLAYER_HP[diff]) 
    
    boss = Boss()
    boss.set_hp(BOSS_HP[diff]) 
    
    return player, boss, p_bullets, b_bullets

def draw_text(screen, my_font, text, x, y, color):
    text_obj = my_font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    screen.blit(text_obj, text_rect)


def run_game_frame(screen, player, boss, p_bullets, b_bullets, diff_settings, WIDTH, HEIGHT, RED, my_font):
    
    new_p_bullets = player.update()
    new_b_bullets = boss.update(diff_settings)
    
    p_bullets.extend(new_p_bullets)
    b_bullets.extend(new_b_bullets)
    
    for p in p_bullets[:]:
        p.update()
        if p.rect.bottom < 0 or p.rect.top > HEIGHT or p.rect.left > WIDTH or p.rect.right < 0:
            p_bullets.remove(p)
            
    for b in b_bullets[:]:
        b.update()
        if b.rect.bottom < 0 or b.rect.top > HEIGHT or b.rect.left > WIDTH or b.rect.right < 0:
            b_bullets.remove(b)

    for b in b_bullets[:]: 
        if player.rect.colliderect(b.rect):
            player.hit()
            b_bullets.remove(b) 
            
    for p in p_bullets[:]: 
        if boss.rect.colliderect(p.rect):
            boss.hit(1)
            p_bullets.remove(p) 
    
    if player.is_dead():
        return "main_menu"
    if boss.is_dead():
        return "win_screen"

    player.draw(screen)
    boss.draw(screen)
    for p in p_bullets:
        screen.blit(p.image, p.rect)
    for b in b_bullets:
        screen.blit(b.image, b.rect)
        
    draw_text(screen, my_font, f"HP: {player.hp}", WIDTH - 100, 30, RED)

    return None