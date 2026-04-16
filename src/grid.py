from collections import namedtuple

from config import CANVAS_WIDTH, CANVAS_HEIGHT, CAMERA_Z_DEPTH, CAMERA_Z_START, CAMERA_ZOOM
import numpy as np

Point3d = namedtuple('Point3D', ['x', 'y', 'z'])

# class Point3d:
#     def __init__(self, x, y, z):
#         self.x = int(x)
#         self.y = int(y)
#         self.z = z


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
        # self.clear_grid()

    def clear_grid(self):
        self.grid[:] = ' '

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

    def plot_point(self, p):
        p = self.project_3d(self.pitch(self.yaw(Point3d(p.x - self.camera_x, p.y - self.camera_y, p.z - self.camera_z))))

        return Point3d(p.x, p.y, p.z)

    def draw_line(self, v1, v2):
        delta_x = v2.x - v1.x
        delta_y = v2.y - v1.y

        steps = int(max(abs(delta_x), abs(delta_y)))

        # Same point case
        if steps == 0:
            if self.is_in_bounds(v1.x, v1.y):
                self.grid[int(v1.y), int(v1.x)] = "#"
            return

        # Line interpolation (DDA algorithm)
        for i in range(steps + 1):
            x = int(v1.x + (i * delta_x) / steps)
            y = int(v1.y + (i * delta_y) / steps)

            if self.is_in_bounds(x, y):
                self.grid[y, x] = "#"

    def draw_edges_sorted(self, edge_pairs):
        """
        edge_pairs: list of (p1_world, p2_world) Point3d tuples.
        Projects all edges, sorts by average Z (farthest first) and then draws them.
        """
        projected = []
        for p1_world, p2_world in edge_pairs:
            p1 = self.plot_point(p1_world)
            p2 = self.plot_point(p2_world)
            if p1 is None or p2 is None:
                continue
            avg_z = (p1.z + p2.z) / 2
            projected.append((avg_z, p1, p2))

        # Far edges first
        projected.sort(key=lambda t: t[0], reverse=True)

        for _, p1, p2 in projected:
            self.draw_line(p1, p2)
