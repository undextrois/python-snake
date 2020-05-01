import random
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
screen_win = curses.initscr()                            # initialise screen
screen_h, screen_w = screen_win.getmaxyx()                           # get  window with and height relative to the set by user
w = curses.newwin(screen_h, screen_w, 0, 0)                 # create window by x y
w.keypad(1)                                     # accept keyboard input
curses.noecho()
curses.curs_set(0)                              # hide terminal cursor
w.border(0)                                     # add border
w.timeout(100)                                  # refresh screen every 100 milliseconds

#set snake initial position
snk_x = screen_w/4 
snk_y = screen_h/2 
# body parts 1 left and 2 left of the head
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]
score = 0
food  = [screen_h/2, screen_w/2]                                #render food on the screen relative to xy
w.addch(int(food[0]), int(food[1]),curses.ACS_PI)             #add food to the screen
key = curses.KEY_RIGHT                              #start the default key control
while True:                                         # infinite loop for every movement of the snake
    w.addstr(0,4,'SCORE :' + str(score) + ' ')
    prev_key = key
    next_key = w.getch()                            # set variable for the next key press
    key = key if next_key == -1 else next_key       # check key press switching
    #game pause & resume is pressed
    if key == ord(' '): 
        key = -1 
        while key != ord(' '):
            key = w.getch()
        key = prev_key   
        continue
    #check for invalid key pressed 
    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:    
        key = prev_key
    # check collission if snake is on its height, or on its width or on its itself
    if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break
    if snake[0] in snake[1:]: break
    # determine location of new head of the snake 
    new_head = [snake[0][0], snake[0][1]]
    # key press detection
    if key == KEY_DOWN:
        new_head[0] += 1
    if key == KEY_UP:
        new_head[0] -= 1
    if key == KEY_LEFT:
        new_head[1] -= 1
    if key == KEY_RIGHT:
        new_head[1] += 1
    if key == 27 :                 
        curses.endwin()
        quit()

    snake.insert(0, new_head)       # add new head

    if snake[0] == food:            # did snake run into food ?
        food = None                 # reset food var
        score += 1
        while food is None:         # no food
            # calculate new food location sh-1, sw-1
            food = [
                random.randint(1,  screen_h - 10),
                random.randint(1, screen_w - 10)
            ]
            if food in snake: food = []
           # food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()                          # remove tail 
        w.addch(int(tail[0]), int(tail[1]), ' ') #
    
    w.addch(int(snake[0][0]), int(snake[0][1]), '#') # add head of snake to the screen
curses.endwin()
print("\nScore - " + str(score))