# -------------------------------------------------------------------------------------------------------------------- #
# Program: Running Simulator 2k19 Objects
# Authors: Michael Schmauderer and Jake Rutkowski
# Description: Objects for the running sim 2k19 game.
# Date Modified: 5/27/2019
# Version: 1.1

# -------------------------------------------------------------------------------------------------------------------- #
# Import Libraries
from graphics import *

# -------------------------------------------------------------------------------------------------------------------- #
# Global Variables
backgroundSpeed = 2
idleCharacterSpeed = backgroundSpeed - .5

# -------------------------------------------------------------------------------------------------------------------- #
# Classes


class Character:
    """Basic building blocks for a character."""
    def __init__(self, x, y, name, speed, window, controls, size=1, rotation=0):
        """Constructs a character object."""
        self.x = x
        self.y = y
        self.name = name
        self.trueIdentity = name
        self.speed = speed
        self.window = window
        self.size = size
        self.rotation = rotation
        self.imageCycle = 0
        self.direction = "right"
        self.state = "standing idle"
        self.isJumping = False
        self.jumpHeights = (25, 20, 15, 12, 9, 6, 1, -1, -6, -9, -12, -15, -20, -25)
        self.controls = controls
        self.runLeft = []
        self.runRight = []
        self.duckLeft = []
        self.duckRight = []
        self.createAnimations()
        characters = []
        characters.append(self)
        self.mistakes = 0

    def createAnimations(self):
        """Creates lists of images for each animation."""

        # Images for running to the left (all in order of how they will be used)
        self.runLeft.append(Image(Point(self.x, self.y),
                                  "assets/images/characters/{}/{}-upLeft.png".format(self.name, self.name)))
        self.runLeft.append(Image(Point(self.x, self.y),
                                  "assets/images/characters/{}/{}-upMidLeft.png".format(self.name, self.name)))
        self.runLeft.append(Image(Point(self.x, self.y),
                                  "assets/images/characters/{}/{}-upLeft.png".format(self.name, self.name)))

        # Images for running to the right
        self.runRight.append(Image(Point(self.x, self.y),
                                   "assets/images/characters/{}/{}-upRight.png".format(self.name, self.name)))
        self.runRight.append(Image(Point(self.x, self.y),
                                   "assets/images/characters/{}/{}-upMidRight.png".format(self.name, self.name)))
        self.runRight.append(Image(Point(self.x, self.y),
                                   "assets/images/characters/{}/{}-upRight.png".format(self.name, self.name)))

        # Images for ducking to the left
        self.duckLeft.append(Image(Point(self.x, self.y),
                                   "assets/images/characters/{}/{}-downLeft.png".format(self.name, self.name)))
        self.duckLeft.append(Image(Point(self.x, self.y),
                                   "assets/images/characters/{}/{}-downMidLeft.png".format(self.name, self.name)))
        self.duckLeft.append(Image(Point(self.x, self.y),
                                   "assets/images/characters/{}/{}-downLeft.png".format(self.name, self.name)))

        # Images for ducking to the right
        self.duckRight.append(Image(Point(self.x, self.y),
                                    "assets/images/characters/{}/{}-downRight.png".format(self.name, self.name)))
        self.duckRight.append(Image(Point(self.x, self.y),
                                    "assets/images/characters/{}/{}-downMidRight.png".format(self.name, self.name)))
        self.duckRight.append(Image(Point(self.x, self.y),
                                    "assets/images/characters/{}/{}-downRight.png".format(self.name, self.name)))

    def clearAnimations(self):
        """Clears the animation lists."""
        self.runLeft.clear()
        self.runRight.clear()
        self.duckLeft.clear()
        self.duckRight.clear()

    def draw(self):
        """Draws the object by updating the anchor point."""

        # Help organize and make main() less redundant
        self.undraw()
        self.move()

        # Chooses an animation list based on the current state
        if self.state == "running":

            # Narrows down the animation list even further using the current direction
            if self.direction == "left":

                # Transform the image based on size and rotation
                self.runLeft[self.imageCycle].transform(self.size, self.rotation)

                # Resets the anchor point of the image as the x and y values have likely changed
                self.runLeft[self.imageCycle].anchor = Point(self.x, self.y)

                # Draws the image

                self.runLeft[self.imageCycle].draw(self.window)

            elif self.direction == "right":
                self.runRight[self.imageCycle].transform(self.size, self.rotation)
                self.runRight[self.imageCycle].anchor = Point(self.x, self.y)
                self.runRight[self.imageCycle].draw(self.window)

        elif self.state == "standing idle":
            if self.direction == "left":
                # No iterator needed for idle images because they are a single frame
                self.runLeft[0].transform(self.size, self.rotation)
                self.runLeft[0].anchor = Point(self.x, self.y)
                self.runLeft[0].draw(self.window)
            elif self.direction == "right":
                self.runRight[0].transform(self.size, self.rotation)
                self.runRight[0].anchor = Point(self.x, self.y)
                self.runRight[0].draw(self.window)

        elif self.state == "crouching":
            if self.direction == "left":
                self.duckLeft[self.imageCycle].transform(self.size, self.rotation)
                self.duckLeft[self.imageCycle].anchor = Point(self.x, self.y)
                self.duckLeft[self.imageCycle].draw(self.window)
            elif self.direction == "right":
                self.duckRight[self.imageCycle].transform(self.size, self.rotation)
                self.duckRight[self.imageCycle].anchor = Point(self.x, self.y)
                self.duckRight[self.imageCycle].draw(self.window)

        elif self.state == "crouching idle":
            if self.direction == "left":
                self.duckLeft[0].transform(self.size, self.rotation)
                self.duckLeft[0].anchor = Point(self.x, self.y)
                self.duckLeft[0].draw(self.window)
            elif self.direction == "right":
                self.duckRight[0].transform(self.size, self.rotation)
                self.duckRight[0].anchor = Point(self.x, self.y)
                self.duckRight[0].draw(self.window)

        elif self.state == "jumping":
            if self.direction == "left":
                self.runLeft[0].transform(self.size, self.rotation)
                self.runLeft[0].anchor = Point(self.x, self.y)
                self.runLeft[0].draw(self.window)
            elif self.direction == "right":
                self.runRight[0].transform(self.size, self.rotation)
                self.runRight[0].anchor = Point(self.x, self.y)
                self.runRight[0].draw(self.window)

        # Always check if the character has left the play area after each movement
        self.checkBorders()

    def undraw(self):
        """Undraws the object and adjusts the animation iterator."""

        # Once again chooses an animation list based on current state
        if self.state == "running":

            # Narrowed down by current direction
            if self.direction == "left":

                # Undraw the current image
                self.runLeft[self.imageCycle].undraw()

                # Increments the imageCycle variable if it is an index within the animation list
                if self.imageCycle < len(self.runLeft) - 1:
                    self.imageCycle += 1

                # Reset the imageCycle variable to 0 after the last index is reached
                else:
                    self.imageCycle = 0

            elif self.direction == "right":
                self.runRight[self.imageCycle].undraw()
                if self.imageCycle < len(self.runRight) - 1:
                    self.imageCycle += 1
                else:
                    self.imageCycle = 0

        # No need to reset imageCycle here since it is an idle image and does not use that variable
        elif self.state == "standing idle":
            if self.direction == "left":
                self.runLeft[0].undraw()
            elif self.direction == "right":
                self.runRight[0].undraw()

        elif self.state == "crouching":
            if self.direction == "left":
                self.duckLeft[self.imageCycle].undraw()
                if self.imageCycle < len(self.duckLeft) - 1:
                    self.imageCycle += 1
                else:
                    self.imageCycle = 0

            elif self.direction == "right":
                self.duckRight[self.imageCycle].undraw()
                if self.imageCycle < len(self.duckRight) - 1:
                    self.imageCycle += 1
                else:
                    self.imageCycle = 0

        elif self.state == "crouching idle":
            if self.direction == "left":
                self.duckLeft[0].undraw()
            elif self.direction == "right":
                self.duckRight[0].undraw()

        elif self.state == "jumping":
            if self.imageCycle < len(self.jumpHeights) - 1:
                self.imageCycle += 1
            else:
                self.imageCycle = 0
                self.isJumping = False
                self.state = "standing idle"

            if self.direction == "left":
                # The frame used for jumping is the same as the frame used for idle
                self.runLeft[0].undraw()

            elif self.direction == "right":
                self.runRight[0].undraw()

    def move(self):
        """Updates the state, direction and coordinates of the image based on key input."""

        # Store keys pressed in a set called keys
        keys = self.window.checkKeys()

        # Not hardcoded key values because different characters may have different controls
        # Tests keys being pressed

        # Crouching
        if self.controls[2] in keys and not self.isJumping:

            # Running right while crouching
            if self.controls[3] in keys:

                # Updates the state
                self.state = "crouching"

                # Updates the direction
                self.direction = "right"

                # Updates the x value
                self.x += self.speed

                # Resets the imageCycle variable if state or direction change
                if self.state != "crouching" or self.direction != "right":
                    self.imageCycle = 0

            # Running left while crouching
            elif self.controls[1] in keys:
                self.state = "crouching"
                self.direction = "left"
                self.x -= self.speed
                if self.state != "crouching" or self.direction != "left":
                    self.imageCycle = 0

            # Crouching idle
            else:
                self.state = "crouching idle"
                self.imageCycle = 0
                self.x -= idleCharacterSpeed

        # Jumping
        elif self.controls[0] in keys or self.state == "jumping":
            self.isJumping = True
            if self.state != "jumping":
                self.state = "jumping"
            self.y -= self.jumpHeights[self.imageCycle]

            # Jumping to the right
            if self.controls[3] in keys:
                self.direction = "right"
                self.x += self.speed + 3

            # Jumping to the left
            elif self.controls[1] in keys:
                self.direction = "left"
                self.x -= self.speed + 3

        # Running to the right
        elif self.controls[3] in keys:
            self.state = "running"
            self.direction = "right"
            self.x += self.speed
            if self.state != "running" or self.direction != "right":
                self.imageCycle = 0

        # Running to the left
        elif self.controls[1] in keys:
            self.state = "running"
            self.direction = "left"
            self.x -= self.speed
            if self.state != "running" or self.direction != "left":
                self.imageCycle = 0

        # Idle
        else:
            self.imageCycle = 0
            self.state = "standing idle"
            self.x -= idleCharacterSpeed

    def checkBorders(self):
        """Keeps characters on the screen."""

        # Left border
        if self.x - (8 * self.size) < 0:
            self.x = 8 * self.size

        # Right border
        if self.x + (8 * self.size) > self.window.getWidth():
            self.x = self.window.getWidth()-(8 * self.size)

        # Top border
        if self.y - (12 * self.size) < 0:
            self.y = 12 * self.size

        # Bottom border
        if self.y + (8 * self.size) > 431:
            self.y = 431 - (12 * self.size)


