import pygame

class InputManager:
    def __init__(self):
        self.key_actions = {}
        self.mouse_actions = {}
        self.scroll_action = None

    # -------------------------------------------------
    # Keyboard
    # -------------------------------------------------
    def bind_key(self, key, action):
        self.key_actions[key] = action
    
    # -------------------------------------------------
    # Mouse
    # -------------------------------------------------
    def bind_mouse(self, button, action):
        self.mouse_actions[button] = action

    def bind_scroll(self, action):
        self.scroll_action = action

    # -------------------------------------------------
    # Event Dispatching
    # -------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            action = self.key_actions.get(event.key)
            if action:
                action()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = self.mouse_actions.get(event.button)
            if action:
                action()

        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_actions.get(1, lambda: None)()
            elif pygame.mouse.get_pressed()[2]:
                self.mouse_actions.get(3, lambda: None)()
                

        elif event.type == pygame.MOUSEWHEEL:
            if self.scroll_action:
                self.scroll_action(event)

