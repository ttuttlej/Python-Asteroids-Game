import math
from abc import ABC
from abc import abstractmethod
from Velocity import Velocity
from Point import Point

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class FlyingObject(ABC):
    """
    Class: Flying_object (BASE CLASS)
    Purpose: Contains information relevant to ALL obejcts that move across the screen
    """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
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

