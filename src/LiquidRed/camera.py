import numpy as np

from .geometry import Point3d


class Camera:
    """
    Camera representing the viewer/player in the 3D scene.

    This class handles position, orientation (yaw and pitch),
    and simple movement physics such as jumping.

    Parameters
    ----------
    x : float, optional
        Initial x-coordinate of the camera. Default is 0.
    y : float, optional
        Initial y-coordinate of the camera. Default is 0.
    z : float, optional
        Initial z-coordinate of the camera. Default is -1.
    focal_length : float, optional
        Focal length of the camera. Higher values produce a narrower
        field of view. Default is 5.
    zoom : float, optional
        Zoom scaling factor applied during projection. Default is 1.
    gravity : float, optional
        Gravity constant used for jump physics. Default is 5.

    Attributes
    ----------
    x : float
        Current x-coordinate.
    y : float
        Current y-coordinate.
    z : float
        Current z-coordinate.
    yaw_angle : float
        Rotation around the vertical axis (left-right), in radians.
    pitch_angle : float
        Rotation around the horizontal axis (up-down), in radians.
    jump : float
        Timestamp when jump started (0 if grounded).
    """

    def __init__(self, x=0, y=0, z=-1, focal_length=5, zoom=1, gravity=5):
        self.focal_length = focal_length
        self.zoom = zoom
        self.z = z
        self.x = x
        self.y = y
        self.yaw_angle = 0
        self.pitch_angle = 0
        self.jump = 0
        self.gravity = gravity

    def yaw(self, p):
        """
        Apply rotation in the XZ plane (yaw rotation).

        Parameters
        ----------
        p : Point3d
            Input point to be rotated.

        Returns
        -------
        Point3d
            Rotated point after applying yaw transformation.
        """
        return Point3d(
            p.x * np.cos(self.yaw_angle) - p.z * np.sin(self.yaw_angle),
            p.y,
            p.x * np.sin(self.yaw_angle) + p.z * np.cos(self.yaw_angle),
        )

    def pitch(self, p):
        """
        Apply rotation in the YZ plane (pitch rotation).

        Parameters
        ----------
        p : Point3d
            Input point to be rotated.

        Returns
        -------
        Point3d
            Rotated point after applying pitch transformation.
        """
        return Point3d(
            p.x,
            p.y * np.cos(self.pitch_angle) - p.z * np.sin(self.pitch_angle),
            p.y * np.sin(self.pitch_angle) + p.z * np.cos(self.pitch_angle),
        )

    def update(self, pressed, now):
        """
        Update the camera state based on user input and physics.

        This method should be called every frame. It handles movement,
        rotation, and jumping behavior.

        Parameters
        ----------
        pressed : set[str]
            Set of currently pressed keys.
        now : float
            Current timestamp (e.g., from ``time.time()``).

        Notes
        -----
        Default controls:

        - **W / S** → Move forward / backward
        - **A / D** → Strafe left / right
        - **, / .** → Yaw left / right
        - **J** → Jump
        """
        if self.jump:
            self.y = -(5 * (now - self.jump) - self.gravity / 2 * (now - self.jump) ** 2)

        if self.y > 0:
            self.jump = 0
            self.y = 0

        speed = 0.1

        if "w" in pressed:
            self.x += speed * np.sin(self.yaw_angle)
            self.z += speed * np.cos(self.yaw_angle)

        if "s" in pressed:
            self.x -= speed * np.sin(self.yaw_angle)
            self.z -= speed * np.cos(self.yaw_angle)

        if "a" in pressed:
            self.x -= speed * np.cos(self.yaw_angle)
            self.z -= speed * np.sin(self.yaw_angle)

        if "d" in pressed:
            self.x += speed * np.cos(self.yaw_angle)
            self.z += speed * np.sin(self.yaw_angle)

        if "," in pressed:
            self.yaw_angle += 0.002

        if "." in pressed:
            self.yaw_angle -= 0.002

        if "j" in pressed and self.jump == 0:
            self.jump = now