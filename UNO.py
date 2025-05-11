import pygame
import GameState

GameState = GameState.GameState()


def draw_screen(screen):
    background_colour = (255,0,0)

    pygame.display.set_caption("UNO")
    screen.fill(background_colour)
   
    pygame.display.flip()


def load_images(cards):
    images = []
    cards = list(set(cards)) # Remove doubles

    for card in cards:
        images.append(pygame.image.load("images/" + card + ".png"))

    return images


def draw_cards(screen, images, player_hand, comp_hand, pile):
    screen.blit(images[0], (500, 500))

    pygame.display.flip()


def draw_winning_screen(winner):
    pass


def main():
    running = True
    screen = pygame.display.set_mode((1500, 1000))

    GameState.initiate_cards()
    GameState.distribute_cards()
    draw_screen(screen)

    images = load_images(GameState.cards)
    draw_cards(screen, images, 0, 0 ,0)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


main()