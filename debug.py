import pygame

pygame.init()
font = pygame.font.Font(None, 20)

def debug(info, x=10, y=10):
    """Used for Pygame debug information display. Call this function during the main loop.
    Args:
        info (str): The debug information to display.
        x (int, optional): The x position of the debug text. Defaults to 10.
        y (int, optional): The y position of the debug text. Defaults to 10
        
        Example:
            `debug(f"FPS: {fps}", 10, 10)`"""
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, "white")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    display_surf.blit(debug_surf, debug_rect)