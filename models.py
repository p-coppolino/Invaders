"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Paliska Bradley, bp355 and Philip Coppolino, pcc78
12/9/2021
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    # def getImage(self):
    #     return self._image
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y):
        """
        Initializes the ship.

        Parameter x: x is the horizontal coordinate of the object center
        Precondition: x is an int or a float

        Parameter y: y is the vertical coordinate of the object center
        Precondition: y is an int or a float
        """
        super().__init__(x = x, y = y, width = SHIP_WIDTH, height = SHIP_HEIGHT, source = SHIP_IMAGE1, format = (2,4))
        self._frame = 0
        self._animator = None

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if this alien bolt collides with the player

        This method returns False if bolt was not fired by an alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        boltcorners = bolt.findcorners()
        for xy in boltcorners:
            if self.contains(xy) and bolt.getisenemy():
                #print('collides activated')
                return True
            else: return False

    # COROUTINE METHOD TO ANIMATE THE SHIP

    # def _blowupship(self,dt):
    #     frames = self.count/DEATH_SPEED
    #     animating = True
    #     while animating:
    #         dt = (yield)
    #         show = frame * dt
    #         try:
    #             self.frame = show // 1
    #         except:
    #             self.frame = self.count
    #             animating = False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source):
        """
        Initializes the alien.

        Parameter x: x is the horizontal coordinate of the object center
        Precondition: x is an int or a float

        Parameter y: y is the vertical coordinate of the object center
        Precondition: y is an int or a float

        Parameter source: source is the source file for this image
        Precondition: source is a string refering to a valid file

        """
        super().__init__(x = x, y = y, width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source = source)

        # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        boltcorners = bolt.findcorners()
        for xy in boltcorners:
            if self.contains(xy) and not bolt.getisenemy():
                return True
            else: return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _isenemy: True if the bolt came from an alien, False otherwise
    # Invariant: _isenemy is a bool

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getisenemy(self):
        return self._isenemy

    def getVelocity(self):
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, isenemy):
        """
        Initializes the laser bolt.

        Parameter x: x is the horizontal coordinate of the object center
        Precondition: x is an int or a float

        Parameter y: y is the vertical coordinate of the object center
        Precondition: y is an int or a float

        Parameter color: the color of the bolt
        Precondition: bad is s string
        """

        if isenemy:
            color = 'red'
            velocity = -BOLT_SPEED
            self._isenemy = True
        else:
            color = 'blue'
            velocity = BOLT_SPEED
            self._isenemy = False

        super().__init__(x = x, y = y, width = BOLT_WIDTH, height = BOLT_HEIGHT, fillcolor = color, linecolor = 'black')

        self._velocity = velocity

        self._corners = self.findcorners()



    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    def findcorners(self):
        """

        """
        halfwidth = BOLT_WIDTH / 2
        halfheight = BOLT_HEIGHT / 2
        topleft = (self.x-halfwidth, self.y+halfheight)
        topright = (self.x+halfwidth, self.y+halfheight)
        bottomleft = (self.x-halfwidth, self.y-halfheight)
        bottomright = (self.x+halfwidth, self.y-halfheight)
        return [topleft, topright, bottomleft, bottomright]




# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
