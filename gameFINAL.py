import pgzrun
import random
import time
import media
from itertools import cycle
 

music.play('dinnosoundtrack')

TITLE = 'DINOPLAY'

 

#Gathering the dimensions of the background image

WIDTH = 1060

HEIGHT = 972

#Global timer variables for the countdown

score = 0

timer = 0

 

 

'''INTRODUCING THE GAME STATES'''

game = Actor ('dino_background')

# Setting the screens used in the game

game.state = ['title', 'dino_background', 'the_end', 'you_win']

#Setting the title screen to begin with

game.current_state = game.state[0]

 

'''INTRODUCING THE DINOSAUR'''

explorer = Actor('dinosaur8bit')

explorer.pos = (100, 830)

# Image cycle for walking toward the right

explorer.rwalk = ['dinobackleg','dinosaur8bit','dinofrontleg']

# Image cycle for walking toward the left

explorer.lwalk = ['left_dinobackleg', 'leftdinosaur8bit','left_dinofrontleg']

current_state = 0

# Dinosaur starts in a still stance

explorer.walking = False

explorer.facing_right = False

 

# The property for the dinosaur to stay still in a standing stance

    #This is used in the on_key_down function

explorer.rdino = 'dinosaur8bit'

explorer.ldino = 'leftdinosaur8bit'

 

# Setup a cycle to easily walk through all of the images to the right

explorer.rwalk_cycle = cycle(explorer.rwalk)

# Setup a cycle to easily walk through all of the images to the left

explorer.lwalk_cycle = cycle(explorer.lwalk)

 

fireballs = []


 

'''PUTTING IT ALL TOGETHER'''

def draw():

    #Beginning the game at the title screen

    if game.current_state == 'title':

        #Function for the title screen

        draw_main_menu()

    # Up arrow triggers the game screen

    elif game.current_state == 'dino_background':

        global fireballs

        # Drawing the interactive portion

        draw_game_background()

        # Tell the explorer to draw to the screen

        explorer.draw()

        for fireball in fireballs:

        # Tell each zombie to draw to the screen

            fireball.draw()

        if explorer.left > WIDTH-10:

            explorer.x = 0

        screen.draw.text(f"{score}", (110, 20))

    elif game.current_state == 'the_end':

        draw_end_game()

    elif game.current_state == 'you_win':

        draw_win()

 
     

'''TIMER'''

# Create class that acts as a countdown

def countdown():

    # Triggers the timer to begin when the player is ready

    if game.current_state == 'dino_background':

        global score

        global timer

        # Max time

        total_seconds = 1000

        # Adding one repeatedly

        timer += 1

        score = timer

        # Once timer equals total_seconds

        if total_seconds == timer:

            # Then swicth the game to win screen

            game.current_state = game.state[3]

 

  

       

'''ALL GAME STATES'''

# Game state [0]: the title screen

def draw_main_menu():

    game.draw()

    #Drawing out the details

    screen.blit('title', (0,0))

    screen.blit('press-enter', (450, 700))

    #This triggers the next game state to begin playing

    if keyboard.RETURN:

        #Sound effect to indicate the beginning of the game

        sounds.coin.play()

        game.current_state = game.state[1]

        clock.schedule_interval(spawn_fireball, 1.5)

 

# Game state [1]: colorful background

def draw_game_background():

    global timer

    #Displaying the timer as the score

    screen.draw.text("{timer}", (0,10))

    #Drawing out the background

    game.draw()

    screen.blit('dino_background', (0,0))

    #Back button (trigger with letter b on the keyboard)

    if keyboard.B:

        #Setting the timer to zero

        timer = 0

        #Setting the game state to the beginning

        game.current_state = game.state[0]

        clock.unschedule(spawn_fireball)

   

# Game state [2]: lose background

def draw_end_game():

    game.draw()

    screen.blit('the_end', (0,0))

 

#Game state [3]: win background

def draw_win():

    game.draw()

    screen.blit('you_win', (0,0))

 

 

 

'''UPDATING THE SCREEN AND ANIMATIONS'''

# Updating the screen

def update(dt):

    # Check arrow keys

    check_keys(dt)

    if game.current_state == 'title':

        timer = 0

    if game.current_state == 'dino_background':

        countdown()

        global fireballs

        # Call our function to move the fireballs

        move_fireball(dt)

        # Remove any fireballs that are no longer on screen

        fireballs = fireball_cleanup()

    #Keeping track if dino hits the fireball

    check_dino_collisions()

 

 

 

