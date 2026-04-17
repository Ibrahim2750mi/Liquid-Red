from config import CAMERA_Z_START, CAMERA_Z_DEPTH, CAMERA_ZOOM, GRAVITY
from geometry import Point3d

import numpy as np

class Camera:
    def __init__(self, x=0, y=0, z=CAMERA_Z_START, focal_length=CAMERA_Z_DEPTH, zoom=CAMERA_ZOOM):
        self.focal_length = focal_length
        self.zoom = zoom
        self.z = z
        self.x = x
        self.y = y
        self.yaw_angle = 0
        self.pitch_angle = 0
        self.jump = 0

    def yaw(self, p):
        return Point3d(
            p.x*np.cos(self.yaw_angle) - p.z * np.sin(self.yaw_angle),
            p.y,
            p.x*np.sin(self.yaw_angle) + p.z * np.cos(self.yaw_angle)
        )

    def pitch(self, p):
        return Point3d(
            p.x,
            p.y*np.cos(self.pitch_angle) - p.z*np.sin(self.pitch_angle),
            p.y*np.sin(self.pitch_angle) + p.z*np.cos(self.pitch_angle)
        )

    def update(self, pressed, now):
        if self.jump:
            self.y = -(5 * (now - self.jump) - GRAVITY / 2 * (now - self.jump) ** 2)
        if self.y > 0:
            self.jump = 0
            self.y = 0

        speed = 0.1

        if 'w' in pressed:
            self.x += speed * np.sin(self.yaw_angle)
            self.z += speed * np.cos(self.yaw_angle)

        if 's' in pressed:
            self.x -= speed * np.sin(self.yaw_angle)
            self.z -= speed * np.cos(self.yaw_angle)
        if 'a' in pressed:
            self.x -= speed * np.cos(self.yaw_angle)
            self.z -= speed * np.sin(self.yaw_angle)
        if 'd' in pressed:
            self.x += speed * np.cos(self.yaw_angle)
            self.z += speed * np.sin(self.yaw_angle)
        if "," in pressed:
            self.yaw_angle += 0.002
        if "." in pressed:
            self.yaw_angle -= 0.002

        if "j" in pressed and self.jump == 0:
            self.jump = now
