import pygame

def draw_img(screen, img, x, y, scale = (0, 0)):
    if scale != (0, 0):
        pygame.transform.scale(img, scale)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)
