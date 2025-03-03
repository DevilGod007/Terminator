import pygame
import chess
import os
import chess.pgn
import random
from engine import evaluate_moves  # Import your AI engine

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SIDE_PANEL_WIDTH = 300
SQUARE_SIZE = WIDTH // 8
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
LIGHT_BROWN, DARK_BROWN = (222, 184, 135), (139, 69, 19)
HIGHLIGHT_COLOR = (0, 255, 0)

# Load piece images
IMAGE_PATH = "images"
piece_images = {}
piece_names = {'p': 'pawn', 'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king'}

for piece, name in piece_names.items():
    piece_images[f'w{piece}'] = pygame.image.load(os.path.join(IMAGE_PATH, f'w_{name}.png'))
    piece_images[f'b{piece}'] = pygame.image.load(os.path.join(IMAGE_PATH, f'b_{name}.png'))

# Pygame window
screen = pygame.display.set_mode((WIDTH + SIDE_PANEL_WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Chess board
board = chess.Board()
selected_square = None
game_over = False
winner = ""

# Ensure train directory exists
TRAIN_DIR = "train"
os.makedirs(TRAIN_DIR, exist_ok=True)

# Randomly assign AI as White or Black
ai_plays_white = random.choice([True, False])

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if selected_square is not None:
                moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]
                if chess.square(col, 7 - row) in moves:
                    pygame.draw.circle(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
                piece_img = piece_images.get(piece_key)
                if piece_img:
                    screen.blit(pygame.transform.scale(piece_img, (SQUARE_SIZE, SQUARE_SIZE)), (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_game_over():
    font = pygame.font.SysFont(None, 72)
    text = font.render(f"Game Over: {winner}", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))

def draw_move_log():
    font = pygame.font.SysFont(None, 30)
    move_log_surface = pygame.Surface((SIDE_PANEL_WIDTH, HEIGHT))
    move_log_surface.fill((200, 200, 200))
    moves = board.move_stack
    for i, move in enumerate(moves):
        move_text = font.render(f"{i+1}: {move.uci()}", True, BLACK)
        move_log_surface.blit(move_text, (10, 30 * i))
    screen.blit(move_log_surface, (WIDTH, 0))

def make_ai_move():
    global game_over, winner
    if not board.is_game_over() and board.turn == (chess.WHITE if ai_plays_white else chess.BLACK):
        best_move = evaluate_moves(board)  # AI calculates best move
        if best_move and best_move in board.legal_moves:
            board.push(best_move)
            check_game_over()

def check_game_over():
    global game_over, winner
    if board.is_checkmate():
        game_over = True
        winner = "White wins!" if board.turn else "Black wins!"
    elif board.is_stalemate():
        game_over = True
        winner = "Draw (Stalemate)"
    elif board.is_insufficient_material():
        game_over = True
        winner = "Draw (Insufficient Material)"
    elif board.is_seventyfive_moves():
        game_over = True
        winner = "Draw (75-move rule)"
    elif board.is_fivefold_repetition():
        game_over = True
        winner = "Draw (Fivefold Repetition)"
    if game_over:
        save_game_pgn()

def save_game_pgn():
    game = chess.pgn.Game()
    game.headers["Event"] = "Pygame Chess Game"
    game.headers["Site"] = "Local"
    game.headers["Date"] = "????.??.??"
    game.headers["Round"] = "1"
    game.headers["White"] = "AI" if ai_plays_white else "Player"
    game.headers["Black"] = "Player" if ai_plays_white else "AI"
    node = game
    for move in board.move_stack:
        node = node.add_variation(move)
    game_count = len(os.listdir(TRAIN_DIR)) + 1
    game_file = os.path.join(TRAIN_DIR, f"game_{game_count}.pgn")
    with open(game_file, "w") as pgn_file:
        pgn_file.write(str(game))

def handle_click(pos):
    global selected_square, game_over
    if game_over:
        return
    
    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    if not (0 <= col < 8 and 0 <= row < 8):
        return

    square = chess.square(col, 7 - row)
    if selected_square is None:
        if board.piece_at(square) and board.piece_at(square).color == board.turn:
            selected_square = square
    else:
        move = chess.Move(selected_square, square)
        if move in board.legal_moves:
            board.push(move)
            check_game_over()
            if not game_over:
                make_ai_move()
        selected_square = None

def main():
    global selected_square, game_over
    running = True

    # AI plays first if it is White
    if ai_plays_white:
        make_ai_move()

    while running:
        draw_board()
        draw_pieces()
        draw_move_log()
        if game_over:
            draw_game_over()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and board.turn != (chess.WHITE if ai_plays_white else chess.BLACK):
                    handle_click(pygame.mouse.get_pos())
                    make_ai_move()  # AI moves after player

    pygame.quit()

if __name__ == "__main__":
    main()
