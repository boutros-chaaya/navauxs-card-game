import pygame
import sys
import random


class Carte(pygame.sprite.Sprite):
    def __init__(self, nom, force, defense, famille, num, coords = (0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.nom = nom
        self.num = num
        self.force = force
        self.defense = defense
        self.famille = famille
        image = pygame.image.load(f'images/{self.num}.png').convert_alpha()
        flipped = pygame.image.load(f'images/closed card.png').convert_alpha()
        self.flipped = pygame.transform.scale(flipped, (85, 120))
        self.image = pygame.transform.scale(image, (85, 120))

        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.clicked = False

    def __repr__(self):
        # represent function
        return f'<< {str(self.nom)} ({str(self.famille)})  -- F {str(self.force)} / D {str(self.defense)} >>'
    
    def combat(self, c2):
        if self.force >= c2.defense and c2.force >= self.defense:
            return 'Morts'
        elif self.force < c2.defense and c2.force < self.defense:
            return 'Survies'
        elif self.force >= c2.defense and c2.force < self.defense:
            return 'PLAYER 1 WINS'
        elif self.force < c2.defense and c2.force >= self.defense:
            return 'PLAYER 2 WINS'

        return 'mabaarif'
    
    def draw(self, coords, closed):
        action = False

        #self.clicked = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        # check mouse over and clicked
        if self.rect.collidepoint(pos):
            if not closed:
                pygame.draw.rect(GAME.screen, GAME.WHITE, self.rect, 1)
                if pygame.mouse.get_pressed()[0] and self.clicked == False:
                    action = True
                    self.clicked = True
                                    
                if key[pygame.K_RETURN] and self.clicked == False:
                    action = True
                    self.clicked = True
                    
                if not pygame.mouse.get_pressed()[0]:
                    self.clicked = False

        self.rect.center = coords

        if closed:
            surf = self.flipped
        elif not closed:
            surf = self.image
        GAME.screen.blit(surf, self.rect)
        return action


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
        GAME.screen.blit(self.img, self.rect)

        return action 


class Deck(pygame.sprite.Sprite):
    def __init__(self, n, player, enemy):
        pygame.sprite.Sprite.__init__(self)
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
                c = random.choice(self.deck)
            except:
                break
            c.coords = (GAME.sw//2, GAME.sh//2)
            self.player_hand.add(c)
            self.deck.pop(self.deck.index(c))
        while len(self.enemy_hand) < 3:
            try:
                d = random.choice(self.deck)
            except:
                break
            self.enemy_hand.add(d)
            self.deck.pop(self.deck.index(d))   


class Game:
    def __init__(self):
        # game globals
        pygame.init()
        self.sw, self.sh = 852, 600
        self.screen = pygame.display.set_mode((self.sw, self.sh))
        pygame.display.set_caption("Navaux's Card Game")
        self.clock = pygame.time.Clock()
        self.fps = 60 
        # pygame.mouse.set_visible(False)
        self.WHITE = (255, 255, 255)
        #self.choose = False

        # game images
        table_top = pygame.image.load('images/table_top.png').convert_alpha()
        self.table_top = pygame.transform.scale(table_top, (self.sw, self.sh))
        self.table_rect = self.table_top.get_rect(center=(self.sw//2, self.sh//2))

        # sprite groups
        self.card_group = pygame.sprite.Group()
        self.p1 = pygame.sprite.Group()
        self.p2 = pygame.sprite.Group()
        self.deck = Deck(16, self.p1, self.p2)
        self.chosen_cards = []
        self.selected_card = None
    
    def pop_list(self):
        if self.chosen_cards:
            self.chosen_cards.pop(0)

    def choose_card(self, sprite):
        self.chosen_cards.append(sprite)
        self.selected_card = sprite
        #print(self.chosen_cards)
        if len(self.chosen_cards) > 1:
            self.chosen_cards.pop(0)
        
        return sprite
         
    def draw_hands(self):
        # draw the cards       
        for index, sprite in enumerate(self.p2):
            sprite.draw((300 + index * 100, self.sh//3 - 50), True)
            
        for index, sprite in enumerate(self.p1):
            if sprite.draw((300 + index * 100, self.sh - self.sh//3 + 50), False):
                self.choose_card(sprite)
        
        if self.chosen_cards:
            draw_img(self.chosen_cards[0].image, (GAME.sw//2 - 100, GAME.sh//2))

    def fight(self, c1, c2):
        if c1.force >= c2.defense and c2.force >= c1.defense:
            return 'Morts'
        elif c1.force < c2.defense and c2.force < c1.defense:
            return 'Survies'
        elif c1.force >= c2.defense and c2.force < c1.defense:
            return 'PLAYER 1 WINS'
        elif c1.force < c2.defense and c2.force >= c1.defense:
            return 'PLAYER 2 WINS'

        return 'mabaarif'

            
    def play(self):
        
        self.screen.blit(self.table_top, self.table_rect)
        self.screen.fill((50, 100, 50))
        pygame.draw.line(self.screen, self.WHITE, (0, self.sh//2), (self.sw, self.sh//2))
        self.deck.card_distrib()
        self.draw_hands()
        
        if self.chosen_cards:
            print(self.fight(self.chosen_cards[0], random.choice(self.p2.sprites())))
        
        self.pop_list()
        



def draw_img(img, coords):
    rect = img.get_rect(center=coords)
    GAME.screen.blit(img, rect)
    
        



GAME = Game()
# main game loop
run = True
while run: 

    GAME.play()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    
    pygame.display.update()
    GAME.clock.tick(GAME.fps)

pygame.quit()
sys.exit()
