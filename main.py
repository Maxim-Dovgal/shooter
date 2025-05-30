from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

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

class Boss(GameSprite):
    hp = 19
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.hp <= 0:
            self.rect.y = -100
            self.hp = 19
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
boss = Boss("vorox.png", randint(80, win_width - 80), -40, 80, 120, 1)

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
        collides = sprite.groupcollide(monsters, bullets, True, True)
        boss.update()
        boss.draw()
        if life <= 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (1040, 570))
        
        if score >= goal:
            finish = True
            window.blit(win, (1040, 570))
        if sprite.spritecollide(boss, bullets, False):
            boss.hp -= 1
            sprite.spritecollide(boss, bullets, True)
        for c in collides:
            score = score + 1
            monster = Enemy('vorox.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False):
            sprite.spritecollide(player, monsters, True)
            life = life - 1
        text = font2.render('Рахунок: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        print(boss.hp)
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (win_width - 50, 10))


    clock.tick(60)
    display.update()