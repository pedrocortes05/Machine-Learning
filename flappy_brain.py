import pygame
from pygame.locals import *
import random
import time
from Neural_Network import NeuralNetwork
import numpy as np


pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Brain")

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 300
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
slave_birds = 100
output_list = [0] * slave_birds

#load images
bg = pygame.image.load("Sprites/background.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, bird_number):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.die = False
        self.score = 0
        self.pass_pipe = False
        self.inputs = np.zeros((5, 1))
        self.bird_number = bird_number
        self.brain = NeuralNetwork(5, 2, 1)
        """
        for num in [14, 11, 10]:
            img = pygame.image.load(f"Sprites/Danganronpa_1_Monokuma_Fullbody_Sprite_{num}.png")
            self.images.append(img)
        """
        self.images.append(pygame.image.load("Sprites/Danganronpa_1_Monokuma_Fullbody_Sprite_14.png"))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0

    def jump(self):
        self.vel = -10

    def think(self, pipes):
        self.inputs[0, 0] = self.rect.y / screen_height
        self.inputs[1, 0] = self.vel
        self.inputs[2, 0] = pipes[0].rect.top / screen_height
        self.inputs[3, 0] = pipes[0].rect.bottom / screen_height
        self.inputs[4, 0] = pipes[0].rect.left / screen_width
        #print(self.inputs)
        self.output = self.brain.feed_forward(self.inputs)

        if self.output > 0.5:
            self.jump()

    def update(self, pipes):
        #gravity
        if not self.die:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
                
            #jump
            self.think(pipes)
            #self.jump()

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
        
            #rotate
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            output_list[self.bird_number] = self.score
            print("berd ded")
            self.kill()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/pipe.png")
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

"""
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

monokuma = Bird(100, int(screen_height / 2))
bird_group.add(monokuma)

run = True
while run:
    clock.tick(fps)

    #screen.blit(bg, (0,0))
    #screen.blit(bg, (0,468))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #check the score
    if len(pipe_group) > 0:
        for bird in bird_group.sprites():
            if bird.rect.left > pipe_group.sprites()[0].rect.left and bird.rect.right < pipe_group.sprites()[0].rect.right and not bird.pass_pipe:
                bird.pass_pipe = True
            if bird.pass_pipe and not bird.die:
                if bird.rect.left > pipe_group.sprites()[0].rect.right:
                    bird.score += 1
                    bird.pass_pipe = False
                    print(bird.score)

    #look for collision
    #TODO loop
    for bird in bird_group.sprites():
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
            bird.die = True

    #check if every fucking berd is ded
    for bird in bird_group.sprites():
        if not bird.die:
            game_over == False
            break
        game_over == True


    #check if bird has hit the ground
    for bird in bird_group.sprites():
        if bird.rect.bottom >= 768:
            bird.die = True

    if not game_over:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #TODO scroll the ground

        pipe_group.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
        

pygame.quit()
"""