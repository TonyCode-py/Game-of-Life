import sys
import time
import pygame
import numpy as np
import pygame.locals as pl

def initialize(width, height):
    """
    Randomly initialize the matrix. Value of each unit is 0 or 1.
    0 stands for death and 1 stands for live.
    """
    lives = np.round(np.random.rand(width, height))
    lives = lives.astype(np.int64)
    return lives

def show(lives):
    """ Only for test """
    height, width = lives.shape
    for i in range(height):
        for j in range(width):
            if lives[i,j] == 1:
                print("█",end="")
            else:
                print("  ",end="")
        print("")

def near_sum(lives, i, j, height, width):
    """ Return the sum of the eight grids' value around the current grid """
    nsum = (lives[(i-1)%height,(j-1)%width]+lives[(i-1)%height,j]
            + lives[(i-1)%height,(j+1)%width] + lives[i,(j-1)%width]
            + lives[i,(j+1)%width] + lives[(i+1)%height,(j-1)%width]
            + lives[(i+1)%height,j] + lives[(i+1)%height,(j+1)%width])
    return nsum
        
        
    
def one_iteration(lives):
    """ Evolve one time according to the rule """
    new_lives = lives.copy()
    height, width = lives.shape
    for i in range(height):
        for j in range(width):
            if lives[i,j] == 1:
                if (near_sum(lives, i, j, height, width) == 2 or
                    near_sum(lives, i, j, height, width) == 3):
                    new_lives[i,j] = 1
                else:
                    new_lives[i,j] = 0
            else:
                if near_sum(lives, i, j, height, width) == 3:
                    new_lives[i,j] = 1
                else:
                    new_lives[i,j] = 0
    return new_lives

def set_icon(iconname):
    """
    Give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel
    the windowicon will be set to the bitmap, but the black pixels will be full alpha channel
     
    """
    icon=pygame.Surface((32,32))
    icon.set_colorkey((0,0,0))#and call that color transparant
    rawicon=pygame.image.load(iconname)#must be 32x32, black is transparant
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)#set wind


def draw_cells(screen,lives,color,game_width,game_height,rect_length,rect_interval):
    """ Show current state on the screen """
    height, width = lives.shape
    for i in range(height):
        for j in range(width):
            if lives[i,j] == 1:
                pygame.draw.rect(screen,color,(i*(rect_length+rect_interval),
                                               j*(rect_length+rect_interval),
                                               rect_length,rect_length))

def draw_button(screen, msg, x, y, w, h,
                inactive_color, active_color,fontsize=12):
    """ Draw a single button with text """
    mousex, mousey = pygame.mouse.get_pos()
    if x < mousex < x+w and y  < mousey < y+h:
        pygame.draw.rect(screen, active_color, (x,y,w,h))
    else:
        pygame.draw.rect(screen, inactive_color, (x,y,w,h))
    font=pygame.font.SysFont('SimHei',fontsize)
    textSurface = font.render(msg, True, (0,0,0))
    textRect = textSurface.get_rect()
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurface, textRect)



def draw_buttons(screen,inactive_color, active_color,
                 screen_width,screen_height,game_width,
                 button_width,button_height):
    """" Draw buttons beside game region """
    margin_top = 40
    interval = 30
    x = game_width + (screen_width - game_width - button_width) / 2
    y = [margin_top + (button_height + interval)*i for i in range(4)]
    msg = ['Start evolve', 'Stop evolve', 'Evolve one step',
           'Random initialize']
    for i in range(4):   
        draw_button(screen, msg[i], x, y[i], button_width,
                    button_height,inactive_color, active_color)
    
    

# define constants and parameters
white = (255,255,255)
gray  = (224,224,224)
blue  = (102,178,255)
black = (0,0,0)
light_gray = (235,235,235)
screen_width = 640
screen_height = 480


game_width = 500
game_height = screen_height
button_width = 120
button_height = 30
rect_interval = 1
rect_length = 10
start_button_width = 200
start_button_height = 50
start_button_x = (screen_width - start_button_width)/2
start_button_y = (screen_height - start_button_height)/2+100
        
interval = 0.1
game_start = False
start_continous_evolve = False
evolve = False
num_lives = 0
show_num_lives = True
init = False
num_x = 40
num_y = 40


margin_top = 40
button_interval = 30
button_x = game_width + (screen_width - game_width - button_width) / 2
button_y = [margin_top + (button_height + button_interval)*i for i in range(4)]


# initialize pygame
pygame.init()

set_icon('dna.ico')

screen = pygame.display.set_mode((screen_width, screen_height))


screen.fill(white)

pygame.display.set_caption('Game of Life')

font=pygame.font.SysFont('SimHei',30)

# main loop
while True:
    screen.fill(white)

    x, y = pygame.mouse.get_pos()

    if game_start:
        draw_cells(screen,lives,black,game_width,game_height,rect_length,rect_interval)

        draw_buttons(screen,gray,light_gray,screen_width,screen_height,
                     game_width, button_width,button_height)
        
        if start_continous_evolve:
            lives = one_iteration(lives)

        time.sleep(interval)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pl.MOUSEBUTTONDOWN:
                if (button_x <= x <= button_x+button_width and
                    button_y[0] <= y <= button_y[0]+button_height):
                    start_continous_evolve = True
                elif (button_x <= x <= button_x+button_width and
                    button_y[1] <= y <= button_y[1]+button_height):
                    start_continous_evolve = False
                elif (button_x <= x <= button_x+button_width and
                    button_y[2] <= y <= button_y[2]+button_height):
                    lives = one_iteration(lives)
                elif (button_x <= x <= button_x+button_width and
                    button_y[3] <= y <= button_y[3]+button_height):
                    lives = initialize(num_y,num_x)
                else:
                    h, w = lives.shape
                    for i in range(h):
                        for j in range(w):
                            sx = i*(rect_length+rect_interval)
                            sy = j*(rect_length+rect_interval)
                            if (sx <= x <= sx + rect_length and
                                sy <= y <= sy + rect_length):
                                if lives[i,j] == 0:
                                    lives[i,j] = 1
                                elif lives[i,j] == 1:
                                    lives[i,j] = 0
    else:
        draw_button(screen, 'Start Game', start_button_x, start_button_y,
                    start_button_width, start_button_height, gray,
                    light_gray, 20)
        title = pygame.image.load('title.jpg')
        title = pygame.transform.scale(title,(300,240))
        screen.blit(title,((screen_width-300)/2,start_button_y-240-20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pl.MOUSEBUTTONDOWN:
                if (start_button_x <= x <= start_button_x+start_button_width
                    and start_button_y <= y <= start_button_y+start_button_height):
                    game_start = True
                    lives = initialize(num_y,num_x)
    pygame.display.update()
