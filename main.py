import pygame
import chess
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

pieces = ['r', 'n', 'b', 'k', 'q', 'p']
pieceImages = {}
for piece in pieces:
    pieceImages['w' + piece] = pygame.image.load(f"ChessPieces/w{piece}.png")
    pieceImages['b' + piece] = pygame.image.load(f"ChessPieces/b{piece}.png")

for image in pieceImages:
    pieceImages[image] = pygame.transform.scale(pieceImages[image], (SQ_SIZE, SQ_SIZE))

board = chess.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Display")


def displayBoard():
    for row in range(8):
        for col in range(8):
            colour = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, colour, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def displayPieces():
    for square in chess.SQUARES:
        curPiece = board.piece_at(square)
        if curPiece:
            piece_colour = "b"
            piece_symbol = curPiece.symbol().lower()
            if curPiece.color == chess.WHITE:
                piece_colour = "w"

            pieceImage = pieceImages[piece_colour + piece_symbol]
            row = math.floor(square/8)
            col = square % 8

            screen.blit(pieceImage, (col * SQ_SIZE, (7 - row) * SQ_SIZE))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displayBoard()
    displayPieces()
    pygame.display.flip()

pygame.quit()
