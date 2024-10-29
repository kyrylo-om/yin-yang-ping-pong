import os
import threading
import time
import random


def start_thread(target, arguments=None):
    if arguments is None:
        thread = threading.Thread(target=target)
    else:
        thread = threading.Thread(target=target, args=arguments)

    thread.daemon = True
    thread.start()

    return thread


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def main(stdscr):
    def ball_update(color, y, x, vel_y, vel_x, array_index):
        nonlocal barrier, hp

        alt_color = "w" if color == "b" else "b"

        while not game_state:
            if array_index > len(balls) - 1:
                break

            colliding_up = y + 2 * vel_y > height or y + vel_y < 0
            colliding_side = x + 3 * vel_x > width or x + vel_x < 0

            if colliding_up:
                if game_mode == 2 and vel_y == 1 and color == "w":
                    segment = width // 4
                    if barrier != -1 and segment * barrier < x < segment * (barrier + 1):
                        pass
                    elif x != segment and x != segment * 2 and x != segment * 3:
                        pass
                        remove_ball(array_index)
                        break

                vel_y *= -1
            if colliding_side:
                vel_x *= -1
            if not colliding_up and not colliding_side:
                if blocks[y][x + vel_x] == color:
                    blocks[y][x + vel_x] = alt_color
                    blocks[y][x + 2 * vel_x] = alt_color
                    blocks[y + vel_y][x + vel_x] = alt_color
                    blocks[y + vel_y][x + 2 * vel_x] = alt_color
                    vel_x *= -1

                    update_block_count(color, 4)

                if blocks[y + vel_y][x + vel_x] == color or blocks[y][x] == color:
                    blocks[y + vel_y][x] = alt_color
                    blocks[y + vel_y][x + vel_x] = alt_color
                    blocks[y + vel_y][x + 2 * vel_x] = alt_color
                    blocks[y + vel_y][x - vel_x] = alt_color
                    vel_y *= -1

                    if random.choice([0, 1]):
                        vel_x = -1
                    else:
                        vel_x = 1

                    update_block_count(color, 4)

            x = clamp(x + vel_x, 0, width)
            y = clamp(y + vel_y, 0, height)

            balls[array_index][1] = y
            balls[array_index][2] = x

            time.sleep(speed)

    def input_management():
        nonlocal pad_velocity, speed, barrier, balls_ammo, game_state, game_color

        speed_gear = 4

        while game_state == 0:
            pressed_key = stdscr.getch()
            if pressed_key != -1:
                if game_mode == 2:
                    match pressed_key:
                        case curses.KEY_LEFT:
                            if pad_velocity > 0:
                                pad_velocity = -0.5
                            else:
                                pad_velocity -= 0.5
                        case curses.KEY_RIGHT:
                            if pad_velocity < 0:
                                pad_velocity = 0.5
                            else:
                                pad_velocity += 0.5
                        case 32:
                            if balls_ammo > 0:
                                add_ball("w", height - 2, int(pad_x + 4), -1, 0)
                                balls_ammo -= 1
                        case 49:
                            barrier = 0
                        case 50:
                            barrier = 1
                        case 51:
                            barrier = 2
                        case 52:
                            barrier = 3
                        case 27:
                            game_state = -1
                        case 99:
                            change_color()
                else:
                    match pressed_key:
                        case 61:
                            add_ball("w", height - 2, random.randrange(0, width), -1, random.choice([-1, 1]))
                            add_ball("b", 0, random.randrange(0, width), -1, random.choice([-1, 1]))
                        case 45:
                            if len(balls) > 0:
                                balls.pop()
                                balls.pop()
                        case 27:
                            game_state = -1
                        case 99:
                            change_color()
                        case curses.KEY_DOWN:
                            if speed_gear > 1:
                                speed_gear -= 1
                            match speed_gear:
                                case 1:
                                    speed = 0.5
                                case 2:
                                    speed = 0.2
                                case 3:
                                    speed = 0.1
                                case 4:
                                    speed = 0.05
                                case 5:
                                    speed = 0.03
                                case 6:
                                    speed = 0.02
                                case 7:
                                    speed = 0.01
                                case 8:
                                    speed = 0.005
                                case 9:
                                    speed = 0.001
                        case curses.KEY_UP:
                            if speed_gear < 9:
                                speed_gear += 1
                            match speed_gear:
                                case 1:
                                    speed = 0.5
                                case 2:
                                    speed = 0.2
                                case 3:
                                    speed = 0.1
                                case 4:
                                    speed = 0.05
                                case 5:
                                    speed = 0.03
                                case 6:
                                    speed = 0.02
                                case 7:
                                    speed = 0.01
                                case 8:
                                    speed = 0.005
                                case 9:
                                    speed = 0.001

    def pad_movement():
        nonlocal pad_x, pad_velocity

        while game_state == 0:
            if pad_x + pad_velocity < 0 or pad_x + pad_velocity > width - 9:
                pad_velocity *= -1
            pad_x += pad_velocity
            time.sleep(0.02)

    def reload_ammo():
        nonlocal balls_ammo

        while game_state == 0:
            if balls_ammo < 3:
                balls_ammo += 1
            time.sleep(3)

    def change_color():
        nonlocal game_color

        game_color += 1
        if game_color > 10:
            game_color = 0
        match game_color:
            case 0:
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
            case 1:
                curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
                curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            case 2:
                curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_MAGENTA)
                curses.init_pair(2, curses.COLOR_RED, curses.COLOR_CYAN)
            case 3:
                curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
                curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
            case 4:
                curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_YELLOW)
                curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
            case 5:
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
                curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
            case 6:
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
                curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_WHITE)
            case 7:
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
            case 8:
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            case 9:
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
            case 10:
                curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_RED)
                curses.init_pair(2, curses.COLOR_RED, curses.COLOR_YELLOW)

    def raise_difficulty():
        while game_state == 0:
            add_ball("b", 0, random.randrange(0, width), 1, random.choice([-1, 1]))
            time.sleep(10)

    def add_ball(color, y, x, vel_y, vel_x):
        for i, ball in enumerate(balls):
            if ball is None:
                balls[i] = [color, y, x, vel_y, vel_x, i]
                start_thread(ball_update, [color, y, x, vel_y, vel_x, i])
                break
        else:
            balls.append([color, y, x, vel_y, vel_x])
            start_thread(ball_update, [color, y, x, vel_y, vel_x, len(balls) - 1])

    def remove_ball(array_index):
        balls[array_index] = None

    def update_block_count(color, count):
        nonlocal white_blocks, black_blocks, game_state

        if color == "w":
            white_blocks -= count
            black_blocks += count
        else:
            white_blocks += count
            black_blocks -= count

        if game_mode == 2:
            if width * (black_blocks / (white_blocks + black_blocks)) > width - width // 6:
                game_state = 1
            if width * (black_blocks / (white_blocks + black_blocks)) < width // 6:
                game_state = 2

    def update_screen():
        stdscr.addstr(0, 0, " " * (width * height), curses.color_pair(2))
        for i, line in enumerate(blocks):
            for j, block in enumerate(line):
                if block == "w":
                    stdscr.addstr(i, j, " ", curses.color_pair(1))

        segment = width // 4
        stdscr.addstr(height, 0, " " * width)
        if game_mode == 2:
            if barrier != -1:
                stdscr.addstr(height, barrier * segment, "#" * segment)
            stdscr.addstr(height - 1, int(pad_x) + 4, "^", curses.color_pair(2))
            stdscr.addstr(height, int(pad_x), "<==" + "○" * balls_ammo + "·" * (3 - balls_ammo) + "==>")
            for i in range(3):
                stdscr.addstr(height, segment * (i + 1), "|")
            stdscr.addstr(height, segment // 2, "1")
            stdscr.addstr(height, segment + segment // 2, "2")
            stdscr.addstr(height, 2 * segment + segment // 2, "3")
            stdscr.addstr(height, 3 * segment + segment // 2, "4")

        stdscr.addstr(height + 1, 1, "-" * (width - 2))
        stdscr.addstr(height + 2, 0, " " * width, curses.color_pair(1))
        stdscr.addstr(height + 2, 0, " " * int(width * (black_blocks / (white_blocks + black_blocks))), curses.color_pair(2))
        if game_mode == 2:
            stdscr.addstr(height + 2, width // 6, "|", curses.color_pair(2))
            stdscr.addstr(height + 2, width - width // 6, "|", curses.color_pair(1))
        stdscr.addstr(height + 2, 0, str(black_blocks), curses.color_pair(2))
        stdscr.addstr(height + 2, width - len(str(white_blocks)), str(white_blocks), curses.color_pair(1))
        stdscr.addstr(height + 3, 1, "-" * (width - 2))
        for ball in balls:
            if ball is not None:
                if ball[0] == "b":
                    color_pair = 1
                else:
                    color_pair = 2
                stdscr.addstr(ball[1], ball[2], "○", curses.color_pair(color_pair))

        stdscr.refresh()

    height, width = stdscr.getmaxyx()
    if height % 2 == 1:
        height -= 1
    height -= 4
    blocks = [["w"] * width for _ in range(height // 2)] + [["b"] * width for _ in range(height // 2)]
    white_blocks = width * (height // 2)
    black_blocks = width * (height // 2)

    pad_x = width // 2
    pad_velocity = 0.5

    balls = []

    speed = 0.05

    barrier = -1

    hp = 4

    balls_ammo = 3

    game_state = 0

    game_color = 0

    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.nodelay(True)
    curses.curs_set(False)
    stdscr.clear()

    start_thread(input_management)
    start_thread(pad_movement)
    start_thread(reload_ammo)
    # start_thread(raise_difficulty)

    if game_mode == 2:
        add_ball("b", 0, random.randrange(0, width), 1, random.choice([-1, 1]))

    while True:
        # updates screen every 30 milliseconds resulting in a screen refresh rate of
        # approximately 30 fps
        update_screen()

        if game_state != 0:
            if game_state == 1:
                stdscr.clear()
                stdscr.addstr(height // 2, width // 2, "You win!")
                time.sleep(1)
                stdscr.addstr(height // 2 + 1, width // 2 - 3, "(Press any key)")
                stdscr.nodelay(False)
                stdscr.getch()
            if game_state == 2:
                stdscr.clear()
                stdscr.addstr(height // 2, width // 2, "You lose!")
                time.sleep(1)
                stdscr.addstr(height // 2 + 1, width // 2 - 3, "(Press any key)")
                stdscr.nodelay(False)
                stdscr.getch()
            break
        time.sleep(0.03)


game_mode = 0


def menu():
    def print_title():
        os.system("cls" if os.name == "nt" else "clear")
        print((""
               " __     ___                 __     __\n"
               " \\ \\   / (_)                \\ \\   / /\n"
               "  \\ \\_/ / _ _ __   __ _ _____\\ \\_/ /_ _ _ __   __ _\n"
               "   \\   / | | '_ \\ / _` |______\\   / _` | '_ \\ / _` |\n"
               "    | |  | | | | | (_| |       | | (_| | | | | (_| |\n"
               "  __|_| _|_|_| |_|\\__, |     __|_|\\__,_|_| |_|\\__, |\n"
               " |  __ (_)         __/ |    |  __ \\            __/ |\n"
               " | |__) | _ __   _|___/_____| |__) |__  _ __  |___/\n"
               " |  ___/ | '_ \\ / _` |______|  ___/ _ \\| '_ \\ / _` |\n"
               " | |   | | | | | (_| |      | |  | (_) | | | | (_| |\n"
               " |_|   |_|_| |_|\\__, |      |_|   \\___/|_| |_|\\__, |\n"
               "                 __/ |                         __/ |\n"
               "                |___/                         |___/ \n"
               ))

    def user_choice():
        global game_mode

        print_title()

        print("\nPlease input one of the following options:")
        print("\n1 - Play Relaxed")
        print("2 - Play Competitive")
        print("3 - How to play?")
        print("4 - Exit game")

        user_input = input('>>> ')
        match user_input:
            case "1":
                game_mode = 1
                wrapper(main)
                menu()
            case "2":
                game_mode = 2
                wrapper(main)
                menu()
            case "3":
                print_title()
                print("--Rules for Relaxed:--\n\n"
                      "Press + or - to add or remove balls!\n"
                      "Press up or down to speed up or slow down the balls!\n"
                      "Press c to mix the colors a bit! (also works in competitive)\n"
                      "Esc to return to the menu (also works in competitive)\n\n"
                      "Observe the chaos!")
                print("\n--Rules for Competitive:--\n\n"
                      "Your goal is to outweigh the opposing color!\n"
                      "Reach the domination line as fast as you can!\n\n"
                      "Press 1, 2, 3, 4 to activate the barriers!"
                      "If your ball doesn't land on a barrier, it disappears!\n"
                      "Press arrow keys to move the shooting platform.\n"
                      "Press space to shoot balls (you have limited ammo)")
                print("\n\nAnd also - you control the size of your battleground!\n"
                      "Resize the window to your liking and play by your rules!")

                print("\n\n\n(Press enter to return to the menu)")
                input(">>> ")
                menu()
            case "4":
                pass
            case _:
                user_choice()

    user_choice()


try:
    import curses
except ImportError:
    if os.name == "nt":
        os.system("pip install windows-curses")
finally:
    import curses
    from curses import wrapper

menu()
