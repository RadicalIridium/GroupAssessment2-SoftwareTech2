import pygame
import sys

import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphs")
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)

heap = [] # min-heap implemented as list

def draw_heap(heap, highlight_indices=[]):
    screen.fill((255, 255, 255))
    option()
    if not heap:
        text = FONT.render("Heap is empty", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.flip()
        return
    
    levels = int(math.log2(len(heap))) + 1
    max_nodes = 2 ** levels - 1
    node_positions = []

    for i in range(len(heap)):
        level = int(math.floor(math.log2(i + 1)))
        index_in_level = i - (2 ** level - 1)
        gap = WIDTH // (2 ** level + 1)
        x = gap * (index_in_level + 1)
        y = 60 + level * 70
        node_positions.append((x, y))
    
    # Draw edges
    for i in range(len(heap)):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap):
            pygame.draw.line(screen, (0, 0, 0), node_positions[i], node_positions[left], 2)
        if right < len(heap):
            pygame.draw.line(screen, (0, 0, 0), node_positions[i], node_positions[right], 2)

        # Draw nodes
    for i, val in enumerate(heap):
        color = (100, 200, 250)
        if i in highlight_indices:
            color = (255, 100, 100)
        pygame.draw.circle(screen, color, node_positions[i], 20)
        text = FONT.render(str(val), True, (0, 0, 0))
        text_rect = text.get_rect(center=node_positions[i])
        screen.blit(text, text_rect)
    pygame.display.flip()


def heapify_up(heap, index):
    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] > heap[index]:
            heap[parent], heap[index] = heap[index], heap[parent]
            draw_heap(heap, [parent, index])
            pygame.time.wait(400)
            index = parent
        else:
            break


def heapify_down(heap, index):
    n = len(heap)
    while True:
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right
        if smallest != index:
            heap[index], heap[smallest] = heap[smallest], heap[index]
            draw_heap(heap, [index, smallest])
            pygame.time.wait(400)
            index = smallest
        else:
            break


def insert(heap, val):
    heap.append(val)
    draw_heap(heap, [len(heap) - 1])
    pygame.time.wait(300)
    heapify_up(heap, len(heap) - 1)


def delete(heap, val):
    heap.remove(val)
    draw_heap(heap, [0])
    pygame.time.wait(300)
    heapify_down(heap, 0)

def extract_min(heap):
    if len(heap) == 0:
        return None
    root = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    draw_heap(heap, [0])
    pygame.time.wait(300)
    heapify_down(heap, 0)
    return root


def option():
    buttons = {
        'Exit': pygame.Rect(550, 530, 200, 50),
        'Insert': pygame.Rect(50, 530, 200, 50),
        'Delete': pygame.Rect(300, 530, 200, 50),
        'value_box': pygame.Rect(50, 480, 80, 30),
    }

    for text, rect in buttons.items():
        if text != 'value_box':
            pygame.draw.rect(screen, (150, 150, 200), rect)
            draw_text(text, (rect.x + 30, rect.y + 15))
        else:
            pygame.draw.rect(screen, (100, 100, 100), rect)
            draw_text('Value', (rect.x, rect.y - 16))

    pygame.display.flip()
    return buttons


def input(rect, mode):
    value_text = ""
    value_box = rect
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if rect.collidepoint(pos):
                        mode = True
                    else:
                        mode = False
            elif event.type == pygame.KEYDOWN and mode == True:
                if event.key == pygame.K_BACKSPACE:
                    value_text = value_text[:-1]
                elif event.unicode.isdigit() and len(value_text) < 4:
                    value_text += event.unicode
                if event.key == pygame.K_END:
                    mode = False
            elif mode == False:
                running = False
    
        for box, text in [
                (value_box,  value_text),
            ]:
                pygame.draw.rect(screen, (100, 100, 100), box)
                screen.blit(FONT.render(text,  True, (0,0,0)), (box.x + 5, box.y + 8))
                screen.blit(FONT.render('Value', True, (0,0,0)), (box.x, box.y - 16))
 
        pygame.display.flip()
        clock.tick(30)
    return value_text

def main():
    screen.fill((200, 200, 250))
    running = True
    insertions = [random.randint(1, 100) for _ in range(10)]
    idx = 0
    buttons = option()
    draw_heap(heap)
    value = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            if idx < len(insertions):
                insert(heap, insertions[idx])
                idx += 1
                pygame.time.wait(600)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for name, rect in buttons.items():
                        if rect.collidepoint(pos):
                            if name == "Exit":
                                running = False
                            elif name == "Insert":
                                if value != None:
                                    if value not in heap:
                                        insert(heap, value)
                                        value = None
                                    else:
                                        draw_text("enter vaild value",(135, 490, 80, 30))
                                    pygame.display.flip()
                            elif name == "Delete":
                               if value != None:
                                    if value in heap:
                                        delete(heap, value)
                                        value = None
                                    else:
                                        draw_text("enter vaild value",(135, 490, 80, 30))
                                    pygame.display.flip()
                            elif name == 'value_box':
                                active_input = True
                                txt = input(buttons['value_box'], active_input)
                                try:
                                    value = int(txt)
                                except:
                                    pass
                                else:
                                    value = int(txt)