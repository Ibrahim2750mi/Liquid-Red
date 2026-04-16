from collections import namedtuple

from config import CANVAS_WIDTH, CANVAS_HEIGHT, CAMERA_Z_DEPTH, CAMERA_Z_START, CAMERA_ZOOM, LIGHT_DIRECTION_VECTOR
from geometry import point_position_wrt_line
import numpy as np

Point3d = namedtuple('Point3D', ['x', 'y', 'z'])

# class Point3d:
#     def __init__(self, x, y, z):
#         self.x = int(x)
#         self.y = int(y)
#         self.z =

def project(func):
    def wrapper(self, *args, **kwargs):
        arg_list = []
        for arg in args:
            arg_list.append(self.plot_point(arg))
        return func(self, *arg_list, **kwargs)
    return wrapper


class Renderer:
    def __init__(self):
        # Create 2D grid
        self.grid = np.full((CANVAS_HEIGHT, CANVAS_WIDTH), " ", dtype='<U1')
        self.camera_z_depth = CAMERA_Z_DEPTH
        self.camera_z = CAMERA_Z_START
        self.camera_x = 0
        self.camera_y = 0
        self.camera_yaw = 0
        self.camera_pitch = 0
        self.jump = 0

        self.z_buffer = np.full((CANVAS_HEIGHT, CANVAS_WIDTH), np.inf, dtype=float)
        # self.clear_grid()

    def clear_grid(self):
        self.grid[:] = ' '
        self.z_buffer[:] = np.inf

    def show_grid(self):
        lines = []
        width = 2 * CANVAS_WIDTH + 3
        lines.append('-' * width)

        for row in self.grid:
            lines.append('| ' + ' '.join(row) + ' |')

        lines.append('-' * width)

        print("\033[H", end="")  # reset cursor
        print('\n'.join(lines))

    def yaw(self, p):
        return Point3d(
            p.x*np.cos(self.camera_yaw) - p.z * np.sin(self.camera_yaw),
            p.y,
            p.x*np.sin(self.camera_yaw) + p.z * np.cos(self.camera_yaw)
        )

    def pitch(self, p):
        return Point3d(
            p.x,
            p.y*np.cos(self.camera_pitch) - p.z*np.sin(self.camera_pitch),
            p.y*np.sin(self.camera_pitch) + p.z*np.cos(self.camera_pitch)
        )

    def project_3d(self, point):
        base = max((point.z + self.camera_z_depth), 0.01)
        screen_x = (point.x * self.camera_z_depth * CAMERA_ZOOM /
                   base + CANVAS_WIDTH / 2)

        screen_y = (point.y * self.camera_z_depth * CAMERA_ZOOM /
                   base + CANVAS_HEIGHT / 2)

        return Point3d(screen_x, screen_y, point.z * CAMERA_ZOOM)

    @staticmethod
    def is_in_bounds(x, y):
        return 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT

    def is_visible(self, p):
        if p.z > self.z_buffer[p.y, p.x]:
            return False
        self.z_buffer[p.y, p.x] = p.z
        return True

    def plot_point(self, p):
        p = self.project_3d(self.pitch(self.yaw(Point3d(p.x - self.camera_x, p.y - self.camera_y, p.z - self.camera_z))))

        return Point3d(p.x, p.y, p.z)

    @project
    def draw_line(self, v1, v2):
        delta_x = v2.x - v1.x
        delta_y = v2.y - v1.y
        delta_z = v2.z - v1.z

        steps = int(max(abs(delta_x), abs(delta_y)))

        # Same point case
        if steps == 0:
            if self.is_in_bounds(v1.x, v1.y) and self.is_visible(v1):
                    self.grid[int(v1.y), int(v1.x)] = "#"
            return

        # Line interpolation (DDA algorithm)
        for i in range(steps + 1):
            x = int(v1.x + (i * delta_x) / steps)
            y = int(v1.y + (i * delta_y) / steps)
            z = int(v1.z + (i * delta_z) / steps)
            if self.is_in_bounds(x, y) and self.is_visible(Point3d(x, y, z)):
                self.grid[y, x] = "#"

    @project
    def draw_triangle(self, v1, v2, v3, char="#"):

        min_x = int(max(0, np.floor(min(v1.x, v2.x, v3.x))))
        max_x = int(min(CANVAS_WIDTH - 1, np.ceil(max(v1.x, v2.x, v3.x))))
        min_y = int(max(0, np.floor(min(v1.y, v2.y, v3.y))))
        max_y = int(min(CANVAS_HEIGHT - 1, np.ceil(max(v1.y, v2.y, v3.y))))

        area = point_position_wrt_line(v1, v2, v3)
        if area == 0:
            return

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):

                p = Point3d(x, y, 0)

                w1 = point_position_wrt_line(v2, v3, p) / area
                w2 = point_position_wrt_line(v3, v1, p) / area
                w3 = point_position_wrt_line(v1, v2, p) / area

                # Barycentric condition that a point is inside a triangle
                if w1 >= 0 and w2 >= 0 and w3 >= 0:

                    # Depth interpolation
                    z = w1 * v1.z + w2 * v2.z + w3 * v3.z

                    if self.is_visible(Point3d(x, y, z)):
                        self.grid[y, x] = char
