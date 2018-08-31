from FlyingObject import FlyingObject
import arcade


LEVIATHAN_RADIUS = 70
LEVIATHAN_SPEED = .5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Leviathan(FlyingObject):
    def __init__(self):
        super().__init__()
        self.radius = LEVIATHAN_RADIUS
        self.angle = 0
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT + 500
        self.velocity.dy = -LEVIATHAN_SPEED

    def draw(self):
        img = "images/Leviathan.png"
        texture = arcade.load_texture(img)

        width = 700
        height = 700
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

