import pygame
import sys
from .stack import Stack
from .queue import Queue 

#Bug Fixing
print("Correct File, S,Q")

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20
START_X_Q = 20  # Added so the queue does not start in the middle of the box, but on the left side


# Visualiser for the Stack
def stack_visualiser(screen, font):
    stack = Stack()
    counter = 1
    running = True

    falling_item = None # Added for Animation requirements
    fall_y = 0  # Added for Animation requirements

    push_btn = pygame.Rect(30, 500, 200, 50)
    pop_btn = pygame.Rect(60, 500, 200, 50)
    quit_btn = pygame.Rect(90, 500, 200, 50)
            
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                    
                if push_btn.collidepoint(mouse):
                    falling_item = counter
                    fall_y = -100 
                    counter += 1
                    
                elif pop_btn.collidepoint(mouse) and not stack.is_empty():
                    stack.pop()
                
                elif quit_btn.collidepoint(mouse):
                    running = False
            
        if falling_item is not None:
            fall_y += 10

            if fall_y > BASE_Y - len(stack._data) * (BLOCK_HEIGHT + 5):
                stack.push(falling_item)
                falling_item = None

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
            pygame.draw.rect(screen, (255, 200,0), rect)

            text = font.render(str(falling_item), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        info_text = font.render("SPACE: Push, BACKSPACE: Pop, ESC: Return to menu", True, (200, 200, 200))
        screen.blit(info_text, (10, 10))
        
        
        
        pygame.display.flip()
        clock.tick(30)

# Visualiser for the Queue
def queue_visualiser(screen, font):
    queue = Queue()
    counter = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    queue.enqueue(counter)
                    counter += 1
                
                elif event.key == pygame.K_BACKSPACE and not queue.is_empty():
                    queue.dequeue()
                
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((50, 50, 50))
        for i, val in enumerate(queue._data):
            rect = pygame.Rect(START_X_Q + i * (BLOCK_WIDTH + 5),
                                BASE_Y ,
                                BLOCK_WIDTH,
                                BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        info_text = font.render("SPACE: Enqueue, BACKSPACE: Dequeue, ESC: Return to menu", True, (200, 200, 200))
        screen.blit(info_text, (10, 10))
        
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
