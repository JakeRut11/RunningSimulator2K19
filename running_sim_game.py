# -------------------------------------------------------------------------------------------------------------------- #
# Program: Running Simulator 2k19 Game
# Authors: Michael Schmauderer and Jake Rutkowski
# Description: Main game loop for the running sim 2k19 game.
# Date Modified: 5/27/2019
# Version: 1.1

# -------------------------------------------------------------------------------------------------------------------- #
# Import Libraries
from running_sim_objects import *
import random
import simpleaudio as sa

# -------------------------------------------------------------------------------------------------------------------- #
# Global Variables

# Create the window for the game
window = GraphWin("Running Sim 2k19", 1024, 512, autoflush=False)

# Variables for characters in the game
characters = []
char = 0
selectedCharacter = ""

# Variables for obstacles in the game
obstacles = []
obstacleTimer = 1000

# Variables for the different backgrounds in the game
back1 = Image(Point(512, 256), "assets/images/maps/ogBackground.png")
back2 = Image(Point(1536, 256), "assets/images/maps/ogBackground.png")
start = Image(Point(512, 256), "assets/images/menus/runningSimulatorStartScreen.png")
controls = Image(Point(512, 256), "assets/images/menus/runningSimulatorControlsScreen.png")
multiplayerControls = Image(Point(512, 256), "assets/images/menus/runningSimulatorMultiplayerControlsScreen.png")
characterSelection = Image(Point(512, 256), "assets/images/menus/runningSimulatorCharacterScreen.png")

# Create the seconds timer
sec = 0
secondsTimer = Text(Point(985, 30), "")

