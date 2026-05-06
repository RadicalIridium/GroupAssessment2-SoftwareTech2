import pygame
import random
import sys
import heapq


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game")
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

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

TEXT_COLOR_1 = (0, 0, 0) # Black
TEXT_COLOR_2 = (255, 255, 255)  # White

# New Color
VISTIED_COLOR = (255, 165, 0)  # Orange 
PATH_COLOR = (255, 205, 50)    # Yellow

# Grid Constants (for pathfinding visualization, and Dynamic Programming visualization)
GRID_SIZE = 8
CELL_SIZE = 60
GRID_OFFSET_X = (WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = (HEIGHT - GRID_SIZE * CELL_SIZE) // 2

grid = [["empty"] * GRID_SIZE for _ in range(GRID_SIZE)]


def get_neighbors(row, col):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and grid[r][c] != "obstacle":
            neighbors.append((r, c))
    return neighbors

def dijkstra(start, end):
    dist = {start: 0}
    prev = {start: None}
    queue = [(0, start[0], start[1])]
    visited_order = [] # To store the order of visited nodes for visualization

    while queue:
        cost, row, col = heapq.heappop(queue)  

        if (row, col) == end:
            break  

        for (r, c) in get_neighbors(row, col):
            new_cost = cost + 1   

            if (r, c) not in dist or new_cost < dist[(r, c)]:
                # found a cheaper way to reach this cell
                dist[(r, c)]      = new_cost
                prev[(r, c)] = (row, col)
                heapq.heappush(queue, (new_cost, r, c))

                if (r, c) != end:
                    visited_order.append((r, c))  # record for animation

    return prev, visited_order

def trace_path(prev, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = prev.get(current)  

    path.reverse()   
    return path

# Helper function to draw the grid (for pathfinding visualization, and Dynamic Programming visualization?)
def draw_grid(screen, font):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell = grid[row][col]
            x = GRID_OFFSET_X + col * CELL_SIZE
            y = GRID_OFFSET_Y + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if cell == "obstacle":
                color = BUTTON_COLOR_BLUE
            elif cell == "start":
                color = BUTTON_COLOR_GREEN
            elif cell == "end":
                color = BUTTON_COLOR_RED
            elif cell == "path":
                color = PATH_COLOR
            elif cell == "visited":
                color = VISTIED_COLOR
            else:
                color = TEXT_COLOR_2

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BUTTON_COLOR_GREY, rect, 1)

            # Draw Numbers and Letters as labels for rows and columns, (Like a chess board)
            if row == 0:
                letter = chr(ord('A') + col)
                text = font.render(letter, True, TEXT_COLOR_1)
                screen.blit(text, (x + CELL_SIZE // 2 - text.get_width() // 2, y - 20))
            
            if col == 0:
                number = str(row + 1)
                text = font.render(number, True, TEXT_COLOR_1)
                screen.blit(text, (x - 20, y + CELL_SIZE // 2 - text.get_height() // 2))


# pathfinding visualise
def pathfinding_visualise(screen, font):
    global grid
    grid = [["empty"] * GRID_SIZE for _ in range(GRID_SIZE)]

    start = None
    end = None
    running = True

    #Buttons 
    start_btn = pygame.Rect(15, 500, 120, 50)
    quit_btn = pygame.Rect(650, 500, 120, 50)

    # Animations
    visited_order = []  
    path = []   
    anim_index = 0    
    anim_timer = 0
    anim_delay = 3    
    anim_phase = ""   

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if start_btn.collidepoint((mouse_x, mouse_y)):
                    if start is not None and end is not None:
                        # reset any previous result
                        for r in range(GRID_SIZE):
                            for c in range(GRID_SIZE):
                                if grid[r][c] in ("visited", "path"):
                                    grid[r][c] = "empty"

                        came_from, visited_order = dijkstra(start, end)
                        path       = trace_path(came_from, end) if end in came_from else []
                        anim_index = 0
                        anim_timer = 0
                        anim_phase = "searching"
                elif quit_btn.collidepoint((mouse_x, mouse_y)):
                    running = False
                else:
                    col = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
                    row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if event.button == 1:
                            if start is None:
                                start = (row, col)
                                grid[row][col] = "start"
                            elif end is None and (row, col) != start:
                                end = (row, col)
                                grid[row][col] = "end"
                            elif (row, col) != start and (row, col) != end:
                                grid[row][col] = "obstacle"
                        elif event.button == 3:
                            if (row, col) == start:
                                start = None
                            elif (row, col) == end:
                                end = None
                            grid[row][col] = "empty"

        anim_timer += 1
        if anim_timer >= anim_delay:
            anim_timer = 0

            if anim_phase == "searching":
                if anim_index < len(visited_order):
                    r, c = visited_order[anim_index]
                    grid[r][c] = "visited"
                    anim_index += 1
                else:
                    anim_phase = "path"
                    anim_index = 0

            elif anim_phase == "path":
                if anim_index < len(path):
                    r, c = path[anim_index]
                    if grid[r][c] not in ("start", "end"):
                        grid[r][c] = "path" 
                    anim_index += 1
                else:
                    anim_phase = "" 

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, font)

        pygame.draw.rect(screen, (BUTTON_COLOR_GREEN), start_btn)
        pygame.draw.rect(screen, (BUTTON_COLOR_GREY), quit_btn)
        
        screen.blit(font.render("Start", True, (TEXT_COLOR_2)),
            (start_btn.x + 20, start_btn.y + 10))

        screen.blit(font.render("QUIT", True, (TEXT_COLOR_2)),
            (quit_btn.x + 25, quit_btn.y + 10))
            
        pygame.display.flip()
        clock.tick(30)

#Helper function to reconstruct path from DP table (for Dynamic Programming visualisation)
def reconstruct_path(dp):
    path = []
    row, col = GRID_SIZE - 1, GRID_SIZE - 1

    if dp[row][col] == 0:
        return []  # no path exists
 
    while (row, col) != (0, 0):
        path.append((row, col))
 
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif dp[row-1][col] == 0:
            col -= 1 
        elif dp[row][col-1] == 0:
            row -= 1  
        elif dp[row-1][col] >= dp[row][col-1]:
            row -= 1
        else:
            col -= 1

    path.append((0, 0))
    path.reverse()
    return path

# Dynamic Programming visualizer
def dynamic_programming_visualiser(screen, font):
    global grid
    grid = [["empty"] * GRID_SIZE for _ in range(GRID_SIZE)]

    dp = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    
    fill_order = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            fill_order.append((row, col))
    
    path        = []
    dp_computed = False   
    
    running = True

    #buttons
    start_btn = pygame.Rect(15, 500, 120, 50)
    quit_btn = pygame.Rect(650, 500, 120, 50)

    #Animations
    anim_phase = ""
    anim_index = 0
    anim_timer = 0
    anim_delay = 4

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if start_btn.collidepoint((mouse_x, mouse_y)) and anim_phase == "":
                    dp = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                    for r in range(GRID_SIZE):
                        for c in range(GRID_SIZE):
                            if grid[r][c] in ("path", "visited"):
                                grid[r][c] = "empty"

                    dp[0][0] = 1 if grid[0][0] != "obstacle" else 0

                    # First row
                    for c in range(1, GRID_SIZE):
                        if grid[0][c] == "obstacle":
                            break  # everything to the right is blocked
                        dp[0][c] = dp[0][c-1]

                    # First column
                    for r in range(1, GRID_SIZE):
                        if grid[r][0] == "obstacle":
                            break  # everything below is blocked
                        dp[r][0] = dp[r-1][0]

                    # Rest of grid
                    for r in range(1, GRID_SIZE):
                        for c in range(1, GRID_SIZE):
                            if grid[r][c] != "obstacle":
                                dp[r][c] = dp[r-1][c] + dp[r][c-1]

                    dp_computed = True
                    anim_index  = 0
                    anim_timer  = 0
                    anim_phase  = "filling"

                elif quit_btn.collidepoint((mouse_x, mouse_y)):
                    running = False

                else:
                    col = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
                    row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and anim_phase == "":
                        if event.button == 1:
                            if (row, col) != (0, 0) and (row, col) != (GRID_SIZE-1, GRID_SIZE-1): # An obstacle cannot be placed on the start or end cell
                                grid[row][col] = "obstacle"
                        elif event.button == 3:
                            grid[row][col] = "empty"

        anim_timer += 1
        if anim_timer >= anim_delay:
            anim_timer = 0
 
            if anim_phase == "filling":
                if anim_index < len(fill_order):
                    r, c = fill_order[anim_index]
                    if grid[r][c] != "obstacle":
                        grid[r][c] = "visited"
                    anim_index += 1
                else:
                    anim_phase = "path"
                    anim_index = 0
                    path = reconstruct_path(dp)
 
            elif anim_phase == "path":
                if anim_index < len(path):
                    r, c = path[anim_index]
                    if (r, c) not in ((0, 0), (GRID_SIZE-1, GRID_SIZE-1)):
                        grid[r][c] = "path"
                    anim_index += 1
                else:
                    anim_phase = ""

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, font)

        if dp_computed:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if dp[r][c] > 0 and grid[r][c] != "obstacle":
                        x = GRID_OFFSET_X + c * CELL_SIZE
                        y = GRID_OFFSET_Y + r * CELL_SIZE
                        num = font.render(str(dp[r][c]), True, TEXT_COLOR_1)
                        screen.blit(num, num.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)))

            total = dp[GRID_SIZE-1][GRID_SIZE-1]
            msg = f"Total Paths: {total}" if total > 0 else "No Paths Available"
            screen.blit(font.render(msg, True, TEXT_COLOR_1),
                (GRID_OFFSET_X, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE + 10))

        pygame.draw.rect(screen, BUTTON_COLOR_GREEN, start_btn)
        pygame.draw.rect(screen, BUTTON_COLOR_GREY,  quit_btn)
 
        screen.blit(font.render("Run DP", True, TEXT_COLOR_2),
                    (start_btn.x + 15, start_btn.y + 15))
        screen.blit(font.render("QUIT",   True, TEXT_COLOR_2),
                    (quit_btn.x + 25,  quit_btn.y + 15))
        
        screen.blit(font.render("Paths move right and down only", True, TEXT_COLOR_1),
            (GRID_OFFSET_X, 10))
 
        pygame.display.flip()
        clock.tick(30) 



def run(screen):
    font = pygame.font.SysFont(None, 28)
    
    menu_items = [
    "Pathfinding Puzzle Visualisation (press enter)", 
    "Event Queue Simulator Visualisation (press enter)", 
    "Dynamic Programming Puzzle Visualisation (press enter)", 
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
                    if choice == "Pathfinding Puzzle Visualisation (press enter)":
                        pathfinding_visualise(screen, font)
                    elif choice == "Event Queue Simulator Visualisation (press enter)":
                        #event_queue_visualiser(screen, font)
                        pass
                    elif choice == "Dynamic Programming Puzzle Visualisation (press enter)":
                        dynamic_programming_visualiser(screen, font)
                        pass
                    elif choice == "Back":
                        running = False
        clock.tick(30)