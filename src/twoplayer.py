import pygame as pg
import pygame.midi
import sys
import random
import os
import time
from settings import *

pg.midi.init()
sfx = pg.midi.Output(0)
sfx.set_instrument(80,1)

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.score = [0,0]
        self.font_name = os.path.join("fonts", "font.ttf")

    def play_note(self,vel,vol,dur):
        sfx.note_on(vel,vol,1)
        time.sleep(dur)
        sfx.note_off(vel,vol,1)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pg.display.flip()

    def update(self):
        self.all_sprites.update()
        p1.update()
        p2.update()
        b.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill(BG_COLOUR)
        # self.all_sprites.draw(self.screen)
        pg.draw.rect(self.screen, FG_COLOUR, [p1.rect.x, p1.rect.y, p1.w, p1.h]) # Draw paddle
        pg.draw.rect(self.screen, FG_COLOUR, [p2.rect.x, p2.rect.y, p2.w, p2.h]) # Draw paddle
        pg.draw.rect(self.screen, FG_COLOUR, [b.rect.x, b.rect.y, b.w, b.h]) # Draw ball
        self.draw_text(str(self.score[0]), 220, FG_COLOUR, WIDTH * 1/4, 10)
        self.draw_text(str(self.score[1]), 220, FG_COLOUR, WIDTH * 3/4, 10)

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

class Paddle1(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.vel = PADDLE_VEL
        self.w = 8
        self.h = 100
        self.x = 40
        self.y = HEIGHT/2 - self.h/2
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.vy = 0

        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.vy = self.vel
        if keys[pg.K_w]:
            self.vy = -self.vel

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.y += self.vy

class Paddle2(Paddle1):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.vel = PADDLE_VEL
        self.w = 8
        self.h = 100
        self.x = WIDTH - 40
        self.y = HEIGHT/2 - self.h/2
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.vy = 0

        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.vy = self.vel
        if keys[pg.K_UP]:
            self.vy = -self.vel

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.y += self.vy

class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.vel = 1
        self.vec = [self.vel, self.vel]
        self.w = 10
        self.h = 10
        self.x = (WIDTH / 2) - (self.w / 2)
        self.y = 30
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        # Right edge of board
        if self.rect.right == WIDTH:
            self.vec[0] *= -1
            g.play_note(90,127,0.01)
            g.score[0] += 1
        # Left edge of board
        if self.rect.left == 0:
            self.vec[0] *= -1
            g.play_note(90,127,0.01)
            g.score[1] += 1
        # Top edge of board
        if self.rect.top == 0:
            self.vec[1] *= -1
            g.play_note(90,127,0.01)
        # Bottom edge of board
        if self.rect.bottom == HEIGHT:
            self.vec[1] *= -1
            g.play_note(90,127,0.01)
        # Right edge of paddle
        if self.rect.left == p1.rect.right and self.rect.top >= p1.rect.top and self.rect.bottom <= p1.rect.bottom or \
        self.rect.left == p2.rect.right and self.rect.top >= p2.rect.top and self.rect.bottom <= p2.rect.bottom:
            self.vec[0] *= -1
            g.play_note(90,127,0.01)
        # Left edge of paddle
        if self.rect.right == p1.rect.left and self.rect.top >= p1.rect.top and self.rect.bottom <= p1.rect.bottom or \
        self.rect.right == p2.rect.left and self.rect.top >= p2.rect.top and self.rect.bottom <= p2.rect.bottom:
            self.vec[0] *= -1
            g.play_note(90,127,0.01)
        # Above edge of paddle
        if self.rect.bottom == p1.rect.top and self.rect.right <= p1.rect.right and self.rect.left >= p1.rect.left or \
        self.rect.bottom == p2.rect.top and self.rect.right <= p2.rect.right and self.rect.left >= p2.rect.left:
            self.vec[1] *= -1
            g.play_note(90,127,0.01)

        # Underneath edge of paddle
        if self.rect.top == p1.rect.bottom and self.rect.right >= p1.rect.right and self.rect.left <= p1.rect.left or \
        self.rect.top == p2.rect.bottom and self.rect.right >= p2.rect.right and self.rect.left <= p2.rect.left:
            self.vec[1] *= -1
            g.play_note(90,127,0.01)

        self.rect.x += self.vec[0]
        self.rect.y += self.vec[1]

g = Game()
p1 = Paddle1()
p2 = Paddle2()
b = Ball()

while g.running:
    g.new()
    pygame.mixer.music.load('pong.wav')
    pygame.mixer.music.play(0)


pg.quit()
sys.exit()
