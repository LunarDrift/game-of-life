import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Click and Drag")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create a draggable rectangle (x, y, width, height)
rect_width = 50
rect_height = 50
draggable_rect = pygame.Rect(100, 100, rect_width, rect_height)
is_dragging = False
mouse_offset_x = 0
mouse_offset_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is on the rectangle
            if draggable_rect.collidepoint(event.pos):
                is_dragging = True
                # Calculate the offset to maintain relative position
                mouse_offset_x = event.pos[0] - draggable_rect.x
                mouse_offset_y = event.pos[1] - draggable_rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging when the mouse button is released
            is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # Move the rectangle if it is being dragged
            if is_dragging:
                draggable_rect.x = event.pos[0] - mouse_offset_x
                draggable_rect.y = event.pos[1] - mouse_offset_y
                # Optional: clamp the rect to the screen boundaries
                draggable_rect.clamp_ip(screen.get_rect())

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, draggable_rect)
    pygame.display.flip()

pygame.quit()
