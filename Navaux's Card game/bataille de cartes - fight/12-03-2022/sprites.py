import pygame, sys
from utilities import draw_img
import random


class Button:
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        #self.clicked = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        # check mouse over and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                action = True
                self.clicked = True
            
            if key[pygame.K_RETURN] and self.clicked == False:
                action = True
                self.clicked = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            


        # draw button 
        screen.blit(self.img, self.rect)

        return action 


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('gunshot3.mp3')

    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(GAME.crosshair, GAME.target_grp, True)

    def update(self):
        self.rect.center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


class Target(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Game:
    def __init__(self):
        self.white = (255, 255 ,255)
        self.level = 3
        self.target_count = {
            '1' : 5,
            '2' : 12,
            '3' : 18,
            '4' : 25,
            '5' : 0
        }
        #sprites and groups
        self.crosshair = Crosshair('crosshair.png')
        self.crosshair_group = pygame.sprite.Group()
        self.crosshair_group.add(self.crosshair)
        # target
        self.target_grp = pygame.sprite.Group()
        for target in range(self.target_count[str(self.level)]):
            self.new_target = Target('target.png', random.randrange(0, sw), random.randrange(0, sh))
            self.target_grp.add(self.new_target)
        
        # Buttons
        self.start_button = Button(sw // 2 - 225, sh // 2, start_img)
        self.exit_button = Button(sw // 2 + 200, sh // 2, exit_img)
        self.exit2_button = Button(sw // 2  + 100, sh // 2 - 200, exit2)
        self.restart_button = Button(sw // 2  - 100, sh // 2 - 200, restart_img)


    def add_targets(self):
        for target in range(self.target_count[str(self.level)]):
            self.new_target = Target('target.png', random.randrange(0, sw), random.randrange(0, sh))
            self.target_grp.add(self.new_target)

    def update(self):
        if self.level < 5:
            render_txt(f'Targets: {self.target_count[str(self.level)] - self.target_grp.__len__()} /{self.target_count[str(self.level)]}',
                        font, self.white, 150, 100)

    def update_level(self):
        if self.target_grp.__len__() == 0:
            if self.level < 5:
                self.level += 1
            else: 
                self.game_over()
            self.add_targets()

    def game_over(self):
        render_txt('Congrats', font, (255, 255, 255), sw/2, sh/2)
        if GAME.restart_button.draw() or key[pygame.K_RETURN]:
            self.level = 1
        if GAME.exit2_button.draw():
            pygame.quit()
            sys.exit()


# render text
def render_txt(txt, font, color, x, y):
        img = font.render(txt, True, color)
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)

# score
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surface = font.render(str(current_time), True, "Black")
    score_rectangle_ = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle_)
    return current_time



# game globals
pygame.init()
sw ,sh = 1980, 1080
screen = pygame.display.set_mode()
clock = pygame.time.Clock()
fps = 60
pygame.mouse.set_visible(False)
main_menu = True
level = 1
font = pygame.font.SysFont(None, 50)
start_time = 0



# images 
bg_pngimg = pygame.image.load('bg.png').convert_alpha()
bg_img = pygame.transform.scale(bg_pngimg, (sw, sh))
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
restart_img = pygame.image.load('restart_btn.png').convert_alpha()
exit2 = pygame.transform.scale(exit_img, (120, 42))


GAME = Game()

# main loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            GAME.crosshair.shoot()    

    draw_img(screen, bg_img, sw/2, sh/2)


    if main_menu:
        if GAME.exit_button.draw():
            run = False
        key = pygame.key.get_pressed()
        if GAME.start_button.draw() or key[pygame.K_RETURN]:
            main_menu = False
            start_time = int(pygame.time.get_ticks() / 1000)

        GAME.crosshair_group.draw(screen)
        GAME.crosshair_group.update()
    
    else:
        GAME.target_grp.draw(screen)
        GAME.update()
        GAME.update_level()
        GAME.crosshair_group.draw(screen)
        GAME.crosshair_group.update()
        #display_score()
        
    


    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()