# Create the high score counter
highScore = 0
highScoreCounter = Text(Point(window.getWidth()//2, 30), "")

# Create the difficulty variable
difficulty = "Easy"
difficultyID = Text(Point(170, 30), "")

# Create the leader variable for multiplayer
leader = ""
leaderID = Text(Point(window.getWidth()//2, 30), "")

# Create the individual scores variables for multiplayer
scores = Text(Point(920, 65), "")

# Start screen variables
gamemode = "highscore"
singleplayerBox = Rectangle(Point(304, 363), Point(466, 423))
multiplayerBox = Rectangle(Point(486, 363), Point(648, 423))
singleplayerText = Text(Point(385, 393), "Highscore\nMode")
multiplayerText = Text(Point(567, 393), "Multiplayer\nMode")

# Character selection variables
directions = Text(Point(window.getWidth()//2, 470), "--Use The Number Keys--\nto Select a Character")
p1Directions = Text(Point(window.getWidth()//2, 125), "Player 1, Select Your Character")
p2Directions = Text(Point(window.getWidth()//2, 125), "Player 2, Select Your Character")

# Controls screen variables
controlsScreenInstructions = Text(Point(window.getWidth()//2, 480), "Press Any Key to Continue")
p1ControlsDirections = Text(Point(window.getWidth()//2, 320), "Keys to Remember:\n\nPlayer 1: w,a,s,d")
p2ControlsDirections = Text(Point(window.getWidth()//2, 400), "Player 2: 8,4,5,6 (numpad)")

# Music
menuMusic = sa.WaveObject.from_wave_file("assets/sounds/wiiShop8Bit.wav")
gameMusic = sa.WaveObject.from_wave_file("assets/sounds/wiiSportsResort8Bit.wav")
oof = sa.WaveObject.from_wave_file("assets/sounds/oof.wav")

# -------------------------------------------------------------------------------------------------------------------- #
# Global Properties
window.setBackground("white")

# All characters start off alive and well
isDead = False

# Properties for the seconds timer
secondsTimer.setSize(34)
secondsTimer.setStyle("bold")

# Properties for the individual scores counter
scores.setSize(24)
scores.setStyle("bold")

# Properties for the high score counter
highScoreCounter.setSize(30)
highScoreCounter.setStyle("bold")
highScoreCounter.setTextColor("red")

# Properties for the leader ID
leaderID.setSize(30)
leaderID.setStyle("bold")
leaderID.setTextColor("red")

# Properties for the difficulty ID
difficultyID.setSize(26)
difficultyID.setStyle("bold")

# Properties for the character selection screen
p1Directions.setSize(30)
p1Directions.setStyle("bold")
p2Directions.setSize(30)
p2Directions.setStyle("bold")

# Properties for the start screen
singleplayerBox.setFill("gray")
singleplayerText.setSize(20)

multiplayerBox.setFill("gray")
multiplayerText.setSize(20)

directions.setSize(30)
directions.setStyle("bold")

# Properties for the controls screen
controlsScreenInstructions.setSize(30)
controlsScreenInstructions.setStyle("bold")

p1ControlsDirections.setSize(24)
p2ControlsDirections.setSize(24)

# -------------------------------------------------------------------------------------------------------------------- #
# Functions


def moveBackground():
    """Moves the background and any obstacles."""
    # Reset background images if necessary
    if back1.anchor.x <= -512:          # Moves the first image from past the left side to past the right side
        back1.undraw()
        back1.anchor.x = 1536
        back1.draw(window)
    back1.move(-backgroundSpeed, 0)     # Moves the first image to the left at the background speed

    if back2.anchor.x <= -512:          # Moves the second image from past the left side to past the right side
        back2.undraw()
        back2.anchor.x = 1536
        back2.draw(window)
    back2.move(-backgroundSpeed, 0)     # Moves the second image to the left at the background speed


def checkCollision():
    """Checks whether a character object is colliding with an obstacle object."""
    global isDead, char, sec, leader

    # Tests whether a character is colliding with the hitbox of the test spike
    for obstacle in obstacles:
        if characters[char].x + (8 * characters[char].size) >= obstacle.hitBox.p1.x and \
                                characters[char].x - (8 * characters[char].size) <= obstacle.hitBox.p2.x:
            if characters[char].state != "crouching" and characters[char].state != "crouching idle":
                if characters[char].y + (11 * characters[char].size) >= obstacle.hitBox.p1.y and \
                                        characters[char].y - (11 * characters[char].size) <= obstacle.hitBox.p2.y:
                    isDead = True
            else:
                if characters[char].y + (5 * characters[char].size) >= obstacle.hitBox.p1.y and \
                                        characters[char].y - (5 * characters[char].size) <= obstacle.hitBox.p2.y:
                    isDead = True

    # Moves a character all the way to the left (backwards) if they hit a spike and reset the timer, add a mistake
    if isDead:
        oof.play() # -- this is very annoying
        characters[char].x = 20
        characters[char].mistakes += 1

        # Update the current leader based on who has less mistakes
        if gamemode == "multiplayer":
            if characters[0].mistakes > characters[1].mistakes:
                leader = "Player 2"
            else:
                leader = "Player 1"

        sec = 0
        isDead = False

    # Increment the char counter to test another character
    char += 1

    # Reset the char counter when it goes beyond the amount of characters
    if char > len(characters) - 1:
        char = 0


def createObstacles():
    """Creates obstacles at random."""
    # Select a random number, 0 - 4
    r = random.randrange(4)

    # If the number is 0, create a spike obstacle
    if r == 0:
        obstacles.append(Spike(1200, 415, .25, "assets/images/obstacles/Spikes.png", window))

    # If the number is 1, create a creepy crawly obstacle
    elif r == 1:
        obstacles.append(CreepyCrawly(1200, 415, .25,"assets/images/obstacles/CreepyCrawly.png", window))

    # If the number is 2, create a rocket obstacle
    elif r == 2:
        obstacles.append(Rocket(1200, 340, .25, "assets/images/obstacles/Rocket.png", window))

    # If the number is 3, create a space invader obstacle
    elif r == 3:
        obstacles.append(SpaceInvader(1200, 340, .3, "assets/images/obstacles/SpaceInvader.png", window))

    # If the number is, create a monkey obstacle
    else:
        obstacles.append(Monkey(1200, 310, .5, "assets/images/obstacles/Monkey.png", window))


def createCharacters(name):
    """Creates a list of characters based on input."""

    # Appends a character to the characters list based on the name of that character
    if name == "Jamir":
        if gamemode == "highscore":
            characters.append(Character(window.getWidth()//2, 395, "Jamir", 7, window, ("w", "a", "s", "d"), 3))

        # Uses w,a,s,d if player 1 in multiplayer mode, otherwise uses numpad keys 8,4,5,6
        else:
            if len(characters) > 0:
                characters.append(Character(window.getWidth() // 2, 395, "Jamir", 7, window, ("8", "4", "5", "6"), 3))
            else:
                characters.append(Character(window.getWidth() // 2, 395, "Jamir", 7, window, ("w", "a", "s", "d"), 3))

    elif name == "Shalissa":
        if gamemode == "highscore":
            characters.append(Character(window.getWidth()//2, 395, "Shalissa", 7, window, ("w", "a", "s", "d"), 3))
        else:
            if len(characters) > 0:
                characters.append(Character(window.getWidth() // 2, 395, "Shalissa", 7, window,
                                            ("8", "4", "5", "6"), 3))
            else:
                characters.append(Character(window.getWidth() // 2, 395, "Shalissa", 7, window,
                                            ("w", "a", "s", "d"), 3))

    elif name == "Weeb Sean":
        if gamemode == "highscore":
            characters.append(Character(window.getWidth()//2, 395, "Weeb Sean", 7, window, ("w", "a", "s", "d"), 3))
        else:
            if len(characters) > 0:
                characters.append(Character(window.getWidth() // 2, 395, "Weeb Sean", 7, window,
                                            ("8", "4", "5", "6"), 3))
            else:
                characters.append(Character(window.getWidth() // 2, 395, "Weeb Sean", 7, window,
                                            ("w", "a", "s", "d"), 3))

    elif name == "Shadow Man":
        if gamemode == "highscore":
            characters.append(Character(window.getWidth()//2, 395, "Shadow Man", 7, window, ("w", "a", "s", "d"), 3))
        else:
            if len(characters) > 0:
                characters.append(Character(window.getWidth() // 2, 395, "Shadow Man", 7, window,
                                            ("8", "4", "5", "6"), 3))
            else:
                characters.append(Character(window.getWidth() // 2, 395, "Shadow Man", 7, window,
                                            ("w", "a", "s", "d"), 3))

# -------------------------------------------------------------------------------------------------------------------- #
# Main


def main():
    """Runs the actual game."""
    global sec, obstacleTimer, highScore, difficulty, gamemode

    # Start menu music
    playMenuMusic = menuMusic.play()

    # Used to determine if a user is still on the start screen
    stillOnStartScreen = True
    stillOnStartScreen2 = True

    # Create the start up screen
    start.draw(window)
    singleplayerBox.draw(window)
    singleplayerText.draw(window)
    multiplayerBox.draw(window)
    multiplayerText.draw(window)

    # Creates a time to return to if the user does not click a gamemode button
    while stillOnStartScreen:

        # Retrieve current mouse location
        window.getMouse()
        mouse = window.getCurrentMouseLocation()

        # Test if highscore mode button was selected, highlights selection and updates gamemode
        if 304 < mouse.x < 466 and 363 < mouse.y < 423:
            multiplayerText.setTextColor("black")
            multiplayerText.setStyle("normal")
            singleplayerText.setTextColor("yellow")
            singleplayerText.setStyle("bold")
            gamemode = "highscore"

        # Retrieve current mouse location (again)
        window.getMouse()
        mouse = window.getCurrentMouseLocation()

        # Tests if multiplayer mode button was selected, highlights selection and updates gamemode
        if 486 < mouse.x < 648 and 363 < mouse.y < 423:
            singleplayerText.setTextColor("black")
            singleplayerText.setStyle("normal")
            multiplayerText.setTextColor("yellow")
            multiplayerText.setStyle("bold")
            gamemode = "multiplayer"

        # Creates a time to return to if the user does not click the continue button
        while stillOnStartScreen2:
            window.getMouse()

            # Retrieves the current mouse location
            mouse = window.getCurrentMouseLocation()

            # Show character selection screen if user clicks the continue button/undraws last screen
            if 304 < mouse.x < 648 and 256 < mouse.y < 343:
                characterSelection.draw(window)
                directions.draw(window)
                start.undraw()
                singleplayerBox.undraw()
                singleplayerText.undraw()
                multiplayerBox.undraw()
                multiplayerText.undraw()

                # Singleplayer
                if gamemode == "highscore":

                    # Store key press as key
                    key = window.getKey()

                    # Selects a character based on key pressed
                    if key == "1":
                        createCharacters("Jamir")
                    elif key == "2":
                        createCharacters("Shalissa")
                    elif key == "3":
                        createCharacters("Weeb Sean")
                    elif key == "4":
                        createCharacters("Shadow Man")

                # Multiplayer
                else:

                    # Draw directions for player 1
                    p1Directions.draw(window)

                    # Stores first key being pressed
                    key1 = window.getKey()

                    # Selects a first character based on the key being pressed
                    if key1 == "1":
                        createCharacters("Jamir")
                    elif key1 == "2":
                        createCharacters("Shalissa")
                    elif key1 == "3":
                        createCharacters("Weeb Sean")
                    elif key1 == "4":
                        createCharacters("Shadow Man")
                    p1Directions.undraw()

                    # Draw directions for player 2
                    p2Directions.draw(window)

                    # Stores second key being pressed
                    key2 = window.getKey()

                    # Selects a second character based on the key being pressed
                    if key2 == "1":
                        createCharacters("Jamir")
                    elif key2 == "2":
                        createCharacters("Shalissa")
                    elif key2 == "3":
                        createCharacters("Weeb Sean")
                    elif key2 == "4":
                        createCharacters("Shadow Man")

                # Draw the singleplayer controls screen, continue when any key is pressed/undraw last screen
                if gamemode == "highscore":
                    controls.draw(window)
                    controlsScreenInstructions.draw(window)
                    window.getKey()
                    characterSelection.undraw()
                    directions.undraw()

                # Draw the multiplayer controls screen, continue when any key is pressed/undraw last screen
                else:
                    multiplayerControls.draw(window)
                    controlsScreenInstructions.draw(window)
                    p1ControlsDirections.draw(window)
                    p2ControlsDirections.draw(window)
                    window.getKey()
                    characterSelection.undraw()
                    directions.undraw()
                    p2Directions.undraw()

                # Initialize the background images and characters list/undraw last screen
                back1.draw(window)
                back2.draw(window)

                if gamemode == "highscore":
                    controls.undraw()
                    controlsScreenInstructions.undraw()

                else:
                    multiplayerControls.undraw()
                    controlsScreenInstructions.undraw()
                    p1ControlsDirections.undraw()
                    p2ControlsDirections.undraw()

                # Timer for the main game loop
                timeStart = int(time.time() * 100)

                # Main game loop

                # Stop all music
                sa.stop_all()

                # Play main game music
                playGameMusic = gameMusic.play()
                while not window.isClosed():

                    # Main game music loop
                    if not playGameMusic.is_playing():
                        playGameMusic = gameMusic.play()

                    # Another current time variable to check the main timer
                    timeCurrent = int(time.time() * 100)

                    # If a second has passed, add a second to the timer
                    if timeStart // 100 != timeCurrent // 100:
                        sec += 1

                    # If any time has passed...
                    if timeStart != timeCurrent:
                        timeStart = timeCurrent

                        # Create another obstacle every -- seconds
                        if timeCurrent % obstacleTimer == 0:
                            createObstacles()

                        # Move characters and obstacles
                        if timeCurrent % 4 == 0:
                            for character in characters:
                                character.draw()

                            for obstacle in obstacles:
                                obstacle.draw()
                                # Remove obstacles once they are off the screen (lag)
                                if obstacle.x < -50:
                                    obstacle.undraw()
                                    obstacles.pop(obstacles.index(obstacle))

                            if gamemode == "highscore":
                                # Update the seconds timer for highscore mode (singleplayer)
                                secondsTimer.undraw()
                                secondsTimer.setText(sec)
                                secondsTimer.draw(window)

                                # Update the high score counter for highscore mode (singleplayer)
                                highScoreCounter.undraw()
                                highScoreCounter.setText("High Score: {}".format(highScore))
                                highScoreCounter.draw(window)
                            else:
                                # Update the scores counters
                                scores.undraw()
                                scores.setText("Mistakes\nPlayer 1: {}\nPlayer 2: {}"
                                               .format(characters[0].mistakes, characters[1].mistakes))
                                scores.draw(window)

                                # Update the leader ID
                                leaderID.undraw()
                                leaderID.setText("Leader: {}".format(leader))
                                leaderID.draw(window)

                            # Update the difficulty ID
                            difficultyID.undraw()
                            difficultyID.setText("Difficulty: {}".format(difficulty))
                            difficultyID.draw(window)

                            # Speed up the game/change difficulty if the player survives for -- seconds
                            if 30 <= sec < 90:
                                obstacleTimer = 1000
                                difficulty = "Moderate"
                            elif sec >= 90:
                                obstacleTimer = 700
                                difficulty = "Hard"
                                for character in characters:
                                    if character.name != "Rainbow":
                                        character.undraw()
                                        character.name = "Rainbow"
                                        character.clearAnimations()
                                        character.createAnimations()
                                        character.draw()
                            else:
                                obstacleTimer = 1500
                                difficulty = "Easy"
                                for character in characters:
                                    if character.name == "Rainbow":
                                        character.undraw()
                                        character.name = character.trueIdentity
                                        character.clearAnimations()
                                        character.createAnimations()
                                        character.draw()

                            # Update the high score each time a new high score is reached
                            if sec > highScore:
                                highScore = sec

                            # Check for collisions, move the background, update the window
                            checkCollision()
                            moveBackground()
                            window.update()

            # Goes back to start screen if the continue button was never clicked
            else:
                stillOnStartScreen2 = True

        else:
            stillOnStartScreen = True

# -------------------------------------------------------------------------------------------------------------------- #
# Call Main
main()
