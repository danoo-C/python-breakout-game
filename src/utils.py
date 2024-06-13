import pygame
import os
import threading
#import simpleaudio as sa

# the name speaks for itself :)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

class button:
    def __init__(self,screen, x,y,w,h,text,bg, fg, texture_path):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.bg = bg
        self.fg = fg
        self.rect = None
        self.font = pygame.font.Font(None, 36)
        self.using_texture = True
        if texture_path != "":
            self.using_texture = False
            self.original_texture = pygame.image.load(texture_path).convert_alpha()
            self.texture = self.trim_texture()

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.using_texture:
            pygame.draw.rect(self.screen, self.bg, self.rect)
        else:
            self.screen.blit(self.texture,self.rect)
        draw_text(self.text, self.font, self.fg, self.screen, self.x + self.w //2, self.y+self.h//2)

    def trim_texture(self):
        texture_width, texture_height = self.original_texture.get_size()
        trim_rect = pygame.Rect(0, 0, self.w, self.h)
        trimmed_texture = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        trimmed_texture.blit(self.original_texture, (0, 0), trim_rect)
        return trimmed_texture

#draw the texture on the screen
class texture:
    def __init__(self,screen, x,y,desired_w,desired_h, texture_path):
        self.screen = screen
        self.x = x
        self.y = y
        self.h = desired_h
        self.w = desired_w
        self.texture_path = texture_path
        self.original_texture = pygame.image.load(texture_path).convert_alpha()
        self.texture = self.trim_texture()
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def refresh(self):
        self.rect = pygame.rect(self.x, self.y, self.w, self.h)
    def render(self):
        self.screen.blit(self.texture, self.rect)

    def trim_texture(self):
        texture_width, texture_height = self.original_texture.get_size()
        trim_rect = pygame.Rect(0, 0, self.w, self.h)
        trimmed_texture = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        trimmed_texture.blit(self.original_texture, (0, 0), trim_rect)
        return trimmed_texture



