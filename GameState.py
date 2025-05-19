import random

class GameState:
    def __init__(self):
        self.cards = []
        self.colors = ['red', 'green', 'blue', 'yellow']
        self.ranks = [i for i in range(1, 10)] + ['+2', 'skip', 'reverse']
        self.cards_per_player = 7

        self.pile = []
        self.player_hand = []
        self.comp_hand = []
        self.turn = 'player'
        self.choose_card = False
    

    def initiate_cards(self):
        for color in self.colors:
            for rank in self.ranks:
                self.cards.append(f'{color}_{rank}')

                # Deze kaarten moeten 2 keer toegevoegd worden
                if rank in ['+2', 'skip', 'reverse']:
                    self.cards.append(f'{color}_{rank}')
        
        # Deze kaarten moeten 4 keer toegevoegd worden
        self.cards.extend(['black_+4', 'black_wildcard'] * 4) 


    def distribute_cards(self):
        for _ in range(self.cards_per_player):
            self.player_hand.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
            self.comp_hand.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
            
        self.pile.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))


    def play_card(self, card):
        if self.turn == 'player':
            if self.valid_move(card):
                self.player_hand.remove(card)
            else:
                return False
        else:
            self.comp_hand.remove(card)

        if card in ['black_+4', 'black_wildcard'] and self.turn == 'player':
            self.choose_card = True

        self.pile.append(card)
        self.turn = 'player' if self.turn == 'comp' else 'comp'


    def take_card(self):
        if self.turn == 'player':
            self.player_hand.append(self.cards(random.randint(0, len(self.cards) - 1)))
        else:
            self.comp_hand.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))


    def valid_move(self, card):
        if card not in ['black_+4', 'black_wildcard'] and self.pile[-1] not in ['black_+4', 'black_wildcard']:
            splitted_card = card.split("_")
            splitted_pile_card = self.pile[-1].split("_")

            if splitted_card[0] == splitted_pile_card[0] or splitted_card[1] == splitted_pile_card[1]:
                return True
        else:
            return True
    

    def play_comp_move(self):
        for card in self.comp_hand:
            if self.valid_move(card):
                self.play_card(card)
                return True
            
        self.take_card()
        self.turn = 'player' if self.turn == 'comp' else 'comp'
        
    
