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
            self.player_hand.remove(card)
        else:
            self.comp_hand.remove(card)
        self.pile.append(card)


    def take_card(self):
        if self.turn == 'player':
            self.player_hand.append(self.cards(random.randint(0, len(self.cards) - 1)))
        else:
            self.comp_hand.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))

    def valid_move(self, card):
        pass
    
