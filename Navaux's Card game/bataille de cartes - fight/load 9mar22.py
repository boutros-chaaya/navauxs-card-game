import pygame
import sys
import random
import time
import utilities


class Carte:
    def __init__(self, nom, force, defense, famille, num):
        self.nom = nom
        self.num = num
        self.force = force
        self.defense = defense
        self.famille = famille
        self.surface = pygame.image.load(f'images/{self.num}.png').convert_alpha()
        

    def __repr__(self):
        # represent function
        return f'<< {str(self.nom)} ({str(self.famille)})  -- F {str(self.force)} / D {str(self.defense)} >>'

    def draw_card(self):
        pass


class Deck:
    def __init__(self, n, player, enemy):
        self.player_hand = player
        self.enemy_hand = enemy
        self.num_of_cards = n
        self.deck = self.deck_gen()
    
    def rand_carte(self):
        # random instance of a card
        setcartes = {'toro': (2, 5, 'disques', 13), 'centurion': (6, 7, 'disques', 2), 'shark': (3, 6, 'disques', 10), 'serpent': (3, 7, 'disques', 12),
                    'papillon': (6, 3, 'disques', 9), 'buffle': (7, 1, 'disques', 1), 'ours': (3, 4, 'disques', 8), 'tortue': (1, 9, 'disques', 14),
                    'aigle': (10, 2, 'pointes', 0), 'dragon': (8, 9, 'pointes', 4), 'loup': (3, 6, 'pointes', 7), 'lion': (3, 6, 'pointes', 6),
                    'licorne': (4, 5, 'pointes', 5), 'scorpion': (6, 7, 'pointes', 11), 'cerf': (3, 4, 'pointes', 3), 'zebre': (3, 4, 'pointes', 15)}

        card_keys = list(setcartes.keys())
        animal = random.choice(card_keys)
        c = Carte(animal, setcartes[animal][0], setcartes[animal]
                [1], setcartes[animal][2], setcartes[animal][3])
        return c


    def deck_gen(self):
        # function that generates a deck of n cards
        cards = [self.rand_carte() for i in range(self.num_of_cards)]
        return cards

    def card_distrib(self):
        # distribuits 3 cards to the player 1 and 2
        while len(self.player_hand) < 3:
            try:
                c = random.randint(0, len(self.deck) - 1)
            except:
                break
            self.player_hand.append(self.deck[c])
            self.deck.pop(c)
        while len(self.enemy_hand) < 3:
            try:
                d = random.randint(0, len(self.deck) - 1)
            except:
                break
            self.enemy_hand.append(self.deck[d])
            self.deck.pop(d)


class Pointer:
    def __init__(self, img, xpos, ypos, scale = (0, 0)):
        self.img = img
        self.xpos = xpos
        self.xindex = 0
        self.ypos = ypos
        self.scale = scale

        self.draw_pointer()

    def draw_pointer(self):
        utilities.draw_image(screen, self.img, self.xpos[self.xindex], self.ypos, self.scale)

    def move_right(self):
        if self.xindex < 2:
            self.xindex += 1 
        else:
            self.xindex = 0

    def move_left(self):
        self.xindex -= 1
        if self.xindex == -1:
            self.xindex = 2
        if self.xindex == -2:
            self.xindex = 1
        if self.xindex < -3:
            self.xindex = 2

    def get_pos(self):
        card_num = f'Card {self.xindex + 1}'
        return self.xindex


