import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

DIRECTS = [[0, -1],[1, 0],[0, 1],[-1, 0]]


class Player:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'player'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5

        self.attackTimer = 0
        self.attackDelay = 60
        self.attackSpeed = 5
        self.attackDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
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

        if keys[self.keySHOT] and self.attackTimer == 0:
            dx = DIRECTS[self.direct][0] * self.attackSpeed
            dy = DIRECTS[self.direct][1] * self.attackSpeed
            Attack(self, self.rect.centerx, self.rect.centery, dx, dy, self.attackDamage)
            self.attackTimer = self.attackDelay

        if self.attackTimer > 0: self.attackTimer -= 1

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(window,'white', self.rect.center, (x, y), 4)
    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')

class Attack:
    def __init__(self, parent, px, py, dx, dy, damage):
        attacks.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            attacks.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    attacks.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)

attacks = []
objects = []
Player('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Player('red', 250, 500, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for attack in attacks: attack.update()
    for obj in objects: obj.update()

    window.fill('black')
    for attack in attacks: attack.draw()
    for obj in objects: obj.draw()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()