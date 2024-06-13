#             _                              _       _   
#            | |                            (_)     | |  
#   ___ _ __ | |_ _ __ _   _     _ __   ___  _ _ __ | |_ 
#  / _ \ '_ \| __| '__| | | |   | '_ \ / _ \| | '_ \| __|
# |  __/ | | | |_| |  | |_| |   | |_) | (_) | | | | | |_ 
#  \___|_| |_|\__|_|   \__, |   | .__/ \___/|_|_| |_|\__|
#                       __/ |   | |                      
#                      |___/    |_|  
#                    
# made by DAVALEX


#import game files
import game
import menu

import pygame

pygame.init()

# Get the size of the main screen
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Breakout by DAVALEX")

m = menu.menu(screen)
g = game.game(screen)

def shutdown():
    print("no error. safely exitting game!")
    pygame.quit()
    exit(0)

while 1:
    #if a mainloop function returns 0 that means that the execution should stop thus exiting the game
    menu_selection = m.main_menu()
    if(menu_selection == 0):
        shutdown()
        
    if(not g.game_page(menu_selection)):
        shutdown()
    