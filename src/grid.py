import numpy as np

from config import CANVAS_HEIGHT, CANVAS_WIDTH, LIGHT_DIRECTION_VECTOR
from geometry import Point3d, compute_surface_normal, get_lambert_char, point_position_wrt_line


def project(func):
    """
    Projects 3D points in the arguments to the 2D grid.
    """
    def wrapper(self, *args, **kwargs):
        arg_list = []
        for arg in args:
            arg_list.append(self.plot_point(arg))
        return func(self, *arg_list, **kwargs)

    return wrapper


class Renderer:
    """
    Holds the grid and all the drawing mechanics.
    Attributes:
        :argument z-buffer: Keeps the nearest z-layer from camera visible. It prevents from behind objects to be drawn
        infront.

    """
    def __init__(self, camera):
        self.grid = np.full((CANVAS_HEIGHT, CANVAS_WIDTH), " ", dtype="<U1")
        self.camera = camera

        self.z_buffer = np.full((CANVAS_HEIGHT, CANVAS_WIDTH), np.inf, dtype=float)

    def clear_grid(self):
        """
        Clears the grid and resets the z-buffer.
        """
        self.grid[:] = " "
        self.z_buffer[:] = np.inf

    def show_grid(self):
        """
        Renders the grid.
        """
        lines = []
        width = 2 * CANVAS_WIDTH + 3
        lines.append("-" * width)

        for row in self.grid:
            lines.append("| " + " ".join(row) + " |")

        lines.append("-" * width)

        print("\033[H", end="")  # reset cursor
        print("\n".join(lines))

    def project_3d(self, point):
        """
        Converts 3D point coordinates to 2D coordinates using perspective projection.
        """
        base = max((point.z + self.camera.focal_length), 0.01)
        screen_x = point.x * self.camera.focal_length * self.camera.zoom / base + CANVAS_WIDTH / 2

        screen_y = point.y * self.camera.focal_length * self.camera.zoom / base + CANVAS_HEIGHT / 2

        return Point3d(screen_x, screen_y, point.z * self.camera.zoom)

    @staticmethod
    def is_in_bounds(x, y):
        """
        Checks whether the point is inside the canvas boundaries.
        """
        return 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT

    def is_visible(self, p, char="+"):
        """
        Checks the z-buffer, to see if its in the most front. # (mesh-char) bypasses z-buffer.
        """
        if p.z > self.z_buffer[p.y, p.x] and char != "#":
            return False
        self.z_buffer[p.y, p.x] = p.z
        return True

    def plot_point(self, p):
        """
        Collectively applies perspective-projection, rotation matrix and camera offset to the point.
        """
        p = self.project_3d(
            self.camera.pitch(self.camera.yaw(Point3d(p.x - self.camera.x, p.y - self.camera.y, p.z - self.camera.z)))
        )

        return Point3d(p.x, p.y, p.z)

    @project
    def draw_line(self, v1, v2, char=None):
        """
        Uses DDA line algorithm to join two points. Using only integral coordinates intermediates.
        """
        delta_x = v2.x - v1.x
        delta_y = v2.y - v1.y
        delta_z = v2.z - v1.z

        steps = int(max(abs(delta_x), abs(delta_y)))

        # Same point case
        if steps == 0:
            if self.is_in_bounds(v1.x, v1.y) and self.is_visible(Point3d(*map(int, v1)), char):
                self.grid[int(v1.y), int(v1.x)] = char or "#"
            return

        # Line interpolation (DDA algorithm)
        for i in range(steps + 1):
            x = int(v1.x + (i * delta_x) / steps)
            y = int(v1.y + (i * delta_y) / steps)
            z = int(v1.z + (i * delta_z) / steps)
            if self.is_in_bounds(x, y) and self.is_visible(Point3d(x, y, z), char):
                self.grid[y, x] = char or "#"

    @project
    def draw_triangle(self, v1, v2, v3, char="#"):
        """
        Rasterize a filled triangle using barycentric coordinates.
        It determines if a point lies inside a triangle by evaluating its barrycentric weights.
        """

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

    def draw_plane(self, v0, v1, v2, v3, char=None):
        """
        Draws a plane using two triangles (v0, v1, v2) and (v0, v2, v3) and implements lighting using lambert shading.
        """
        normal = compute_surface_normal(v0, v1, v2)
        intensity = max(0, np.dot(normal, LIGHT_DIRECTION_VECTOR), np.dot(-normal, LIGHT_DIRECTION_VECTOR))
        char = char or get_lambert_char(intensity)

        self.draw_triangle(v0, v1, v2, char=char)
        self.draw_triangle(v0, v2, v3, char=char)

    def draw_plane_xy(self, x0, x1, y0, y1, z, char=None):
        """To draw a plane in xy dimension."""
        self.draw_plane(Point3d(x0, y0, z), Point3d(x1, y0, z), Point3d(x1, y1, z), Point3d(x0, y1, z), char)

    def draw_plane_xz(self, x0, x1, z0, z1, y, char=None):
        """To draw a plane in xz dimension."""
        self.draw_plane(Point3d(x0, y, z0), Point3d(x1, y, z0), Point3d(x1, y, z1), Point3d(x0, y, z1), char)

    def draw_plane_yz(self, y0, y1, z0, z1, x, char=None):
        """To draw a plane in yz dimension."""
        self.draw_plane(Point3d(x, y0, z0), Point3d(x, y1, z0), Point3d(x, y1, z1), Point3d(x, y0, z1), char)