class Spike:
    """Basic building block for a spike object."""
    def __init__(self, x, y, size, imagePath, window):
        """Constructs a spike object."""
        self.x = x
        self.y = y
        self.size = size
        self.imagePath = imagePath
        self.window = window
        self.image = Image(Point(self.x, self.y), self.imagePath)
        self.image.transform(size)
        self.hitBox = Rectangle(Point(0, 0), Point(0, 0))

    def draw(self):
        """Draws a spike object."""
        self.undraw()
        self.move(backgroundSpeed)
        self.image = Image(Point(self.x, self.y), self.imagePath)
        self.image.transform(self.size)
        self.image.draw(self.window)

        # Creates a hitbox for the spike object (these numbers are calculated through guess & check)
        self.hitBox = Rectangle(Point(self.x - (126 * self.size), self.y - (112 * self.size)),
                                Point(self.x + (126 * self.size), self.y + (126 * self.size)))
        self.hitBox.setOutline("red")

        # Only used for testing purposes
        #self.hitBox.draw(self.window)

    def undraw(self):
        """Undraws an obstacle."""
        self.image.undraw()
        self.hitBox.undraw()

    def move(self, speed):
        """Moves an obstacle by editing the x value."""
        self.x -= speed


class Monkey(Spike):
    """Basic building block for a monkey object."""
    def draw(self):
        """Draws a monkey object."""
        self.undraw()
        self.move(backgroundSpeed)
        self.image = Image(Point(self.x, self.y), self.imagePath)
        self.image.transform(self.size)
        self.image.draw(self.window)

        # Creates a hitbox for the monkey object (these numbers are calculated through guess & check)
        self.hitBox = Rectangle(Point(self.x - (75 * self.size), self.y - (130 * self.size)),
                                Point(self.x + (104 * self.size), self.y + (127 * self.size)))
        self.hitBox.setOutline("red")

        # Only used for testing purposes
        #self.hitBox.draw(self.window)


