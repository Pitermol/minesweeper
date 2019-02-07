import random
import os
import pygame
import sys

pygame.init()
size = 320, 470
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def end_screen():
    intro_text = ["GAME OVER",
                  "PLEASE PUSH SPACE TO QUIT"]

    fon = pygame.transform.scale(load_image('game_over.jpg'), (320, 470))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(10)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("red"),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass

    def on_click_right(self, cell, right):
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_click_right(self, mouse_pos, right):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click_right(cell, right)


class Minesweeper(Board):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        print(1)
        # вначале все клетки закрыты
        self.board = [[-12] * width for _ in range(height)]
        i = 0
        while i < n:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -12:
                self.board[y][x] = -10
                i += 1
        print(self.board)
        self.ind = 0

    def game_end(self):
        for y in range(self.height):
            for x in range(self.width):

                # мина - синий квадрат
                if self.board[y][x] == 10:
                    pygame.draw.rect(screen, pygame.Color("blue"),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                      self.cell_size))

                if self.board[y][x] >= 0 and self.board[y][x] != 10:
                    font = pygame.font.Font(None, self.cell_size - 6)
                    text = font.render(str(self.board[y][x]), 1, (100, 255, 100))
                    screen.blit(text, (x * self.cell_size + self.left + 3, y * self.cell_size + self.top + 3))

                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)
        board.render()
        pygame.display.flip()

    def on_click_right(self, cell, right):
        x, y = cell
        print(self.board[y][x])
        self.board[y][x] *= right
        print(self.board[y][x])

    def open_cell(self, cell):
        x, y = cell
        # проверяем на бомбу
        if abs(self.board[y][x]) == 10:
            for z in range(len(self.board)):
                for c in range(len(self.board[z])):
                    if abs(self.board[c][z]) == 10:
                        self.board[c][z] = -15
            print(self.board)
            self.ind = 1
            return
        s = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                    continue
                if abs(self.board[y + dy][x + dx]) == 10:
                    s += 1
        self.board[y][x] = s
        print(self.board)

    def on_click(self, cell):
        self.open_cell(cell)

    def render(self):
        self.game_over = False
        all_sprites = pygame.sprite.Group()
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 10 or self.board[y][x] == 12:
                    pygame.draw.rect(screen, pygame.Color('red'), (x * self.cell_size + self.left + 3, y * self.cell_size + self.top + 3, self.cell_size - 3, self.cell_size - 3))
                elif self.board[y][x] >= 0 and self.board[y][x] != 10 and self.board[y][x] != -10:
                    font = pygame.font.Font(None, self.cell_size - 6)
                    text = font.render(str(self.board[y][x]), 1, (100, 255, 100))
                    screen.blit(text, (x * self.cell_size + self.left + 3, y * self.cell_size + self.top + 3))
                elif self.board[y][x] == -15:
                    pygame.draw.rect(screen, pygame.Color('green'), (
                    x * self.cell_size + self.left + 3, y * self.cell_size + self.top + 3, self.cell_size - 3,
                    self.cell_size - 3))

                pygame.draw.rect(screen, pygame.Color('white'),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)


right = 1
board = Minesweeper(5, 5, 2)
board.set_view(10, 10, 30)
# Включено ли обновление поля
time_on = False
ticks = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            right *= -1
            print(right, 1212)
            board.get_click_right(event.pos, right)
            right *= -1
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
    clock.tick(50)
    ticks += 1
pygame.quit()
