from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import numpy as np

class Character(object):
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
        self.charImage = heroUp
        self.bossImage = boss
        self.skeletonImage = skeletton
        self.extractLevels()

    def draw(self, canvas):
        # Draw Background
        canvas.create_image(0, 0,anchor=NW, image=background)
        # Draw Character
        canvas.create_image(self.charX, self.charY, anchor=NW, image=self.charImage)
        # Draw Walls
        y = 0
        counter = 0
        for row in self.levelMap :
            x = 0
            for p in row:
                if p == "1":
                    canvas.create_image(x*90 + 9, y*90 + 9, anchor=NW, image=wall)
                x += 1
            y += 1
        # Get random XY coordinates for the skeletons
        while len(self.skeletonsXY) < 3:
            randY = np.random.randint(0,9)
            randX = np.random.randint(0,9)
            if self.levelMap[randY][randX] == "0":
                self.skeletonsXY.append([randX,randY])
        # Draw Skeletons
        for skeleton in self.skeletonsXY:
            canvas.create_image(skeleton[0] * 90 + 9, skeleton[1] * 90 + 9, anchor=NW, image=self.skeletonImage)
        # Get random Boss XY coordinates
        while len(self.bossXY) < 2:
            randY = np.random.randint(0,9)
            randX = np.random.randint(0,9)
            if self.levelMap[randY][randX] == "0":
                self.bossXY.append(randX)
                self.bossXY.append(randY)
        # Draw Boss
        canvas.create_image(self.bossXY[0] * 90 + 9, self.bossXY[1] * 90 + 9, anchor=NW, image=self.bossImage)
        # Draw HUD
        canvas.create_text(650, 20, fill="white", font=fontStyle, text="Hero (Level {}) HP: {}/10 | DP: {} | SP: {}".format(self.charLvl, self.charHP, self.charDP, self.charSP))

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

# Create the tk environment as usual
root = Tk()
canvas = Canvas(root, width=900, height=900)
# Define HUD fontstyle
fontStyle = tkFont.Font(family="Arial Black", size=15)

# Load images
boss = ImageTk.PhotoImage(Image.open("artifacts/boss.png"))
heroRight = ImageTk.PhotoImage(Image.open("artifacts/hero-right.png"))
heroUp = ImageTk.PhotoImage(Image.open("artifacts/hero-up.png"))
heroDown = ImageTk.PhotoImage(Image.open("artifacts/hero-down.png"))
heroLeft = ImageTk.PhotoImage(Image.open("artifacts/hero-left.png"))
background = ImageTk.PhotoImage(Image.open("artifacts/floor-map.png"))
wall = ImageTk.PhotoImage(Image.open("artifacts/wall.png"))
skeletton = ImageTk.PhotoImage(Image.open("artifacts/skeleton.png"))

####
## @TODO Load the rest of the pictures for movement animatio
####

# Draw character
char = Character()

# Create a function that can be called when a key pressing happens
def on_key_press(e):
    #Stay within map bounds and avoid walls
    if e.keysym == "Up":
        nextCharY1 = char.charXY[1] - 1
        if nextCharY1 >= 0 and nextCharY1 < 10 and char.levelMap[nextCharY1][char.charXY[0]] != "1":
            char.charY = char.charY - 90
            char.charXY[1] = nextCharY1 #increase Y coordinate by 1
            char.charImage = heroUp
    elif e.keysym == "Down":
        nextCharY2 = char.charXY[1] + 1
        if nextCharY2 >= 0 and nextCharY2 < 10 and char.levelMap[nextCharY2][char.charXY[0]] != "1":
            char.charY = char.charY + 90
            char.charXY[1] = nextCharY2
            char.charImage = heroDown
    elif e.keysym == "Right":
        nextCharX1 = char.charXY[0] + 1
        if nextCharX1 >= 0 and nextCharX1 < 10 and char.levelMap[char.charXY[1]][nextCharX1] != "1":
            char.charX = char.charX + 90
            char.charXY[0] = nextCharX1
            char.charImage = heroRight
    elif e.keysym == "Left":
        nextCharX2 = char.charXY[0] - 1
        if nextCharX2 >= 0 and nextCharX2 < 10 and char.levelMap[char.charXY[1]][nextCharX2] != "1":
            char.charX = char.charX - 90
            char.charXY[0] = nextCharX2
            char.charImage = heroLeft
    # draw the char again in the new position
    char.draw(canvas)

# Tell the canvas that we prepared a function that can deal with the key press events
canvas.bind("<KeyPress>", on_key_press)
canvas.pack()

# Select the canvas to be in focused so it actually recieves the key hittings
canvas.focus_set()

# Draw the char initial position
char.draw(canvas)

root.mainloop()