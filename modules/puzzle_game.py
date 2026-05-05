import pygame
import random
import sys


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game")
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()





def run(screen):
    font = pygame.font.SysFont(None, 28)
    
    menu_items = [
    "Pathfinding Puzzle Visualization (press enter)",
    "Event Queue Visualization (press enter)",
    "Dynamic Programming Puzzle Visualization (press enter)",
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
                    if choice == "Pathfinding Puzzle Visualization (press enter)":
                        #main(screen, pathfinding_visualize)
                        pass
                    elif choice == "Event Queue Visualization (press enter)":
                        #main(screen, event_queue_visualize)
                        pass
                    elif choice == "Dynamic Programming Puzzle Visualization (press enter)":
                        #main(screen, dynamic_programming_visualize)
                        pass
                    elif choice == "Back":
                        running = False
        clock.tick(30)