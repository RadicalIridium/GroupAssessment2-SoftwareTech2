#(Code based on https://www.geeksforgeeks.org/dsa/sorting-algorithm-visualization-merge-sort/)

import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting")
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()


ARRAY_SIZE = 31
arr_clr =[(0, 204, 102)]*ARRAY_SIZE
clr_ind = 0
clr =[(0, 204, 102), (255, 0, 0), (0, 0, 153), (255, 102, 0)]
array = [0] * ARRAY_SIZE

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
    
def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)

def make_array(size):
    for i in range(1, ARRAY_SIZE):
        arr_clr[i]= clr[0]
        array[i]= random.randrange(100, 350)
    return array

array = make_array(ARRAY_SIZE)

def refill():
    screen.fill((30, 30, 30))
    draw()
    pygame.display.update()
    pygame.time.delay(20)


def mergesort(array, l, r):
    mid =(l + r)//2
    if l<r:
        mergesort(array, l, mid)
        mergesort(array, mid + 1, r)
        merge(array, l, mid,
            mid + 1, r)
def merge(array, x1, y1, x2, y2):
    i = x1
    j = x2
    temp =[]
    pygame.event.pump() 
    while i<= y1 and j<= y2:
        arr_clr[i]= clr[1]
        arr_clr[j]= clr[1]
        refill()
        arr_clr[i]= clr[0]
        arr_clr[j]= clr[0]
        if array[i]<array[j]:
                temp.append(array[i])
                i+= 1
        else:
                temp.append(array[j])
                j+= 1
    while i<= y1:
        arr_clr[i]= clr[1]
        refill()
        arr_clr[i]= clr[0]
        temp.append(array[i])
        i+= 1
    while j<= y2:
        arr_clr[j]= clr[1]
        refill()
        arr_clr[j]= clr[0]
        temp.append(array[j])
        j+= 1
    j = 0    
    for i in range(x1, y2 + 1): 
        pygame.event.pump() 
        array[i]= temp[j]
        j+= 1
        arr_clr[i]= clr[2]
        refill()
        if y2-x1 == len(array)-2:
            arr_clr[i]= clr[3]
        else: 
            arr_clr[i]= clr[0]

def draw():
    width = WIDTH - 50
    option()
    element_width =(width -(ARRAY_SIZE - 1))// (ARRAY_SIZE)
    boundry_arr = width / (ARRAY_SIZE - 1)

    # Drawing the array values as lines
    for i in range(1, ARRAY_SIZE):
        pygame.draw.line(screen, arr_clr[i], (boundry_arr * i, 200), (boundry_arr * i, array[i] + 100),\
            element_width)
    pygame.display.flip()

def main():
    screen.fill((30, 30, 30))
    running = True
    buttons = option()
    array = make_array(ARRAY_SIZE)
    draw()
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
                                screen.fill((30, 30, 30))
                                buttons = option()
                                array = make_array(ARRAY_SIZE)
                                draw()
                            elif name == "Start":
                                 mergesort(array, 1, len(array) - 1)