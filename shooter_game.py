#Створи власний Шутер!
from pygame import *
from random import randint


#Класс Спрайт
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale( image.load(img), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
    def fire(self):
        global bullets

        bullet = Bullet("bullet.png", self.rect.centerx - 15 / 2 , self.rect.top, 15, 16, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

        
#Глобальные переменные
goal = 0
lost = 0

#Размеры окна
win_width = 700
win_height = 500

#создание окна
win = display.set_mode((win_width, win_height))
display.set_caption("Maze")

#фон игры
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Игровые персонажи
player = Player("rocket.png", win_width / 2 - 45, win_height - 80, 6, 40, 65)
bullets = sprite.Group()

monstrs = sprite.Group()
for i in range(randint(3,6)):
    enemy = Enemy("ufo.png",randint(80, win_width - 80), 0, 2, 65, 40)
    monstrs.add(enemy)

#Текст 
font.init()
def text(text = "Text", x = 0, y = 0, size = 36, color = (255,255,255)):
    text_line = font.Font(None, size)
    text_line = text_line.render(text, True, color)
    win.blit(text_line, (x, y))

#Музыка
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire = mixer.Sound("fire.ogg")

#Цикл игры
game = True
finished = False
clock = time.Clock()
FPS = 60

while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
        
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                player.fire()
                fire.play()
    
    
    win.blit(background, (0, 0))

    if not finished:
        text("Баллы: " + str(goal),x = 10, y = 10)
        text("Пропущено: " + str(lost), 10, 40)
        
        player.update()
        bullets.update()
        monstrs.update()

        bullets.draw(win)
        monstrs.draw(win)
        player.reset()

        collides = sprite.groupcollide(bullets, monstrs, True, True)
        for col in collides:
            goal += 1
            enemy = Enemy("ufo.png",randint(80, win_width - 80), 0, 2, 65, 40)
            monstrs.add(enemy)


    if goal >= 15:
        finished = True
        text("!!!Ты победил!!!",175, 230, 64, (0, 255, 0) )
    if lost >= 3:
        finished = True
        text("!!!Game Ower!!!",175, 230, 64, (255, 0, 0) )

    display.update()
    clock.tick(FPS)