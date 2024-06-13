from utils import *
import pygame
import os

class menu:
    def __init__(self,screen):
        self.screen = screen
        self.w, self.h = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font(None, 36)

        self.original_texture = 0

        texture_path = "textures\\bg_m.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.bg = pygame.transform.scale(picture, (self.w, self.h))

        self.leave_game_path_u = "textures\\quit_u.png"
        self.leave_game_path_c = "textures\\quit_c.png"

        self.play_game_path_u = "textures\\play_u.png"
        self.play_game_path_c = "textures\\play_c.png"

        self.back_path_u = "textures\\back_u.png"
        self.back_path_c = "textures\\back_c.png"

        self.infinity_path_u = "textures\\infinity_u.png"
        self.infinity_path_c = "textures\\infinity_c.png"

        self.classic_path_u = "textures\\classic_u.png"
        self.classic_path_c = "textures\\classic_c.png"

    def game_select_page(self):
        pygame.mouse.set_visible(True)
        #create butons objects

        #calculate button dimensions based on texture sizes and screen dimensions
        button1_w = 400
        backButton_w = 300
        button1_h = 50
        button1_x =  self.w // 2 - button1_w //2
        button1_y = self.h // 2 -80
        
        backButton_x = self.w // 2 - backButton_w //2
        button2_y = button1_y + button1_h + 20
        button3_y = button2_y + button1_h + 20

        game1Button = button(self.screen,button1_x, button1_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.classic_path_u)
        game2Button = button(self.screen,button1_x, button2_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.infinity_path_u)
        backButton = button(self.screen,backButton_x, button3_y, backButton_w, button1_h,  "", (255,255,255), (0,0,0), self.back_path_u)

        g1_switch = False
        g2_switch = False
        b_switch = False

        g1_switch_h = False
        g2_switch_h = False
        b_switch_h = False

        while True:
            self.screen.fill((0,0,0))
            bg_rect = (0,0,self.w,self.h)
            self.screen.blit(self.bg, bg_rect)


            #draw_text("Main Menu", self.font, (255,255,255), self.screen, self.w // 2, self.h // 4)

            #draw the buttons
            game1Button.draw()
            game2Button.draw()
            backButton.draw()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0 #exit game
                
                #mouse event handeling 
                #todo: create a object that will auto check every object for click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game1Button.rect.collidepoint(event.pos):
                        return 1 # classic gamemode
                    if game2Button.rect.collidepoint(event.pos):
                        return 2 # inffinity gamemode
                    if backButton.rect.collidepoint(event.pos):
                        return 0 # back to menu
                    
                if game1Button.rect.collidepoint(pygame.mouse.get_pos()): # hover effect
                    g1_switch = True
                    g1_switch_h = False
                else:
                    g1_switch = False
                    g1_switch_h = False


                if game2Button.rect.collidepoint(pygame.mouse.get_pos()): # hover effect
                    g2_switch = True
                    g2_switch_h = False
                else:
                    g2_switch = False
                    g2_switch_h = False

                if backButton.rect.collidepoint(pygame.mouse.get_pos()): # hover effect
                    b_switch = True
                    b_switch_h = False
                else:
                    b_switch = False
                    b_switch_h = False

            if not g1_switch_h: # hover effect
                if g1_switch:
                    game1Button = button(self.screen,button1_x, button1_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.classic_path_c)
                    g1_switch_h = True
                else:
                    game1Button = button(self.screen,button1_x, button1_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.classic_path_u)
                    g1_switch_h = True

            if not g2_switch_h: # hover effect
                if g2_switch:
                    game2Button = button(self.screen,button1_x, button2_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.infinity_path_c)
                    g2_switch_h = True
                else:
                    game2Button = button(self.screen,button1_x, button2_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.infinity_path_u)
                    g2_switch_h = True

            if not b_switch_h: # hover effect
                if b_switch:
                    backButton = button(self.screen,backButton_x, button3_y, backButton_w, button1_h, "", (255,255,255), (0,0,0), self.back_path_c)
                    b_switch_h = True
                else:
                    backButton = button(self.screen,backButton_x, button3_y, backButton_w, button1_h, "", (255,255,255), (0,0,0), self.back_path_u)
                    b_switch_h = True
            

            pygame.display.update() #update screen

    def main_menu(self):
        pygame.mouse.set_visible(True)
        #create butons objects
        
        button1_w = 300
        button1_h = 50
        button1_x =  self.w // 2 - button1_w //2 
        button1_y = self.h // 2 - 50
        
        button2_y = button1_y + button1_h + 30
        gameButton = button(self.screen,button1_x, button1_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.play_game_path_u)
        exitButton = button(self.screen,button1_x, button2_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.leave_game_path_u)

        switch_c_texture1 = False
        switch_c_texture1_handled = False
        switch_c_texture2 = False
        switch_c_texture2_handled = False
        while True:
            self.screen.fill((0,0,0))
            bg_rect = (0,0,self.w,self.h)
            self.screen.blit(self.bg, bg_rect)


            #draw_text("Main Menu", self.font, (255,255,255), self.screen, self.w // 2, self.h // 4)

            #draw the buttons
            gameButton.draw()
            exitButton.draw()
            


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0 #exit game
                
                #mouse event handeling 
                #todo: create a object that will auto check every object for click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gameButton.rect.collidepoint(event.pos):
                        r = self.game_select_page()
                        if r != 0:
                            return r
                    if exitButton.rect.collidepoint(event.pos):
                        return 0 # exit game
                if gameButton.rect.collidepoint(pygame.mouse.get_pos()): # hover effect
                    switch_c_texture1 = True
                    switch_c_texture1_handled = False
                else:
                    switch_c_texture1 = False
                    switch_c_texture1_handled = False


                if exitButton.rect.collidepoint(pygame.mouse.get_pos()): # hover effect
                    switch_c_texture2 = True
                    switch_c_texture2_handled = False
                else:
                    switch_c_texture2 = False
                    switch_c_texture2_handled = False

            # hover effect handling
            if not switch_c_texture1_handled:
                if switch_c_texture1:
                    gameButton = button(self.screen,button1_x, button1_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.play_game_path_c)
                    switch_c_texture1_handled = True
                else:
                    gameButton = button(self.screen,button1_x, button1_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.play_game_path_u)
                    switch_c_texture1_handled = True

            if not switch_c_texture2_handled:
                if switch_c_texture2:
                    exitButton = button(self.screen,button1_x, button2_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.leave_game_path_c)
                    switch_c_texture2_handled = True
                else:
                    exitButton = button(self.screen,button1_x, button2_y, button1_w, button1_h, "", (255,255,255), (0,0,0), self.leave_game_path_u)
                    switch_c_texture2_handled = True

            pygame.display.update() #update screen

    def trim_texture(self): # trim the texture so it only draws the section of the texture as big as the rectangle
        texture_width, texture_height = self.original_texture.get_size()
        trim_rect = pygame.Rect(0, 0, self.w, self.h)
        trimmed_texture = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        trimmed_texture.blit(self.original_texture, (0, 0), trim_rect)
        return trimmed_texture 

