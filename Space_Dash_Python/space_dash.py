import pygame
import random
import time

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0,0,225)
gray = (112,128,144)
pygame.init()

# resolution - width,height
screenWidth = 1200
screenHeight = 700
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Space Dash')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

img = pygame.image.load('ship.png')
img_width = img.get_size()[0]
img_height = img.get_size()[1]


def show_score(current_score):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Score:' + str(current_score), True, white)
    screen.blit(text, [3, 3])


def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(screen, gray, [x_block, y_block, block_width, block_height])
    pygame.draw.rect(screen, gray, [x_block, y_block + block_height + gap, block_width, screenHeight])


def makeTextObjs(text, font):
    textscreen = font.render(text, True, white)
    return textscreen, textscreen.get_rect()


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key
    return None


def msg_screen(text):
    smallText = pygame.font.Font('freesansbold.ttf', 25)
    largeText = pygame.font.Font('freesansbold.ttf', 75)

    titletextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = screenWidth / 2, screenHeight / 2
    screen.blit(titletextSurf, titleTextRect)

    typtextSurf, typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center = screenWidth / 2, ((screenHeight / 2) + 100)
    screen.blit(typtextSurf, typTextRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()

    main()


def gameOver():
    msg_screen('Game over')


def bird(x, y, image):
    screen.blit(image, (x, y))


def main():
    x = 150
    y = 200
    y_move = 0

    x_block = screenWidth
    y_block = 0

    block_width = 25
    block_height = random.randint(0, screenHeight / 2)
    gap = img_height * 5

    # speed of blocks
    block_move = 5

    score = 0
    game_over = False

    # Game Loop/ Game State
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # keydown - when button is pressed keyup - when it's released
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 5

        y = y + y_move

        bg = pygame.image.load('bg.jpg')
        screen.blit(bg, (0,0))
        bird(x, y, img)
        show_score(score)

        # Adding difficulty relative to score
        # Increasing the speed and decreasing the gap of blocks

        if 3 <= score < 5:
            block_move = 6
            gap = img_height * 3.3

        if 5 <= score < 8:
            block_move = 7
            gap = img_height * 3.1

        if 8 <= score < 14:
            block_move = 8
            gap = img_height * 3

        if score >= 14:
            block_move = 8
            gap = img_height * 2.5

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        # boundaries
        if y > screenHeight - img_height or y < 0:
            gameOver()

        # blocks on screen or not
        if x_block < (-1 * block_width):
            x_block = screenWidth
            block_height = random.randint(0, screenHeight / 2)

        # Collision Detection

        # detecting whether we are past the block or not in X
        if x + img_width > x_block and x < x_block + block_width:
            if y < block_height or y + img_height > block_height + gap:
                gameOver()

        if x > x_block + block_width and x < x_block + block_width + img_width / 5:
            score += 1

        pygame.display.update()
        clock.tick(80)


main()
pygame.quit()
quit()