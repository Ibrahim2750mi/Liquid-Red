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

import os

# Constants (define these somewhere globally)
CANVAS_WIDTH = 80
CANVAS_HEIGHT = 40
CAMERA_Z_DEPTH = 5
CAMERA_ZOOM = 1


class Point3d:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = z


class Renderer:
    def __init__(self):
        # Create 2D grid
        self.grid = [[' ' for _ in range(CANVAS_WIDTH)]
                     for _ in range(CANVAS_HEIGHT)]
        self.clear_grid()

    def clear_grid(self):
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                self.grid[y][x] = ' '

    def show_grid(self):
        for row in self.grid:
            print(" ".join(row))

    def clear_screen(self):
        os.system("clear")   # use "cls" on Windows
        self.clear_grid()

    def project_3d(self, point):
        screen_x = (point.x * CAMERA_Z_DEPTH * CAMERA_ZOOM /
                   (point.z + CAMERA_Z_DEPTH) + CANVAS_WIDTH / 2)

        screen_y = (point.y * CAMERA_Z_DEPTH * CAMERA_ZOOM /
                   (point.z + CAMERA_Z_DEPTH) + CANVAS_HEIGHT / 2)

        return Point3d(screen_x, screen_y, point.z * CAMERA_ZOOM)

    def is_in_bounds(self, x, y):
        return 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT

    def plot_point(self, p, symbol):
        p = self.project_3d(p)
        x, y = int(p.x), int(p.y)

        if self.is_in_bounds(x, y):
            self.grid[y][x] = symbol

    def draw_line(self, v1, v2):
        delta_x = v2.x - v1.x
        delta_y = v2.y - v1.y

        steps = int(max(abs(delta_x), abs(delta_y)))

        # Same point case
        if steps == 0:
            x, y = int(v1.x), int(v1.y)
            if self.is_in_bounds(x, y):
                self.grid[y][x] = '#'
            return

        # Line interpolation (DDA algorithm)
        for i in range(steps + 1):
            x = int(v1.x + (i * delta_x) / steps)
            y = int(v1.y + (i * delta_y) / steps)

            if self.is_in_bounds(x, y):
                self.grid[y][x] = '#'

