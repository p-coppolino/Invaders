"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Paliska Bradley, bp355 and Philip Coppolino, pcc78
12/9/2021
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    #Attribute _right: the alien direction (True = right and False = left)
    #Invariant: _right is a bool

    #Attribute _player: the bolt from ship (True = ship and False = alien)
    #Invariant: _player is a bool

    #Attribute _mright: x coordinate of the alien most on the right
    #Invariant: _mright is an int or a float

    #Attribute _mleft: x coordinate of the alien most on the left
    #Invariant: _mleft is an int or a float

    #Attribute _mdown: y coordinate of the lowest alien
    #Invariant: _mleft is an int or a float

    #Attribute _step: number of alien steps since last bolt they fired
    #Invariant: _step is an int

    #Attribute _firestep: when to fire (in alien steps)
    #Invariant: _firestep is an int or None

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def state(self):
        """
        Determine the message to give to
        """
        if self._ship == None and self._lives > 0:
            return 'pause'
        if self._ship == None and self._lives == 0:
            return 'over'
        indexlist = []
        max = GAME_HEIGHT
        for col in self._aliens:
            for aliens in col[::-1]:
                if aliens is not None:
                    if max > aliens.y:
                        max = aliens.y
                if aliens.y <= DEFENSE_LINE:
                    return 'over'
        currentwin = False
        livingaliens = []
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    livingaliens.append(alien)
        if len(livingaliens) == 0:
            return 'win'

    def new(self):
        """
        When the game is unpaused recreate a new ship
        """
        self._ship = Ship(GAME_WIDTH//2, SHIP_BOTTOM+SHIP_HEIGHT//2)


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        initialize the attributes before the animation starts
        """

        self._aliencreation()
        self._ship = Ship(GAME_WIDTH//2, SHIP_BOTTOM+SHIP_HEIGHT//2)
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=2,linecolor='black')
        self._time = 0
        self._lives = 3
        self._right = True
        self._mright = 0
        self._mleft = GAME_WIDTH
        self._bolts = []
        self._mdown = 0
        self._player = False
        self._step = 0
        self._firestep = random.randint(1, BOLT_RATE)

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """

        """
        if self._ship != None:
            self._shipmovement(input)
            self._fireship(input)
            self._hitdetection()
        if self._aliens != None:
            self._alienmovement(dt)
            self._firealien()
            self._boltmovement(dt)



    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def _aliencreation(self):
        """
        Return the list of aliens in the right position
        """
        ystart = GAME_HEIGHT - (ALIEN_CEILING + (ALIEN_HEIGHT*(ALIEN_ROWS-1))+(ALIEN_V_SEP * ALIEN_ROWS))
        aliens = []
        for row in range(ALIENS_IN_ROW):
            aliens.append([])
            xoffset = 2 * ALIEN_H_SEP + (ALIEN_H_SEP + ALIEN_WIDTH)* row
            for col in range(ALIEN_ROWS):
                yoffset = ystart + (col*(ALIEN_V_SEP + ALIEN_HEIGHT))
                imageselector = ALIEN_IMAGES1[(col//2) % len(ALIEN_IMAGES1)]
                aliens[row].append(Alien(xoffset,yoffset,imageselector))
        self._aliens = aliens



    def _shipmovement(self,input):
        """
        Move the ship

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        if input.is_key_down('right'):
            if self._ship.x < GAME_WIDTH - SHIP_WIDTH//2:
                self._ship.x += SHIP_MOVEMENT
        if input.is_key_down('left'):
            if self._ship.x > SHIP_WIDTH//2:
                self._ship.x -= SHIP_MOVEMENT



    def _alienmovement(self,dt):
        """
        Move the aliens

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        self._time += dt
        if self._time > ALIEN_SPEED:
            self._step += 1
            if self._right == True:
                self._mostright()
                for row in self._aliens:
                    for alien in row:
                        if self._mright + ALIEN_H_WALK < GAME_WIDTH - ALIEN_WIDTH/2:
                            alien.x += ALIEN_H_WALK
                        else:
                            alien.y -= ALIEN_V_WALK
                            self._right = False
            else:
                self._mostleft()
                for row in self._aliens:
                    for alien in row:
                        if self._mleft - ALIEN_H_WALK > ALIEN_WIDTH/2:
                            alien.x -= ALIEN_H_WALK
                        else:
                            alien.y -= ALIEN_V_WALK
                            self._right = True
            self._time = 0


    def _boltmovement(self,dt):
        """
        Move the bolt

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        for bolt in self._bolts:
            bolt.y += bolt._velocity
            bolt.findcorners()


    def _mostright(self):
        """
        Find the most right alien
        """
        mright = 0
        for row in self._aliens:
            for alien in row:
                if alien.x > mright:
                    mright = alien.x
        self._mright = mright


    def _mostleft(self):
        """
        Find the most left alien
        """
        mleft = GAME_WIDTH
        for row in self._aliens:
            for alien in row:
                if alien.x < mleft:
                    mleft = alien.x
        self._mleft = mleft


    def _fireship(self,input):
        """
        Make the ship fire a bolt

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)
        """
        alreadybolt = False
        for shoot in self._bolts:
            if shoot.getVelocity() > 0:
                alreadybolt = True
            if GAME_HEIGHT <= shoot.y:
                self._bolts.remove(shoot)
                alreadybolt = False
        if input.is_key_down('spacebar') and alreadybolt is False:
            self._bolts.append(Bolt(self._ship.x, SHIP_BOTTOM+SHIP_HEIGHT, False))


    def _firealien(self):
        """
        Make the most bottom alien from a random column fire a bolt. The aliens
        fire a bolt every (random number between 1 and 5) steps.
        """
        if self._step == self._firestep:
            activecols = []
            for col in self._aliens:
                activecol = False
                for alien in col:
                    if alien is not None:
                        activecol = True
                if activecol is True:
                    activecols.append(self._aliens.index(col))
            if len(activecols) != 0:
                shootingcol = activecols[random.randint(0, (len(activecols)-1))]
                for alien in self._aliens[shootingcol][::-1]:
                    if alien is not None:
                        shooter = alien
                self._bolts.append(Bolt(shooter.x,shooter.y,True))
                self._firestep = random.randint(1, BOLT_RATE)
                self._step = 0


    def _hitdetection(self):
        """
        Detect if the ship or the aliens gets hit by a bold
        """
        for bolt in self._bolts:
            if self._ship.collides(bolt):
                self._ship = None
                self._bolts.remove(bolt)
                self._lives -= 1
            for row in self._aliens:
                for alien in row:
                    if alien.collides(bolt):
                        self._aliens[self._aliens.index(row)].remove(alien)
                        self._bolts.remove(bolt)


    def draw(self, view):
        """
        Draws the game objects to the view.
        """
        for row in self._aliens:
            for alien in row:
                alien.draw(view)
        if self._ship !=None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
    # HELPER METHODS FOR COLLISION DETECTION
