import numpy as np

from .geometry import Point3d, compute_surface_normal, get_lambert_char, point_position_wrt_line


def project(func):
    """
    Decorator to project 3D input points to 2D screen space before rendering.

    This applies ``Renderer.plot_point`` to all positional arguments.

    Parameters
    ----------
    func : callable
        Rendering function that operates on projected points.

    Returns
    -------
    callable
        Wrapped function with automatic projection.
    """
    def wrapper(self, *args, **kwargs):
        arg_list = [self.plot_point(arg) for arg in args]
        return func(self, *arg_list, **kwargs)

    return wrapper


class Renderer:
    """
    Renderer for ASCII-based 3D rasterization.

    This class maintains a 2D character grid and a z-buffer for depth testing,
    and provides methods to draw geometric primitives.

    Parameters
    ----------
    camera : Camera
        Camera used for projection and transformations.
    light_direction_vector : np.ndarray
        Direction vector for lighting calculations.
    canvas_width : int
        Width of the rendering grid.
    canvas_height : int
        Height of the rendering grid.

    Attributes
    ----------
    grid : np.ndarray
        2D array of characters representing the rendered frame.
    z_buffer : np.ndarray
        Depth buffer storing nearest z-values per pixel.
    """

    def __init__(self, camera, light_direction_vector, canvas_width, canvas_height):
        self.grid = np.full((canvas_height, canvas_width), " ", dtype="<U1")
        self.camera = camera
        self.light_direction_vector = light_direction_vector
        self.z_buffer = np.full((canvas_height, canvas_width), np.inf, dtype=float)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def clear_grid(self):
        """
        Clear the rendering grid and reset the z-buffer.
        """
        self.grid[:] = " "
        self.z_buffer[:] = np.inf

    def show_grid(self):
        """
        Render the grid to the terminal.
        """
        lines = []
        width = 2 * self.canvas_width + 3
        lines.append("-" * width)

        for row in self.grid:
            lines.append("| " + " ".join(row) + " |")

        lines.append("-" * width)

        print("\033[H", end="")  # reset cursor
        print("\n".join(lines))

    def project_3d(self, point):
        """
        Project a 3D point onto the 2D screen using perspective projection.

        Parameters
        ----------
        point : Point3d
            Input 3D point.

        Returns
        -------
        Point3d
            Projected 2D point with depth.
        """
        base = max((point.z + self.camera.focal_length), 0.01)

        screen_x = point.x * self.camera.focal_length * self.camera.zoom / base + self.canvas_width / 2
        screen_y = point.y * self.camera.focal_length * self.camera.zoom / base + self.canvas_height / 2

        return Point3d(screen_x, screen_y, point.z * self.camera.zoom)

    def is_in_bounds(self, xi, yi):
        """
        Check if coordinates are within the canvas.

        Parameters
        ----------
        xi : ndarray
        yi : ndarray

        Returns
        -------
        bool
        """
        return (xi >= 0) & (xi < self.canvas_width) & (yi >= 0) & (yi < self.canvas_height)

    def is_visible(self, xi, yi, zi, char="+"):
        """
        Perform z-buffer depth test.

        Parameters
        ----------
        xi : ndarray
            x_i of points.
        yi : ndarray
            y_i of points.
        zi : ndarray
            z_i of points.
        char : str, optional
            Character used for rendering. ``'#'`` bypasses z-buffer.

        Returns
        -------
        bool
            True if the point is visible.
        """
        visible = (zi < self.z_buffer[yi, xi]) | (char == "#")
        self.z_buffer[yi[visible], xi[visible]] = zi[visible]

        return visible

    def plot_point(self, p):
        """
        Transform a world-space point into screen-space.

        Applies:
        - camera translation
        - yaw rotation
        - pitch rotation
        - perspective projection

        Parameters
        ----------
        p : Point3d

        Returns
        -------
        Point3d
        """
        p = self.project_3d(
            self.camera.pitch(
                self.camera.yaw(
                    Point3d(p.x - self.camera.x, p.y - self.camera.y, p.z - self.camera.z)
                )
            )
        )

        return Point3d(p.x, p.y, p.z)

    @project
    def draw_line(self, v1, v2, char=None):
        """
        Draw a line between two points using the DDA algorithm.

        Parameters
        ----------
        v1 : Point3d
        v2 : Point3d
        char : str, optional
            Character used for rendering.
        """
        delta_x = v2.x - v1.x
        delta_y = v2.y - v1.y
        delta_z = v2.z - v1.z

        steps = int(max(abs(delta_x), abs(delta_y)))
        if steps == 0:
            if self.is_in_bounds(int(v1.x), int(v1.y)):
                self.grid[int(v1.y), int(v1.x)] = char or "#"
            return

        t = np.arange(steps + 1) / steps
        xi = (v1.x + t * delta_x).astype(int)
        yi = (v1.y + t * delta_y).astype(int)
        zi = v1.z + t * delta_z

        in_bounds = self.is_in_bounds(xi, yi)
        xi, yi, zi = xi[in_bounds], yi[in_bounds], zi[in_bounds]
        visible = self.is_visible(xi, yi, zi)
        self.grid[yi[visible], xi[visible]] = char or "#"

    @project
    def draw_triangle(self, v1, v2, v3, char="#"):
        """
        Rasterize a filled triangle using barycentric coordinates.

        Parameters
        ----------
        v1, v2, v3 : Point3d
            Triangle vertices.
        char : str, optional
            Fill character.
        """
        min_x = int(max(0, np.floor(min(v1.x, v2.x, v3.x))))
        max_x = int(min(self.canvas_width - 1, np.ceil(max(v1.x, v2.x, v3.x))))
        min_y = int(max(0, np.floor(min(v1.y, v2.y, v3.y))))
        max_y = int(min(self.canvas_height - 1, np.ceil(max(v1.y, v2.y, v3.y))))

        if min_x >= max_x or min_y >= max_y:
            return

        # build pixel coordinate grids, make vector for numpy speedup
        xs = np.arange(min_x, max_x + 1)
        ys = np.arange(min_y, max_y + 1)
        gx, gy = np.meshgrid(xs, ys)

        # vectorized barycentric, all points at once
        area = point_position_wrt_line(v1, v2, v3.x, v3.y)
        if area == 0:
            return

        w1 = point_position_wrt_line(v2, v3, gx, gy) / area
        w2 = point_position_wrt_line(v3, v1, gx, gy) / area
        w3 = point_position_wrt_line(v1, v2, gx, gy) / area

        # mask of pixels inside triangle, barrycentric condition of point lying inside triangle
        inside = (w1 >= 0) & (w2 >= 0) & (w3 >= 0)

        # depth interpolation across all pixels at once
        z = w1 * v1.z + w2 * v2.z + w3 * v3.z

        abs_gy = gy[inside]
        abs_gx = gx[inside]
        abs_z = z[inside]
        visible = self.is_visible(abs_gx, abs_gy, abs_z, char)

        self.grid[abs_gy[visible], abs_gx[visible]] = char

    def draw_plane(self, v0, v1, v2, v3, char=None):
        """
        Draw a quadrilateral plane using two triangles with Lambert shading.

        Parameters
        ----------
        v0, v1, v2, v3 : Point3d
            Vertices of the plane.
        char : str, optional
            Override shading character.
        """
        normal = compute_surface_normal(v0, v1, v2)
        intensity = max(
            0,
            np.dot(normal, self.light_direction_vector),
            np.dot(-normal, self.light_direction_vector),
        )

        char = char or get_lambert_char(intensity)

        self.draw_triangle(v0, v1, v2, char=char)
        self.draw_triangle(v0, v2, v3, char=char)

    def draw_plane_xy(self, x0, x1, y0, y1, z, char=None):
        """Draw a plane parallel to the XY plane."""
        self.draw_plane(
            Point3d(x0, y0, z),
            Point3d(x1, y0, z),
            Point3d(x1, y1, z),
            Point3d(x0, y1, z),
            char,
        )

    def draw_plane_xz(self, x0, x1, z0, z1, y, char=None):
        """Draw a plane parallel to the XZ plane."""
        self.draw_plane(
            Point3d(x0, y, z0),
            Point3d(x1, y, z0),
            Point3d(x1, y, z1),
            Point3d(x0, y, z1),
            char,
        )

    def draw_plane_yz(self, y0, y1, z0, z1, x, char=None):
        """Draw a plane parallel to the YZ plane."""
        self.draw_plane(
            Point3d(x, y0, z0),
            Point3d(x, y1, z0),
            Point3d(x, y1, z1),
            Point3d(x, y0, z1),
            char,
        )