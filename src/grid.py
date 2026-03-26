
def print_grid(grid):

    for i in range(33):
        print('---',end='')
    print()
    for row in grid:
        print('| ',end='')
        for elt in row:
            print(elt+'  ',end='')
        print('| ')

    for i in range(33):
        print('---',end='')





grid=[]
for i in range(32):
    row=[]
    for j in range(32):
        row.append('*')
    grid.append(row)


print_grid(grid)