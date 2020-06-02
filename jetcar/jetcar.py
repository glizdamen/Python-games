import pygame
import sys
import os
import random

class Sprite:
    def __init__(self, x, y, vel, width, height, img):
        self.x, self.y = x, y
        self.vel = vel
        self.width, self.height = width, height
        self.img = img

    def show(self, surface):
        surface.blit(self.img, (self.x, self.y))

def collision(x, y, width, height, x2, y2, width2, height2):
    if x2 - width <= x <= x2 + width2 and y2 - height <= y <= y2 + height2:
        return True
    else:
        return False
    
def menu(mode, *score):
    font = pygame.font.Font(os.path.join('assets', 'font.TTF'), 100)
    font2 = pygame.font.Font(os.path.join('assets', 'font.TTF'), 40)

    transparent = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'menu.png')).convert(),
                                                                                            (screenWidth, screenHeight))
    transparent.set_alpha(200)

    if mode == 'main':
        text = font.render('JetCar', True, (0, 0, 255))
        text2 = font.render('JetCar', True, (0, 150, 255))
        text3 = font2.render('Press  space  to  begin', True, (0, 0, 255))

        background = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'road0.png')).convert(),
                                                                                            (screenWidth, screenHeight))

        win.blit(background, (0, 0))
        win.blit(transparent, (0, 0))
        win.blit(text, (screenWidth // 2 - text.get_width() // 2 + 3, screenHeight // 2 - text.get_height() // 2 + 3))
        win.blit(text2, (screenWidth // 2 - text2.get_width() // 2, screenHeight // 2 - text2.get_height() // 2))
        win.blit(text3, (screenWidth // 2 - text3.get_width() // 2, 400))
    else:
        text = font.render('Game Over', True, (255, 0, 0))
        text2 = font2.render('Press  space  to  continue', True, (0, 0, 255))
        text3 = font2.render(f'Score  {score[0]}', True, (0, 200, 0))

        win.blit(transparent, (0, 0))
        win.blit(text, (screenWidth // 2 - text.get_width() // 2, screenHeight // 2 - text.get_height() // 2))
        win.blit(text2, (screenWidth // 2 - text2.get_width() // 2, 400))
        win.blit(text3, (screenWidth // 2 - text3.get_width() // 2, 400 - text3.get_height() - 15))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            break

def gameLoop():
    clock = pygame.time.Clock()
    fps = 60
    frameCount = 0

    pygame.mixer.music.load(os.path.join('assets', 'theme.ogg'))
    pygame.mixer.music.play(-1)
    hitSound = pygame.mixer.Sound(os.path.join('assets', 'hit.ogg'))

    playerWidth, playerHeight = 9 * pixelSize, 16 * pixelSize
    playerImg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'cars', 'player.png')).convert_alpha(),
                                                                                            (playerWidth, playerHeight))
    player = Sprite(screenWidth // 2 - playerWidth // 2, screenHeight // 2 + playerHeight - pixelSize * 10, 10,
                                                                                playerWidth, playerHeight, playerImg)
    font = pygame.font.Font(os.path.join('assets', 'font.TTF'), 64)
    score = 0

    backgrounds = []
    for i in range(2):
        backgrounds.append(Sprite(0, 0, 10, screenWidth, screenHeight, pygame.transform.scale(pygame.image.load(
                            os.path.join('assets', f'road{i}.png')).convert(), (screenWidth, screenHeight))))
    backgrounds[1].y = -screenHeight

    carWidth, carHeight = 9 * pixelSize, 12 * pixelSize
    carImg = []
    for i in range(9):
        carImg.append(pygame.transform.scale(pygame.image.load(os.path.join('assets', 'cars', f'car{i}.png'))
                                             .convert_alpha(), (carWidth, carHeight)))
    carPos = [9 * pixelSize, 21 * pixelSize, 33 * pixelSize]
    cars = []

    run = True
    while run:
        clock.tick(fps)

        if frameCount >= fps * 3 and frameCount % fps * 2 == 0:
            cars.append(Sprite(carPos[random.randrange(len(carPos))], -carHeight, 5, carWidth,
                               carHeight, carImg[random.randrange(len(carImg))]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x >= pixelSize * 8:
            player.x -= player.vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player.width <= screenWidth - pixelSize * 8:
            player.x += player.vel

        for background in backgrounds:
            if background.y >= screenHeight:
                background.y = -screenHeight
            background.y += background.vel
            background.show(win)

        win.blit(font.render(str(score), True, (0, 0, 0)), (3, -13))


        for car in cars:
            if car.y >= screenHeight:
                del car
            elif collision(car.x + pixelSize, car.y + pixelSize, car.width - 2 * pixelSize, car.height - 2 * pixelSize,
                           player.x + pixelSize, player.y, player.width - 2 * pixelSize, player.height - 4 * pixelSize):
                for car in cars:
                    car.show(win)
                player.show(win)
                pygame.mixer.music.stop()
                hitSound.play()
                menu('gameover', score)
                run = False
            else:
                car.y += car.vel
                car.show(win)

        player.show(win)

        pygame.display.update()
        win.fill((0, 0, 0))
        frameCount += 1
        if frameCount % fps * 2 == 0:
            score += 1

def main():
    global screenWidth, screenHeight, win, pixelSize
    pixelSize = 10
    screenWidth, screenHeight = 51 * pixelSize, 51 * pixelSize
    pygame.init()
    win = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('JetCar')
    pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'icon.png')))
    pygame.mixer.music.load(os.path.join('assets', 'menu.ogg'))
    pygame.mixer.music.play(-1)
    menu('main')
    pygame.mixer.music.stop()
    while True:
        gameLoop()

if __name__ == '__main__':
    main()
