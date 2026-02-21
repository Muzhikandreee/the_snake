from random import choice, randint
import pygame

# Настройки констант
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость змейки
SPEED = 15

# Настройки окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


# Базовый класс для игровых объектов
class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.reset()

    def reset(self, snake_positions=None):
        """Устанавливает новую позицию яблока, отличающуюся от тела змейки."""
        while True:
            new_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if snake_positions is None or new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Изменяет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Осуществляет движение змейки."""
        current_head_position = self.get_head_position()
        dx, dy = self.direction
        new_head_position_x = (
            current_head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_position_y = (
            current_head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_head_position_x, new_head_position_y)

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки в начальное."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


# Обработчик событий клавиатуры
def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


# Основной игровой цикл
def main():
    """Главный игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Обновляем позицию яблока, если змейка его съела
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.reset(snake.positions)

        # Проверяем поражение при столкновении с телом
        if snake.get_head_position() in snake.positions[1:] and snake.length > 1:
            print("Игра завершилась.")
            snake.reset()

        # Чистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка элементов
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