class Game:
    def __init__(self, screen, sw, sh):
        self.screen_width = sw
        self.screen_height = sh
        self.screen = screen
        pygame.display.set_caption("Chris Navaux's game")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.game_font = pygame.font.Font('fonts/Pixeltype.ttf', 70)
        self.font1 = pygame.font.Font(None, 50)
        self.BG_COLOR = (50, 100, 50)
        self.light_grey = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.red_color = pygame.Color('Red')
        self.blue_color = pygame.Color('Blue')
        self.pink_color = pygame.Color('Pink')
        self.yellow_color = pygame.Color('Yellow')
        self.closed_image = pygame.image.load('images/flipped.png').convert_alpha()
        self.cursor_img = pygame.image.load("images/recursor.png").convert_alpha()
        # card coords
        self.x1, self.y1 = self.screen_width / 3 - 25, self.screen_height - self.screen_height / 3 + 100
        self.x2, self.y2 = self.screen_width / 2, self.screen_height - self.screen_height / 3 + 100
        self.x3 , self.y3 = self.screen_width - self.screen_width / 3 + 25, self.screen_height - self.screen_height / 3 + 100
        self.player_hand_slots = [(self.x1, self.y1), (self.x2,self.y2), (self.x3, self.y3)]
        self.ai_slots = [(self.screen_width / 3 - 25, self.screen_height / 3 - 125), (self.screen_width / 2, self.screen_height / 3 - 125), (self.screen_width - self.screen_width / 3 + 25, self.screen_height / 3 - 125)]
        # game variables
        self.player_hand = []
        self.selected_card = []
        self.enemy_hand = []
        self.count1 = 0
        self.count2 = 0
        self.DECK = Deck(16, self.player_hand, self.enemy_hand)
        # cursor
        self.cursor = Pointer(self.cursor_img, [self.x1, self.x2, self.x3], self.y1 + 120, (50, 50))
        self.cursor_pos = self.cursor.get_pos()
        self.card_select = False

        # game functions
        
        self.initialize()
    
    def initialize(self):
        self.draw_game_constants()
        self.draw_hands()
        self.draw_deck()
        


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.cursor.move_right()
                        
                    if event.key == pygame.K_LEFT:
                        self.cursor.move_left()
                        
                    if event.key == pygame.K_SPACE:
                        self.select_card()

                              

    def draw_text(self, text, font, font_color, x, y):
        img = font.render(text, True, font_color)
        self.screen.blit(img, (x, y))
    
    def draw_game_constants(self):
        self.draw_text('SCORE', self.game_font, self.light_grey, 40, 100)
        self.draw_text(f'{self.count1} | {self.count2}', self.game_font, self.light_grey, 60, 150)

        pygame.draw.line(self.screen, self.light_grey, (0, self.screen_height/2), (self.screen_width, self.screen_height/2), 1)
        self.draw_text(utilities.get_time(), self.font1, self.WHITE, self.screen_width - 200, 0)
        self.draw_text('SCORE', self.game_font, self.light_grey, 40, 100)
        self.draw_text(f'{self.count1} | {self.count2}', self.game_font, self.light_grey, 60, 150)

        pygame.draw.line(self.screen, self.light_grey, (0, self.screen_height/2), (self.screen_width, self.screen_height/2), 1)

    def draw_image(self, img, x, y, scale=(0, 0)):
        # next line is so that if there is no scale parameter passed the image would not transform
        if scale != (0, 0):
            img = pygame.transform.scale(img, scale)

        rect = img.get_rect(center=(x, y))
        self.screen.blit(img, rect)

    def draw_hands(self):
            # player_hand
            for i in self.player_hand:
                self.draw_image(i.surface, self.player_hand_slots[self.player_hand.index(
                    i)][0], self.player_hand_slots[self.player_hand.index(i)][1], (100, 150))

            # player 2
            for j in self.enemy_hand:
                self.draw_image(self.closed_image, self.ai_slots[self.enemy_hand.index(
                    j)][0], self.ai_slots[self.enemy_hand.index(j)][1], (100, 150))
            
            if self.selected_card:
                self.draw_image(self.selected_card[-1].surface, self.screen_width / 2 - 100, self.screen_height/2, (100, 150))

    def draw_deck(self):
        # deck YOGURT
        self.draw_image(self.closed_image, 100, 350, (100, 150))
        if len(self.DECK.deck) > 9:
            self.draw_text(str(len(self.DECK.deck)), self.game_font, self.RED, 80, 335)
        else:
            self.draw_text(str(len(self.DECK.deck)), self.game_font, self.RED, 90, 335)

    def select_card(self):
        card_index = self.cursor.get_pos()
        if card_index == 0:
            self.selected_card.append(self.player_hand[0])
        if card_index == 1:
            self.selected_card.append(self.player_hand[1])
        if card_index == 2:
            self.selected_card.append(self.player_hand[2])

        if len(self.selected_card) > 1:
            self.selected_card.pop(0)
            


pygame.init()
screen_width = 1000 / 1.2
screen_height = 800 / 1.2
screen = pygame.display.set_mode((screen_width, screen_height))
GAME = Game(screen, screen_width, screen_height)


while True:
    GAME.screen.fill(GAME.BG_COLOR)
    GAME.check_events()
    GAME.initialize()
    GAME.DECK.card_distrib()
    GAME.cursor.draw_pointer()
    GAME.clock.tick(GAME.FPS)
    pygame.display.update()
