import pygame
import sys
import time
import random
import utilities
pygame.font.init()


# global variables
sw, sh = 800, 600
sw_, sh_ = 800, 850
center = sw_ // 2, sh_ // 2
xc, yc = center
screen = pygame.display.set_mode((sw_, sh_))
pygame.display.set_caption("Jeu de Cartes de Christophe Navaux")
clock = pygame.time.Clock()
fps = 60

# fonts and colors
font = pygame.font.SysFont("comicsans", 50)
score_font = pygame.font.SysFont("comicsans", 35)
message_font = pygame.font.SysFont("cambria ", 20)
result_font = pygame.font.SysFont("cambria", 27)
bg = pygame.image.load("bg.jpg")
bg_img = pygame.transform.scale(bg, (sw_, sh_))

white = (250, 250, 250)
black = (0, 0, 0)
green = (0, 250, 0)
red = (200, 0, 0)
blue = (0, 0, 0)
bg_color = (94, 129, 162)





# game functions
def draw_text(txt, font, color, x, y):
	img = font.render(txt, 1, color)
	rect = img.get_rect(center=(x, y))
	screen.blit(img, rect)

def draw_textL(txt, font, color, x, y):
	img = font.render(txt, 1, color)
	screen.blit(img, (x, y))

def draw_img(img, x, y):
	rect = img.get_rect(center=(x, y))
	screen.blit(img, rect)

