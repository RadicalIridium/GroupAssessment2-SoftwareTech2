import pygame
import sys
import random
from .stack import Stack
from .queue import Queue 
from .bst import BinaryTree

#Bug Fixing
print("Correct File, S,Q")
"""
To-do
* Decide Colour and style for all games
"""
#linked list numbers placeholder
numbers = [5, 3, 9, 1, 7, 4]

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()
cell_width = WIDTH // len(numbers)

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

        screen.fill((200, 200, 250))

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


        pygame.draw.rect(screen, (0, 140, 0), push_btn)
        pygame.draw.rect(screen, (160, 0, 0), pop_btn)
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

        screen.fill((200, 200, 250))
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

        pygame.draw.rect(screen, (0, 140, 0), enqueue_btn)
        pygame.draw.rect(screen, (160, 0, 0), dequeue_btn)
        pygame.draw.rect(screen, (100, 100, 100), quit_btn)

        screen.blit(font.render("Enqueue", True, (255, 255, 255)),
            (enqueue_btn.x + 20, enqueue_btn.y + 10))

        screen.blit(font.render("Dequeue", True, (255, 255, 255)),
            (dequeue_btn.x + 30, dequeue_btn.y + 10))

        screen.blit(font.render("QUIT", True, (255, 255, 255)),
            (quit_btn.x + 25, quit_btn.y + 10))
        
        pygame.display.flip()
        clock.tick(30)


