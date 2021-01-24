import matplotlib.pyplot as plt
from matplotlib import animation
from Neural_Network import *
from flappy_brain import *
import seaborn as sns


def nextGeneration():
    print(output_list)
    big_brain = output_list.index(max(output_list))
    for x in range(slave_birds):
        monokuma = Bird(x, deepcopy(bird_brains[big_brain]))
        if x != 0:
            monokuma.brain.mutate(0.1)
        bird_group.add(monokuma)

def init_pipes():
    global time_now
    global last_pipe
    time_now = pygame.time.get_ticks()
    pipe_height = random.randint(-100, 100)
    btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
    top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
    pipe_group.add(btm_pipe)
    pipe_group.add(top_pipe)
    last_pipe = time_now

def calculate_fitness():
    sum = 0
    for bird in bird_group.sprites():
        sum += bird.score

    for bird in bird_group.sprites():
        fitness = bird.score / sum


#create groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#start birds
for x in range(slave_birds):
    monokuma = Bird(x)
    bird_group.add(monokuma)

init_pipes()

run = True
while run:
    clock.tick(fps)
    screen.fill((0, 0, 0))

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
            bird.score += 0.01

    #print(output_list)

    #look for collision
    for bird in bird_group.sprites():
        """
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
            bird.die = True
        """
        if pygame.sprite.spritecollide(bird, pipe_group, False, False) or bird.rect.top < 0:
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


    if len(bird_group.sprites()) == 0:
        for pipe in pipe_group.sprites():
            pipe.kill()
        init_pipes()
        nextGeneration()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
        
print(output_list)
pygame.quit()