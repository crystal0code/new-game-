import pygame
import random

# Инициализация Pygame
pygame.init()

# Определяем размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chaos Jump")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Цвет монет
BLACK = (0, 0, 0)

# Персонаж
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_vel = 5
jumping = False
jump_height = 10
gravity = 0.5
y_velocity = 0

# Платформы
platforms = []
for i in range(5):
    platforms.append((random.randint(0, WIDTH - 100), random.randint(100, HEIGHT - 50)))

# Монеты
coins = []
num_coins = 10  # Количество монет
for _ in range(num_coins):
    coins.append((random.randint(0, WIDTH - 20), random.randint(50, HEIGHT - 50)))  # Генерация монет

# Счетчик монет
coin_count = 0

# Основной цикл игры
running = True
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Запоминаем время старта

while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_vel
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if keys[pygame.K_SPACE]:
        if not jumping:
            jumping = True
            y_velocity = -jump_height

    # Логика прыжка
    if jumping:
        player_y += y_velocity
        y_velocity += gravity
        if player_y >= HEIGHT - player_size:
            player_y = HEIGHT - player_size
            jumping = False

        # Проверка столкновения с платформами
        for plat_x, plat_y in platforms:
            if plat_x < player_x < plat_x + 100 and player_y + player_size >= plat_y:
                player_y = plat_y - player_size
                y_velocity = -jump_height  # Подскакивание
                platforms.remove((plat_x, plat_y))  # Удаляем платформу
                # Добавляем новую платформу на случайное место
                new_plat_x = random.randint(0, WIDTH - 100)
                new_plat_y = random.randint(100, HEIGHT - 50)
                platforms.append((new_plat_x, new_plat_y))
                break  # Выход из цикла, чтобы не обрабатывать остальные платформы

    # Проверка на столкновение с монетами
    for coin_x, coin_y in coins[:]:  # Используем срез для безопасного удаления
        if (coin_x < player_x < coin_x + 20) and (coin_y < player_y < coin_y + 20):
            coins.remove((coin_x, coin_y))
            coin_count += 1  # Увеличиваем счетчик монет

    # Обновление экрана
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))  # Игрок
    for plat_x, plat_y in platforms:
        pygame.draw.rect(screen, GREEN, (plat_x, plat_y, 100, 20))  # Платформы

    # Рисуем монеты
    for coin_x, coin_y in coins:
        pygame.draw.circle(screen, YELLOW, (coin_x + 10, coin_y + 10), 10)  # Рисуем монету

    # Таймер
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Время в секундах
    font = pygame.font.Font(None, 36)
    text = font.render(f"Время: {seconds} сек", True, BLACK)
    screen.blit(text, (WIDTH - 150, 10))  # Позиция текста

    # Счетчик монет
    coin_text = font.render(f"Монет: {coin_count}", True, BLACK)
    screen.blit(coin_text, (10, 10))  # Позиция текста монет

    pygame.display.update()

# Завершение работы Pygame
pygame.quit()