def draw_grid(screen, highlight_index=None):
    screen.fill((30, 30, 30))
    for i, num in enumerate(numbers):
        color = (200, 200, 200)
        if i == highlight_index:
            color = (255, 100, 100)
        rect = pygame.Rect(i * cell_width, 0, cell_width - 2, HEIGHT)
        pygame.draw.rect(screen, color, rect)
        text = FONT.render(str(num), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


# Visualiser for the linked list
def linked_list_visualiser(screen, font):
    pass


# part of the BST visualiser, to draw the tree structure
def draw_tree(screen, node, x, y, spacing, font, highlight=None, highlight_colour=(0, 140, 0), delete_highlight=None):
    if node is None:
        return
    
    if node == delete_highlight:
        color = (200, 0, 0)
    elif node == highlight:
        color = highlight_colour
    else:
        color = (100, 150, 250)

    # Draw node
    pygame.draw.circle(screen, color, (x, y), 25)
    text = font.render(str(node.value), True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(x, y)))

    # Left child
    if node.left:
        child_x = x - spacing
        child_y = y + 80

        pygame.draw.line(screen, (0, 0, 0), (x, y), (child_x, child_y))
        draw_tree(screen, node.left, child_x, child_y, spacing // 2, font, highlight, highlight_colour, delete_highlight)

    # Right child
    if node.right:
        child_x = x + spacing
        child_y = y + 80

        pygame.draw.line(screen, (0, 0, 0), (x, y), (child_x, child_y))
        draw_tree(screen, node.right, child_x, child_y, spacing // 2, font, highlight, highlight_colour, delete_highlight)

# Visualiser for the BST
def bst_visualiser(screen, font):
    tree = BinaryTree()
    counter = 1
    running = True

    #buttons
    insert_btn = pygame.Rect(30, 500, 120, 50)
    delete_btn = pygame.Rect(160, 500, 120, 50)
    quit_btn = pygame.Rect(290, 500, 120, 50)

    inorder_btn = pygame.Rect(545, 500, 60, 50)
    preorder_btn = pygame.Rect(610, 500, 60, 50)
    postorder_btn = pygame.Rect(675, 500, 60, 50)

    # Animation Values
    animating = False
    highlight_path = []
    path_index = 0
    pending_insert = None
    current = None

    anim_delay = 15
    anim_timer = 0

    # Traversal Values
    traversal_path = []
    traversal_index = 0
    traversal_active = False
    traversal_timer = 0
    traversal_delay = 20
    traversal_current = None

    #Text input
    input_text = ""
    input_active = False
    input_box = pygame.Rect(420, 500, 100, 50)

    #Delete Animation
    delete_target = None
    delete_timer = 0
    delete_delay = 40
    
    val = [50, 25, 75] # initial values to create a simple tree for testing, and stops random inserts from creating a very unbalanced tree.
    for v in val:
        tree.insert(v)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if insert_btn.collidepoint(mouse) and not animating:
                    pending_insert = random.randint(1, 100)
                    highlight_path = tree.find_insert_path(pending_insert)
                    path_index = 0
                    current = highlight_path[0] if highlight_path else None
                    animating = True
                        
                elif delete_btn.collidepoint(mouse) and input_text:
                        delete_target = int(input_text) if input_text.isdigit() else None
                        delete_timer = 0
                        input_text = ""

                elif quit_btn.collidepoint(mouse):
                    running = False

                elif inorder_btn.collidepoint(mouse) and not animating and not traversal_active:
                    traversal_path = tree.inorder_nodes()
                    traversal_index = 0
                    traversal_current = traversal_path[0] if traversal_path else None
                    traversal_active = True

                elif preorder_btn.collidepoint(mouse) and not animating and not traversal_active:
                    traversal_path = tree.preorder_nodes()
                    traversal_index = 0
                    traversal_current = traversal_path[0] if traversal_path else None
                    traversal_active = True

                elif postorder_btn.collidepoint(mouse) and not animating and not traversal_active:
                    traversal_path = tree.postorder_nodes()
                    traversal_index = 0
                    traversal_current = traversal_path[0] if traversal_path else None
                    traversal_active = True
                
                elif input_box.collidepoint(mouse):
                    input_active = True
                else:
                    input_active = False

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN and input_text:
                    delete_target = int(input_text) if input_text.isdigit() else None
                    delete_timer = 0
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                     input_text = input_text[:-1]
                else:
                    if len(input_text) < 3 and event.unicode.isdigit():  # max 3 digits (1-100)
                         input_text += event.unicode
 

        if animating:
            anim_timer += 1

            if anim_timer >= anim_delay:
                anim_timer = 0
                path_index += 1

                if path_index < len(highlight_path) and highlight_path[path_index] is not None:
                    current = highlight_path[path_index]
                else:
                    tree.insert(pending_insert)
                    current = None
                    animating = False
                    pending_insert = None

        if traversal_active:
            traversal_timer += 1
            if traversal_timer >= traversal_delay:
                traversal_timer = 0
                traversal_index += 1
                if traversal_index < len(traversal_path):
                    traversal_current = traversal_path[traversal_index]
                else:
                    traversal_active = False
                    traversal_current = None

        if delete_target is not None:
            delete_timer += 1
            if delete_timer >= delete_delay:
                tree.delete(delete_target)
                delete_target = None
                delete_timer = 0
        

        screen.fill((200, 200, 250))

        active_highlight = traversal_current if traversal_active else current
        highlight_colour = (100, 100, 250) if traversal_active else (0, 140, 0)
        draw_tree(screen, tree.root, WIDTH // 2, 80, 200, font, active_highlight, highlight_colour,
                  tree.search(delete_target) if delete_target else None)

        pygame.draw.rect(screen, (0, 140, 0), insert_btn)
        pygame.draw.rect(screen, (160, 0, 0), delete_btn)
        pygame.draw.rect(screen, (100, 100, 100), quit_btn)

        pygame.draw.rect(screen, (0, 90, 120), inorder_btn)
        pygame.draw.rect(screen, (0, 90, 120), preorder_btn)
        pygame.draw.rect(screen, (0, 90, 120), postorder_btn)

        screen.blit(font.render("Insert", True, (255, 255, 255)),
                    (insert_btn.x + 20, insert_btn.y + 10))

        screen.blit(font.render("Delete", True, (255, 255, 255)),
                    (delete_btn.x + 20, delete_btn.y + 10))

        screen.blit(font.render("QUIT", True, (255, 255, 255)),
                    (quit_btn.x + 25, quit_btn.y + 10))
        
        screen.blit(font.render("In", True, (255, 255, 255)),
                    (inorder_btn.x + 20, inorder_btn.y + 10))
        screen.blit(font.render("Pre", True, (255, 255, 255)),
                    (preorder_btn.x + 20, preorder_btn.y + 10))
        screen.blit(font.render("Post", True, (255, 255, 255)),
                    (postorder_btn.x + 20, postorder_btn.y + 10))
        
        input_colour = (255, 255, 255) if input_active else (180, 180, 180)
        pygame.draw.rect(screen, input_colour, input_box)
        screen.blit(font.render(input_text, True, (0, 0, 0)),
                    (input_box.x + 5, input_box.y + 15))

        pygame.display.flip()
        clock.tick(30)


def run(screen):
    font = pygame.font.SysFont(None, 28)
    
    menu_items = [
    "Stack Visualization (press enter)", #Unfinished
    "Queue Visualization (press enter)", #Unfinished
    "Linked List Visualization (not implemented)",
    "BST Visualization (press enter)", #Unfinished
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
                    elif choice == "Linked List Visualization (press enter)":
                        linked_list_visualiser(screen, font)
                    elif choice == "BST Visualization (press enter)":
                        bst_visualiser(screen, font)
                    elif choice == "Back":
                        running = False
        clock.tick(30)
