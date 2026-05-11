import pygame
import sys
import collections

from modules import heaps_visualiser

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphs")
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)


def option():
    buttons = {
        'Exit': pygame.Rect(550, 530, 200, 50),
        'Reset': pygame.Rect(150, 530, 200, 50),
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 30, rect.y + 15))
        
    pygame.display.flip()
    return buttons

# Graph nodes positioned manually
nodes_pos = {
    'A': (100, 100),
    'B': (250, 60),
    'C': (250, 200),
    'D': (400, 100),
    'E': (500, 150),
    'F': (400, 300)
}

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

nodes = {}
def draw_graph(visited=set(), frontier=set(), current=None):
    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = nodes_pos[node]
        for n in neighbors:
            x2, y2 = nodes_pos[n]
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)
    # Draw nodes
    for node, (x, y) in nodes_pos.items():
        color = (200, 200, 200)
        if node in visited:
            color = (100, 200, 100)
        if node in frontier:
            color = (255, 200, 100)
        if node == current:
            color = (255, 100, 100)
        pygame.draw.circle(screen, color, (x, y), 25)
        nodes[node] = pygame.draw.circle(screen, color, (x, y), 25)
        text = FONT.render(node, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
    pygame.display.flip()

def bfs(start):
    visited = set()
    queue = collections.deque([start])
    order = ''

    while queue:
        current = queue.popleft()
        visited.add(current)
        order = order + f'{current} '
        draw_text('Order Visited: ' + order, (150, 400, 200, 50))
        draw_graph(visited=visited, frontier=set(queue), current=current)
        pygame.time.wait(700)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)

#DFS funtion
def dfs(start):
    visited = set()
    stack = [start]
    order = ''

    while stack:
        node = stack.pop()
        if node not in visited:        
            visited.add(node)
            order = order + f'{node} '
            draw_text('Order Visited: ' + order, (150, 400, 200, 50))
            draw_graph(visited=visited, frontier=set(stack), current=node)
            for point in reversed(graph[node]):
                if point not in visited:
                    stack.extend(point)
            pygame.time.wait(700)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main(screen, choice):
    screen.fill((200, 200, 250))
    running = True
    buttons = option()
    draw_text("Click on node to start", (WIDTH // 10, 480))
    draw_graph()
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
                                draw_text("Click on node to start", (WIDTH // 10, 480))
                                draw_graph()
                    for text, circle in nodes.items():
                        if circle.collidepoint(pos):
                            choice(text)

def run(screen):

    font = pygame.font.SysFont(None, 28)
    
    menu_items = [
    "DFS Visualization (press enter)",
    "BFS Visualization (press enter)",
    "Heaps Visualization (press enter)", #Unfinished
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
                    if choice == "DFS Visualization (press enter)":
                        main(screen, dfs)
                    elif choice == "BFS Visualization (press enter)":
                        main(screen, bfs)
                    elif choice == "Heaps Visualization (press enter)":
                        heaps_visualiser.main()
                    elif choice == "Back":
                        running = False
        clock.tick(30)