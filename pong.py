import curses
from curses import KEY_UP, KEY_DOWN

# Constants for the game
MAX_SCORE = 10
PADDLE_HEIGHT = 3
BALL_SPEED = 1

# Initialize the game state
score1 = 0  # Player 1's score
score2 = 0  # Player 2's score
paddle1_y = 10  # Player 1's paddle position
paddle2_y = 10  # Player 2's paddle position
ball_x = 40  # Ball's x position
ball_y = 12  # Ball's y position
ball_dx = BALL_SPEED  # Ball's x velocity
ball_dy = BALL_SPEED  # Ball's y velocity
paused = False  # Game is paused

# Function to initialize the screen
def init_screen(screen):
    # Set up the screen
    curses.curs_set(0)  # Invisible cursor
    screen.nodelay(1)  # Non-blocking input
    screen.keypad(1)  # Enable special keys
    curses.noecho()  # Turn off auto echoing of keypresses
    curses.cbreak()  # React to keys without needing Enter

# Function to draw the game state
def draw_screen(screen):
    screen.clear()  # Clear the screen
    # Draw the paddles and ball
    for i in range(PADDLE_HEIGHT):
        screen.addstr(paddle1_y + i, 2, '|')
        screen.addstr(paddle2_y + i, 77, '|')
    screen.addstr(ball_y, ball_x, 'O')
    # Draw the scores
    screen.addstr(0, 35, f'Score: {score1} - {score2}')
    screen.refresh()  # Refresh the screen to show changes

# Function to update the game state
def update_game():
    global ball_x, ball_y, ball_dx, ball_dy, score1, score2
    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy
    # Check for collision with top and bottom
    if ball_y <= 0 or ball_y >= curses.LINES - 1:
        ball_dy *= -1
    # Check for collision with paddles
    if ball_x <= 3 and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
        ball_dx *= -1
    elif ball_x >= 76 and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
        ball_dx *= -1
    # Check for scoring
    if ball_x <= 0:
        score2 += 1
        reset_ball()
    elif ball_x >= curses.COLS - 1:
        score1 += 1
        reset_ball()
    # Check for win condition
    if score1 >= MAX_SCORE or score2 >= MAX_SCORE:
        return False  # End the game
    return True  # Continue the game

# Function to reset the ball to the center
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = curses.COLS // 2
    ball_y = curses.LINES // 2
    ball_dx = BALL_SPEED
    ball_dy = BALL_SPEED

# Main game loop
def main(screen):
    init_screen(screen)
    while True:
        if not paused:
            continue_game = update_game()
            if not continue_game:
                break
        draw_screen(screen)
        key = screen.getch()
        # Handle paddle movement
        if key == ord('w') and paddle1_y > 0:
            paddle1_y -= 1
        elif key == ord('s') and paddle1_y < curses.LINES - PADDLE_HEIGHT:
            paddle1_y += 1
        elif key == KEY_UP and paddle2_y > 0:
            paddle2_y -= 1
        elif key == KEY_DOWN and paddle2_y < curses.LINES - PADDLE_HEIGHT:
            paddle2_y += 1
        # Handle pause and resume
        elif key == 27:  # Escape key
            paused = not paused
        curses.napms(50)  # Sleep for 50 milliseconds

# Run the game
curses.wrapper(main)
