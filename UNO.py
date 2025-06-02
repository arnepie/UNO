import pygame
import GameState
import os 

# Initialize pygame
pygame.init()

# Start in menu screen
game_status = "menu"

# Initialize GameState object
GameState = GameState.GameState()

# Set up the game window
screen = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption("UNO")

# Draw screen for game
def draw_screen():
    background_colour = (255,0,0)
    screen.fill(background_colour)
    
# Load images for the cards
def load_images(cards):
    images = {}
    image_folder = os.path.join(os.path.dirname(__file__), "images")

    for card in cards:
        path = os.path.join(image_folder, card + ".png")
        images[card] = pygame.image.load(path)

    # Load the back of a card
    images['back'] = pygame.image.load(os.path.join(image_folder, "back.png"))
    return images

# Draw the current state of the cards on the screen
def draw_cards(images):
    # Draw draw pile (back of card)
    screen.blit(images.get('back'), (500, 400))

    # Draw top card of the discard pile
    if GameState.pile:
        top_card = GameState.pile[-1]

        if top_card.endswith('+4'):
            image_key = 'black_+4'
        elif top_card.endswith('wildcard'):
            image_key = 'black_wildcard'
        else:
            image_key = top_card

        screen.blit(images.get(image_key), (600, 400))

    # Draw player's hand
    for i, card in enumerate(GameState.player_hand):
        if images.get(card):
            x_pos = 100 + (100 * i)
            screen.blit(images.get(card), (x_pos, 750))
    
    # Draw computer's hand (back of cards)
    for i in range(len(GameState.comp_hand)):
        if images.get('back'):
            x_pos = 100 + (100 * i)
            screen.blit(images.get('back'), (x_pos, 150))

# Draw the color selection screen for wild cards
def draw_color_choosing_screen():
    Background = pygame.Rect(550, 425, 450, 150)
    
    if 'black' in GameState.pile[-1]:  # Player chooses color
        # Define color boxes
        blue_rectangle = pygame.Rect(575, 450, 100, 100)
        green_rectangle = pygame.Rect(675, 450, 100, 100)
        red_rectangle = pygame.Rect(775, 450, 100, 100)
        yellow_rectangle = pygame.Rect(875, 450, 100, 100)

        # Draw background and color options
        pygame.draw.rect(screen, (255, 255, 255 ), Background)
        pygame.draw.rect(screen,(0,0,255), blue_rectangle )
        pygame.draw.rect(screen,(0,128,0), green_rectangle)
        pygame.draw.rect(screen,(255,0,0), red_rectangle)
        pygame.draw.rect(screen,(255,255,0), yellow_rectangle)

        pygame.display.flip()

    else:  # Computer has chosen a color
        splitted_card = GameState.pile[-1].split("_")
        font = pygame.font.Font('freesansbold.ttf', 36)
        text = font.render(f"The computer has chosen {splitted_card[0]}!", True, (0, 0, 0))
        textRect = text.get_rect()

        padding_x, padding_y = 40, 30
        rect_width = textRect.width + padding_x
        rect_height = textRect.height + padding_y
        rect_x = (screen.get_width() - rect_width) // 2
        rect_y = (screen.get_height() - rect_height) // 2
        Background = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

        pygame.draw.rect(screen, (255, 255, 255), Background)
        
        textRect.center = Background.center
        screen.blit(text, textRect)

        pygame.display.flip()
        pygame.time.delay(2000)
        GameState.choose_card = False

