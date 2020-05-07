# Breakball - a Breakout/Arkanoid clone

import pygame
import sys
import os
import random

# Menu function
def menu(textChoice):
    # Set up fonts
    font = pygame.font.SysFont(pygame.font.get_fonts()[0], 80, True)
    font2 = pygame.font.SysFont(pygame.font.get_fonts()[0], 20, True)

    # Render the text
    if textChoice == 'win':
        text = font.render('You Win', True, (0, 255, 0))
        text2 = font2.render('Press space to continue...', True, (255, 255, 255))
    elif textChoice == 'gameover':
        text = font.render('Game Over', True, (255, 0, 0))
        text2 = font2.render('Press space to continue...', True, (255, 255, 255))
    else:
        text = font.render('Breakball', True, (0, 150, 255))
        text3 = font.render('Breakball', True, (0, 0, 255))
        text2 = font2.render('Press space to begin...', True, (255, 255, 255))

    # Menu loop
    while True:
        pygame.time.delay(200)

        # Listen for the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Break the loop if space is pressed
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            break

        win.fill((0, 0, 0))

        # Show the text
        if not textChoice == 'win' and not textChoice == 'gameover':
            win.blit(text3, (screenWidth // 2 - text.get_width() // 2 + 2, 200 + 2))
        win.blit(text, (screenWidth // 2 - text.get_width() // 2, 200))
        win.blit(text2, (screenWidth // 2 - text2.get_width() // 2, 400))

        pygame.display.update()

# Function for detecting collision
def collision(x, y, width, height, x2, y2, width2, height2):
    if x2 - width <= x <= x2 + width2 and y2 - height <= y <= y2 + height2:
        return True
    else:
        return False

class Sprite:
    # Create a sprite object
    def __init__(self, x, y, width, height, vel, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img = img
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.visible = True

    # Show the sprite if visible is set to True
    def show(self, surface):
        if self.visible:
            surface.blit(self.img, (self.x, self.y))

class Ball(Sprite):
    # Create a ball object. Class Ball inherits from the class Sprite and adds two new attributes
    def __init__(self, x, y, width, height, xVel, yVel, img):
        super().__init__(x, y, width, height, 0, img)
        self.xVel = xVel
        self.yVel = yVel

def gameLoop():
    # Set up the clock
    FPS = 60
    clock = pygame.time.Clock()
    
    # Set up image variables
    ballImg = pygame.image.load(os.path.join('assets', 'ball.png'))
    paddleImg = pygame.image.load(os.path.join('assets', 'paddle.png'))
    blockImg = pygame.image.load(os.path.join('assets', 'block.png'))

    # Load the bounce sound
    bounceSound = pygame.mixer.Sound(os.path.join('assets', 'bounce.ogg'))

    # Create the paddle and the ball
    paddle = Sprite(screenWidth // 2 - 100 // 2, 450, 100, 20, 5, paddleImg)
    ball = Ball(screenWidth // 2 - 20 //2, paddle.y - 20, 20, 20, 5, 5, ballImg)

    # Create the blocks
    blockX = 0
    blockY = 50
    blockCounter = 0
    blocks = [[], []]
    for i in range(2):
        for j in range(10):
            blocks[i].append(Sprite(blockX, blockY, 50, 50, 0, blockImg))
            blockX += 50
            blockCounter += 1
        blockX = 0
        blockY += 50

    # Main game loop
    while True:
        # Tick the clock
        clock.tick(FPS)

        # Listen for the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the paddle
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle.x > 0:
            paddle.x -= paddle.vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle.x < screenWidth - paddle.width:
            paddle.x += paddle.vel

        # Bounce the ball off the walls
        if ball.x <= 0 or ball.x >= screenWidth - ball.width:
            ball.xVel = -ball.xVel
            bounceSound.play()
        if ball.y <= 0:
            ball.yVel = -ball.yVel
            bounceSound.play()

        # Bounce the ball off the paddle
        if paddle.x - ball.width // 2 <= ball.x <= paddle.x + paddle.width - \
           ball.width // 2 and ball.y + ball.height == paddle.y:
            ball.yVel = -ball.yVel
            bounceSound.play()

        # Check for collision with blocks
        for i in range(2):
            for block in blocks[i]:
                if block.visible and \
                        collision(ball.x, ball.y, ball.width, ball.height, block.x, block.y, block.width, block.height):
                    block.visible = False
                    blockCounter -= 1
                    # Randomize the bounce direction
                    bounceX = random.choice([True, False])
                    ball.yVel = -ball.yVel
                    if bounceX:
                        ball.xVel = -ball.xVel
                    bounceSound.play()

        # End the game if the player knocks all the blocks out
        if blockCounter <= 0:
            # Stop the game music and play the win music
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            pygame.mixer.music.load(os.path.join('assets', 'win.ogg'))
            pygame.mixer.music.play(-1, 0.0)
            menu('win')
            pygame.mixer.music.stop()
            # Play the game music again
            pygame.mixer.music.load(os.path.join('assets', 'theme.ogg'))
            pygame.mixer.music.play(-1, 0.0)
            break

        # End the game if the player misses the ball
        if ball.y > screenWidth:
            # Stop the game music and play the game over music
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            pygame.mixer.music.load(os.path.join('assets', 'gameover.ogg'))
            pygame.mixer.music.play(-1, 0.0)
            menu('gameover')
            pygame.mixer.music.stop()
            # Play the game music again
            pygame.mixer.music.load(os.path.join('assets', 'theme.ogg'))
            pygame.mixer.music.play(-1, 0.0)
            break

        # Move the ball
        ball.x += ball.xVel
        ball.y += ball.yVel

        # Show the ball and the paddle
        ball.show(win)
        paddle.show(win)

        # Show the blocks
        for i in range(2):
            for block in blocks[i]:
                block.show(win)

        # Update and refresh the screen
        pygame.display.update()
        win.fill((0, 0, 0))

# Main program
def main():
    # Create the game window
    global screenWidth, screenHeight, win
    screenWidth = 500
    screenHeight = 500
    pygame.init()
    win = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Breakball')
    pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'icon.png')))

    # Play the menu music and stop it when the menu ends
    pygame.mixer.music.load(os.path.join('assets', 'menu.ogg'))
    pygame.mixer.music.play(-1, 0.0)
    menu('')
    pygame.mixer.music.stop()
    # Play the game music
    pygame.mixer.music.load(os.path.join('assets', 'theme.ogg'))
    pygame.mixer.music.play(-1, 0.0)
    
    # Main loop
    while True:
        gameLoop()

# Run the program
if __name__ == '__main__':
    main()
