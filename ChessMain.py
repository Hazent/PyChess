# Here we store all information about current state of game

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animations
IMAGES = {}

# Initialise global dictionary of images. Only called once in the main
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # We can access an image by saying for example 'IMAGES['wp']'


# Main driver for the code, handles user input and updating graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = () # Keeps track of the last clicked square (tuple: (row, col))
    playerClicks = [] # Keeps track of the player clicks (two tuples: [(6, 4), (4, 4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Undo function by pressing 'z'
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # The x and y coördinates of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # User wants to deselect the square
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append both 1st and 2nd click
                if len(playerClicks) == 2: # After second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () # Resets the user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen) # Draws the squares on the board
    drawPieces(screen, gs.board) # Draws the pieces on top of the squares

# Draws the board using white's perspective
def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x+y) % 2)]
            p.draw.rect(screen, color, p.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draws the pieces on the board using the current board state
def drawPieces(screen, board):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = board[x][y]
            if piece != "--": #Square is not occupied
                screen.blit(IMAGES[piece], p.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
