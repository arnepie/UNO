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
    

    def initiate_cards(self):
        for color in self.colors:
            for rank in self.ranks:
                self.cards.append(f'{color}_{rank}')

                # Deze kaarten moeten 2 keer toegevoegd worden
                if rank in ['+2', 'skip', 'reverse']:
                    self.cards.append(f'{color}_{rank}')
        
        # Deze kaarten moeten 4 keer toegevoegd worden
        self.cards.extend(['black_+4', 'black_wildcard'] * 4)
        
        print(self.cards)


    def distribute_cards(self):
        for _ in range(self.cards_per_player):
            random_card = random.choice(self.cards)
            self.player_hand.append(random_card)
            self.cards.remove(random_card)

            random_card = random.choice(self.cards)
            self.comp_hand.append(random_card)
            self.cards.remove(random_card)

        print(self.player_hand)
        print(self.comp_hand)


    def play_card(self):
        pass