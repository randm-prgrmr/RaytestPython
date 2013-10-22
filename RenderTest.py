import pygame
import math
from math import cos, sin, sqrt, pi, acos, tan
class GameObject(object):
    def __init__(self,res=[640,480]):
        self.RUNNING=True
        #----------------------------
        self.posX=2
        self.posY=2
        self.dirX = 0.4328;#//-1;
        self.dirY = 0.9015;#//0
        self.planeX = 0.5950;#//0
        self.planeY = -0.2857;#//0.66
        #----------------------------
        self.colors = [0x000000, 0x800000, 0x2080C4, 0x000080, 0x00C0C0, 0xC0C000];
        self.w = res[0]
        self.h = res[1]
        self.TURNRIGHT,self.TURNLEFT,self.FWD,self.BACK = False,False,False,False
        
def rotate(v, angle=90):
    '''rotate vector v by angle degrees'''
    angle=angle * .0174 #degrees to radians
    x = v[0] * cos(angle) - v[1] * sin(angle);
    y = v[0] * sin(angle) + v[1] * cos(angle);
    return [x,y]

def vsum(v1, v2):
    '''return sum of 2D vectors v1 and v2'''
    return [v1[0] + v2[0], v1[1] + v2[1]]
   
def render(Game):
    '''draw the scene on the display'''
    for col in range(game.w):
        # calculate ray position and direction
        #       x-coord in camera space
        cameraX = float(2 * col / float(game.w) - 1)#NEW FLOAT
        rayPosX = game.posX
        rayPosY = game.posY
        rayDirX = game.dirX + game.planeX * cameraX
        rayDirY = game.dirY + game.planeY * cameraX# + .0000000001#*NEW
        #which map grid square we are in
        mapX = int(rayPosX); 
        mapY = int(rayPosY)
        #length of ray form current position to next x or y side
        'sideDistX = 0; sideDistY = 0'
        #length of ray from one x or y side to next x or y side
        if rayDirX == 0: rayDirX = 0.000001
        if rayDirY == 0: rayDirY = 0.000001
        
        deltaDistX = sqrt(1.0+ (rayDirY*rayDirY) / (rayDirX*rayDirX))#.0 i change
        deltaDistY = sqrt(1.0+ (rayDirX*rayDirX) / (rayDirY*rayDirY))
        perpWallDist = 0.0;
        '-----------------------------------'
        #what direction to step in x or y (either +1 or -1)
        stepX = 0;
        stepY = 0
        hit = 0  #was there a wall hit?
        side = 0 #was a NS or EW wall hit?
        
        if rayDirX < 0:
            stepX = -1;
            sideDistX = (rayPosX - mapX) * deltaDistX
        else:
            stepX = 1;
            sideDistX = (mapX+1.0 - rayPosX) * deltaDistX
            
        if rayDirY < 0:
            stepY = -1;
            sideDistY = (rayPosY - mapY) * deltaDistY
        else:
            stepY = 1;
            sideDistY = (mapY+1.0 - rayPosY) * deltaDistY

        #digital differential analysis
        hit = 0
        while hit == 0:
            #jump to next map square OR in x-dir OR in y-dir
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                side=0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side=1
            if (WORLDMAP[mapX][mapY] > 0):
                hit = 1

        #Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
        if side == 0:
            perpWallDist = abs((mapX - rayPosX + (1-stepX)/2) / rayDirX)#.0
        else:
            perpWallDist = abs((mapY - rayPosY + (1-stepY)/2) / rayDirY)#.0
        if perpWallDist ==0: perpWallDist = 0.000001
        #Calculate height of line to draw on screen
        lineHeight = abs(int(game.h / perpWallDist));
        #calculate lowest and highest pixel to fill in current stripe]
        drawStart = -lineHeight / 2 + game.h / 2;#*NEW .0
        drawEnd = lineHeight / 2 + game.h / 2;#*NEW .0
        #////////////////////////////////////////////////////////////
        #calculate value of wallX
        wallX = 0 #where exactly the wall was hit
        if (side == 1):
            wallX = rayPosX + ((mapY - rayPosY + (1 - stepY) / 2) / rayDirY) * rayDirX
        else:
            wallX = rayPosY + ((mapX - rayPosX + (1 - stepX) / 2) / rayDirX) * rayDirY;
        wallX -= math.floor((wallX));
        #/////////////DRAW THE "3D" WALLS/////////////////////
        color=game.colors[WORLDMAP[mapX][mapY]]
        if side==1: color= color/2
        #pygame.draw.line(VIDEO,color,(col,drawStart),(col,drawEnd))
        
        if drawStart<0:drawStart=0
        if drawEnd>=game.h:drawEnd=game.h-1
        pygame.draw.rect(VIDEO,color,(col, drawStart, 1, drawEnd-drawStart));
  
def inputHandler(game,event):
    if event.type == pygame.QUIT: game.RUNNING=False
    if event.type == pygame.KEYDOWN:
        print event.key
        if event.key == pygame.K_q: game.RUNNING=False
        if event.key == pygame.K_RIGHT: game.TURNRIGHT = True
        if event.key == pygame.K_LEFT: game.TURNLEFT = True
        if event.key == pygame.K_UP: game.FWD = True
        if event.key == pygame.K_DOWN: game.BACK = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT: game.TURNRIGHT = False
        if event.key == pygame.K_LEFT: game.TURNLEFT = False
        if event.key == pygame.K_UP: game.FWD = False
        if event.key == pygame.K_DOWN: game.BACK = False
        
def movePlayer(seconds,game):
    rotSpeed = seconds * 3.0
    if game.TURNRIGHT:
        game.dirX, game.dirY = rotate([game.dirX, game.dirY], -2)
        game.planeX, game.planeY = rotate((game.planeX,game.planeY),-2) 
        
    if game.TURNLEFT:
        game.dirX, game.dirY = rotate([game.dirX, game.dirY], 2)
        game.planeX, game.planeY = rotate((game.planeX,game.planeY),2)
        
    if game.FWD:
        game.posX, game.posY = vsum((game.posX,game.posY), (game.dirX*.08, game.dirY*.08))

    if game.BACK:
        game.posX, game.posY = vsum((game.posX,game.posY), (game.dirX*-.08, game.dirY*-.08))

game = GameObject([640,480])
VIDEO = pygame.display.set_mode((game.w,game.h))
clock = pygame.time.Clock();
WORLDMAP = [
    [1,1,1,1,1,1,1,1],
    [1,2,0,0,0,3,3,1],
    [1,0,0,0,0,0,2,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,5,1],
    [1,1,1,1,1,1,1,1]]

def main():
    while game.RUNNING:
        milliseconds = clock.tick_busy_loop(60)
        for event in pygame.event.get():
            inputHandler(game,event)
        movePlayer(milliseconds/1000,game)
        
        VIDEO.fill((0,0,0))
        pygame.draw.rect(VIDEO,0x555555,pygame.Rect(0,game.h/2,game.w,game.h));
        render(game)

        pygame.display.flip()
        pygame.display.set_caption('RenderTest Python: FPS: %.2f' %clock.get_fps())

main()
