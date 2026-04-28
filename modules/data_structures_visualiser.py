import time

import pygame
import sys
import random
from .stack import Stack
from .queue import Queue 
from .bst import BinaryTree
from .linked_list import LinkedList

#Bug Fixing
print("Correct File, S,Q")

# Constants and Global Variables
WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 150
START_X_2 = 20  # Added so the queue does not start in the middle of the box, but on the left side
NODE_W = 60
NODE_H = 40
NODE_GAP = 40
NODE_Y = 250
DROP_START_Y = 80 

# Colors
BACKGROUND_COLOR = (200, 200, 250)
ITEM_COLOR = (100, 150, 250)

HIGHLIGHT_COLOR_GREEN = (0, 140, 0)
HIGHLIGHT_COLOR_RED = (255, 0, 0)
HIGHLIGHT_COLOR_BLUE = (100, 100, 250)

BUTTON_COLOR_GREEN = (0, 140, 0)
BUTTON_COLOR_RED = (160, 0, 0)
BUTTON_COLOR_GREY = (100, 100, 100)
BUTTON_COLOR_BLUE = (0, 90, 120)

TEXT_COLOR_1 = (0, 0, 0)
TEXT_COLOR_2 = (255, 255, 255)

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

        screen.fill((BACKGROUND_COLOR))

        for i, val in enumerate(stack._data):
            rect = pygame.Rect(START_X,
                               BASE_Y - i * (BLOCK_HEIGHT + 5),
                               BLOCK_WIDTH,
                               BLOCK_HEIGHT)
            pygame.draw.rect(screen, (ITEM_COLOR), rect)

            text = font.render(str(val), True, (TEXT_COLOR_1))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            
        if falling_item is not None:
            rect = pygame.Rect(START_X, fall_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (ITEM_COLOR), rect)

            text = font.render(str(falling_item), True, (TEXT_COLOR_1))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if popped_item is not None:
            rect = pygame.Rect(START_X, popped_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (255, 0, 0), rect)

            text = font.render(str(popped_item), True, (TEXT_COLOR_1))
            screen.blit(text, text.get_rect(center=rect.center))


        pygame.draw.rect(screen, (0, 140, 0), push_btn)
        pygame.draw.rect(screen, (160, 0, 0), pop_btn)
        pygame.draw.rect(screen, (100, 100, 100), quit_btn)

        screen.blit(font.render("PUSH", True, (TEXT_COLOR_2)),
            (push_btn.x + 20, push_btn.y + 10))

        screen.blit(font.render("POP", True, (TEXT_COLOR_2)),
            (pop_btn.x + 30, pop_btn.y + 10))

        screen.blit(font.render("QUIT", True, (TEXT_COLOR_2)),
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
                    slide_off_x = START_X_2 
                
                elif quit_btn.collidepoint(mouse):
                    running = False

        if slide_on_item is not None:
            slide_on_x -= 15

            if slide_on_x <= START_X_2 + len(queue._data) * (BLOCK_WIDTH + 5):
                queue.enqueue(slide_on_item)
                slide_on_item = None

        if slide_off_item is not None:
            slide_off_x -= 10

            if slide_off_x < - 100:
                queue.dequeue()
                slide_off_item = None

        screen.fill((BACKGROUND_COLOR))
        for i, val in enumerate(queue._data):
            if slide_off_item is not None and i == 0:
                continue

            rect = pygame.Rect(START_X_2 + i * (BLOCK_WIDTH + 5),
                                BASE_Y ,
                                BLOCK_WIDTH,
                                BLOCK_HEIGHT)
            pygame.draw.rect(screen, (ITEM_COLOR), rect)
            text = font.render(str(val), True, (TEXT_COLOR_1))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if slide_on_item is not None:
            rect = pygame.Rect(slide_on_x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)

            text = font.render(str(slide_on_item), True, (TEXT_COLOR_1))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        if slide_off_item is not None:
            rect = pygame.Rect(slide_off_x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (HIGHLIGHT_COLOR_RED), rect)

            text = font.render(str(slide_off_item), True, (TEXT_COLOR_1))
            screen.blit(text, text.get_rect(center=rect.center))

        pygame.draw.rect(screen, (BUTTON_COLOR_GREEN), enqueue_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_RED), dequeue_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_GREY), quit_btn)

        screen.blit(font.render("Enqueue", True, (TEXT_COLOR_2)),
            (enqueue_btn.x + 20, enqueue_btn.y + 10))

        screen.blit(font.render("Dequeue", True, (TEXT_COLOR_2)),
            (dequeue_btn.x + 30, dequeue_btn.y + 10))

        screen.blit(font.render("QUIT", True, (TEXT_COLOR_2)),
            (quit_btn.x + 25, quit_btn.y + 10))
        
        pygame.display.flip()
        clock.tick(30)


