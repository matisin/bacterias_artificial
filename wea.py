from curses import wrapper
def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    stdscr.getkey()
    for i in range(0, 10):

        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(i, i))

    stdscr.refresh()

wrapper(main)
