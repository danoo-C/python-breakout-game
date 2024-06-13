from utils import *
import pygame
import time
import math
import random
import os


# this function calculates the number of gameobjects that fits on the screen
#returns a list of rectangles
def create_rect_gameobjects(scr_w, scr_h,  w, h):
    space = 30
    count_x = ((scr_w - w*2 - space*2) // (w+space))
    count_y = ((scr_h // 2 - h*2 - space*2) // (h+space))
    rects = []
    current_x = space + w
    current_y = h * 2 + space * 2
    for y in range(count_y):
        current_y+=space
        for x in range(count_x):
            
            current_x+=space
            rects.append(pygame.Rect(current_x, current_y,w,h))
            
            current_x += w
        current_y +=h
        current_x = space + w
    return rects



class ball:
    def __init__(self,screen, x, y,width,height, texture_path):
        self.screen = screen
        self.direction = 0
        self.speed = 0
        self.w_scr, self.h_scr = pygame.display.get_surface().get_size()
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y,self.w, self.h)
        self.shouldPlayBounce = False

        self.original_texture = pygame.image.load(texture_path).convert_alpha()
        self.texture = self.trim_texture()
        

    def render(self):
    # Check for collision with the left or right side of the screen
        if self.x < 0 or self.x > self.w_scr:
            # Reverse the horizontal direction of the ball upon collision with the side walls
            self.direction = 180 - self.direction
            self.shouldPlayBounce = True
            if self.x < 0:
                self.x = self.w +1
            else:
                self.x = self.w_scr -self.w-1
        # Check for collision with the top or bottom of the screen
        if self.y < 0 or self.y > self.h_scr:
            # Reverse the vertical direction of the ball upon collision with the top or bottom walls
            self.direction = -self.direction
            self.y = self.h + 1
            self.shouldPlayBounce = True


        # add to the current x, y based on the angle and speed of ball
        r = math.radians(self.direction)
        x = math.cos(r) * self.speed
        y = math.sin(r) * self.speed
        self.rect = self.rect.move(x, y)
        self.x = self.rect.x
        self.y = self.rect.y

        # draw the ball
        self.screen.blit(self.texture, self.rect)


    def draw(self):
        self.rect = pygame.Rect(self.x, self.y,self.w, self.h)
        self.screen.blit(self.texture, self.rect)

    
    def trim_texture(self):
        texture_width, texture_height = self.original_texture.get_size()
        trim_rect = pygame.Rect(0, 0, self.w, self.h)
        trimmed_texture = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        trimmed_texture.blit(self.original_texture, (0, 0), trim_rect)
        return trimmed_texture

class rectangle_gameobject:
    def __init__(self, screen, rect, width, height, texture_path):
        self.screen = screen
        self.rect = rect
        self.alive = True
        self.w = width
        self.h = height

        self.original_texture = pygame.image.load(texture_path).convert_alpha()
        self.texture = self.trim_texture()
        
        

    def check_collision(self, player_object):
        if not self.alive:
            return False
        return self.rect.colliderect(player_object.rect)
    
    def draw(self):
        if self.alive:
            self.screen.blit(self.texture, self.rect)

    def trim_texture(self):
        texture_width, texture_height = self.original_texture.get_size()
        trim_rect = pygame.Rect(0, 0, self.w, self.h)
        trimmed_texture = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        trimmed_texture.blit(self.original_texture, (0, 0), trim_rect)
        return trimmed_texture


def colision_physicsh(direction): 
    return -direction #+ random.randint(-5,5)

class game:
    def __init__(self,screen):
        self.screen = screen
        self.w, self.h = pygame.display.get_surface().get_size()
        self.font = pygame.font.Font(None, 36)
        self.plate_rect = None
        self.player = None
        self.last_gamelogicTime = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
        self.speed = 0.005
        self.gameobject_rects = []
        self.randc = lambda: random.randint(0,255)
        self.gameobjects = []
        self.gameobject_strenghts = []

        self.healt = 3

        self.score = 0
        self.last_score = 0
        self.fps_limiter_time = 0
        self.gameState = 0
        self.can_exit_game_when_esc = False

        self.stating_ball_speed = 2
        self.playing_ball_speed = 7


        self.pauseMenu_has_drawn_first_frame = False
        #self.sound_effectPlayer = soundeffects()

        


        #load the textures
        #we use the trim_texture method for game object textures - no scaling needed for them
        #and for the background and menu pages we use the scale method - when we play on a different resolution than classic 1920x1080 the scale needs to remain the same for the menu to not look messed up
        texture_path = "textures\\plate_hd.png"
        self.original_texture = pygame.image.load(texture_path).convert_alpha()
        self.plate_texture = self.trim_texture()

        texture_path = "textures\\heart.png"
        self.original_texture = pygame.image.load(texture_path).convert_alpha()
        self.healt_texture = self.trim_texture()

        texture_path = "textures\\heart_2.png"
        self.original_texture = pygame.image.load(texture_path).convert_alpha()
        self.healt_texture_minus = self.trim_texture()




        texture_path = "textures\\bg.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.bg = pygame.transform.scale(picture, (self.w, self.h))

        texture_path = "textures\\bg_m.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.bg_m = self.trim_texture()

        texture_path = "textures\\Pause_menu.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.pause_bg = pygame.transform.scale(picture, (self.w, self.h))

        texture_path = "textures\\Pause_menu_0_oppacity.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.pause_bg_0_oppacity = pygame.transform.scale(picture, (self.w, self.h))

        texture_path = "textures\\Death_screen.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.loose_bg = pygame.transform.scale(picture, (self.w, self.h))

        texture_path = "textures\\bg_m.png"
        picture = pygame.image.load(texture_path).convert_alpha()
        self.win_bg = pygame.transform.scale(picture, (self.w, self.h))

    def revive_rand_gameobject(self):
        alive_gameobjects = [i for i, g in enumerate(self.gameobjects) if g.alive == 0]
        if not alive_gameobjects:
            random.choice(self.gameobjects).alive = True
        
        random_index = random.choice(alive_gameobjects)
        self.gameobjects[random_index].alive = True
            

    def other_screen(self): # this handles the screens win, death, and pause
        if (self.gameState == 2):# win
            bg_rect = (0,0,self.w,self.h)
            self.screen.blit(self.win_bg, bg_rect)
            #draw_text("You Won!", pygame.font.Font(None, 72), (0,255,0), self.screen, self.w // 2, self.h // 2)
            draw_text("esc to get back to menu", self.font, (255,255,255), self.screen, self.w // 2, self.h // 2 -160 )
            draw_text("Score: " + str(self.last_score), pygame.font.Font(None, 72), (255,255,255), self.screen, self.w // 2,self.h // 2 + 15)
            self.can_exit_game_when_esc = True

        elif self.gameState == 1:# death
            bg_rect = (0,0,self.w,self.h)
            self.screen.blit(self.loose_bg, bg_rect)
            #draw_text("You Died!", pygame.font.Font(None, 72), (255,0,000), self.screen, self.w // 2, self.h // 2)
            draw_text("esc to get back to menu", self.font, (255,255,255), self.screen, self.w // 2, self.h // 2 -160 )
            draw_text("Score: " + str(self.last_score), pygame.font.Font(None, 72), (255,255,255), self.screen, self.w // 2, self.h // 2 + 15)
            self.can_exit_game_when_esc = True

        elif self.gameState == 3:# pause
            bg_rect = (0,0,self.w,self.h)
            if not self.pauseMenu_has_drawn_first_frame:
                self.screen.blit(self.pause_bg, bg_rect)
                self.pauseMenu_has_drawn_first_frame = True
            else:
                self.screen.blit(self.pause_bg_0_oppacity, bg_rect)
            #draw_text("Game paused", pygame.font.Font(None, 72), (0,255,255), self.screen, self.w // 2, self.h // 2)
            draw_text("esc to get back to menu, space to resume", self.font, (255,255,255), self.screen, self.w // 2, self.h // 2 -160 )
            draw_text("Current Score: " + str(self.last_score), pygame.font.Font(None, 72), (255,255,255), self.screen, self.w // 2, self.h // 2 + 15)
            self.can_exit_game_when_esc = True


    def gamemode_inffinity(self):
        alive_gamobjects_count = 0
        self.gameobject_rects = create_rect_gameobjects(self.w, self.h, 100,30)
        for i,r in enumerate(self.gameobject_rects):
            self.gameobjects.append(rectangle_gameobject(self.screen, r,100,30,"textures\\block_hd.png" ))

        while True:
            broke_gameobjects_all = True

            self.frame_count += 1

            pygame.mouse.set_visible(False)
            
            
            current_time = time.time()

            #delta time implementation
            if current_time - self.last_gamelogicTime >= self.speed:

                

                if self.gameState == 0:
                    self.pauseMenu_has_drawn_first_frame = False
                    #draw bg
                    bg_rect = (0,0,self.w,self.h)
                    self.screen.blit(self.bg, bg_rect)

                    #plate logic
                    plate_w = 160
                    plate_h = 30
                    plate_y_bottom = 150
                    (mx,my) = pygame.mouse.get_pos()
                    self.plate_rect = pygame.Rect(mx-plate_w//2, self.h -plate_y_bottom,plate_w, plate_h)
                    self.screen.blit(self.plate_texture, self.plate_rect)
                    #pygame.draw.rect(self.screen, (255,255,100), self.plate_rect)
                    
                    self.player.render()

                    draw_text("DAVALEX™ | FPS: "+str(round(self.fps,2)), pygame.font.Font(None, 20), (255,255,255), self.screen, self.w -100, 20) # draw watermark

                    #respawn the ball
                    if self.player.y >= self.h - 10: 
                        self.healt -= 1

                        self.player = ball(self.screen, max(mx-200, 200),700, 25,25, "textures\\player_hd.png")
                        self.player.speed = self.stating_ball_speed 
                        self.player.direction = 45

                        if self.healt <= 0:

                            self.gameState = 1 #die

                    for i in range(3): # draw the healt
                        heart_texture_w = 55
                        heart_texture_h = 55
                        heart_rect = (10 * (i*10) + 20, self.h - heart_texture_h - 20, 10 * (i*10)+ 20 + heart_texture_w, self.h - heart_texture_h - 20)
                        if(i < self.healt):

                            self.screen.blit(self.healt_texture, heart_rect)
                        else:
                            self.screen.blit(self.healt_texture_minus, heart_rect)

                    for g in self.gameobjects: # loop trught all gameogjects
                        if g.check_collision(self.player): # check for colision

                            g.alive = False # hide gameobject
                            self.player.direction = colision_physicsh(self.player.direction) # set direction
                            self.score +=1
                        if g.alive:
                            broke_gameobjects_all = False # if a gameobject is alive then the game will not end (win)
                            alive_gamobjects_count += 1
                            
                        g.draw() # draw the gameobject

                    if alive_gamobjects_count < 25: # cheack if theres less than 25 gameobjects alive, if so revive a random one
                        self.revive_rand_gameobject()
                    alive_gamobjects_count = 0

                    # draw score
                    draw_text(str(round(self.score)), pygame.font.Font(None, 75), (100,255,255), self.screen, self.w //2,100)
                    self.last_score = self.score
                    #self.score = 0

                    if broke_gameobjects_all: 
                        self.gameState = 2 # win

                    
                else: # go to other screen if gamode != 0
                    self.other_screen()

                pygame.display.update()

                if self.player.rect.colliderect(self.plate_rect): # bounce off plate
                                self.player.direction = colision_physicsh(self.player.direction)# + random.randint(-10,10)
                                self.player.speed = self.playing_ball_speed 
                                #self.sound_effectPlayer.play("bounce")

                #sound effect for player bouncing off wall                
                if self.player.shouldPlayBounce: # bounce off sound
                    #self.sound_effectPlayer.play("bounce")
                    self.player.shouldPlayBounce = False

                self.last_gamelogicTime = current_time
 


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.gameState == 3 or self.can_exit_game_when_esc:
                            return 1
                        self.gameState = 3
                    if event.key == pygame.K_SPACE:
                        if self.gameState == 3:
                            self.gameState = 0  
                            self.can_exit_game_when_esc = False
                        
            # fps calc
            current_time = time.time()        
            elapsed_time = current_time - self.start_time
            if elapsed_time >= 1:   
                self.fps = self.frame_count / elapsed_time
                self.frame_count = 0
                self.start_time = current_time
    
    def gamedode_classic(self):
        self.gameobject_rects = create_rect_gameobjects(self.w, self.h, 100,30)
        for i,r in enumerate(self.gameobject_rects):
            self.gameobjects.append(rectangle_gameobject(self.screen, r,100,30,"textures\\block_hd.png" )) 

        while True:
            broke_gameobjects_all = True

            self.frame_count += 1

            pygame.mouse.set_visible(False)
            
            
            current_time = time.time()

            #delta time implementation
            if current_time - self.last_gamelogicTime >= self.speed:
                if self.gameState == 0:

                    #background
                    self.screen.fill((0,0,0))
                    bg_rect = (0,0,self.w,self.h)
                    self.screen.blit(self.bg, bg_rect)


                    #draw_text("Game Page", pygame.font.Font(None, 72), (255,255,255), self.screen, self.w // 2, self.h // 2)
                    #draw_text("esc to get back to menu", self.font, (255,255,255), self.screen, self.w // 2, self.h // 2 + 80)

                    #plate logic
                    plate_w = 160
                    plate_h = 30
                    plate_y_bottom = 150
                    (mx,my) = pygame.mouse.get_pos()
                    self.plate_rect = pygame.Rect(mx-plate_w//2, self.h -plate_y_bottom,plate_w, plate_h)
                    self.screen.blit(self.plate_texture, self.plate_rect)
                    #pygame.draw.rect(self.screen, (255,255,100), self.plate_rect)
                    
                    self.player.render() # draw player

                    draw_text("DAVALEX™ | FPS: "+str(round(self.fps,2)), pygame.font.Font(None, 20), (255,255,255), self.screen, self.w -100, 20) # watermark

                    if self.player.y >= self.h - 10: # respawn player or end game
                        self.healt -= 1

                        self.player = ball(self.screen, max(mx-200, 200),700, 25,25, "textures\\player_hd.png")
                        self.player.speed = self.stating_ball_speed 
                        self.player.direction = 45

                        if self.healt <= 0:

                            self.gameState = 1 #die

                    for i in range(3): # draw the hearts representing the healt
                        heart_texture_w = 55
                        heart_texture_h = 55
                        heart_rect = (10 * (i*10) + 20, self.h - heart_texture_h - 20, 10 * (i*10)+ 20 + heart_texture_w, self.h - heart_texture_h - 20)
                        if(i < self.healt):

                            self.screen.blit(self.healt_texture, heart_rect)
                        else:
                            self.screen.blit(self.healt_texture_minus, heart_rect)

                    for g in self.gameobjects: # loop trught all gameogjects
                        if g.check_collision(self.player): # cheack for colision

                            g.alive = False # hide gameobject
                            self.player.direction = colision_physicsh(self.player.direction) # set direction
                            
                        if g.alive:
                            broke_gameobjects_all = False # if a gameobject is alive then the game will not end (win)
                        else:
                            self.score +=1
                            
                        g.draw() # draw the gameobject
 

                    draw_text(str(round(self.score)), pygame.font.Font(None, 75), (100,255,255), self.screen, self.w //2,100) # draw score
                    self.last_score = self.score
                    self.score = 0

                    if broke_gameobjects_all: 
                        self.gameState = 2 # win

                    
                else:
                    self.other_screen()# when the game ended or paused it will draw the "other screen"

                pygame.display.update()

                if self.player.rect.colliderect(self.plate_rect): # bounce off plate
                                self.player.direction = colision_physicsh(self.player.direction) #+ random.randint(-10,10)
                                self.player.speed = self.playing_ball_speed 
                                #self.sound_effectPlayer.play("bounce")

                #sound effect for player bouncing off wall                
                if self.player.shouldPlayBounce: # bounce off sound
                    #self.sound_effectPlayer.play("bounce")
                    self.player.shouldPlayBounce = False

                self.last_gamelogicTime = current_time
 


            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.gameState == 3 or self.can_exit_game_when_esc:
                            return 1
                        self.gameState = 3
                    if event.key == pygame.K_SPACE:
                        if self.gameState == 3:
                            self.gameState = 0  
                            self.can_exit_game_when_esc = False
                        
            # fps calculation
            current_time = time.time()        
            elapsed_time = current_time - self.start_time
            if elapsed_time >= 1:   
                self.fps = self.frame_count / elapsed_time
                self.frame_count = 0
                self.start_time = current_time

    def game_page(self, gamemode):
        
        #game inicialization code, it basically just resets the variables
        self.player = ball(self.screen, random.randint(30,self.w),700, 25,25, "textures\\player_hd.png")
        self.player.speed = self.stating_ball_speed 
        self.player.direction = 45
        
        self.gameobjects = []
        self.gameState = 0

        self.healt = 3
        self.score = 0
        self.last_score = 0
        self.can_exit_game_when_esc = False
         # start the game with the given gamemode
        if(gamemode==1):
            return self.gamedode_classic()
        elif(gamemode==2):
            return self.gamemode_inffinity()

    def trim_texture(self): # trim the texture so it only draws the section of the texture as big as the rectangle
        texture_width, texture_height = self.original_texture.get_size()
        trim_rect = pygame.Rect(0, 0, self.w, self.h)
        trimmed_texture = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        trimmed_texture.blit(self.original_texture, (0, 0), trim_rect)
        return trimmed_texture

            
