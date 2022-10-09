import pygame as pg
import sys 
import numpy as np

RECTSIZE = 10
OFFSET = 1
MAPW,MAPH = (18,32)
SC_SIZE = SW,SH = (MAPW*(RECTSIZE+OFFSET),MAPH*(RECTSIZE+OFFSET))

pg.font.init()

class MapManager:
    def __init__(self) -> None:
        self.rules = {
            "die":[0,1,4,5,6,7,8],
            "born":[3]
        }
        self.map = np.zeros((MAPH,MAPW),dtype=bool)


    def get(self,x,y):
        try:
            return self.map[y][x]
        except:
            return False

    def Update(self):
        new_cells = np.zeros((MAPH,MAPW),dtype=bool)
        
        y = 0
        for line in self.map:
            x = 0
            for tile in line:
                near_tiles = [
                    self.get(x-1,y+1),self.get(x,y+1),self.get(x+1,y+1),
                    self.get(x-1,y),                self.get(x+1,y),
                    self.get(x-1,y-1),self.get(x,y-1),self.get(x+1,y-1)
                ]
                count = np.sum(near_tiles)
                result = self.ApplyResult(count,x,y)
                new_cells[y][x] = result
                x += 1
            y += 1
        self.map = new_cells
    
    def ApplyResult(self,count,x,y):
        if self.map[y][x] == False:
            for i in self.rules["born"]:
                if count == i:
                    return True
            return False
        else: #cell is alive
            for i in self.rules["die"]:
                if count == i:
                    return False
            return True

    def Render(self,surf):
        mov_value = RECTSIZE+OFFSET
        y = 0
        for line in self.map:
            x = 0
            for tile in line:
                if tile == True:
                    pg.draw.rect(surf,"white",(x*mov_value,y*mov_value,RECTSIZE,RECTSIZE))
                else: #cell is dead
                    pg.draw.rect(surf,(30,30,30),(x*mov_value,y*mov_value,RECTSIZE,RECTSIZE))
                x +=1
            y += 1




class App:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SC_SIZE)
        self.clock = pg.time.Clock()
        self.dt = 0
        self.paused = True
        self.font = pg.font.Font("FFFFORWA.TTF",20)
        self.dtcounter = 0
        self.ufps = 10
        self.wanteddt = 1000/self.ufps

    def start_game(self):
        self.mapmanager = MapManager()

    def run(self):
        self.start_game()
        while True:
            pg.display.set_caption(str(self.clock.get_fps()))
            self.screen.fill("black")
            self.dt = self.clock.tick(60)
            self.dtcounter += self.dt

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.paused = not self.paused

            if pg.mouse.get_pressed()[0]: #lmb
                mpos = pg.mouse.get_pos()
                try:
                    self.mapmanager.map[mpos[1]//(RECTSIZE+OFFSET)][mpos[0]//(RECTSIZE+OFFSET)] = 1
                except:
                    pass

            if pg.mouse.get_pressed()[1]: #rmb
                mpos = pg.mouse.get_pos()
                try:
                    self.mapmanager.map[mpos[1]//(RECTSIZE+OFFSET)][mpos[0]//(RECTSIZE+OFFSET)] = 1
                except:
                    pass

            self.mapmanager.Render(self.screen)
            if self.paused:
                self.screen.blit(self.font.render("PAUSED",False,"red"),(0,0))
            else: #the game is running
                if self.dtcounter >= self.wanteddt:
                    self.dtcounter = 0
                    self.mapmanager.Update()

            pg.display.update()

if __name__ == '__main__':
    app = App()
    app.run()