import pygame
import chess

pygame.init()

# Constants
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

board = chess.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Display")


def displayBoard():
    for row in range(8):
        for col in range(8):
            colour = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, colour, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displayBoard()
    pygame.display.flip()

pygame.quit()
