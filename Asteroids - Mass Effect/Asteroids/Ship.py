from FlyingObject import FlyingObject
import arcade

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
INVINCIBILITY_LIFE = 200

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Ship(FlyingObject):
    """
    Class: Ship
    Purpose: Contains all information related to the ship including: 
            (Ship controls, drawing to screen)
    """
    def __init__(self):
        super().__init__()
        self.invincibility_life = INVINCIBILITY_LIFE 
        self.invincible = False
        self.radius = SHIP_RADIUS
        self.ship_begin()
            
    def ship_begin(self):
        # Starts the ship at the center of the screen
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT/2
        
    def throttle(self):
        # Increases the velocity of the ship in the direction its facing
        self.calculate_velocity(SHIP_THRUST_AMOUNT)
    
    def apply_brake(self):
        # Decreases velocity of the ship
        self.calculate_velocity(-SHIP_THRUST_AMOUNT)

    def turn_left(self):
        # Turns the ship left at a certain angular velocity(SHIP_TURN_AMOUNT)
        self.angle += SHIP_TURN_AMOUNT

    def turn_right(self):
        self.angle -= SHIP_TURN_AMOUNT

    def draw(self):
        # Load the image of the ship from the images folder
        img = "images/NormandySR2flattened.png"
        texture = arcade.load_texture(img)

        width = 150
        height = 100
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        angle = self.angle - 90 # Shift the unit cirlce 90 degrees
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    def draw_invincibility(self):
        # Load the image of the ship from the images folder
        self.invincibility_life -= 1

        if self.invincibility_life == 0:
            self.invincible = False

        img = "images/normandy - teal.png"
        texture = arcade.load_texture(img)

        width = 150
        height = 100
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        angle = self.angle - 90 # Shift the unit cirlce 90 degrees
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)