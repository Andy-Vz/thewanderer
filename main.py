from tkinter import *
import numpy as np
from PIL import ImageTk, Image
import tkinter.font as tkFont

class Wanderer(object):
    def __init__(self):
        self.charX = 9 # initial pixel values
        self.charY = 9  # initial pixel values
        self.charHP = 10
        self.charDP = 5
        self.charSP = 5
        self.charLvl = 1
        self.levelMap = None
        self.charXY = [0,0] # Variable that will track the characters position
        self.bossXY = []
        self.skeletonsXY = []
        self.heroUp = ImageTk.PhotoImage(Image.open("artifacts/hero-up.png"))
        self.charImage = self.heroUp
        self.heroDown = ImageTk.PhotoImage(Image.open("artifacts/hero-down.png"))
        self.heroRight = ImageTk.PhotoImage(Image.open("artifacts/hero-right.png"))
        self.heroLeft = ImageTk.PhotoImage(Image.open("artifacts/hero-left.png"))
        self.bossImage = ImageTk.PhotoImage(Image.open("artifacts/boss.png"))
        self.backgroundImage = ImageTk.PhotoImage(Image.open("artifacts/floor-map.png"))
        self.wallImage = ImageTk.PhotoImage(Image.open("artifacts/wall.png"))
        self.skeletonImage = ImageTk.PhotoImage(Image.open("artifacts/skeleton.png"))
        self.hudFontStyle = tkFont.Font(family="Arial Black", size=15)
        self.extractLevels()

    def draw(self, canvas):
        self.drawCharMap(canvas)
        self.drawWalls(canvas)
        self.drawBoss(canvas)
        self.drawSkeleton(canvas)
        self.drawHud(canvas)

    def drawCharMap(self,canvas):
        # Draw background
        canvas.create_image(0, 0,anchor=NW, image=self.backgroundImage)
        # Draw Character
        canvas.create_image(self.charX, self.charY, anchor=NW, image=self.charImage)

    def drawWalls(self,canvas):
        # Draw Walls
        y = 0
        counter = 0
        for row in self.levelMap :
            x = 0
            for p in row:
                if p == "1":
                    canvas.create_image(x*90 + 9, y*90 + 9, anchor=NW, image=self.wallImage)
                x += 1
            y += 1

    def drawSkeleton(self,canvas):
        # Get random XY coordinates for the skeletons
        while len(self.skeletonsXY) < 3:
            randY = np.random.randint(0,9)
            randX = np.random.randint(0,9)
            if self.levelMap[randY][randX] == "0":
                self.skeletonsXY.append([randX,randY])
        # Draw Skeletons
        for skeleton in self.skeletonsXY:
            canvas.create_image(skeleton[0] * 90 + 9, skeleton[1] * 90 + 9, anchor=NW, image=self.skeletonImage)

    def drawBoss(self,canvas):
        # Get random Boss XY coordinates
        while len(self.bossXY) < 2:
            randY = np.random.randint(0,9)
            randX = np.random.randint(0,9)
            if self.levelMap[randY][randX] == "0":
                self.bossXY.append(randX)
                self.bossXY.append(randY)
        canvas.create_image(self.bossXY[0] * 90 + 9, self.bossXY[1] * 90 + 9, anchor=NW, image=self.bossImage)

    def drawHud(self,canvas):
        print("loaded")
        canvas.create_text(650, 20, fill="white", font=self.hudFontStyle, text="Hero (Level {}) HP: {}/10 | DP: {} | SP: {}".format(self.charLvl, self.charHP, self.charDP, self.charSP))

    def extractLevels(self):
        # Draw the walls
        initLevelMap = open("levels/level1.txt", "r")
        lineCount = -1
        mapVar = [] #will contain the cleaned version of the map position [[xxxxxxx],[xxxxxx],[],[]]

        for mapLine in initLevelMap:
            lineCount += 1
            positions = mapLine.strip().split(",")
            # Save xPositions
            mapVar.append(positions)

        self.levelMap = mapVar

    # Create a function that can be called when a key pressing happens
    def handleMovement(self,e):
        #Stay within map bounds and avoid walls
        if e.keysym == "Up":
            nextCharY1 = wanaderer.charXY[1] - 1
            if nextCharY1 >= 0 and nextCharY1 < 10 and wanaderer.levelMap[nextCharY1][wanaderer.charXY[0]] != "1":
                wanaderer.charY = wanaderer.charY - 90
                wanaderer.charXY[1] = nextCharY1 #increase Y coordinate by 1
                wanaderer.charImage = self.heroUp
        elif e.keysym == "Down":
            nextCharY2 = wanaderer.charXY[1] + 1
            if nextCharY2 >= 0 and nextCharY2 < 10 and wanaderer.levelMap[nextCharY2][wanaderer.charXY[0]] != "1":
                wanaderer.charY = wanaderer.charY + 90
                wanaderer.charXY[1] = nextCharY2
                wanaderer.charImage = self.heroDown
        elif e.keysym == "Right":
            nextCharX1 = wanaderer.charXY[0] + 1
            if nextCharX1 >= 0 and nextCharX1 < 10 and wanaderer.levelMap[wanaderer.charXY[1]][nextCharX1] != "1":
                wanaderer.charX = wanaderer.charX + 90
                wanaderer.charXY[0] = nextCharX1
                wanaderer.charImage = self.heroRight
        elif e.keysym == "Left":
            nextCharX2 = wanaderer.charXY[0] - 1
            if nextCharX2 >= 0 and nextCharX2 < 10 and wanaderer.levelMap[wanaderer.charXY[1]][nextCharX2] != "1":
                wanaderer.charX = wanaderer.charX - 90
                wanaderer.charXY[0] = nextCharX2
                wanaderer.charImage = self.heroLeft
        # draw the char again in the new position
        wanaderer.draw(canvas)







# Create the tk environment
root = Tk()
canvas = Canvas(root, width=900, height=900)
# Draw the wanderer game
wanaderer = Wanderer()
# Tell the canvas that we prepared a function that can deal with the key press events
canvas.bind("<KeyPress>", wanaderer.handleMovement)
canvas.pack()
# Select the canvas to be in focused so it actually recieves the key hittings
canvas.focus_set()
# Draw the char initial position
wanaderer.draw(canvas)
root.mainloop()