import random
import time
from queue import PriorityQueue

# Definição de constantes
EMPTY = ' '
SNAKE_HEAD = '■'
SNAKE_BODY = '▪'
FOOD = '*'
WALL = '▓'

class SnakeAI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Inicializa a cobra com dois segmentos
        self.snake = [(width // 2, height // 2), (width // 2 - 1, height // 2)]
        self.direction = (1, 0)
        self.food = None
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.place_food()
        self.food_eaten = 0
        self.moves_made = 0

    def place_food(self):
        while True:
            # Garante que a comida não apareça nas paredes
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def update_grid(self):
        # Preenche o grid com espaços vazios
        self.grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        
        # Adiciona as paredes
        for i in range(self.width):
            self.grid[0][i] = WALL
            self.grid[self.height-1][i] = WALL
        for i in range(self.height):
            self.grid[i][0] = WALL
            self.grid[i][self.width-1] = WALL
        
        # Adiciona a cobra
        for i, (x, y) in enumerate(self.snake):
            self.grid[y][x] = SNAKE_HEAD if i == 0 else SNAKE_BODY
        
        # Adiciona a comida
        if self.food:
            self.grid[self.food[1]][self.food[0]] = FOOD

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))
        print("\n")

    def is_valid_move(self, x, y):
        return (0 <= x < self.width and 0 <= y < self.height and
                self.grid[y][x] not in [WALL, SNAKE_BODY])

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self):
        start = self.snake[0]
        goal = self.food

        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current = frontier.get()[1]

            if current == goal:
                break

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)

                if self.is_valid_move(next_pos[0], next_pos[1]):
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + self.heuristic(goal, next_pos)
                        frontier.put((priority, next_pos))
                        came_from[next_pos] = current

        if goal not in came_from:
            return None

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def move(self):
        path = self.find_path()
        if not path:
            return False

        next_pos = path[0]
        self.snake.insert(0, next_pos)

        if next_pos == self.food:
            self.place_food()
            self.food_eaten += 1
        else:
            self.snake.pop()

        self.moves_made += 1
        return True

    def run(self):
        while True:
            self.update_grid()
            self.print_grid()
            if not self.move():
                print("Fim do jogo!")
                print(f"Alimentos consumidos: {self.food_eaten}")
                print(f"Movimentos realizados: {self.moves_made}")
                break
            time.sleep(0.3)

# Exemplo de uso
if __name__ == "__main__":
    game = SnakeAI(20, 10)
    game.run()