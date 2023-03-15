import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60 

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("win the game!!")

tile_size = 50


bj_image = pygame.image.load('img/background.jpg')
sun_image = pygame.image.load('img/sun.png')
img1 = pygame.transform.scale(bj_image,(800,800))
img2 = pygame.transform.scale(sun_image,(80,80))

class player():
    def __init__(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'img/palyer{num}.png')
            img_right = pygame.transform.scale(img_right,(50,50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left) 
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0        
    def update(self):
        dx = 0
        dy = 0
        circulation_cooldown = 5
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
            
        if key[pygame.K_SPACE] == False:
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False :
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]        
        
        if self.counter > circulation_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
              self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
                
     
        
        self.vel_y += 1
        if self.vel_y > 10 :
            self.vel_y = 10
                
        dy += self.vel_y        
        
        
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx,self.rect.y, self.width,self.height):
                dx = 0
                
            if tile[1].colliderect(self.rect.x,self.rect.y + dy, self.width,self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
        
        
        
        
        
            
        
        
        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0 
        
        
        
        
        
        
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        
class World():
    def __init__(self,data):
        
        self.tile_list = []
        grass_image = pygame.image.load('img/dirt.png')
        border_image = pygame.image.load('img\land.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_image, (50,50))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size         
                    img_rect.y = row_count * tile_size
                    
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img1 = pygame.transform.scale(border_image, (50,50))
                    img_rect1 = img1.get_rect()
                    img_rect1.x = col_count * tile_size
                    img_rect1.y = row_count * tile_size
                    tile = (img1,img_rect1)
                    self.tile_list.append(tile) 
                if tile == 3:
                    img = enemy(col_count * tile_size, row_count * tile_size + 15)
                    enemy_group.add(img)
                col_count += 1
            row_count += 1 
                 
    def draw(self):
       for tile in self.tile_list:
           screen.blit(tile[0],tile[1])
           pygame.draw.rect(screen, (255,255,255), tile[1],2)             


class enemy (pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/enemy1.png')
        img = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    
    
    
    
    
world_data = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,0,1,1,0,0,1,1,1,0,0,1,1,2],
    [2,0,0,0,0,0,0,0,0,0,3,3,0,0,0,2],
    [2,1,1,1,0,0,0,1,0,1,1,1,0,0,1,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,1,1,1,1,1,0,0,1,1,1,1,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,0,0,1,1,1,0,0,1,1,1,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,0,0,1,1,0,1,1,0,1,1,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2], 
    [2,0,0,0,0,0,0,0,0,3,0,0,3,0,0,2],
    [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
]



player = player(100,screen_height - 130)

enemy_group = pygame.sprite.Group()

world = World(world_data)
run = True
while run:
    
    clock.tick(fps)
    
    screen.blit(img1,(0,0))
    screen.blit(img2,(50,50))

    
    world.draw()
    enemy_group.draw(screen)
    player.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
    
    pygame.display.update()
            
pygame.quit()