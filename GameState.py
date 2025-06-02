import random
import pygame

class GameState:
    def __init__(self):
        self.cards = []  # All possible cards
        self.colors = ['red', 'green', 'blue', 'yellow']  # The colors used in the game
        self.ranks = [0] + [i for i in range(1, 10)] + ['+2', 'skip', 'reverse']  # The ranks, including numbers and action cards
        self.cards_per_player = 7  # Number of cards each player starts with

        self.pile = []  # Discard pile
        self.player_hand = []  # Hand of the player
        self.comp_hand = []  # Hand of the computer
        self.turn = 'player'  # The current turn
        self.choose_card = False  # Used for color picking after wild cards
        self.pending_effect = None  # Stores any pending action

    # Creates and shuffles the deck of cards
    def initiate_cards(self):
        for color in self.colors:
            for rank in self.ranks:
                self.cards.append(f'{color}_{rank}')
                # Each +2, skip, reverse appears twice
                if rank in ['+2', 'skip', 'reverse']:
                    self.cards.append(f'{color}_{rank}')

        # Add wildcards and +4s (4 each)
        self.cards.extend(['black_+4', 'black_wildcard'] * 4)

        # Shuffle the deck
        random.shuffle(self.cards)

    # Deals cards to both players and starts the pile
    def distribute_cards(self):
        for _ in range(self.cards_per_player):
            self.player_hand.append(self.cards.pop())
            self.comp_hand.append(self.cards.pop())
        
        # Ensure the starting pile card isn't a special one
        card = self.cards.pop()
        while ('+2' in card) or ('reverse' in card) or ('skip' in card) or ('black' in card):
            card = self.cards.pop()
        self.pile.append(card)
        print(f"Start of the game, card on the pile: {self.pile[-1]}")

    # Player or computer plays a card
    def play_card(self, card):
        print(f"{self.turn} played {card}")

        # For player, check move validity
        if self.turn == 'player':
            if not self.valid_move(card):
                print("Invalid move!")
                return False
            self.player_hand.remove(card)

        else:
            self.comp_hand.remove(card)

        # Add the card to the pile
        self.pile.append(card)

        # Handle black cards
        if 'black' in card:
            if self.turn == 'player':
                self.choose_card = True  # Player needs to pick a color

            else:
                # Computer picks a color randomly
                chosen_color = random.choice(self.colors)
                self.pile[-1] = self.pile[-1].replace('black', chosen_color)

                # Set pending effect for +4
                if '+4' in card:
                    self.pending_effect = {'type': '+4', 'target': self.opponent()}
                    print(f"Effect +4 activated on {self.pending_effect['target']}")
                else:
                    self.turn = self.opponent()

                self.choose_card = True
                return True

        # Effect of the cards
        if '+2' in card:
            self.pending_effect = {'type': '+2', 'target': self.opponent()}
            print(f"Effect +2 activated on {self.pending_effect['target']}")
        elif '+4' in card:
            self.pending_effect = {'type': '+4', 'target': self.opponent()}
            print(f"Effect +4 activated on {self.pending_effect['target']}")
        elif 'skip' in card or 'reverse' in card:
            self.pending_effect = {'type': 'skip', 'target': self.opponent()}
            print(f"Effect skip activated on {self.pending_effect['target']}")

        # If card was not a draw card, change the turn
        if not ('+2' in card or '+4' in card):
            self.turn = self.opponent()
            print(f"Turned changed to {self.turn}")

        return True

    # Get the opponent of the current player
    def opponent(self):
        return 'player' if self.turn == 'comp' else 'comp'

    # Apply any pending effects
    def apply_pending_effect(self):
        if self.pending_effect is None:
            return False

        effect = self.pending_effect
        target = effect['target']

        print(f"Applying {effect['type']} to {target}")

        if effect['type'] == '+2':
            for _ in range(2):
                self.draw_card(target)
            print(f"{target} took 2 cards")

            self.turn = self.opponent()
            print(f"Turn after effect: {self.turn}")

        elif effect['type'] == '+4':
            for _ in range(4):
                self.draw_card(target)
            print(f"{target} took 4 cards")

            self.turn = self.opponent()
            print(f"Turn after effect: {self.turn}")

        elif effect['type'] == 'skip':
            self.turn = self.opponent()
            print(f"{target} is skipped, turn to {self.turn}")

        # Reset effect
        self.pending_effect = None
        return True

    # Draw a card for a player
    def draw_card(self, player):
        if len(self.cards) == 0:
            # Reshuffle the pile when deck runs out
            top = self.pile.pop()

            # Normalize black cards before reshuffling
            reshuffled = []
            for card in self.pile:
                if '+4' in card and any(color in card for color in self.colors):
                    reshuffled.append('black_+4')
                elif 'wildcard' in card and any(color in card for color in self.colors):
                    reshuffled.append('black_wildcard')
                else:
                    reshuffled.append(card)

            self.cards = reshuffled
            self.pile = [top]
            random.shuffle(self.cards)
            print("Reshuffled the pile")

        # Assign the drawn card
        if player == 'player':
            self.player_hand.append(self.cards.pop())
            print("Player took one card")
        else:
            self.comp_hand.append(self.cards.pop())
            print("Computer took one card")

    # Check if a move is valid
    def valid_move(self, card):
        # Wildcards are always valid
        if card not in ['black_+4', 'black_wildcard']:
            splitted_card = card.split("_")
            splitted_pile_card = self.pile[-1].split("_")

            # Valid if color or rank matches
            if splitted_card[0] == splitted_pile_card[0] or splitted_card[1] == splitted_pile_card[1]:
                return True
        else:
            return True  # Wildcards
        
        return False
    
    # Have the computer play a move
    def play_comp_move(self):
        # Try to play a valid card
        for card in self.comp_hand:
            if self.valid_move(card):
                self.play_card(card)
                return
        
        # If no card is playable, draw one
        self.draw_card("comp")
        self.turn = self.opponent()
        print(f"Turn after computer: {self.turn}")
    
