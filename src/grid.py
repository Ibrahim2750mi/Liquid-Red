def print_grid(grid):
    for i in range(33):
        print('---',end='')
    print()
    for row in grid:
        print('| ',end='')
        for elt in row:
            print(elt+'  ',end='')
        print('|')
    for i in range(33):
        print('---',end='')
    print()

def draw_line(grid, x1, y1, x2, y2, char=None):
    dx=abs(x2-x1)
    dy=abs(y2-y1)

    sx=1 if x1<x2 else -1
    sy=1 if y1<y2 else -1

    if char is None:
        auto_char='.'
    else:
        auto_char=char

    err=dx-dy

    while True:
        grid[y1][x1]=auto_char

        if x1==x2 and y1==y2:
            break

        e2=2*err

        if e2>-dy:
            err-=dy
            x1+=sx

        if e2<dx:
            err+=dx
            y1+=sy


grid = []
for i in range(32):
    row = []
    for j in range(32):
        row.append('*')
    grid.append(row)

draw_line(grid, 2, 2, 25, 20)
draw_line(grid, 0, 0, 31, 0)
draw_line(grid, 0, 0, 0, 31)
draw_line(grid, 31, 0, 31, 31)
draw_line(grid, 0, 31, 31, 31)
print_grid(grid)