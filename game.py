import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    height, width = 20, 20
    player_pos = width // 2
    player_char = '😊'
    food_char = '🍎'
    bomb_char = '💣'

    falling_items = []
    score = 10
    game_over = False

    while not game_over:
        stdscr.clear()

        # Draw player
        stdscr.addstr(height - 1, player_pos, player_char)

        # Update falling items
        new_falling = []
        for item in falling_items:
            x, y, char = item
            y += 1
            if y < height - 1:
                stdscr.addstr(y, x, char)
                new_falling.append((x, y, char))
            else:
                # Item reached bottom
                if x == player_pos:
                    if char == food_char:
                        score += 1
                        player_char = '😊'
                    elif char == bomb_char:
                        score -= 2
                        player_char = '😠'
                if score <= 0:
                    game_over = True

        falling_items = new_falling

        # Randomly add new item
        if random.random() < 0.1:  # 10% chance per frame
            x = random.randint(0, width - 1)
            char = food_char if random.random() < 0.5 else bomb_char
            falling_items.append((x, 0, char))

        # Draw score
        stdscr.addstr(0, 0, f"Score: {score}")

        # Get input
        key = stdscr.getch()
        if key == ord('n') and player_pos > 0:
            player_pos -= 1
        elif key == ord('m') and player_pos < width - 1:
            player_pos += 1
        elif key == ord('q'):
            game_over = True

        stdscr.refresh()
        time.sleep(0.1)

    stdscr.addstr(height // 2, width // 2 - 5, "Game Over!")
    stdscr.refresh()
    time.sleep(2)

if __name__ == "__main__":
    curses.wrapper(main)