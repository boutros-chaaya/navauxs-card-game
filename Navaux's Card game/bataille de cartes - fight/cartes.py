import random
import time


class Carte:
    def __init__(self, nom, force, defense, famille):
        self.nom = nom
        self.force = force
        self.defense = defense
        self.famille = famille

    def __repr__(self):
        return f'<< {str(self.nom)} ({str(self.famille)})  -- F {str(self.force)} / D {str(self.defense)} >>'

    def __eq__(self, other):
        if combat(self, other) == 'morts' or combat(self, other) == 'survies':
            return True
        else:
            return False

    def __lt__(self, other):
        if combat(self, other) == f'{other.nom}  gagne':
            return True
        else:
            return False


def rand_carte():
    setcartes = {'taureau': (2, 5, 'disques'), 'centurion': (6, 7, 'disques'), 'requin': (3, 6, 'disques'), 'serpent': (3, 7, 'disques'), 'papillon': (6, 3, 'disques'), 'buffle': (7, 1, 'disques'), 'ours': (3, 4, 'disques'), 'tortue': (
        1, 9, 'disques'), 'aigle': (10, 2, 'pointes'), 'dragon': (8, 9, 'pointes'), 'loup': (3, 6, 'pointes'), 'lion': (3, 6, 'pointes'), 'licorne': (4, 5, 'pointes'), 'scorpion': (6, 7, 'pointes'), 'cerf': (3, 4, 'pointes'), 'zebre': (3, 4, 'pointes')}

    animal = random.choice(list(setcartes.keys()))
    c = Carte(animal, setcartes[animal][0],
              setcartes[animal][1], setcartes[animal][2])
    return c


def random_cards(n):
    cards = [rand_carte() for i in range(n)]
    return cards


def card_distrib(deck, player1, player2):
    while len(player1) < 3:
        try:
            c = random.randint(0, len(deck) - 1)
        except:
            break
        player1.append(deck[c])
        deck.pop(c)
    while len(player2) < 3:
        try:
            d = random.randint(0, len(deck) - 1)
        except:
            break
        player2.append(deck[d])
        deck.pop(d)

    return f'Player 1: {player1} | \nPlayer 2: {player2} |\nCards remaining: {len(deck)}'


def choose_card(hand, player):
    choice = int(input(f"{player} choose a card (1 -> {len(hand)}): "))
    if choice > 3:
        choice = 3
    card_chosen = hand[choice - 1]
    hand.pop(choice - 1)
    print(card_chosen)
    return card_chosen


def combat(c1, c2):
    if c1.force >= c2.defense and c2.force >= c1.defense:
        return 'Morts'
    elif c1.force < c2.defense and c2.force < c1.defense:
        return 'Survies'
    elif c1.force >= c2.defense and c2.force < c1.defense:
        return 'PLAYER 1 WINS'
    elif c1.force < c2.defense and c2.force >= c1.defense:
        return 'PLAYER 2 WINS'

    return 'mabaarif'


def game(deck, player1, player2):
    global count1, count2

    print(card_distrib(deck, player1, player2))
    card1 = choose_card(player1, 'player 1')
    card2 = choose_card(player2, 'player 2')
    fight = combat(card1, card2)

    
    return fight


def who_wins(count1, count2):
    if count1 > count2:
        return "Player 1 wins!"
    if count1 == count2:
        return "Draw!"
    else:
        return "Player 2 wins!"


deck = random_cards(16)
player1 = []
player2 = []
count1 = 0
count2 = 0
    
while True:
    print(game(deck, player1, player2))
    print('------------------')
    # time.sleep(0.5)

    if len(player1) == 0:
        break

print('---------')
print(who_wins(count1, count2))
