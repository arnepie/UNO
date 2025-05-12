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
            x_pos = 50 + (50 * i)
            screen.blit(images.get(card), (x_pos, 750))
    
    for i in range(len(GameState.comp_hand)):
        if images.get('back'):
            x_pos = 50 + (50 * i)
            screen.blit(images.get('back'), (x_pos, 150))


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

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


main()
