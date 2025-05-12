from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, s_width, s_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (s_width, s_height))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width-self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('pyla.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

score = 0
goal = 10
lost = 0
max_lost = 3
life = 3

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()


win_width = 2200
win_height = 1200
window = display.set_mode((win_width, win_height))
display.set_caption('shooooooooooooooooooter')
backround = transform.scale(
    image.load('backgrount.png'),
    (win_width, win_height)
)

player = Player('ar15.png', win_width / 2, win_height - 100, 100, 100, 20)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('vorox.png', randint(
        80, win_width - 80), -40, 50, 80, randint(1, 5))
    monsters.add(monster)


clock = time.Clock()
FPS = 90
finish = False

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            player.fire()

    if not finish:
        window.blit(backround, (0, 0))
        player.update()
        player.draw()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

    clock.tick(FPS)

    display.update()