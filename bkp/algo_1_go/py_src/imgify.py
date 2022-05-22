#!/usr/bin/python3.10
import csv
from PIL import Image
import sys, os

# constants for directions of movement
pos = 1
neg = -1
bidir = 0
block = 7
traj = 8
addr_col = 5
bkg = 9
directions = (pos, neg, bidir)


# reads csv and retrieves grid data
def get_grid(csv_reader):
    grid = []
    for index, row in enumerate(csv_reader):
        grid.append([])
        for j in row:
            grid[index].append(int(j))
    return grid

# inserts a block into image
def putblock(img, x,y, color, stretch_factor):
    # for some reason we have to interpolate the
    # x and y for the image to be generated correctly
    s = stretch_factor
    for i in range(stretch_factor):
        for j in range(stretch_factor):
            img.putpixel((s*y+i,s*x+j), color)

# draws grid on image file
def draw_grid(grid, stretch):
    # colors used to indicate directions
    black = (0,0,0)
    white = (197,197,197)
    grey  = (78,84,82)
    red = (242,29,29)
    blue = (29,183,242)
    green = (29,242,183)
    yellow = (238,217,15)
    # dimensions of image
    width, height = len(grid), len(grid)
    # stretch factor for pixels
    # image file
    img = Image.new(mode = "RGB", size=(stretch*width, stretch*height))
    for i in range(height):
        for j in range(width):
            if grid[i][j] == pos:
                putblock(img,i,j, red, stretch)
            elif grid[i][j] == neg:
                putblock(img,i,j, blue, stretch)
            elif grid[i][j] == bidir:
                putblock(img,i,j, white, stretch)
            elif grid[i][j] == bkg:
                putblock(img,i,j, black, stretch)
            elif grid[i][j] == block:
                putblock(img,i,j, grey, stretch)
            elif grid[i][j] == addr_col:
                putblock(img,i,j, green, stretch)
            elif grid[i][j] == traj:
                putblock(img,i,j, yellow, stretch)
            else:
                print("ERROR, wrong color")
                exit()
    return img

# main execution

path = sys.argv[-1]

# close csv file
#
# imprt and read just exported csv file
csvimport = open(path, "r")
reader = csv.reader(csvimport, delimiter=',')
grid = get_grid(reader)
stretch = int(1000/len(grid))
img = draw_grid(grid, stretch)
print(path[:-3] + "png") 
img.save(path[:-3] + "png")
csvimport.close()


