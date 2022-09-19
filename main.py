import sys
import pygame
from pygame.locals import *

# number of frames per second
# change this value to speed up or slow down your game
FPS = 200

# global vars
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# set up the colours
BLACK = (0  ,0  ,0  )
WHITE = (255,255,255)

# draws the arena the game will be played in. 
def draw_arena():
    DISPLAYSURF.fill((0,0,0))
    # draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    # draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (LINETHICKNESS/4))

# draws the paddle
def draw_paddle(paddle):
    # stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)
  
# draws the ball
def draw_ball(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)
    
# moves the ball return new position
def move_ball(ball, balldirx,balldiry):
    ball.x+=balldirx
    ball.y+=balldiry
    return ball

# check for collision with a wall
def check_edge_collision(ball,balldirx,balldiry):
    if ball.top==(LINETHICKNESS) or ball.bottom==(WINDOWHEIGHT - LINETHICKNESS): 
        balldiry=balldiry*-1
    if ball.left==(LINETHICKNESS) or ball.right==(WINDOWWIDTH-LINETHICKNESS):
       balldirx=balldirx*-1
    return balldirx, balldiry   

#check for collision with a paddle
def check_hit_ball(ball,paddle1,paddle2,balldirx):
    if balldirx == -1 and paddle1.right==ball.left and paddle1.top<ball.top and paddle1.bottom>ball.bottom:
        return -1
    elif balldirx == 1 and paddle2.left==ball.right and paddle2.top<ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: 
        return 1

# checks to see if a point has been scored returns new score
def checkpoint_scored(paddle1, ball, score, balldirx):
    # reset points if left wall is hit
    if ball.left == LINETHICKNESS: 
        return 0
    # 1 point for hitting the ball
    elif balldirx == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    # 5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    # if no points scored, return score unchanged
    else: 
        return score

# computer intelligence
def artificial_intelligence(ball,balldirx,paddle2):
    # if ball is moving away from paddle, center bat
    if balldirx == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 1
    # if ball is moving toward paddle, track it
    elif balldirx == 1:
        if paddle2.centery < ball.centery: 
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2        

# display current score on the screen
def display_score(score):
    resultsurf=basicfont.render("score =%s" %(score), True, WHITE)
    resultrect=resultsurf.get_rect()
    resultrect.topleft=(WINDOWWIDTH -150,25)
    DISPLAYSURF.blit(resultsurf, resultrect)

# main function
def main():
    pygame.init()
    global DISPLAYSURF
    
    # font information
    global basicfont, basicfontsize
    basicfontsize=20
    basicfont=pygame.font.Font("freesansbold.ttf", basicfontsize)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Carl Pong')

    # initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
    score=0
    
    # keep tracks of ball direction
    balldirx=-1 #-1=left, +1=right
    balldiry=-1 #-1=up, +1=down

    # creates rectangles for ball and paddles.
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    score = checkpoint_scored(paddle1,ball,score,balldirx)

    # draws the starting position of the Arena
    draw_arena()
    draw_paddle(paddle1)
    draw_paddle(paddle2)
    draw_ball(ball)

    pygame.mouse.set_visible(0) #make mouse cursor invisible

    # main game loop
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type==MOUSEMOTION:
                mousex,mousey = event.pos
                paddle1.y=mousey

        draw_arena()
        draw_paddle(paddle1)
        draw_paddle(paddle2)
        draw_ball(ball)
        
        ball = moveball(ball, balldirx, balldiry)
        balldirx, balldiry = check_edge_collision(ball,balldirx,balldiry)
        score = checkpoint_scored(paddle1, ball, score, balldirx)
        paddle2 = artificial_intelligence (ball, balldirx, paddle2)
        balldirx = balldirx * checkhitball(ball,paddle1,paddle2, balldirx)
        
        displayscore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
