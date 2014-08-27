#!/usr/bin/python
#coding=utf-8

from Tkinter import *
import tkMessageBox
import random
from collections import deque

FLAGS=10
SIZE=10
#Tabuleiro sera de tamanho SIZE*SIZE :-)

class Minesweeper:
    def __init__(self, master):

        # import images
        self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
        self.tile_mine = PhotoImage(file = "images/tile_mine.gif")
        self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
        self.tile_no = []
        for x in range(1, 9):
            self.tile_no.append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

        # set up frame
        frame = Frame(master)
        frame.pack()

        # create flag and clicked tile variables
        self.correct_flags = 0
        self.clicked = 0

        #random mines
        mine_list = []
        for i in range(0, FLAGS):
            x = random.randint(0, SIZE-1)
            y = random.randint(0, SIZE-1)
            while (x, y) in mine_list:
                x = random.randint(0, SIZE-1)
                y = random.randint(0, SIZE-1)
            mine_list.append((x, y))
        mine_list = sorted(mine_list, key=lambda tup: tup[0])
        
        # create buttons
        self.buttons = dict({})
        self.flags = 0
        x_coord = 0
        y_coord = 0
        for x in range(0, SIZE*SIZE):
            # tile image changeable for debug reasons:
            gfx = self.tile_plain

            mine=0
            if (x_coord, y_coord) in mine_list:
                mine=1
                self.flags+=1

            # 0 = Button widget
            # 1 = if a mine y/n (1/0)
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
            # 3 = button id
            # 4 = [x, y] coordinates in the grid
            # 5 = nearby mines, 0 by default, calculated after placement in grid
            self.buttons[x] = [ Button(frame, image = gfx),
                                mine,
                                0,
                                x,
                                [x_coord, y_coord],
                                0 ]
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))

            # calculate coords:
            y_coord += 1
            if y_coord == SIZE:
                y_coord = 0
                x_coord += 1

        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key][0].grid( row = self.buttons[key][4][0], column = self.buttons[key][4][1] )

        # find nearby mines and display number on tile
        for key in self.buttons:
            nearby_mines = 0
            if self.check_for_mines(key-9):
                nearby_mines += 1
            if self.check_for_mines(key-10):
                nearby_mines += 1
            if self.check_for_mines(key-11):
                nearby_mines += 1
            if self.check_for_mines(key-1):
                nearby_mines += 1
            if self.check_for_mines(key+1):
                nearby_mines += 1
            if self.check_for_mines(key+9):
                nearby_mines += 1
            if self.check_for_mines(key+10):
                nearby_mines += 1
            if self.check_for_mines(key+11):
                nearby_mines += 1
            # store mine count in button data list
            self.buttons[key][5] = nearby_mines
            #if self.buttons[key][1] != 1:
            #    if nearby_mines != 0:
            #        self.buttons[key][0].config(image = self.tile_no[nearby_mines-1])

        #add mine and count at the end
        self.label1 = Label(frame, text = "Jogador 1: "+str(self.correct_flags))
        self.label1.grid(row = 21, column = 0, columnspan = 5)

        self.label2 = Label(frame, text = "Jogador 2: "+str(self.correct_flags))
        self.label2.grid(row = 21, column = 5, columnspan = 10)

    ## End of __init__

    def check_for_mines(self, key):
        try:
            if self.buttons[key][1] == 1:
                return True
        except KeyError:
            pass

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(self.buttons[x])


    # 0 = Button widget
    # 1 = if a mine y/n (1/0)
    # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
    # 3 = button id
    # 4 = [x, y] coordinates in the grid
    # 5 = nearby mines, 0 by default, calculated after placement in grid
    def lclicked(self, button_data):
        if button_data[1] == 1: #if a flag
            if button_data[2] != 1:
                button_data[0].config(image = self.tile_flag)
                button_data[2] = 1
                self.correct_flags += 1
                self.clicked += 1
                self.update_flags()
        else:
            #change image
            if button_data[5] == 0:
                button_data[0].config(image = self.tile_clicked)
                self.clear_empty_tiles(button_data[3])
            else:
                button_data[0].config(image = self.tile_no[button_data[5]-1])
            # if not already set as clicked, change state and count
            if button_data[2] != 1:
                button_data[2] = 1
                self.clicked += 1

    def check_tile(self, key, queue):
        try:
            if self.buttons[key][2] == 0:
                if self.buttons[key][5] == 0:
                    self.buttons[key][0].config(image = self.tile_clicked)
                    queue.append(key)
                else:
                    self.buttons[key][0].config(image = self.tile_no[self.buttons[key][5]-1])
                self.buttons[key][2] = 1
                self.clicked += 1
        except KeyError:
            pass

    def clear_empty_tiles(self, main_key):
        queue = deque([main_key])

        while len(queue) != 0:
            key = queue.popleft()
            self.check_tile(key-9, queue)      #top right
            self.check_tile(key-10, queue)     #top middle
            self.check_tile(key-11, queue)     #top left
            self.check_tile(key-1, queue)      #left
            self.check_tile(key+1, queue)      #right
            self.check_tile(key+9, queue)      #bottom right
            self.check_tile(key+10, queue)     #bottom middle
            self.check_tile(key+11, queue)     #bottom left
    
    def gameover(self):
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

    def victory(self):
        tkMessageBox.showinfo("Game Over", "You Win!")
        global root
        root.destroy()

    def update_flags(self):
        self.label1.config(text = "Jogador 1: "+str(self.correct_flags))
        self.label2.config(text = "Jogador 2: "+str(self.correct_flags))

### END OF CLASSES ###

def main():
    global root
    # create Tk widget
    root = Tk()
    # set program title
    root.title("Campo Minado")
    # create game instance
    minesweeper = Minesweeper(root)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()
