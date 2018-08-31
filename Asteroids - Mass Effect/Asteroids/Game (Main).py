"""
Author: Jason Tuttle
This is the main file that creates the game world and
starts the game.
"""
import arcade
import random
import math
from abc import ABC
from abc import abstractmethod
from Point import Point
from Velocity import Velocity
from Ship import Ship
from Bullet import Bullet
from FlyingObject import FlyingObject
from Leviathon import Leviathan
from Asteroid import Large_Asteroid
from Asteroid import Medium_Asteroid
from Asteroid import Small_Asteroid

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_ROCK_COUNT = 5


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