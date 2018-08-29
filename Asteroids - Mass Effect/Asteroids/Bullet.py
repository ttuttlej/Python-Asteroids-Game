import FlyingObject

class Bullet(FlyingObject):
    """
    Class: Bullet
    Purpose: Contains information relevant only to the bullets
    """
    def __init__(self):
        super().__init__()
        self.frames_to_live = BULLET_LIFE
        self.radius = BULLET_RADIUS

    def fire(self, ship):
        """
        Sets bullet location and velocity to the same location and velocity of the Ship
        Param: Ship object 
              (must be passed from the game class; this is where the ship object is created)
        """
        self.center.x = ship.center.x
        self.center.y = ship.center.y
        self.angle = ship.angle
        self.velocity.dx = ship.velocity.dx
        self.velocity.dy = ship.velocity.dy
        self.calculate_velocity(BULLET_SPEED)

    def draw(self):
        img = "images/laserBlue01.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)   

    def advance(self):
        super().advance()

        # Bullets only live for a select number of frames
        # Once the bullet runs out of lives, kill it
        self.frames_to_live -= 1
        if self.frames_to_live == 0:
            self.alive = False
