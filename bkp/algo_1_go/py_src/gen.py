import csv
import random
import math
import sys, os

# constants for directions of movement
bidir = 0
addr_col = 5


# generates city grid data
def gen_city(size, sep, addr):
    grid = []

    gridlines = range(0, size, sep)
 
   # Initialise grid values
    for i in range(size):
        grid.append([])
        for j in range(size):
            grid[i].append(9)

    addresses_x = random.choices(range(size//sep), k=addr)
    addresses_y = random.choices(range(size//sep), k=addr)

    # make default rows
    for i in gridlines:
        for j in range(size):
            grid[i][j] = bidir

    # make default columns
    for i in gridlines:
        for j in range(size):
            grid[j][i] = bidir
            grid[i][j] = dir

    # insert addresses
    for i in range(len(addresses)):
            x,y = addresses_x[i], addresses_y[i]
            grid[x][y] = addr_col


    return grid


# writes grid to csv file
def gen_csv(grid, csv_writer):
    for i in grid:
        csv_writer.writerow(i)

path = "grid.csv"
csvfile = open(path, "w")

# generate grid
grid = gen_city(50, sep, 25)
# write to csv file
writer = csv.writer(csvfile, delimiter=',')
gen_csv(grid, writer)
# close csv file
csvfile.close()
