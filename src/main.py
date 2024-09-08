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
        self.score = 0
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
            self.draw_text(str(self.score), 220, FG_COLOUR, WIDTH/2, 10)
            pg.display.flip()


    def update(self):
        self.all_sprites.update()
        b.update()
        p.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill(BG_COLOUR)
        # self.all_sprites.draw(self.screen)
        pg.draw.rect(self.screen, FG_COLOUR, [p.rect.x, p.rect.y, p.w, p.h]) # Draw paddle
        pg.draw.rect(self.screen, FG_COLOUR, [b.rect.x, b.rect.y, b.w, b.h]) # Draw ball

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

class Paddle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.vel = 1
        self.w = 100
        self.h = 10
        self.x = (WIDTH / 2) - (self.w / 2)
        self.y = HEIGHT - 75
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.vx = 0

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.vx = self.vel
        if keys[pg.K_LEFT]:
            self.vx = -self.vel

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

        self.rect.x += self.vx

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
        if self.rect.right == WIDTH: # Right edge of board
            self.vec[0] *= -1
        if self.rect.left == 0: # Left edge of board
            self.vec[0] *= -1
        if self.rect.top == 0: # Top edge of board
            self.vec[1] *= -1
        if self.rect.bottom == HEIGHT: # Bottom edge of board
            self.vec[1] *= -1

        if self.rect.top == p.rect.bottom and self.rect.right <= p.rect.right and self.rect.left >= p.rect.left:
            self.vec[1] *= -1

        if self.rect.bottom == p.rect.top and self.rect.right <= p.rect.right and self.rect.left >= p.rect.left: # Top edge of paddle
            self.vec[1] *= -1
            g.score += 1
            g.play_note(60,127,0.05)

        self.rect.x += self.vec[0]
        self.rect.y += self.vec[1]

g = Game()
p = Paddle()
b = Ball()

while g.running:
    g.new()

pg.quit()
sys.exit()
