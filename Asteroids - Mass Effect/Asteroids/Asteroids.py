"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import random
import math
from abc import ABC
from abc import abstractmethod
import Point
import Velocity

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
INVINCIBILITY_LIFE = 200

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

LEVIATHAN_RADIUS = 70
LEVIATHAN_SPEED = .5

#class Point():
#    """
#    Class: Point 
#    Purpose: Holds the coordinate values for the location of items on the screen
#    """
#    def __init__(self):
#        self.x = 0
#        self.y = 0

#class Velocity():
#    """
#    Class: Velocity
#    Purpose: Holds the values for how fast moving objects will move in each direction
#    """
#    def __init__(self):
#        self.dx = 0
#        self.dy = 0

class Flying_Object(ABC):
    """
    Class: Flying_object
    Purpose: Contains information relevant to ALL obejcts that move across the screen
    """
    def __init__(self):
        self.center = Point.Point()
        self.velocity = Velocity.Velocity()
        self.radius = 0
        self.angle = 0
        self.alive = True

    def advance(self):
        """
        Moves the target across the screen
        """    
        self.center.x = self.center.x + self.velocity.dx
        self.center.y = self.center.y + self.velocity.dy

    @abstractmethod # All objects must be drawn to the screen
    def draw(self):
        pass
 
    def calculate_velocity(self, speed):
        """
        Breaks RESULTANT velocity into components relative to its current angle of 
        direction and adds them to the objects velocity components
        param: the RESULTATNT velocity of the object who's velocity components are being 
               calculated must be passed along with object
               (please initialize contstant RESULTATNT velocities at the top)
        """
        self.velocity.dx += math.cos(math.radians(self.angle)) * speed
        self.velocity.dy += math.sin(math.radians(self.angle)) * speed
    
    def wrap(self):
        """
        Check each object to see if it has left the screen.
        If it has, put it on the other side of the screen.
        """
        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0
        if self.center.y > SCREEN_HEIGHT:
            self.center.y = 0
        if self.center.x < 0:
            self.center.x = SCREEN_WIDTH
        if self.center.y < 0:
            self.center.y = SCREEN_HEIGHT

class Ship(Flying_Object):
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


class Bullet(Flying_Object):
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

class Asteroid(Flying_Object):
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

class Leviathan(Flying_Object):
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

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.set_up()

    def set_up(self):
        self.num_of_asteriods = 0
        self.held_keys = set()

        self.leviathan = Leviathan()

        # TODO: declare anything here you need the game class to track
        self.asteroids = []
        for i in range(1,6):
            asteroid = Large_Asteroid()
            self.asteroids.append(asteroid)
        self.bullets = []
        self.ship = Ship()
        self.gameOver = False

    def background(self):
        img = "images/Space.png"
        texture = arcade.load_texture(img)

        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT
        alpha = 1 # For transparency, 1 means not transparent

        x = SCREEN_WIDTH/2
        y = SCREEN_HEIGHT/2
        arcade.draw_texture_rectangle(x, y, width, height, texture, 0, alpha)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()
        self.background()
        
        self.leviathan.draw()

        # TODO: draw each object
        for asteroid in self.asteroids:
            asteroid.draw()

        for bullet in self.bullets:
            bullet.draw()

        # Draw the ship glowing when in invincibility mode
        if self.ship.invincible == True:
            self.ship.draw_invincibility()
        else:
            self.ship.draw()

        if self.gameOver == True:
            self.draw_game_over()


    def draw_game_over(self):
        text = "GAME OVER\nPress F1 to try again"
        start_x = SCREEN_WIDTH / 2
        start_y = SCREEN_HEIGHT / 2
        arcade.draw_text(text, start_x = start_x, start_y = start_y, font_size=24, color=arcade.color.WHITE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()

        # TODO: Tell everything to advance or move forward one step in time
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.wrap()

        for bullet in self.bullets:
            bullet.advance()
            bullet.wrap()

        self.ship.advance()
        self.ship.wrap()

        self.leviathan.advance()

        # TODO: Check for collisions
        self.clean_up()

    def clean_up(self):
        for bullet in self.bullets:
            if bullet.alive == False:
                    self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if asteroid.alive == False:
                self.asteroids.remove(asteroid)

    def check_collisions(self):
        """
        Checks to see if contact has been made between bullets and asteroids
        When in invincibility mode collisions have no affect
        """
        leviathan_contact = self.ship.radius + self.leviathan.radius
        if (abs(self.ship.center.x - self.leviathan.center.x) < leviathan_contact and
             abs(self.ship.center.y - self.leviathan.center.y) < leviathan_contact):
            if self.ship.invincible == False:
                   self.gameOver = True

        for asteroid in self.asteroids:
            ship_contact = self.ship.radius + asteroid.radius

            if (abs(self.ship.center.x - asteroid.center.x) < ship_contact and
                 abs(self.ship.center.y - asteroid.center.y) < ship_contact):
                pass
                if self.ship.invincible == False:
                   self.gameOver = True

        for bullet in self.bullets:
            for asteroid in self.asteroids:

                if bullet.alive and asteroid.alive:
                    bullet_contact = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < bullet_contact and
                                abs(bullet.center.y - asteroid.center.y) < bullet_contact):
                        bullet.alive = False
                        asteroid.break_apart(self.asteroids)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn_right()

        if arcade.key.UP in self.held_keys:
            self.ship.throttle()

        if arcade.key.DOWN in self.held_keys:
            self.ship.apply_brake()

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet()
                bullet.fire(self.ship)
                self.bullets.append(bullet)

            if key == arcade.key.LSHIFT:
                self.ship.invincible = True

            if key == arcade.key.F1:
                # Restarts the game
                self.set_up()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()