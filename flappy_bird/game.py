import pygame as pgm
import sys

pgm.init()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 768 
        self.win = pgm.display.set_mode((self.width, self.height))
        self.bg_img = pgm.transform.scale(pgm.image.load("assets/bg.png").convert(), (self.width, self.height))
        
        self.gameLoop()
        
    def gameLoop(self):
        while True:
            for event in pgm.event.get():
                if event.type == pgm.QUIT:
                    pgm.quit()
                    sys.exit()
            self.win.blit(self.bg_img, (0, 0));
            pgm.display.update()

game = Game()
