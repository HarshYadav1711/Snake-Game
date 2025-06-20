import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255,255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating Game window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("SNAKES")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Creating Text on screen
def text_screen(text, color, x, y):
    screen_text = font.render((text), True, color)
    gameWindow.blit(screen_text, [x,y])

# Creating The Snake Body
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect (gameWindow, color, [x, y, snake_size, snake_size])

# Creating Welcome Window
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,220,229))
        text_screen("Welcome to snakes", black, 260, 250)
        text_screen("Press space to play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('new.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 10
    snake_size = 10
    fps = 60
    snk_list = []
    snk_len = 1

    # Check if highscore file exists
    if(not os.path.exists("highscore,txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt") as f:
        highscore = f.read()

# Height of food
    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)
    score = 0

# Main loop
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(white)
            text_screen("Game over! Press enter to continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                snake_x += velocity_x
                snake_y += velocity_y

                if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                    score += 10
                    food_x = random.randint(20, screen_width // 2)
                    food_y = random.randint(20, screen_height // 2)
                    snk_len += 5
                    if score>int(highscore):
                        highscore = score

                gameWindow.fill(white)
                gameWindow.blit(bgimg, (0,0))
                text_screen("Score: "+ str(score) + " Highscore: "+str(highscore), red, 5, 5)
                pygame.draw.rect (gameWindow, red, [food_x, food_y, snake_size, snake_size])

                head = []
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)

                if len(snk_list) > snk_len:
                    del snk_list[0]

                if head in snk_list[:-1]:
                    game_over = True
                    pygame.mixer.music.load('game over.mp3')
                    pygame.mixer.music.play()

                if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                    game_over = True
                    pygame.mixer.music.load('game over.mp3')
                    pygame.mixer.music.play()
                plot_snake(gameWindow, black, snk_list, snake_size)
            pygame.display.update()
            clock.tick(fps)

    pygame.quit()
    quit()
welcome()