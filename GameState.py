import random

class GameState:
    def __init__(self):
        self.cards = []
        self.colors = ['red', 'green', 'blue', 'yellow']
        self.ranks = [0] + [i for i in range(1, 10)] + ['+2', 'skip', 'reverse']
        self.cards_per_player = 7

        self.pile = []
        self.player_hand = []
        self.comp_hand = []
        self.turn = 'player'
        self.choose_card = False
        self.pending_effect = None  

    def initiate_cards(self):
        for color in self.colors:
            for rank in self.ranks:
                self.cards.append(f'{color}_{rank}')
                if rank in ['+2', 'skip', 'reverse']:
                    self.cards.append(f'{color}_{rank}')

        self.cards.extend(['black_+4', 'black_wildcard'] * 20)
        random.shuffle(self.cards)

    def distribute_cards(self):
        for _ in range(self.cards_per_player):
            self.player_hand.append(self.cards.pop())
            self.comp_hand.append(self.cards.pop())
        
        card = self.cards.pop()
        while ('+2' in card) or ('reverse' in card) or ('skip' in card) or ('black' in card):
            card = self.cards.pop()
        self.pile.append(card)
        print(f"Début de la partie. Carte sur la pile : {self.pile[-1]}")

    def play_card(self, card):
        print(f"{self.turn} joue {card}")
        if self.turn == 'player':
            if not self.valid_move(card):
                print("Coup invalide")
                return False
            self.player_hand.remove(card)
        else:
            self.comp_hand.remove(card)

        if 'black' in card:
            if self.turn == 'player':
                self.choose_card = True
            else:
                self.pile.append(card)
                self.pile[-1] = self.pile[-1].replace('black', random.choice(self.colors))
                self.turn = self.opponent()
                self.choose_card = True
                return True

        # Définition de l'effet si besoin
        if '+2' in card:
            self.pending_effect = {'type': '+2', 'target': self.opponent()}
            print(f"Effet +2 activé sur {self.pending_effect['target']}")
        elif '+4' in card:
            self.pending_effect = {'type': '+4', 'target': self.opponent()}
            print(f"Effet +4 activé sur {self.pending_effect['target']}")

        elif 'skip' in card:
            self.pending_effect = {'type': 'skip', 'target': self.opponent()}
            print(f"Effet skip activé sur {self.pending_effect['target']}")
        elif 'reverse' in card:
            self.pending_effect = {'type': 'skip', 'target': self.opponent()}
            print(f"Effet reverse activé (skip) sur {self.pending_effect['target']}")

        self.pile.append(card)

        # On ne change pas le tour si effet +2 ou +4, sinon on change le tour
        if not ('+2' in card or '+4' in card):
            self.turn = self.opponent()
            print(f"Changement de tour à {self.turn}")

        return True

    def opponent(self):
        return 'player' if self.turn == 'comp' else 'comp'

    def apply_pending_effect(self):
        if self.pending_effect is None:
            return False

        effect = self.pending_effect
        target = effect['target']

        print(f"Application de l'effet {effect['type']} sur {target}")

        if effect['type'] == '+2':
            for _ in range(2):
                self.draw_card(target)
            print(f"{target} a pioché 2 cartes")
            self.turn = self.opponent()
            print(f"Tour après effet: {self.turn}")
        elif effect['type'] == '+4':
            for _ in range(4):
                self.draw_card(target)
            print(f"{target} a pioché 4 cartes")
            self.turn = self.opponent()
            print(f"Tour après effet: {self.turn}")
        elif effect['type'] == 'skip':
            self.turn = self.opponent()
            print(f"{target} est passé, tour à {self.turn}")

        self.pending_effect = None
        return True

    def draw_card(self, player):
        if len(self.cards) == 0:
            top = self.pile.pop()
            self.cards = self.pile[:]
            self.pile = [top]
            random.shuffle(self.cards)
            print("Reshuffle de la pioche")

        if player == 'player':
            self.player_hand.append(self.cards.pop())
            print("Joueur pioche une carte")
        else:
            self.comp_hand.append(self.cards.pop())
            print("Ordinateur pioche une carte")

    def take_card(self):
        print(f"{self.turn} pioche une carte")
        self.draw_card(self.turn)

    def valid_move(self, card):
        if card not in ['black_+4', 'black_wildcard']:
            splitted_card = card.split("_")
            splitted_pile_card = self.pile[-1].split("_")
            if splitted_card[0] == splitted_pile_card[0] or splitted_card[1] == splitted_pile_card[1]:
                return True
        else:
            return True
        return False

    def play_comp_move(self):
        for card in self.comp_hand:
            if self.valid_move(card):
                self.play_card(card)
                return
        self.take_card()
        self.turn = self.opponent()
        print(f"Tour après pioche ordi : {self.turn}")