# Draws the main menu with a "Start Game" button
def draw_start_menu():
    screen.fill((0, 128, 0))
    font = pygame.font.Font('freesansbold.ttf', 80)
    title = font.render("UNO", True, (255,255,255))
    title_rect = title.get_rect(center=(750, 300))
    screen.blit(title, title_rect)

    button_rect = pygame.Rect(575, 500, 350, 100)
    pygame.draw.rect(screen, (255,255,255), button_rect)
    font2 = pygame.font.Font('freesansbold.ttf', 48)
    text = font2.render("Start Game", True, (0,0,0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Displays the winning screen with replay option
def draw_winning_screen(winner):
    screen.fill((0, 128, 0))
    font = pygame.font.Font('freesansbold.ttf', 60)
    text = font.render(f"{winner.capitalize()} wins!", True, (255,255,255))
    text_rect = text.get_rect(center=(750, 350))
    screen.blit(text, text_rect)

    button_rect = pygame.Rect(575, 500, 350, 100)
    pygame.draw.rect(screen, (255,255,255), button_rect)
    font2 = pygame.font.Font('freesansbold.ttf', 48)
    text2 = font2.render("Replay", True, (0,0,0))
    text2_rect = text2.get_rect(center=button_rect.center)
    screen.blit(text2, text2_rect)
    return button_rect

# Main game loop
def main():
    global game_status
    running = True
    winner = None
    game_over = False

    images = load_images(GameState.cards)

    while running:
        if game_status == "menu":
            button_rect = draw_start_menu()

        elif game_status == "game":
            if not game_over:  
                # Check for win condition
                if len(GameState.player_hand) == 0:
                    winner = 'player'
                    game_over = True
                    game_status = "win"
                elif len(GameState.comp_hand) == 0:
                    winner = 'comp'
                    game_over = True
                    game_status = "win"

                # Apply pending effects
                if GameState.apply_pending_effect():
                    draw_screen()
                    draw_cards(images)

                # Show color picker if needed
                if GameState.choose_card:
                    draw_color_choosing_screen()

                # Computer's turn
                elif GameState.turn == 'comp':
                    pygame.time.delay(1000)
                    GameState.play_comp_move()
                    draw_screen()
                    draw_cards(images)

                # Player's turn
                else:
                    draw_screen()
                    draw_cards(images)

        # If there is a winner, draw a winning screen
        elif game_status == "win":
            button_rect = draw_winning_screen(winner)

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Start game from menu
            if game_status == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if button_rect.collidepoint(x, y):
                    GameState.initiate_cards()
                    images = load_images(GameState.cards)
                    GameState.distribute_cards()

                    winner = None
                    game_over = False
                    game_status = "game"

            # Restart game from win screen
            elif game_status == "win" and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_rect.collidepoint(x, y):
                    GameState.__init__()
                    GameState.initiate_cards()
                    images = load_images(GameState.cards)
                    GameState.distribute_cards()

                    winner = None
                    game_over = False
                    game_status = "game"

            # Handle player move
            elif game_status == "game" and not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Player selects color for wild card
                if GameState.choose_card:
                    if 575 <= x <= 675 and 450 <= y <= 550:
                        GameState.pile[-1] = GameState.pile[-1].replace('black', 'blue')
                    elif 675 <= x <= 775 and 450 <= y <= 550:
                        GameState.pile[-1] = GameState.pile[-1].replace('black', 'green')
                    elif 775 <= x <= 875 and 450 <= y <= 550:
                        GameState.pile[-1] = GameState.pile[-1].replace('black', 'red')
                    elif 875 <= x <= 975 and 450 <= y <= 550:
                        GameState.pile[-1] = GameState.pile[-1].replace('black', 'yellow')
                    draw_screen()
                    draw_cards(images)
                    GameState.choose_card = False

                # Player plays a card
                elif GameState.turn == 'player':
                    index = (x - 100) // 100

                    if 0 <= index < len(GameState.player_hand) and y > 700:
                        selected_card = GameState.player_hand[index]
                        if GameState.play_card(selected_card):
                            draw_screen()
                            draw_cards(images)

                    # Player draws a card
                    elif 500 < x < 700 and 300 < y < 500:
                        GameState.draw_card('player')
                        GameState.turn = 'comp'
                        draw_screen()
                        draw_cards(images)

        pygame.display.flip()

# Start the game
if __name__ == "__main__":
    main()
