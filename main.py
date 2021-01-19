from tkinter import *
from PIL import ImageTk, Image


class Character(object):
    def __init__(self):
        self.charX = 9
        self.charY = 9

    def draw(self, canvas):
        # Draw Background
        canvas.create_image(0, 0, anchor=NW, image=background)
        # Draw Character
        canvas.create_image(self.charX, self.charY, anchor=NW, image=boss)

        # Draw the walls


# Create the tk environment as usual
root = Tk()
canvas = Canvas(root, width=900, height=900)

# Load images
boss = ImageTk.PhotoImage(Image.open("artifacts/boss.png"))
background = ImageTk.PhotoImage(Image.open("artifacts/floor-map.png"))
wall = ImageTk.PhotoImage(Image.open("artifacts/wall.png"))

# Draw character
char = Character()


# Create a function that can be called when a key pressing happens
def on_key_press(e):
    # When the keycode is 111 (up arrow) we move the position of our char higher
    if e.keycode == 38:
        char.charY = char.charY - 90
    elif e.keycode == 40:
        char.charY = char.charY + 90
    elif e.keycode == 39:
        char.charX = char.charX + 90
    elif e.keycode == 37:
        char.charX = char.charX - 90
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