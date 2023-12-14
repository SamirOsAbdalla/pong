import pygame
from sys import exit
from enum import Enum


## HELPER VARIABLES
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
class PlayerKeyType(Enum):
    WASD = 0
    ARROWS = 1
####################

## INIT
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
#######


class Player():
    def __init__(self, player_key_type, color):
        self._height = 200
        self._width = 15
        self._color = color
        self._x_offset = 10
        self._pkt = player_key_type
        self._y_vel = 15

        if(player_key_type == PlayerKeyType["WASD"]):
            ## rect is all the way to the left
            self._rect = pygame.Rect(self._x_offset, 
                                    (SCREEN_HEIGHT // 2)  - (self._height // 2),
                                    self._width,
                                    self._height
                                    )
        else:
            ## rect is all the way to the right
            self._rect = pygame.Rect(SCREEN_WIDTH - self._width - self._x_offset, 
                                    (SCREEN_HEIGHT // 2)  - (self._height // 2),
                                    self._width,
                                    self._height
                                    )

    def move_player_up(self):
        self._rect.top -= self._y_vel
        if(self._rect.top < 0):
            self._rect.top = 0

    def move_player_down(self):
        self._rect.top += self._y_vel
        if(self._rect.bottom > SCREEN_HEIGHT):
            self._rect.bottom = SCREEN_HEIGHT

    def handle_wasd_click(self, keys):
        if(keys[pygame.K_w]):
           self.move_player_up()
        if(keys[pygame.K_s]):
           self.move_player_down()
              
    def handle_arrows_click(self, keys):
        if(keys[pygame.K_UP]):
            self.move_player_up()
        if(keys[pygame.K_DOWN]):
           self.move_player_down()

    def player_input(self):
        keys = pygame.key.get_pressed()

        if(self._pkt == PlayerKeyType["WASD"]):
            self.handle_wasd_click(keys)
        else:
            self.handle_arrows_click(keys)
    
    def draw(self):
        pygame.draw.rect(screen, self._color, self._rect)

    def update(self):
        self.player_input()

class Ball():
    def __init__(self):
        self._width = 14
        self._height = 14
        self._rect = pygame.Rect((SCREEN_WIDTH // 2) - (self._width // 2),
                                  (SCREEN_HEIGHT // 2) - (self._height // 2),
                                    self._width,
                                    self._height
                                )
        self._y_vel = 4
        self._x_vel = -5

    ## ball movement methods

    def move_y(self):
        self._rect.top += self._y_vel

    def move_x(self):
         self._rect.left += self._x_vel

    def move_ball(self):
        self.move_y()
        self.move_x()

    ########################

    ## collision methods

    def check_wall_collision(self):
        pass
    
    def check_player_collision(self, player1,player2):
        if(self._rect.colliderect(player1._rect)):
            return "player1"
        elif(self._rect.colliderect(player2._rect)):
            return "player2"
        return None
    
    def check_collision(self, player1, player2):
        self.handle_wall_collision()

        collision_res = self.check_player_collision(player1,player2)
        if(collision_res == "player1"):
            self.handle_player_collision(player1)
        elif(collision_res == "player2"):
            self.handle_player_collision(player2)
        

    def handle_wall_collision(self):
        ## top and bottom wall collision
        if(self._rect.top <= 0):
            self._rect.top = 0
            self._y_vel *= -1
        elif (self._rect.bottom > SCREEN_HEIGHT):
            self._rect.bottom = SCREEN_HEIGHT-1
            self._y_vel *= -1

    def handle_player_collision(self, player):
        if(abs(self._rect.right - player._rect.right) <= self._width
           and self._x_vel < 0):
            self._x_vel *= -1.5
        elif(abs(self._rect.left - player._rect.left) <= self._width
           and self._x_vel > 0):
            self._x_vel *= -1.5
        elif(abs(self._rect.bottom - player._rect.top) < self._height and self._y_vel > 0):
            self._y_vel *= -1
        elif(abs(self._rect.top- player._rect.bottom) < self._height and self._y_vel < 0):
            self._y_vel *= -1
    
    ########################

    def draw(self):
        pygame.draw.rect(screen, "White", self._rect)
    
    def update(self):
        self.move_ball()

player1 = Player(PlayerKeyType["WASD"], "Blue")
player2 = Player(PlayerKeyType["ARROWS"], "Red")
ball = Ball()

def check_collisions():
    ball.check_collision(player1, player2)

## GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")

    check_collisions()

    ball.draw()
    player1.draw()
    player2.draw()

    ball.update()
    player1.update()
    player2.update()
    
    pygame.display.update()
    clock.tick(60)
