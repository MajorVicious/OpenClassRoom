from curses import wrapper
import curses

IMPORTANT = 1

def show(screen):
    pass

def main(stdscr):
    # Clear screen
    curses.init_pair(IMPORTANT, curses.COLOR_RED, curses.COLOR_WHITE)

    while True:
        key = stdscr.getkey()
        stdscr.clear()

        show()


        stdscr.refresh()
        if key in ('x', 'X'):
            break

wrapper(main)