class CreepyCrawly(Spike):
    """Basic building block for a Creepy Crawly object"""
    def draw(self):
        """Draws a creepy crawly object."""
        self.undraw()
        self.move(backgroundSpeed)
        self.image = Image(Point(self.x, self.y), self.imagePath)
        self.image.transform(self.size)
        self.image.draw(self.window)

        # Creates hitbox for the creepy crawly object (these numbers are calculated through guess & check)
        self.hitBox = Rectangle(Point(self.x - (126 * self.size), self.y - (112 * self.size)),
                                Point(self.x + (126 * self.size), self.y + (126 * self.size)))
        self.hitBox.setOutline("red")

        # Only used for testing purposes
        # self.hitBox.draw(self.window)


class Rocket(Spike):
    """Basic building block for a rocket object"""
    def draw(self):
        """Draws a rocket object."""
        self.undraw()
        self.move(backgroundSpeed)
        self.image = Image(Point(self.x, self.y), self.imagePath)
        self.image.transform(self.size)
        self.image.draw(self.window)

        # Creates hitbox for the rocket object (these numbers are calculated through guess & check)
        self.hitBox = Rectangle(Point(self.x - (75 * self.size), self.y - (130 * self.size)),
                                Point(self.x + (104 * self.size), self.y + (127 * self.size)))
        self.hitBox.setOutline("red")

        # Only used for testing purposes
        # self.hitBox.draw(self.window)


class SpaceInvader(Spike):
    """Basic building block for a rocket object"""

    def draw(self):
        """Draws a space invader object."""
        self.undraw()
        self.move(backgroundSpeed)
        self.image = Image(Point(self.x, self.y), self.imagePath)
        self.image.transform(self.size)
        self.image.draw(self.window)

        # Creates hitbox for the space invader object (these numbers are calculated through guess & check)
        self.hitBox = Rectangle(Point(self.x - (75 * self.size), self.y - (130 * self.size)),
                                Point(self.x + (104 * self.size), self.y + (127 * self.size)))
        self.hitBox.setOutline("red")

        # Only used for testing purposes
        # self.hitBox.draw(self.window)
