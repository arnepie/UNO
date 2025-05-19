import pygame
import GameState

GameState = GameState.GameState()
screen = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption("UNO")


def draw_screen():
    background_colour = (255,0,0)
    screen.fill(background_colour)
   
    pygame.display.flip()


def load_images(cards):
    images = {}

    for card in cards:
        images[card] = pygame.image.load("images\\" + card + ".png")
    images['back'] = pygame.image.load("images\\back.png")

    return images


def draw_cards(images):
    screen.blit(images.get('back'), (500, 400))

    if GameState.pile:
        screen.blit(images.get(GameState.pile[-1]), (600, 400))
    
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
    my_rectangle = pygame.Rect(400, 400, 200, 200)
    pygame.draw.rect(screen, (255, 255, 255 ), my_rectangle)
    blue_rectangle = pygame.Rect(100,100,50,50)
    pygame.draw.rect(screen,(0,0,255), blue_rectangle )
    green_rectangle = pygame.Rect(100,100,50,50)
    pygame.draw.rect(screen,(0,128,0), green_rectangle)
    red_rectangle = pygame.Rect(100,100,50,50)
    pygame.draw.rect(screen,(255,0,0), red_rectangle)
    yellow_rectangle = pygame.Rect(100,100,50,50)
    pygame.draw.rect(screen,(255,255,0), yellow_rectangle)

    pygame.display.flip()


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
        print(GameState.choose_card)
        if GameState.choose_card == True:
            draw_color_choosing_screen()

        if GameState.turn == 'comp':
            pygame.time.delay(1000)
            GameState.play_comp_move()
            draw_screen()
            draw_cards(images)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and GameState.turn == 'player':
                x, y = pygame.mouse.get_pos()

                index = (x - 100) // 100
                if 0 <= index < len(GameState.player_hand):
                    selected_card = GameState.player_hand[index]
                    GameState.play_card(selected_card)
                    draw_screen()
                    draw_cards(images)
                    


main()
