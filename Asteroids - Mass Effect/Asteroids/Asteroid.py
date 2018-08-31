import arcade
import random
from FlyingObject import FlyingObject
from abc import abstractmethod

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Asteroid(FlyingObject):
    def __init__(self):
        super().__init__()
        self.rotation_angle = 0
        self.asteroid_begin()

    def asteroid_begin(self):
        """
        Sets each asteroid to a random location.
        This is done outside of the init function to allow for a future
            implementation of restarting the game
        """
        self.center.x = random.uniform(0, SCREEN_WIDTH)
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.angle = random.uniform(0, 360)

    def spin(self):
        # This rotates the asteroid at the specified angular velocity
        self.rotation_angle += self.spin_amount

    @abstractmethod # Every asteroid reacts differently when shot
    def break_apart(self, list_of_asteriods):
        pass

class Large_Asteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.spin_amount = BIG_ROCK_SPIN
        self.large_asteroid_begin()                      
        self.radius = BIG_ROCK_RADIUS


    def large_asteroid_begin(self):
        """
        After location and angle have been chosen randomly, calculate
        the velocity the objects will travel at.
        """
        self.calculate_velocity(BIG_ROCK_SPEED)

    def draw(self):   
        img = "images/asteroid-icon.png"
        texture = arcade.load_texture(img)

        width = 140
        height = 140
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        self.spin()
        angle = self.rotation_angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    def break_apart(self, list_of_asteroids):
        """
        KIlls the Large ateroid and replaces it with 2 medium asteroids and a small one
        """
        self.alive = False
        medium_asteroid = Medium_Asteroid()
        medium_asteroid.velocity.dy = self.velocity.dy + 2
        list_of_asteroids.append(medium_asteroid)
        medium_asteroid = Medium_Asteroid()
        medium_asteroid.velocity.dy = self.velocity.dy - 2
        list_of_asteroids.append(medium_asteroid)
        small_asteroid = Small_Asteroid()
        small_asteroid.velocity.dx = self.velocity.dx + 5
        list_of_asteroids.append(small_asteroid)

class Medium_Asteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.spin_amount = MEDIUM_ROCK_RADIUS
        self.radius = MEDIUM_ROCK_RADIUS

    def draw(self):
        img = "images/asteroid-icon.png"
        texture = arcade.load_texture(img)

        width = 90
        height = 90
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        self.spin()
        angle = self.rotation_angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    def break_apart(self, list_of_asteroids):
        self.alive = False
        small_asteroid = Small_Asteroid()
        small_asteroid.velocity.dy = self.velocity.dy + 1.5
        small_asteroid.velocity.dx = self.velocity.dx + 1.5
        list_of_asteroids.append(small_asteroid)
        small_asteroid = Small_Asteroid()
        small_asteroid.velocity.dy = self.velocity.dy - 1.5
        small_asteroid.velocity.dx = self.velocity.dx - 1.5
        list_of_asteroids.append(small_asteroid)
        
class Small_Asteroid(Asteroid):
    def __init__(self):
        super().__init__()
        self.spin_amount = SMALL_ROCK_SPIN
        self.radius = SMALL_ROCK_RADIUS

    def draw(self):
        img = "images/asteroid-icon.png"
        texture = arcade.load_texture(img)

        width = 65
        height = 65
        alpha = 1 # For transparency, 1 means not transparent

        x = self.center.x
        y = self.center.y
        self.spin()
        angle = self.rotation_angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    def break_apart(self, list_of_asteroids):
        self.alive = False

