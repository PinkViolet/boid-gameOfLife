input_file = "inLife.txt"
output_file = "outLife.txt"
grid = []
generation = 0
row = 0
col = 0

def getInputFile():
    global input_file
    global grid
    global generation
    global row
    global col
    
    infile = open(input_file, "r" )
    temp = [[n for n in list(line)] for line in infile]
    generation = int(temp[0][0])
    row = len(temp) - 1
    col = len(temp[row])
    for i in range(1, row + 1):
        grid.append([])
        for j in range(col):
            grid[i-1].append(int(temp[i][j]))
            
def pendingOutFile(gen):
    global grid
    global row
    global col
    toReturn = "Generation " + str(gen) + "\n"
    #toReturn = ""
    
    for i in range(row):
        for j in range(col):
            toReturn = toReturn + str(grid[i][j])
        toReturn = toReturn + "\n"
    return toReturn

def writeOutFile(pendingStr):
    global output_file
    with open(output_file, "a") as f:
        f.write(pendingStr + "\n")
    
    
def find_8_neighbours(t_row, t_col):
    global grid

    count = 0 # count alive neighbours
    neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
    for i in neighbours:
        if grid[t_row + i[0]][t_col + i[1]] == 1:
            count = count + 1
    return count


def find_5_neighbours(t_row, t_col):
    global grid
    global row
    global col

    count = 0 # count alive neighbours
    if t_row == 0:
        # neighbours of points on top
        neighbours = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    elif t_row == row - 1:
        # neighbours of points at button
        neighbours = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    elif t_col == 0:
        # neighbours of points on left
        neighbours = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    elif t_col == col -1:
        # neighbours of points on right
        neighbours = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1

    return count
    

def find_3_neighbours(t_row, t_col):
    global grid
    global row
    global col

    count = 0 # count alive neighbours
    if t_row == 0 and t_col == 0:
        # neighbours of points on top left corner
        neighbours = [(0, 1), (1, 1), (1, 0)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    elif t_row == 0 and t_col == col - 1:
        # neighbours of points on top right corner
        neighbours = [(0, -1), (1, -1), (1, 0)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    elif t_row == row - 1 and t_col == 0:
        # neighbours of points on button left corner
        neighbours = [(-1, 0), (-1, 1), (0, 1)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    elif t_row == row - 1 and t_col == col - 1:
        # neighbours of points on button right corner
        neighbours = [(0, -1), (-1, -1), (-1, 0)]
        for i in neighbours:
            if grid[t_row + i[0]][t_col + i[1]] == 1:
                count = count + 1
    return count
    

def gridcpy():
    global grid
    global row
    global col
    temp = []
    
    for i in range(row):
        temp.append([])
        for j in range(col):
            temp[i].append(int(grid[i][j]))
    return temp
    
def gameOfLife():
    global grid
    global row
    global col
    global generation

    for gen in range(generation):
        temp = gridcpy()
        for t_row in range(row):
            for t_col in range(col):
                # four corners
                if (t_row == 0 and t_col == 0) or (t_row == 0 and t_col == col - 1) or (t_row == row - 1 and t_col ==0 ) or (t_row == row - 1 and t_col == col - 1):
                    alive = find_3_neighbours(t_row, t_col)
                    # target is alive
                    if grid[t_row][t_col] == 1:
                        if alive < 2 or alive > 3:
                            temp[t_row][t_col] = 0
                    # target is dead
                    else:
                        if alive == 3:
                            temp[t_row][t_col] = 1
                # boundary
                elif t_row == 0 or t_col == 0 or t_row == row - 1 or t_col == col - 1:
                    alive = find_5_neighbours(t_row, t_col)
                    # target is alive
                    if grid[t_row][t_col] == 1:
                        if alive < 2 or alive > 3:
                            temp[t_row][t_col] = 0
                    # target is dead
                    else:
                        if alive == 3:
                            temp[t_row][t_col] = 1
                # center
                else:
                    alive = find_8_neighbours(t_row, t_col)
                    # target is alive
                    if grid[t_row][t_col] == 1:
                        if alive < 2 or alive > 3:
                            temp[t_row][t_col] = 0
                    # target is dead
                    else:
                        if alive == 3:
                            temp[t_row][t_col] = 1
        grid = temp
        writeOutFile(pendingOutFile(gen + 1))
        
        
        
    # end ith generation loop
                    
    
    



def main():
    global row
    global col
    getInputFile()
    writeOutFile(pendingOutFile(0))
    #print(find_3_neighbours(0, 4))
    gameOfLife()

    
    

main()
