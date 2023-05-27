import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 32

label = pygame.font.Font('Font/Sitka.ttc', 20)
GameOver1_label = label.render('Игра окончена. Один из игроков собрал 7 монет!', True, (255, 255, 255))
GameOver2_label = label.render('Игра окончена. Один из игроков уничтожен!', True, (255, 255, 255))

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)

imgBrick = pygame.image.load('images/stonebrick.png')
imgPlayers = [
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
    pygame.image.load('images/player1.png'),
]


imgExplosions = [
    pygame.image.load('images/explosion1.png'),
    pygame.image.load('images/explosion2.png'),
    pygame.image.load('images/explosion3.png'),
    pygame.image.load('images/explosion4.png'),
]
imgCoin = [
    pygame.image.load('images/coin.png')]


DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'player':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1


class Player:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'player'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = 5
        self.shotTimer = 0

        self.moveSpeed = 2
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgPlayers[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgPlayers[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect) or obj != self and obj.type == 'player' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1



    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            global gameplay
            gameplay = False
            objects.remove(self)


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'explosion' and obj.type != 'coin':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Explosion(self.px, self.py)
                        break

    def draw(self):
        pygame.draw.circle(window, 'purple', (self.px, self.py), 2)


class Explosion:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'explosion'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.25
        if self.frame >= 3: objects.remove(self)

    def draw(self):
        image = imgExplosions[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)


class Coin:
    def __init__(self, px, py, coinNum):
        objects.append(self)
        self.type = 'coin'

        self.image = imgCoin[coinNum]
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 600
        self.coinNum = coinNum

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'player' and self.rect.colliderect(obj.rect):
                if self.coinNum == 0:
                    if obj.rank >= 0:
                        obj.rank += 1
                        objects.remove(self)
                        break


    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


bullets = []
objects = []
Player('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Player('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SLASH))
ui = UI()

for _ in range(100):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True

        if not fined: break

    Block(x, y, TILE)

coinTimer = 180


Dead = False
gameplay = True
play = True
while play:

    if gameplay:
        keys = pygame.key.get_pressed()

        if coinTimer > 0:
            coinTimer -= 1
        else:
            Coin(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgCoin) - 1))
            coinTimer = randint(120, 240)

        for bullet in bullets: bullet.update()
        for obj in objects: obj.update()
        ui.update()

        window.fill('black')
        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()
        ui.draw()

        for obj in objects:
            if obj.type == 'player':
                if obj.rank == 7 or obj.hp <= 0:
                    Dead = True
                    gameplay = False


    elif Dead == True and gameplay == False:
        window.fill((30,30,30))
        window.blit(GameOver1_label, (150, 300))
    else:
        window.fill((30,30,30))
        window.blit(GameOver2_label, (150, 300))

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False


pygame.quit()