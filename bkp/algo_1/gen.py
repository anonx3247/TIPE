import csv
import random
import math
import sys, os

# constants for directions of movement
pos = 1
neg = -1
bidir = 0
block = 7
addr_col = 5
directions = (pos, neg, bidir, block)


# generates city grid data
def gen_city(size, sep, proliferation, blocked_proliferation, addr):
    pr = proliferation
    bpr = blocked_proliferation
    weights = (pr, pr, pr*sep, bpr)
    delta = int(math.sqrt(proliferation))
    blocked_delta = int(math.sqrt(blocked_proliferation))

    # we cannot have more colored roads than there are roads
    assert proliferation <= size//sep -1
    # keeps the city grid values
    grid = []

    gridlines = range(0, size, sep)

    positions = []
    for i in range(size//sep):
        positions.append([])
        for j in range(size//sep):
            k = random.randint(1, sep-1)
            l = random.randint(1, sep-1)
            positions[i].append((i*sep+k, j*sep+l))
    
    # We choose a random range of length <= size
    columns = select(gridlines, proliferation**2, delta)
    rows = select(gridlines, proliferation**2, delta)
    blocked_columns = select(gridlines, blocked_proliferation, blocked_delta)
    blocked_rows = select(gridlines, blocked_proliferation, blocked_delta)

    # Initialise grid values
    for i in range(size):
        grid.append([])
        for j in range(size):
            grid[i].append(9)

    addresses = random.choices(range(size//sep), k=addr)

    # make default rows
    for i in gridlines:
        for j in range(size):
            grid[i][j] = bidir

    # make default columns
    for i in gridlines:
        for j in range(size):
            grid[j][i] = bidir

    # insert columns
    for i in columns:
        dir = random.choices(directions, weights, k=1)[0]
        k = 0
        for j in insert_sections(grid, size, sep):
            if k - j > 1:
                dir = random.choices(directions, weights, k=1)[0]
                k = j
            grid[i][j] = dir
            
    # insert rows
    for j in rows:
        dir = random.choices(directions, weights, k=1)[0]
        k = 0
        for i in insert_sections(grid, size, sep):
            if k - i > 1:
                dir = random.choices(directions, weights, k=1)[0]
                k = i
            grid[i][j] = dir

    ## insert blocked columns
    #for i in blocked_columns:
        #for j in insert_sections(grid, size, sep):
            #grid[i][j] = block
#            
    ## insert blocked rows
    #for j in blocked_rows:
        #for i in insert_sections(grid, size, sep):
            #grid[i][j] = block

    # insert addresses
    for i in range(len(addresses)):
            x,y = positions[i][addresses[i]]
            grid[x][y] = addr_col


    return grid

# helper function to create sections of road to be changed
def insert_sections(grid, size, sep):
    parts = random.choices(range(0, size, sep), k=size//sep)
    parts = sorted(parts)
    delims = []
    parts = list(dict.fromkeys(parts)) #removes duplicates
    for k in range(0, len(parts)-1, 2):
        delims += range(parts[k], parts[k+1])
    delims += range(parts[-1], size)
    return delims


# helper function to select columns/rows to be changed
def select(gridlines, proliferation, delta):
    p = proliferation
    return random.choices(gridlines, k=random.randint(p-delta, p+delta))

# writes grid to csv file
def gen_csv(grid, csv_writer):
    for i in grid:
        csv_writer.writerow(i)
# main execution

# select csv file for export
#i = 0
#while os.path.exists("grids/grid{:04d}.csv".format(i)):
    #i += 1
#
#path = "grids/grid{:04d}".format(i)
path = "grid.csv"
print("Generating {}...".format(path[6:]))
csvfile = open(path, "w")

# get grid size and select image stretch size
n = 50
sep = 2
stretch = int(1000/n)
prolif = 0
block_prolif = 0
addr = 25

# generate grid
grid = gen_city(n, sep, prolif, block_prolif, addr)

# write to csv file
writer = csv.writer(csvfile, delimiter=',')
gen_csv(grid, writer)

# close csv file
csvfile.close()
