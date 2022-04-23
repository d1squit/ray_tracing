from pygame import Vector3

class Light ():
    def __init__ (self, position: Vector3, intensity: float):
        self.position = position
        self.intensity = intensity