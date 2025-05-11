import pygame
import logging
from engine.objects import Window

pygame.init()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Start game")

def run_game(num_dino, fps):
    window = Window()
    window.start(num_dino=num_dino)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                pygame.quit()

        window.rendering()
        if fps is not None:
            clock.tick(fps)

if __name__ == "__main__":
    run_game(4, 120)
