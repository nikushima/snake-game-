import tkinter as tk
import random

# Константы для игры
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        # Начальные параметры игры
        self.score = 0
        self.direction = 'down'

        # Метки и холст
        self.label = tk.Label(self.root, text="Score: 0", font=('consolas', 40))
        self.label.pack()

        self.canvas = tk.Canvas(self.root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.root.update()

        self.center_window()

        # Связывание клавиш для управления змейкой
        self.root.bind('<Left>', lambda event: self.change_direction('left'))
        self.root.bind('<Right>', lambda event: self.change_direction('right'))
        self.root.bind('<Up>', lambda event: self.change_direction('up'))
        self.root.bind('<Down>', lambda event: self.change_direction('down'))

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        self.next_turn()

    def center_window(self):
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def next_turn(self):
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        # Обновление позиции змейки
        self.snake.move(x, y)

        if self.snake.eat(self.food):
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.food.generate_new()
        else:
            self.snake.shrink()

        # Проверка столкновений
        if self.check_collisions():
            self.game_over()
        else:
            self.root.after(SPEED, self.next_turn)

    def change_direction(self, new_direction):
        """Изменение направления движения змейки."""
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collisions(self):
        """Проверка столкновений змейки с границами и телом."""
        x, y = self.snake.coordinates[0]

        # Столкновение с границами экрана
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        # Столкновение с телом
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        """Конец игры."""
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                                font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(self.body_size)]
        self.squares = [self.create_square(x, y) for x, y in self.coordinates]

    def create_square(self, x, y):
        """Создание квадрата змейки."""
        return self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")

    def move(self, x, y):
        """Передвижение змейки."""
        self.coordinates.insert(0, (x, y))
        square = self.create_square(x, y)
        self.squares.insert(0, square)

    def eat(self, food):
        """Проверка, съела ли змейка еду."""
        return self.coordinates[0] == food.coordinates

    def shrink(self):
        """Удаление хвоста змейки."""
        del self.coordinates[-1]
        self.canvas.delete(self.squares[-1])
        del self.squares[-1]


class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coordinates = self.generate_coordinates()
        self.food_item = self.create_food()

    def generate_coordinates(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return [x, y]

    def create_food(self):
        """Создание еды на холсте."""
        x, y = self.coordinates
        return self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

    def generate_new(self):
        """Генерация новой еды."""
        self.canvas.delete("food")
        self.coordinates = self.generate_coordinates()
        self.food_item = self.create_food()


# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
