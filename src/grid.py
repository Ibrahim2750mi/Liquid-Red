from collections import namedtuple

from config import CANVAS_WIDTH, CANVAS_HEIGHT, CAMERA_Z_DEPTH, CAMERA_ZOOM

point3d = namedtuple('Point3D', ['x', 'y', 'z', 'char'])

# class Point3d:
#     def __init__(self, x, y, z):
#         self.x = int(x)
#         self.y = int(y)
#         self.z = z


class Renderer:
    def __init__(self):
        # Create 2D grid
        self.grid = [[point3d(i, j, 0, ".") for i in range(CANVAS_WIDTH)]
                     for j in range(CANVAS_HEIGHT)]
        # self.clear_grid()

    def clear_grid(self):
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                self.grid[y][x] = point3d(x, y, 0, " ")

    def show_grid(self):
        lines = []
        width = 2 * CANVAS_WIDTH + 3
        lines.append('-' * width)

        for row in self.grid:
            lines.append('| ' + ' '.join(map(lambda x: x.char, row)) + ' |')

        lines.append('-' * width)

        print("\033[H", end="")  # reset cursor
        print('\n'.join(lines))

    @staticmethod
    def project_3d(point):
        screen_x = (point.x * CAMERA_Z_DEPTH * CAMERA_ZOOM /
                   (point.z + CAMERA_Z_DEPTH) + CANVAS_WIDTH / 2)

        screen_y = (point.y * CAMERA_Z_DEPTH * CAMERA_ZOOM /
                   (point.z + CAMERA_Z_DEPTH) + CANVAS_HEIGHT / 2)

        return point3d(screen_x, screen_y, point.z * CAMERA_ZOOM, point.char)

    @staticmethod
    def is_in_bounds(x, y):
        return 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT

    def plot_point(self, p):
        p = self.project_3d(p)
        x, y = int(p.x), int(p.y)

        if self.is_in_bounds(x, y):
            self.grid[y][x] = p.char

    def draw_line(self, v1, v2):
        delta_x = v2.x - v1.x
        delta_y = v2.y - v1.y

        steps = int(max(abs(delta_x), abs(delta_y)))

        # Same point case
        if steps == 0:
            x, y = int(v1.x), int(v1.y)
            if self.is_in_bounds(x, y):
                self.grid[y][x] = point3d(x, y, 0, "#")
            return

        # Line interpolation (DDA algorithm)
        for i in range(steps + 1):
            x = int(v1.x + (i * delta_x) / steps)
            y = int(v1.y + (i * delta_y) / steps)

            if self.is_in_bounds(x, y):
                self.grid[y][x] = point3d(x, y, 0, "#")

