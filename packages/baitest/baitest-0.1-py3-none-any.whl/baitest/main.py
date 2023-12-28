import curses

def run(stdscr:curses.window):
  while True:
    stdscr.addstr('Hello from curses.', curses.A_ITALIC | curses.A_REVERSE)
    stdscr.refresh()

    stdscr.getkey()


def main():
  curses.wrapper(run)


if __name__ == '__main__':
  main()