'''DINOSAUR ANIMATION'''

# Moves the dinosaur to desired location

def check_keys(dt):

    # Check is the left arrow key is pressed

    if keyboard.left:

        # Move the explorer to the left

        explorer.x -= dt * 150

    # Check if the right arrow key is pressed

    if keyboard.right:

        # Move the explorer to the right

        explorer.x += dt * 150

    explorer.walking = False

   

# Animation that runs when a key is pressed

def on_key_down():

    # If the right key is pressed

    if keyboard.right:

        #Make walking true

        explorer.walking = True

        if explorer.walking:

            # Walking right = facing the right

            explorer.facing_right = True

            # Recreate the cycle (so we start at the beginning)

            explorer.rwalk_cycle = cycle(explorer.rwalk)

            # Stop walking to the left

            clock.unschedule(explorer_lwalk_anim)

            # Schedule an dinosaur to walk to the right

            clock.schedule_interval(explorer_rwalk_anim, 0.1)

    # If the left key is pressed

    elif keyboard.left:

        # Make walking true

        explorer.walking = True

        if explorer.walking:

            # Walking to the left = not facing the right

            explorer.facing_right = False

            # Recreate the cycle (so we start at the beginning)

            explorer.lwalk_cycle = cycle(explorer.lwalk)

            # Stop walking to the right

            clock.unschedule(explorer_rwalk_anim)

            # Schedule the dinosaur to walk to the left

            clock.schedule_interval(explorer_lwalk_anim, 0.1)

           

    #No keys should make the dinosaur not walk at all

    else:

        explorer.walking = False

        clock.unschedule(explorer_rwalk_anim)

        clock.unschedule(explorer_lwalk_anim)   

 

# Run repeatedly to change walk cycle images

#   and create animation

def explorer_rwalk_anim():

    # Each call to next will get us the next

    #   item in the list or cycle back to the

    #   beginning of the list. Set that to the

    #   explorer Actor's image variable.

    explorer.image = next(explorer.rwalk_cycle)

   

def explorer_lwalk_anim():

    # Each call to next will get us the next

    #   item in the list or cycle back to the

    #   beginning of the list. Set that to the

    #   explorer Actor's image variable.

    explorer.image = next(explorer.lwalk_cycle)

 

 

 

'''FIREBALL CODE'''

# Moving the fireballs downward

def move_fireball(dt):

    # Get the fireball list variable

    global fireballs

    # Loop over all the fireballs in the list

    for fireball in fireballs:

        # Moving the fireball down

        fireball.y += dt * 200

        # Check if the fireball is off screen

        if fireball.y > HEIGHT + 100:

            # Mark it as safe to cleanup

            fireball.alive = False

 

# Function to dynamically create fireballs

def spawn_fireball():

    # Get the fireball list variable

    global fireballs

    # Spawning fireball at random range

    xpos = random.randint(50, WIDTH-50)

    # Create fireball actor

    fireball = Actor('fireball')

    # Set the fireball actors position to be off screen

    fireball.pos = (xpos, -50)

    # Add a property to set the fireballs to start "alive"

    fireball.alive = True

    # Append (add) our fireball to the end of the list

    fireballs.append(fireball)

   

# Getting rid of fireballs if off screen

def fireball_cleanup():

    # Get the fireballs list variable

    global fireballs

    # Create a new empty list

    new_list = []

    # Get each fireball from the list of fireball

    for fireball in fireballs:

        # Check if the fireball is "alive"

        #   since alive is True or False this

        #   condition is valid

        if fireball.alive:

            new_list.append(fireball)

    # Return the new list without the fireballs that

    #   are not alive

    return new_list

    if keyboard.B:

        if fireball.alive == False:

            new_list.append(fireball)

 

def check_dino_collisions():

    global fireballs

    # Check all fireballs

    for fireball in fireballs:

        # Checking if dinosaur hit the fireball

        if explorer.colliderect(fireball) and fireball.alive:

            # Sound effect for collision

            #music.play('explode')

            # Changing game state if collision

            game.current_state = game.state[2]

            # Stop spawning fireballs

            clock.unschedule(spawn_fireball)

            # Empty the fireball list

            fireballs = []

            #Sound effect to indicate collison

            sounds.explode.play()

 

# This needs to be the last line to use pygame zero

pgzrun.go()