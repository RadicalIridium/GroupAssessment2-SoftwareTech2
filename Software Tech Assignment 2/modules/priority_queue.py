import pygame
import sys

import random
import math

pygame.init()

#Colors
BACKGROUND_COLOR = (200, 200, 250)
ITEM_COLOR = (100, 150, 250)

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
    screen.fill((BACKGROUND_COLOR))
    option()
    if not heap:
        text = FONT.render("Queue is empty", True, (0, 0, 0))
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
        if len(str(val)) == 3:
            value = str(val)
            txt = value[:1] + ":" + value[1:]
        else:
            value = str(val)
            txt = value[:2] + ":" + value[2:]
        color = (ITEM_COLOR)
        if i in highlight_indices:
            color = (255, 100, 100)
        pygame.draw.circle(screen, color, node_positions[i], 20)
        text = FONT.render(txt, True, (0, 0, 0))
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


def details(val):
    if val != None and val in events:
        if len(str(val)) == 3:
            value = str(val)
            txt4 = value[:1] + ":" + value[1:]
        else:
            value = str(val)
            txt4 = value[:2] + ":" + value[2:]
        txt1 = f"Time: {txt4}"
        txt = f"Event Description: {events[val]}"
        text = FONT.render(txt, True, (0, 0, 0))
        text1 = FONT.render(txt1, True, (0, 0, 0))
        screen.blit(text, (160, HEIGHT // 2))
        screen.blit(text1, (160, HEIGHT // 2 - 40))
        pygame.display.flip()
    else:
        return

def extract_min(heap):
    if len(heap) == 0:
        return None
    root = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    details(root)
    pygame.time.wait(5000)
    screen.fill((BACKGROUND_COLOR))
    option()
    draw_heap(heap, [0])
    pygame.time.wait(300)
    heapify_down(heap, 0)
    return root

def option():
    buttons = {
        'Exit': pygame.Rect(550, 530, 200, 50),
        'Pop': pygame.Rect(50, 530, 200, 50),
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 30, rect.y + 15))

    pygame.display.flip()
    return buttons

events = {
    730: "Start of the day",
    815: "Early morning delivery",
    920: "Meeting with friends",
    1000: "Appointment",
    1145: "Lunch break"}

times = [730, 815, 920, 1000, 1145]

def main():
    screen.fill((BACKGROUND_COLOR))
    running = True
    insertions = [i for i in times]
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
                            elif name == "Pop":
                                extract_min(heap)