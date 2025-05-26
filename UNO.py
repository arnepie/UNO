import pygame
import GameState
import os 

pygame.init()

GameState = GameState.GameState()
screen = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption("UNO")

def draw_screen():
    background_colour = (255,0,0)
    screen.fill(background_colour)
    pygame.display.flip()

def load_images(cards):
    images = {}
    image_folder = os.path.join(os.path.dirname(__file__), "images")

    for card in cards:
        path = os.path.join(image_folder, card + ".png")
        images[card] = pygame.image.load(path)

    images['back'] = pygame.image.load(os.path.join(image_folder, "back.png"))
    return images

def draw_cards(images):
    screen.blit(images.get('back'), (500, 400))

    if GameState.pile:
        top_card = GameState.pile[-1]

        if top_card.endswith('+4'):
            image_key = 'black_+4'
        elif top_card.endswith('wildcard'):
            image_key = 'black_wildcard'
        else:
            image_key = top_card

        screen.blit(images.get(image_key), (600, 400))

    for i, card in enumerate(GameState.player_hand):
        if images.get(card):
            x_pos = 100 + (100 * i)
            screen.blit(images.get(card), (x_pos, 750))
    
    for i in range(len(GameState.comp_hand)):
        if images.get('back'):
            x_pos = 100 + (100 * i)
            screen.blit(images.get('back'), (x_pos, 150))

    pygame.display.flip()

def draw_color_choosing_screen():
    Background = pygame.Rect(550, 425, 450, 150)
    
    if 'black' in GameState.pile[-1]:
        blue_rectangle = pygame.Rect(575, 450, 100, 100)
        green_rectangle = pygame.Rect(675, 450, 100, 100)
        red_rectangle = pygame.Rect(775, 450, 100, 100)
        yellow_rectangle = pygame.Rect(875, 450, 100, 100)

        pygame.draw.rect(screen, (255, 255, 255 ), Background)
        pygame.draw.rect(screen,(0,0,255), blue_rectangle )
        pygame.draw.rect(screen,(0,128,0), green_rectangle)
        pygame.draw.rect(screen,(255,0,0), red_rectangle)
        pygame.draw.rect(screen,(255,255,0), yellow_rectangle)

        pygame.display.flip()

    else:
        splitted_card = GameState.pile[-1].split("_")
        font = pygame.font.Font('freesansbold.ttf', 36)
        text = font.render(f"The computer has chosen {splitted_card[0]}!", True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255 ), Background)
        textRect = text.get_rect()
        textRect.center = Background.center = (750, 750)
        screen.blit(text, textRect)

        pygame.display.flip()
        pygame.time.delay(2000)
        GameState.choose_card = False

def draw_winning_screen(winner):
    pass

def main():
    running = True

    GameState.initiate_cards()
    images = load_images(GameState.cards)
    GameState.distribute_cards()

    draw_screen()
    draw_cards(images)

    while running:
        # Applique les effets en attente avant chaque action
        if GameState.apply_pending_effect():
            draw_screen()
            draw_cards(images)

        if GameState.choose_card:
            draw_color_choosing_screen()

        elif GameState.turn == 'comp':
            pygame.time.delay(1000)
            GameState.play_comp_move()
            draw_screen()
            draw_cards(images)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

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

                elif GameState.turn == 'player':
                    index = (x - 100) // 100
                    if 0 <= index < len(GameState.player_hand) and y > 700:
                        selected_card = GameState.player_hand[index]
                        if GameState.play_card(selected_card):
                            draw_screen()
                            draw_cards(images)
                    elif 500 < x < 700 and 300 < y < 500:
                        GameState.draw_card('player')
                        GameState.turn = 'comp'
                        draw_screen()
                        draw_cards(images)
                pygame.time.delay(1000)
                




if __name__ == "__main__":
    main()

