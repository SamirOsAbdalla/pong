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
        self.__height = 200
        self.__width = 12
        self.__color = color
        self.__x_offset = 10
        self.__pkt = player_key_type
        self.__y_vel = 5

        if(player_key_type == PlayerKeyType["WASD"]):
            ## rect is all the way to the left
            self.__rect = pygame.Rect(self.__x_offset, 
                                    (SCREEN_HEIGHT // 2)  - (self.__height // 2),
                                    self.__width,
                                    self.__height
                                    )
        else:
            ## rect is all the way to the right
            self.__rect = pygame.Rect(SCREEN_WIDTH - self.__width - self.__x_offset, 
                                    (SCREEN_HEIGHT // 2)  - (self.__height // 2),
                                    self.__width,
                                    self.__height
                                    )

    def move_player_up(self):
        self.__rect.top -= self.__y_vel
        if(self.__rect.top < 0):
            self.__rect.top = 0

    def move_player_down(self):
        self.__rect.top += self.__y_vel
        if(self.__rect.bottom > SCREEN_HEIGHT):
            self.__rect.bottom = SCREEN_HEIGHT

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

        if(self.__pkt == PlayerKeyType["WASD"]):
            self.handle_wasd_click(keys)
        else:
            self.handle_arrows_click(keys)

    def draw(self):
        pygame.draw.rect(screen, self.__color, self.__rect)

    def update(self):
        self.player_input()

class Ball():
    def __init__(self):
        self.__width = 20
        self.__height = 20
        self.__rect = pygame.Rect((SCREEN_WIDTH // 2) - (self.__width // 2),
                                  (SCREEN_HEIGHT // 2) - (self.__height // 2),
                                    self.__width,
                                    self.__height
                                )
        self.__y_vel = 10
        self.__x_vel = 10

    def move_y(self):
        self.__rect.top += self.__y_vel

    def move_x(self):
         self.__rect.left += self.__y_vel

    def move_ball(self):
        self.move_y()
        self.move_x()

    def draw(self):
        pygame.draw.rect(screen, "White", self.__rect)
    
    def update(self):
        self.move_ball()

player1 = Player(PlayerKeyType["WASD"], "Blue")
player2 = Player(PlayerKeyType["ARROWS"], "Red")

## GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill("black")
    player1.draw()
    player2.draw()

    player1.update()
    player2.update()

    pygame.display.update()
    clock.tick(60)
