import pygame
import sys
from .stack import Stack
from .queue import Queue 

#Bug Fixing
print("Correct File, S,Q")
"""
To-do
* Decide Colour and style for all games
"""

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 150
START_X_Q = 20  # Added so the queue does not start in the middle of the box, but on the left side


# Visualiser for the Stack
def stack_visualiser(screen, font):
    stack = Stack()
    counter = 1
    running = True

    #Buttons
    push_btn = pygame.Rect(30, 500, 120, 50)
    pop_btn = pygame.Rect(160, 500, 120, 50)
    quit_btn = pygame.Rect(290, 500, 120, 50)
    
    #Animations
    falling_item = None 
    fall_y = 0 

    popped_item = None
    popped_y = 0    


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                    
                if push_btn.collidepoint(mouse) and falling_item is None and popped_item is None:
                    falling_item = counter
                    fall_y = -100 
                    counter += 1
                    
                elif pop_btn.collidepoint(mouse) and not stack.is_empty() and popped_item is None and falling_item is None:
                    popped_item = stack.peek()

                    popped_y = BASE_Y - (len(stack._data) - 1) * (BLOCK_HEIGHT + 5)

                    stack.pop()
                
                elif quit_btn.collidepoint(mouse):
                    running = False
            
        if falling_item is not None:
            fall_y += 15

            if fall_y > BASE_Y - len(stack._data) * (BLOCK_HEIGHT + 5):
                stack.push(falling_item)
                falling_item = None

        if popped_item is not None:
            popped_y -= 20

            if popped_y < -100:
                popped_item = None

        screen.fill((50, 50, 50))

        for i, val in enumerate(stack._data):
            rect = pygame.Rect(START_X,
                               BASE_Y - i * (BLOCK_HEIGHT + 5),
                               BLOCK_WIDTH,
                               BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            
        if falling_item is not None:
            rect = pygame.Rect(START_X, fall_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = font.render(str(falling_item), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if popped_item is not None:
            rect = pygame.Rect(START_X, popped_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (255, 0, 0), rect)

            text = font.render(str(popped_item), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))


        pygame.draw.rect(screen, (0, 200, 0), push_btn)
        pygame.draw.rect(screen, (200, 0, 0), pop_btn)
        pygame.draw.rect(screen, (100, 100, 100), quit_btn)

        screen.blit(font.render("PUSH", True, (255, 255, 255)),
            (push_btn.x + 20, push_btn.y + 10))

        screen.blit(font.render("POP", True, (255, 255, 255)),
            (pop_btn.x + 30, pop_btn.y + 10))

        screen.blit(font.render("QUIT", True, (255, 255, 255)),
            (quit_btn.x + 25, quit_btn.y + 10))
                
        
        pygame.display.flip()
        clock.tick(30)

# Visualiser for the Queue
def queue_visualiser(screen, font):
    queue = Queue()
    counter = 1
    running = True

    #Buttons 
    enqueue_btn = pygame.Rect(30, 500, 120, 50)
    dequeue_btn = pygame.Rect(160, 500, 120, 50)
    quit_btn = pygame.Rect(290, 500, 120, 50)
    
    #Animations
    slide_on_item = None
    slide_on_x = WIDTH

    slide_off_item = None
    slide_off_x = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                if enqueue_btn.collidepoint(mouse) and slide_on_item is None and slide_off_item is None:
                    slide_on_item = counter
                    slide_on_x = WIDTH
                    counter += 1
                
                elif dequeue_btn.collidepoint(mouse) and not queue.is_empty() and slide_off_item is None and slide_on_item is None:
                    slide_off_item = queue.peek()
                    slide_off_x = START_X_Q 
                
                elif quit_btn.collidepoint(mouse):
                    running = False

        if slide_on_item is not None:
            slide_on_x -= 15

            if slide_on_x <= START_X_Q + len(queue._data) * (BLOCK_WIDTH + 5):
                queue.enqueue(slide_on_item)
                slide_on_item = None

        if slide_off_item is not None:
            slide_off_x -= 10

            if slide_off_x < - 100:
                queue.dequeue()
                slide_off_item = None

        screen.fill((50, 50, 50))
        for i, val in enumerate(queue._data):
            if slide_off_item is not None and i == 0:
                continue

            rect = pygame.Rect(START_X_Q + i * (BLOCK_WIDTH + 5),
                                BASE_Y ,
                                BLOCK_WIDTH,
                                BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if slide_on_item is not None:
            rect = pygame.Rect(slide_on_x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = font.render(str(slide_on_item), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if slide_off_item is not None:
            rect = pygame.Rect(slide_off_x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (255, 0, 0), rect)

            text = font.render(str(slide_off_item), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        pygame.draw.rect(screen, (0, 200, 0), enqueue_btn)
        pygame.draw.rect(screen, (200, 0, 0), dequeue_btn)
        pygame.draw.rect(screen, (100, 100, 100), quit_btn)

        screen.blit(font.render("Enqueue", True, (255, 255, 255)),
            (enqueue_btn.x + 20, enqueue_btn.y + 10))

        screen.blit(font.render("Dequeue", True, (255, 255, 255)),
            (dequeue_btn.x + 30, dequeue_btn.y + 10))

        screen.blit(font.render("QUIT", True, (255, 255, 255)),
            (quit_btn.x + 25, quit_btn.y + 10))
        
        pygame.display.flip()
        clock.tick(30)

def run(screen):
    font = pygame.font.SysFont(None, 28)
    
    menu_items = [
    "Stack Visualization (press enter)", #Unfinished
    "Queue Visualization (press enter)", #Unfinished
    "Linked List Visualization (not implemented)",
    "BST Visualization (not implemented)",
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
                    if choice == "Stack Visualization (press enter)":
                        stack_visualiser(screen, font)
                    elif choice == "Queue Visualization (press enter)":
                        queue_visualiser(screen, font)
                    
                    elif choice == "Back":
                        running = False
        clock.tick(30)
