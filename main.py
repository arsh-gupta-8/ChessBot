import pygame
import chess

pygame.init()

# Constants
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
RED = (201, 29, 34, 100)
BLUE = (65, 105, 225, 100)

pieces = ['r', 'n', 'b', 'k', 'q', 'p']
pieceImages = {}
pieceSmallImages = {}
for piece in pieces:
    pieceImages['w' + piece] = pygame.image.load(f"ChessPieces/w{piece}.png")
    pieceImages['b' + piece] = pygame.image.load(f"ChessPieces/b{piece}.png")

for image in pieceImages:
    pieceImages[image] = pygame.transform.scale(pieceImages[image], (SQ_SIZE, SQ_SIZE))
    pieceSmallImages[image] = pygame.transform.scale(pieceImages[image], (SQ_SIZE//4, SQ_SIZE//4))


board = chess.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Display")

legalMoves = []
squareHighlight = False
pieceHighlight = None
whiteTurn = True


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
            row = square//8
            col = square % 8

            screen.blit(pieceImage, (col * SQ_SIZE, (7 - row) * SQ_SIZE))


def displayHighlights():
    if pieceHighlight is not None:
        row = 7 - pieceHighlight // 8
        col = pieceHighlight % 8
        pygame.draw.rect(screen, BLUE, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    for move in legalMoves:
        square = move.to_square
        row = 7 - (square // 8)
        col = square % 8
        pygame.draw.rect(screen, RED, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def pieceClicked():
    x, y = pygame.mouse.get_pos()
    col = x // SQ_SIZE
    row = 7 - (y // SQ_SIZE)
    return chess.square(col, row)


def piecePromote(pmove, selectedSquare):
    print("ran function")
    if board.piece_at(pmove.from_square).piece_type == chess.PAWN:
        print("pawn moved")
        if (chess.square_rank(pmove.to_square)) == 7:  # white promotion
            print("white promotion")
            promotionPos = chess.square_file(selectedSquare) * SQ_SIZE
            sq_colour = BLACK
            if (chess.square_file(selectedSquare) + chess.square_rank(selectedSquare)) % 2:
                sq_colour = WHITE
            pygame.draw.rect(screen, sq_colour, pygame.Rect(promotionPos, 0, SQ_SIZE, SQ_SIZE))
            screen.blit(pieceSmallImages["wq"], (promotionPos, 0))
            screen.blit(pieceSmallImages["wr"], (promotionPos + (SQ_SIZE//2), 0))
            screen.blit(pieceSmallImages["wb"], (promotionPos, (SQ_SIZE // 2)))
            screen.blit(pieceSmallImages["wb"], (promotionPos + (SQ_SIZE // 2), (SQ_SIZE // 2)))
            checkClickPromotion = True
            while checkClickPromotion:
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if promotionPos < x < promotionPos + SQ_SIZE and 0 < x < SQ_SIZE:
                        checkClickPromotion = False
                        if promotionPos < x < (promotionPos + (SQ_SIZE//2)) and 0 < x < SQ_SIZE//2:
                            pmove.promotion = chess.QUEEN
                        elif promotionPos + SQ_SIZE//2 < x < (promotionPos + SQ_SIZE) and 0 < x < SQ_SIZE//2:
                            pmove.promotion = chess.ROOK
                        elif promotionPos < x < (promotionPos + (SQ_SIZE//2)) and SQ_SIZE//2 < x < SQ_SIZE:
                            pmove.promotion = chess.BISHOP
                        elif promotionPos + SQ_SIZE//2 < x < (promotionPos + SQ_SIZE) and SQ_SIZE//2 < x < SQ_SIZE:
                            pmove.promotion = chess.KNIGHT


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            selectedSquare = pieceClicked()

            piece = board.piece_at(selectedSquare)
            if piece and piece.color == board.turn:
                pieceHighlight = selectedSquare
                legalMoves = []
                for move in board.legal_moves:
                    if move.from_square == pieceHighlight:
                        legalMoves.append(move)

            else:
                for move in legalMoves:
                    if move.to_square == selectedSquare:
                        piecePromote(move, selectedSquare)
                        board.push(move)
                        break
                selectedSquare = None
                pieceHighlight = None
                legalMoves = []

    displayBoard()
    displayHighlights()
    displayPieces()
    pygame.display.flip()

pygame.quit()
