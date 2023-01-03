import pygame
import time


def draw_text(screen, text, font, font_color, x, y):
        img = font.render(text, True, font_color)
        screen.blit(img, (x, y))


def draw_image(screen, img, x, y, scale=(0, 0)):
        # next line is so that if there is no scale parameter passed the image would not transform
        if scale != (0, 0):
            img = pygame.transform.scale(img, scale)
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)

def get_time():
    state = 'AM'
    offset = ''
    offset_seconds = ''
    hour = time.localtime()[3]
    minute = time.localtime()[4]
    seconds = time.localtime()[5]

    if hour > 12:
        hour -= 12
        state = 'PM'

    if minute < 10:
        offset = '0'

    if seconds < 10:
        offset_seconds = '0'

    return f'{hour}:{offset}{minute}:{offset_seconds}{seconds} {state}'

