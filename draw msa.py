import pygame

def draw_text_utility(screen, my_font, text, x, y, color):
    
    # สร้าง Object ข้อความ (Text Surface)
    text_obj = my_font.render(text, True, color)
    # สร้างสี่เหลี่ยม (rect) และกำหนดตำแหน่งกึ่งกลาง
    text_rect = text_obj.get_rect(center=(x, y))
    # วาด (blit) ข้อความลงบนหน้าจอ (screen)
    screen.blit(text_obj, text_rect)