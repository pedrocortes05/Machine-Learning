import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from Neural_Network import *
from flappy_brain import *

#create groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

for x in range(slave_birds):
    monokuma = Bird(100, int(screen_height / 2), x)
    bird_group.add(monokuma)

time_now = pygame.time.get_ticks()
pipe_height = random.randint(-100, 100)
btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
pipe_group.add(btm_pipe)
pipe_group.add(top_pipe)
last_pipe = time_now


run = True
while run:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    #screen.blit(bg, (0,0))
    #screen.blit(bg, (0,468))

    bird_group.draw(screen)
    bird_group.update(pipe_group.sprites())
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
        
print(output_list)
pygame.quit()