def draw_bg():
    draw_img(bg_img, sw_//2, sh_//2)

def draw_blue_bg():
    screen.fill(black)
    screen.fill(bg_color, rect)

    
def draw_black():
    screen.fill((0,0,0))


# game classes
class Carte:
    def __init__(self, nom, force, defense, famille, num):
        self.nom = nom
        self.num = num
        self.force = force
        self.defense = defense
        self.famille = famille
        self.scale = (85, 120)
        img = pygame.image.load(f'images/{self.num}.png').convert_alpha()
        self.image = pygame.transform.scale(img, self.scale)
        flipped = pygame.image.load(f'images/closed card.png').convert_alpha()
        self.flipped = pygame.transform.scale(flipped, self.scale)
        self.rect = self.image.get_rect()
        self.clicked = False

    def __repr__(self):
        # represent function
        return f'{str(self.nom)} ({str(self.famille)}) - F {str(self.force)} / D {str(self.defense)}'

    def draw(self, coords, closed=False):
        action = False

        #self.clicked = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        # check mouse over and clicked
        if self.rect.collidepoint(pos):
            if not closed:
                pygame.draw.rect(screen, white, self.rect, 1)
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
        screen.blit(surf, self.rect)
        return action

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


class Deck:
    def __init__(self, n, player, enemy):
        self.player_hand = player
        self.enemy_hand = enemy
        self.num_of_cards = n
        self.deck = self.deck_gen()
        self.image = pygame.transform.scale(pygame.image.load("images/flipped.png"), (85, 120))  

    def __repr__(self):
        return str(self.deck)

    def is_empty(self):
        if len(self.deck) == 0:
            return True

        return False

    def add(self, elt):
        self.deck.append(elt)
    
    def rand_carte(self):
        # random instance of a card
        setcartes = {'toro': (2, 5, 'disques', 13), 'centurion': (6, 7, 'disques', 2), 'shark': (3, 6, 'disques', 10), 'serpent': (3, 7, 'disques', 12),
                    'papillon': (6, 3, 'disques', 9), 'buffle': (7, 1, 'disques', 1), 'ours': (3, 4, 'disques', 8), 'tortue': (1, 9, 'disques', 14),
                    'aigle': (10, 2, 'pointes', 0), 'dragon': (8, 9, 'pointes', 4), 'loup': (3, 6, 'pointes', 7), 'lion': (3, 6, 'pointes', 6),
                    'licorne': (4, 5, 'pointes', 5), 'scorpion': (6, 7, 'pointes', 11), 'cerf': (3, 4, 'pointes', 3), 'zebre': (3, 4, 'pointes', 15)}

        card_keys = list(setcartes.keys())
        animal = random.choice(card_keys)
        c = Carte(animal, setcartes[animal][0], setcartes[animal][1], setcartes[animal][2], setcartes[animal][3])
        return c



    def deck_gen(self):
        # function that generates a deck of n cards
        cards = [self.rand_carte() for i in range(self.num_of_cards)]
        return cards

    def distrib(self):
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

    def draw(self, coords):
        rect = self.image.get_rect(center = coords)
        draw_img(self.image, coords[0], coords[1])
        draw_text(str(len(self.deck)), font, red, coords[0], coords[1])


class Menu:
    def __init__(self, img = None):
        self.img = img

    def play(self):
        self.draw_messages()

    def draw_messages(self):
        draw_bg()
        draw_text("Press any key", font, white, xc, yc + 200)
        draw_text("MAIN MENU", font, white, xc, yc - 200)


class GameOver:
    def __init__(self):
        self.msg = "GAME OVER"

    def play(self, msg):
        time.sleep(0.5)
        self.draw_messages(msg)

    def draw_messages(self, msg):
        draw_bg()
        draw_text(self.msg, font, white, xc, yc - 200)
        draw_text(msg, font, white, xc, yc + 100)
        draw_text(GAME.score, font, white, xc, yc + 200)


class Game:
    def __init__(self, player1, player2, deck):
        self.p1, self.p2 = player1, player2
        self.deck = deck
        self.p2coords = [(sw // 3, sh//3 - 70), (sw // 2, sh//3 - 70), (sw - sw //3, sh//3 - 70)]
        self.p1coords = [(sw // 3, sh - sh//3 + 50), (sw // 2, sh - sh//3 + 50), (sw - sw //3, sh - sh//3 + 50)]
        self.player_hand = []
        self.enemy_hand = []
        self.count1 , self.count2 = 0, 0
        self.score = f'Score: {self.count1} | {self.count2}'
        self.fight_message = [""]
        self.result_message = [""]

    def empty_hands(self):
        time.sleep(0.5)
        self.player_hand.pop()
        self.enemy_hand.pop()

    def show_time(self):
        draw_text(utilities.get_time(), score_font, white, sw - 100, 20)


    def play(self):
        draw_blue_bg()
        self.draw_cards()
        self.deck.distrib()
        self.deck.distrib()
        self.deck.draw((100, sh//2))
        self.draw_chosen()
        self.draw_score(100, 50)
        self.show_time()
        self.draw_messages()
        if self.player_hand:
            self.reset_messages()
        

    def draw_cards(self):
        for card in self.p1:
            if card.draw((self.p1coords[self.p1.index(card)][0], self.p1coords[self.p1.index(card)][1])):
                self.player_hand.append(card)
                oponent = random.choice(self.p2)
                self.enemy_hand.append(oponent)
                if len(self.player_hand) > 1:
                    self.player_hand.pop(0)
                if len(self.enemy_hand) > 1:
                    self.enemy_hand.pop(0)
                
        for card in self.p2:
            card.draw((self.p2coords[self.p2.index(card)][0], self.p2coords[self.p2.index(card)][1]), True)

    def draw_chosen(self):
        if self.player_hand:
            for card in self.player_hand:
                if card.draw((sw//2 -100, sh//2)):
                    self.reset_messages()
                    enemy = self.enemy_hand[0]
                    self.p1.pop(self.p1.index(card))
                    self.p2.pop(self.p2.index(enemy))
                    self.card_fight(card, enemy)

                for card in self.enemy_hand:
                    if card.draw((sw//2 + 100, sh//2)):
                        print("ya kalb")

    def draw_score(self, x, y):
        draw_text(self.score, score_font, white, x, y)

    def draw_messages(self):
        draw_textL("Log :", message_font, green, 30, sh + 20)
        draw_textL("Press ESC to quit game.", message_font, white, 30, sh+40)
        draw_textL("Click a card to select, Double click to fight!", message_font, white, 30, sh+ 60)
        draw_textL("-----------------------------------------------------------------------------------------", message_font, white, 30, sh+80)
        draw_textL(self.fight_message[-1], result_font, white, 30, sh+100)
        draw_textL(self.result_message[-1], result_font, white, 30, sh+140)

    def reset_messages(self):
        rect = pygame.Rect(30, sh + 100, sw, sh)
        screen.fill(black, rect)

    def RESET(self):
        draw_bg()
        self.player_hand = []
        self.enemy_hand = []
        self.player1 = []
        self.player2 = [] 
        self.deck = []    
        self.deck = Deck(16, player1, player2)              
        self.deck.distrib()


    def card_fight(self, c1, c2):
        fight_message = f'{c1} --VS-- {c2}'
        fight = c1.combat(c2)
        if fight == 'PLAYER 1 WINS': 
            self.count1 += 1
            self.score = f'Score: {self.count1} | {self.count2}'
            self.empty_hands()
            self.reset_messages()
        if fight == 'PLAYER 2 WINS':
            self.count2 += 1
            self.score = f'Score: {self.count1} | {self.count2}'
            self.empty_hands()
            self.reset_messages()
        if fight == 'Survies':
            deck.add(c1)
            deck.add(c2)
            self.empty_hands()
            self.reset_messages()
        if fight == "Morts":
            self.empty_hands()
            self.reset_messages()
            

        print(fight_message)
        self.fight_message[0] = fight_message
        print((c1.combat(c2)))
        self.result_message[0] = c1.combat(c2)
        return (c1.combat(c2))



player1 = []
player2 = []
deck = Deck(16, player1, player2)
GAME = Game(player1, player2, deck)
menu = Menu()
game_over = GameOver()
rect = pygame.Rect(0, 0, sw, sh)



def main():
    #game active
    game_active = False

    # main game loop
    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_q and game_active:
                    game_active = False

                if event.key == pygame.K_r and game_active:
                    GAME.RESET()

                if event.key and not game_active:
                    game_active = True



        if game_active: 
            # draw bg
            draw_bg()
            pygame.draw.line(screen, white, (0, sh//2), (sw, sh//2))
            # start game
            GAME.play()


        if not game_active: 
            menu.play()

        if GAME.deck.is_empty():
            if GAME.count1 > GAME.count2:
                game_over.play("PLAYER 1 WINS")
            if GAME.count1 < GAME.count2:
                game_over.play("PLAYER 2 WINS")
            if GAME.count1 == GAME.count2:
                game_over.play('DRAW')

        pygame.display.update()


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()