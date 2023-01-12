import pygame as pg

from objects import TextObject
import config as cg


class Button:
    def __init__(self, x, y, width, height, text, on_click=lambda x: None, * , normal_color="black", hover_color="grey", pressed_color="red", text_color="white", padding=0, **kwargs) -> None:
        self.state = "normal"
        self.on_click = on_click

        self.text = TextObject(x + padding, y + padding, lambda: text, text_color, None, 48)
        
        self.bounds = self.text.bounds
        self.bounds.width += padding * 2 + width
        self.bounds.height += padding * 2 + height
        
        self.bounds.x = x + padding - self.bounds.width // 2
        self.bounds.y = y - height // 2

        self.normal_color = normal_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text_color = text_color
        
        self.arg = kwargs
    
    @property
    def back_color(self):
        return dict(normal = self.normal_color,
                    hover = self.hover_color,
                    pressed = self.pressed_color)[self.state]
    
    def handle_mouse_event(self, type, pos):
        if type == pg.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pg.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pg.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)
    
    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != "pressed":
                self.state = "hover"
        else:
            self.state = "normal"
    
    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = "pressed"
    
    def handle_mouse_up(self, pos):
        if self.state == "pressed":
            self.on_click(**self.arg)
            self.state = "hover"

    def draw(self, screen):
        pg.draw.rect(screen, self.back_color, self.bounds)
        self.text.draw(screen)
