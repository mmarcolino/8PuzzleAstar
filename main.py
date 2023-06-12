import pygame
import sys
from queue import PriorityQueue

# Definindo as dimensões da janela
WIDTH = 400
HEIGHT = 400
FPS = 30  # Reduzindo a taxa de atualização para tornar a visualização mais lenta

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Definindo o tamanho e a margem do tabuleiro
TILE_SIZE = 100
TILE_MARGIN = 5

# Estado inicial e objetivo
initial_state = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

goal_state = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]


def get_user_input():
    print("Insira o estado inicial (use 0 para representar o espaço em branco):")
    for i in range(3):
        for j in range(3):
            initial_state[i][j] = int(input(f"Posição ({i}, {j}): "))

    print("Insira o estado objetivo:")
    for i in range(3):
        for j in range(3):
            goal_state[i][j] = int(input(f"Posição ({i}, {j}): "))


class Puzzle:
    def __init__(self, state, parent=None, move=""):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = self.calculate_cost()

    def __lt__(self, other):
        return self.cost < other.cost

    def calculate_cost(self):
        # Heurística Tiles Out Of Space
        cost = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != goal_state[i][j]:
                    cost += 1
        return cost


def get_blank_position(state):
    # Encontra a posição do espaço em branco
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def get_valid_moves(i, j):
    # Retorna as jogadas válidas para uma determinada posição
    moves = []
    if i > 0:
        moves.append("up")
    if i < 2:
        moves.append("down")
    if j > 0:
        moves.append("left")
    if j < 2:
        moves.append("right")
    return moves


def make_move(state, move):
    # Realiza um movimento no tabuleiro
    new_state = [row[:] for row in state]
    blank_i, blank_j = get_blank_position(state)

    if move == "up":
        new_state[blank_i][blank_j], new_state[blank_i - 1][blank_j] = new_state[blank_i - 1][blank_j], new_state[blank_i][blank_j]
    elif move == "down":
        new_state[blank_i][blank_j], new_state[blank_i + 1][blank_j] = new_state[blank_i + 1][blank_j], new_state[blank_i][blank_j]
    elif move == "left":
        new_state[blank_i][blank_j], new_state[blank_i][blank_j - 1] = new_state[blank_i][blank_j - 1], new_state[blank_i][blank_j]
    elif move == "right":
        new_state[blank_i][blank_j], new_state[blank_i][blank_j + 1] = new_state[blank_i][blank_j + 1], new_state[blank_i][blank_j]

    return new_state


def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_puzzle(surface, puzzle):
    for i in range(3):
        for j in range(3):
            x = j * (TILE_SIZE + TILE_MARGIN)
            y = i * (TILE_SIZE + TILE_MARGIN)
            pygame.draw.rect(surface, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
            if puzzle.state[i][j] != 0:
                draw_text(surface, str(puzzle.state[i][j]), 50, x + 45, y + 30, WHITE)

def depth_first_search(initial_state, screen, clock):
    open_list = [Puzzle(initial_state)]
    closed_list = set()
    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current_puzzle = open_list.pop()
        screen.fill(WHITE)
        draw_puzzle(screen, current_puzzle)
        pygame.display.flip()
        clock.tick(FPS)
        if current_puzzle.state == goal_state:
            # Solução encontrada
            solution_moves = []
            while current_puzzle.parent:
                solution_moves.append(current_puzzle.move)
                current_puzzle = current_puzzle.parent
            solution_moves.reverse()
            print("Solução encontrada:", solution_moves)
            return

        closed_list.add(tuple(map(tuple, current_puzzle.state)))

        blank_i, blank_j = get_blank_position(current_puzzle.state)
        valid_moves = get_valid_moves(blank_i, blank_j)

        for move in valid_moves:
            new_state = make_move(current_puzzle.state, move)
            if tuple(map(tuple, new_state)) not in closed_list:
                new_puzzle = Puzzle(new_state, current_puzzle, move)
                open_list.append(new_puzzle)  

    print("Nenhuma solução encontrada.")

def breadth_first_search(initial_state, screen, clock):
    open_list = [Puzzle(initial_state)]
    closed_list = set()
    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current_puzzle = open_list.pop(0)
        screen.fill(WHITE)
        draw_puzzle(screen, current_puzzle)
        pygame.display.flip()
        clock.tick(FPS)
        if current_puzzle.state == goal_state:
            # Solução encontrada
            solution_moves = []
            while current_puzzle.parent:
                solution_moves.append(current_puzzle.move)
                current_puzzle = current_puzzle.parent
            solution_moves.reverse()
            print("Solução encontrada:", solution_moves)
            return

        closed_list.add(tuple(map(tuple, current_puzzle.state)))

        blank_i, blank_j = get_blank_position(current_puzzle.state)
        valid_moves = get_valid_moves(blank_i, blank_j)

        for move in valid_moves:
            new_state = make_move(current_puzzle.state, move)
            if tuple(map(tuple, new_state)) not in closed_list:
                new_puzzle = Puzzle(new_state, current_puzzle, move)
                open_list.append(new_puzzle)

    print("Nenhuma solução encontrada.")
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8-Puzzle Solver")
    clock = pygame.time.Clock()

    get_user_input()

    search_type = input("Selecione o tipo de busca (1 - A*, 2 - Busca em Profundidade, 3- Busca em Largura): ")

    if search_type == "1":
        open_list = PriorityQueue()
        open_list.put(Puzzle(initial_state))


        solved = False

        while not solved:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not open_list.empty():
                current_puzzle = open_list.get()
                if current_puzzle.state == goal_state:
                    # Solução encontrada
                    solution_moves = []
                    while current_puzzle.parent:
                        solution_moves.append(current_puzzle.move)
                        current_puzzle = current_puzzle.parent
                    solution_moves.reverse()
                    print("Solução encontrada:", solution_moves)
                    break

                blank_i, blank_j = get_blank_position(current_puzzle.state)
                valid_moves = get_valid_moves(blank_i, blank_j)

                for move in valid_moves:
                    new_state = make_move(current_puzzle.state, move)
                    new_puzzle = Puzzle(new_state, current_puzzle, move)
                    open_list.put(new_puzzle)

            screen.fill(WHITE)
            draw_puzzle(screen, current_puzzle)
            pygame.display.flip()
            clock.tick(FPS)


    elif search_type == "2":
        depth_first_search(initial_state, screen, clock)
    elif search_type == "3":
        breadth_first_search(initial_state, screen, clock)
    else:
        print("Tipo de busca inválido.")
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()