# Helper function to draw the linked list,
def draw_linked_list(screen, font, nodes, highlight=None, highlight_colour=HIGHLIGHT_COLOR_GREEN,
                    delete_highlight=None, drop_val=None, drop_x=None, drop_y=None):
 
    for i, node in enumerate(nodes):
        if node == delete_highlight:
            color = HIGHLIGHT_COLOR_RED
        elif node == highlight:
            color = highlight_colour
        else:
            color = ITEM_COLOR
 
        rect = pygame.Rect(START_X_2 + i * (NODE_W + NODE_GAP), NODE_Y - NODE_H // 2, NODE_W, NODE_H)
        pygame.draw.rect(screen, color, rect)
        text = font.render(str(node.value), True, TEXT_COLOR_1)
        screen.blit(text, text.get_rect(center=rect.center))
 
        # Arrow to next node
        if i < len(nodes) - 1:
            next_x = START_X_2 + (i + 1) * (NODE_W + NODE_GAP)
            pygame.draw.line(screen, TEXT_COLOR_1, (rect.right + 2, NODE_Y), (next_x - 2, NODE_Y), 2)
            pygame.draw.polygon(screen, TEXT_COLOR_1, [
                (next_x - 2, NODE_Y),
                (next_x - 10, NODE_Y - 5),
                (next_x - 10, NODE_Y + 5),
            ])

    # NULL label after last node
    if nodes:
        null_x    = START_X_2 + len(nodes) * (NODE_W + NODE_GAP)
        null_rect = pygame.Rect(null_x, NODE_Y - NODE_H // 2, 45, NODE_H)
        last_rect_right = START_X_2 + (len(nodes) - 1) * (NODE_W + NODE_GAP) + NODE_W
        pygame.draw.line(screen, TEXT_COLOR_1, (last_rect_right + 2, NODE_Y), (null_x - 2, NODE_Y), 2)
        pygame.draw.polygon(screen, TEXT_COLOR_1, [
            (null_x - 2, NODE_Y),
            (null_x - 10, NODE_Y - 5),
            (null_x - 10, NODE_Y + 5),
        ])
        pygame.draw.rect(screen, BUTTON_COLOR_GREY, null_rect)
        screen.blit(font.render("NULL", True, TEXT_COLOR_2), (null_rect.x + 2, null_rect.y + 10))
    else:
        screen.blit(font.render("(empty)", True, TEXT_COLOR_1), (START_X_2, NODE_Y - 10))
 
    # Dropping node (insert animation)
    if drop_val is not None:
        drop_rect = pygame.Rect(drop_x, drop_y - NODE_H // 2, NODE_W, NODE_H)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR_GREEN, drop_rect)
        text = font.render(str(drop_val), True, TEXT_COLOR_1)
        screen.blit(text, text.get_rect(center=drop_rect.center))

# Visualiser for the linked list
def linked_list_visualiser(screen, font):
    ll = LinkedList()
    running = True
 
    for v in [10, 20, 30]:
        ll.insert(v, ll.length())
 
    # Buttons
    insert_btn  = pygame.Rect(30,  500, 110, 45)
    delete_btn  = pygame.Rect(150, 500, 110, 45)
    reverse_btn = pygame.Rect(270, 500, 110, 45)
    quit_btn    = pygame.Rect(390, 500, 110, 45)
 
    # Input boxes
    value_box  = pygame.Rect(30,  555, 80, 30)
    index_box  = pygame.Rect(120, 555, 80, 30)
    delete_box = pygame.Rect(270, 555, 80, 30)
 
    value_text  = ""
    index_text  = ""
    delete_text = ""
    active_input = None  # "value" | "index" | "delete" | None
 
    # Animation
    anim_phase = ""   # "insert_traverse"|"insert_drop"|"delete_search"|"delete_remove"|"reverse"
    anim_timer = 0
    anim_delay = 18
 
    # Insert
    ins_val    = None
    ins_index  = None
    ins_path   = []
    ins_path_i = 0
    ins_drop_y = 0.0
 
    # Delete
    del_val    = None
    del_path   = []
    del_path_i = 0
    del_node   = None
    del_hold   = 0
 
    # Reverse
    rev_steps  = []
    rev_step_i = 0
    rev_prev   = None
    rev_curr   = None
    rev_next   = None
 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
 
                if value_box.collidepoint(mouse):
                    active_input = "value"
                elif index_box.collidepoint(mouse):
                    active_input = "index"
                elif delete_box.collidepoint(mouse):
                    active_input = "delete"
                else:
                    active_input = None
 
                if anim_phase == "":
                    if insert_btn.collidepoint(mouse) and value_text.isdigit() and index_text.isdigit():
                        ins_val    = int(value_text)
                        ins_index  = int(index_text)
                        ins_path   = ll.find_insert_traverse_path(ins_index)
                        ins_path_i = 0
                        ins_drop_y = 80.0
                        value_text = ""
                        index_text = ""
                        anim_phase = "insert_traverse" if ins_path else "insert_drop"
 
                    elif delete_btn.collidepoint(mouse) and delete_text.isdigit():
                        del_val     = int(delete_text)
                        del_path    = ll.find_search_path(del_val)
                        del_path_i  = 0
                        del_node    = None
                        del_hold    = 0
                        delete_text = ""
                        anim_phase  = "delete_search"
 
                    elif reverse_btn.collidepoint(mouse) and not ll.length() == 0:
                        rev_steps  = ll.get_reverse_steps()
                        rev_step_i = 0
                        if rev_steps:
                            rev_prev, rev_curr, rev_next = rev_steps[0]
                        anim_phase = "reverse"
 
                if quit_btn.collidepoint(mouse):
                    running = False
 
            elif event.type == pygame.KEYDOWN and active_input:
                if active_input == "value":
                    if event.key == pygame.K_BACKSPACE:
                        value_text = value_text[:-1]
                    elif event.unicode.isdigit() and len(value_text) < 4:
                        value_text += event.unicode
                elif active_input == "index":
                    if event.key == pygame.K_BACKSPACE:
                        index_text = index_text[:-1]
                    elif event.unicode.isdigit() and len(index_text) < 3:
                        index_text += event.unicode
                elif active_input == "delete":
                    if event.key == pygame.K_BACKSPACE:
                        delete_text = delete_text[:-1]
                    elif event.unicode.isdigit() and len(delete_text) < 4:
                        delete_text += event.unicode
 
        # Animation logic
        highlight        = None
        highlight_colour = HIGHLIGHT_COLOR_GREEN
        delete_highlight = None
        drop_val = drop_x = drop_y = None
 
        anim_timer += 1
        stepped = anim_timer >= anim_delay
 
        if anim_phase == "insert_traverse":
            if ins_path_i < len(ins_path):
                highlight = ins_path[ins_path_i]
            if stepped:
                anim_timer = 0
                ins_path_i += 1
                if ins_path_i >= len(ins_path):
                    anim_phase = "insert_drop"
 
        elif anim_phase == "insert_drop":
            ins_drop_y += 8
            drop_val   = ins_val
            drop_x     = START_X_2 + min(ins_index, ll.length()) * (NODE_W + NODE_GAP)
            drop_y     = int(ins_drop_y)
            if ins_drop_y >= NODE_Y:
                ll.insert(ins_val, ins_index)
                anim_phase = ""
                anim_timer = 0
 
        elif anim_phase == "delete_search":
            if del_path_i < len(del_path):
                highlight = del_path[del_path_i]
            if stepped:
                anim_timer = 0
                del_path_i += 1
                if del_path_i >= len(del_path):
                    del_node   = ll.find_by_value(del_val)
                    anim_phase = "delete_remove" if del_node else ""
 
        elif anim_phase == "delete_remove":
            delete_highlight = del_node
            del_hold += 1
            if del_hold >= 40:
                ll.delete_by_value(del_val)
                del_node   = None
                del_hold   = 0
                anim_phase = ""
                anim_timer = 0
 
        elif anim_phase == "reverse":
            # green=prev, blue=next, red=curr (reusing delete_highlight for red)
            highlight        = rev_prev
            highlight_colour = HIGHLIGHT_COLOR_GREEN
            delete_highlight = rev_curr
            if rev_next:
                # draw next in blue by temporarily overriding — handled in draw via second highlight
                pass
            if stepped:
                anim_timer = 0
                rev_step_i += 1
                if rev_step_i < len(rev_steps):
                    rev_prev, rev_curr, rev_next = rev_steps[rev_step_i]
                else:
                    ll.reverse()
                    anim_phase = ""
 
        # Render
        screen.fill(BACKGROUND_COLOR)
 
        draw_linked_list(screen, font, ll.to_nodes(),
                         highlight=highlight,
                         highlight_colour=highlight_colour,
                         delete_highlight=delete_highlight,
                         drop_val=drop_val, drop_x=drop_x, drop_y=drop_y)
 
        pygame.draw.rect(screen, BUTTON_COLOR_GREEN, insert_btn)
        pygame.draw.rect(screen, BUTTON_COLOR_RED,   delete_btn)
        pygame.draw.rect(screen, BUTTON_COLOR_BLUE,  reverse_btn)
        pygame.draw.rect(screen, BUTTON_COLOR_GREY,  quit_btn)
 
        screen.blit(font.render("Insert",  True, TEXT_COLOR_2), (insert_btn.x  + 20, insert_btn.y  + 10))
        screen.blit(font.render("Delete",  True, TEXT_COLOR_2), (delete_btn.x  + 20, delete_btn.y  + 10))
        screen.blit(font.render("Reverse", True, TEXT_COLOR_2), (reverse_btn.x + 10, reverse_btn.y + 10))
        screen.blit(font.render("QUIT",    True, TEXT_COLOR_2), (quit_btn.x    + 25, quit_btn.y    + 10))
 
        for box, text, label, key in [
            (value_box,  value_text,  "Value",   "value"),
            (index_box,  index_text,  "Index",   "index"),
            (delete_box, delete_text, "Del val", "delete"),
        ]:
            pygame.draw.rect(screen, (255, 255, 255) if active_input == key else (180, 180, 180), box)
            screen.blit(font.render(text,  True, TEXT_COLOR_1), (box.x + 5, box.y + 8))
            screen.blit(font.render(label, True, TEXT_COLOR_1), (box.x, box.y - 16))
 
        pygame.display.flip()
        clock.tick(30)



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
    text = font.render(str(node.value), True, (TEXT_COLOR_1))
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
        

        screen.fill((BACKGROUND_COLOR))

        active_highlight = traversal_current if traversal_active else current
        highlight_colour = (ITEM_COLOR) if traversal_active else (0, 140, 0)
        draw_tree(screen, tree.root, WIDTH // 2, 80, 200, font, active_highlight, highlight_colour,
                  tree.search(delete_target) if delete_target else None)

        pygame.draw.rect(screen, (BUTTON_COLOR_GREEN), insert_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_RED), delete_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_GREY), quit_btn)

        pygame.draw.rect(screen, (BUTTON_COLOR_BLUE), inorder_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_BLUE), preorder_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_BLUE), postorder_btn)

        screen.blit(font.render("Insert", True, (TEXT_COLOR_2)),
                    (insert_btn.x + 20, insert_btn.y + 10))

        screen.blit(font.render("Delete", True, (TEXT_COLOR_2)),
                    (delete_btn.x + 20, delete_btn.y + 10))

        screen.blit(font.render("QUIT", True, (TEXT_COLOR_2)),
                    (quit_btn.x + 25, quit_btn.y + 10))
        
        screen.blit(font.render("In", True, (TEXT_COLOR_2)),
                    (inorder_btn.x + 20, inorder_btn.y + 10))
        screen.blit(font.render("Pre", True, (TEXT_COLOR_2)),
                    (preorder_btn.x + 20, preorder_btn.y + 10))
        screen.blit(font.render("Post", True, (TEXT_COLOR_2)),
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
    "Linked List Visualization (press enter)", #Unfinished
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
