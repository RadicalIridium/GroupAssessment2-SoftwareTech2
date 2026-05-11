import pygame
import random
import sys

from modules import merge_sort

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting")
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

array = []
ARRAY_SIZE = 30
bar_width = WIDTH // ARRAY_SIZE


def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)

def make_array():
    ARRAY_SIZE = 30
    array = [random.randint(10, 350) for _ in range(ARRAY_SIZE)]
    return array


def draw_array(array, color_positions=None):
    screen.fill((30, 30, 30))
    option()
    for i, val in enumerate(array):
        color = (100, 200, 250)
        if color_positions and i in color_positions['compare']:
            color = (255, 100, 100)
        if color_positions and i in color_positions['swap']:
            color = (100, 255, 100)
        if color_positions and i in color_positions['other']:
            color = (0, 0, 153)
        if color_positions and i in color_positions['sorted']:
            color = (255, 102, 0)
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - val, bar_width - 2, val))
    pygame.display.flip()


def bubble_sort_visualize(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_array(array, {'compare': [j, j + 1], 'swap': [], 'other': [], 'sorted': []})
            pygame.time.wait(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_array(array, {'compare': [], 'swap': [j, j + 1], 'other': [], 'sorted': []})
                pygame.time.wait(50)
        draw_array(array)

def selection_sort_visualize(array):
    n = len(array)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            draw_array(array, {'compare': [i, j], 'swap': [], 'other': [], 'sorted': []})
            pygame.time.wait(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_array(array, {'compare': [], 'swap': [i, min_idx], 'other': [], 'sorted': []})
        pygame.time.wait(50)
        draw_array(array)

def option():
    buttons = {
        'Exit': pygame.Rect(550, 50, 200, 50),
        'Reset': pygame.Rect(300, 50, 200, 50),
        'Start': pygame.Rect(50, 50, 200, 50)
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 30, rect.y + 15))
        
    pygame.display.flip()
    return buttons

def main(screen, choice):
    screen.fill((200, 200, 250))
    running = True
    array = make_array()
    draw_array(array)
    buttons = option()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for name, rect in buttons.items():
                        if rect.collidepoint(pos):
                            if name == "Exit":
                                running = False
                            elif name == "Reset":
                                screen.fill((200, 200, 250))
                                buttons = option()
                                array = make_array()
                                draw_array(array)
                            elif name == "Start":
                                choice(array)

def run(screen):
    font = pygame.font.SysFont(None, 28)
    
    menu_items = [
    "Bubble Sort Visualization (press enter)",
    "Selection Sort Visualization (press enter)",
    "Merge Sort Visualization (press enter)",
    "Back"
    ]

    selected = 0
    running = True
    while running:
        screen.fill((220, 220, 220))
        for i, item in enumerate(menu_items):
            color = (255, 0, 0) if i == selected else (0, 0, 0)
            text = font.render(item, True, color)
            screen.blit(text, (100, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    choice = menu_items[selected]
                    if choice == "Bubble Sort Visualization (press enter)":
                        main(screen, bubble_sort_visualize)
                    elif choice == "Selection Sort Visualization (press enter)":
                        main(screen, selection_sort_visualize)
                    elif choice == "Merge Sort Visualization (press enter)":
                        merge_sort.main()
                    elif choice == "Back":
                        running = False
        clock.tick(30)