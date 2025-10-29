import sys
import os

sys.path.insert(0, "/system/apps/flappy")
os.chdir("/system/apps/flappy")

from badgeware import screen, Image, PixelFont, SpriteSheet, io, brushes, shapes, run
from mona import Mona
from obstacle import Obstacle
from ai_player import AIPlayer
from leaderboard import Leaderboard

background = Image.load("assets/background.png")
grass = Image.load("assets/grass.png")
cloud = Image.load("assets/cloud.png")
large_font = PixelFont.load("/system/assets/fonts/ziplock.ppf")
small_font = PixelFont.load("/system/assets/fonts/nope.ppf")
ghost = SpriteSheet("/system/assets/mona-sprites/mona-dead.png", 7, 1).animation()
mona = None


class GameState:
    INTRO = 1
    PLAYING = 2
    GAME_OVER = 3


state = GameState.INTRO
demo_mode = True  # Start in demo mode by default
ai_player = None
restart_delay = None  # Timestamp for when to restart in demo mode


def update():
    draw_background()

    if state == GameState.INTRO:
        intro()

    if state == GameState.PLAYING:
        play()

    if state == GameState.GAME_OVER:
        game_over()


# handle the intro screen of the game, shows the game title and a message to
# tell the player how to start the game


intro_start_time = None

def intro():
    global state, mona, demo_mode, ai_player, intro_start_time

    # Track when we entered intro state
    if intro_start_time is None:
        intro_start_time = io.ticks

    # draw title
    screen.font = large_font
    center_text("FLAPPY MONA", 38)

    # Show demo mode indicator
    if demo_mode:
        screen.font = small_font
        center_text("DEMO MODE", 55)
        # Auto-start after a brief pause
        time_in_intro = io.ticks - intro_start_time
        if time_in_intro > 1500:  # Wait 1.5 seconds before starting
            intro_start_time = None
            start_game()
    else:
        # blink button message for manual mode
        if int(io.ticks / 500) % 2:
            screen.font = small_font
            center_text("Press A to start", 70)

        if io.BUTTON_A in io.pressed:
            intro_start_time = None
            start_game()

    # Allow toggling demo mode with button C
    if io.BUTTON_C in io.pressed:
        demo_mode = not demo_mode


def start_game():
    """Initialize game state for a new game."""
    global state, mona, ai_player
    
    # reset game state
    state = GameState.PLAYING
    Obstacle.obstacles = []
    Obstacle.next_spawn_time = io.ticks + 500
    mona = Mona()
    
    # Initialize AI player if in demo mode
    if demo_mode:
        ai_player = AIPlayer()
    else:
        ai_player = None

# handle the main game loop and user input. each tick we'll update the game
# state (read button input, move mona, create new obstacles, etc..) then
# draw the background and sprites


def play():
    global state

    # Handle input - either AI or human player
    if not mona.is_dead():
        if demo_mode and ai_player:
            # AI makes the decision
            if ai_player.should_jump(mona, io.ticks):
                mona.jump()
        elif io.BUTTON_A in io.pressed:
            # Human player input
            mona.jump()

    # update player and check for collision
    mona.update()

    # spawn a new obstacle if the spawn timer has elapsed
    if not mona.is_dead() and Obstacle.next_spawn_time and io.ticks > Obstacle.next_spawn_time:
        Obstacle.spawn()

    # update obstacle positions and draw them
    for obstacle in Obstacle.obstacles:
        if not mona.is_dead():
            obstacle.update()
        obstacle.draw()

    # draw our hero, mona
    mona.draw()

    # show the player their current score
    screen.font = small_font
    shadow_text(f"Score: {mona.score}", 3, 0)
    
    # Show demo mode indicator during gameplay
    if demo_mode:
        shadow_text("DEMO", 3, 12)

    # has mona died this frame? if so it's... GAME OVER
    if mona.is_dead():
        if mona.is_done_dying():
            state = GameState.GAME_OVER

# handle the GAME OVER screen. show the player what score they achieved and
# provide instructions for how to start again


def game_over():
    global state, restart_delay

    # Save score to leaderboard
    if mona and mona.score > 0:
        player_type = "DEMO" if demo_mode else "HUMAN"
        Leaderboard.save_score(mona.score, player_type)

    # game over caption
    screen.font = large_font
    center_text("GAME OVER!", 18)

    # players final score
    screen.font = small_font
    center_text(f"Final score: {mona.score}", 40)
    
    # Show high score
    high_score = Leaderboard.get_high_score()
    if high_score > 0:
        center_text(f"High score: {high_score}", 52)

    # Handle restart based on mode
    if demo_mode:
        # Auto-restart in demo mode after a delay
        if restart_delay is None:
            restart_delay = io.ticks + 2000  # 2 second delay
        
        # Show countdown
        time_left = (restart_delay - io.ticks) / 1000
        if time_left > 0:
            center_text(f"Restarting in {int(time_left + 1)}...", 70)
        
        if io.ticks >= restart_delay:
            restart_delay = None
            state = GameState.INTRO
    else:
        # Manual restart for human player
        if int(io.ticks / 500) % 2:
            screen.brush = brushes.color(255, 255, 255)
            center_text("Press A to restart", 70)

        if io.BUTTON_A in io.pressed:
            # return game to intro state
            state = GameState.INTRO


# draw the scrolling background with parallax layers
background_offset = 0


def draw_background():
    global background_offset

    # clear the whole screen in a bright blue
    screen.brush = brushes.color(73, 219, 255)
    screen.draw(shapes.rectangle(0, 0, 160, 120))

    # if we're on the intro screen or mona is alive then scroll the background
    if not mona or not mona.is_dead() or state == GameState.INTRO:
        background_offset += 1

    for i in range(3):
        # draw the distance background
        bo = ((-background_offset / 8) % background.width) - screen.width
        screen.blit(background, bo + (background.width * i),
                    120 - background.height)

        # draw the cloud background
        bo = ((-background_offset / 8) % (cloud.width * 2)) - screen.width
        screen.blit(cloud, bo + (cloud.width * 2 * i), 20)

    for i in range(3):
        # draw the grass layer
        bo = ((-background_offset / 4) % (grass.width)) - screen.width
        screen.blit(grass, bo + (grass.width * i), 120 - grass.height)

# a couple of helper functions for formatting text


def shadow_text(text, x, y):
    screen.brush = brushes.color(20, 40, 60, 100)
    screen.text(text, x + 1, y + 1)
    screen.brush = brushes.color(255, 255, 255)
    screen.text(text, x, y)


def center_text(text, y):
    w, _ = screen.measure_text(text)
    shadow_text(text, 80 - (w / 2), y)


if __name__ == "__main__":
    run(update)
