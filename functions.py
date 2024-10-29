import threading


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


import os

def main():
    print("Hello. (press enter)")
    input(">>> ")
    print("There is no game.")
    input(">>> ")
    print("That is because, unfortunately, the technical capabilities of this platform seem to not be enough to run it.")
    input(">>> ")
    print("Feel free to download it and try it here: ")
    input(">>> ")
    print("If not, here is a simple 'guess a number' game for you.")
    input(">>> ")
    print("Start? (y / n)")
    if input(">>> ") == "y":
        game()
    else:
        print("Ok. But still, you should check out that other game!")

def game():
    os.system("clear")
    print("Hi!!! Welcome to Guess a Number!!!")
    print("\nI will pick a number between 1 and 1000000000 and you will have to guess it!!!")
    print("Fun, right?")

    print("\nPlease type 'This game is very fun and I can't wait to play it' if you agree!")
    user_input = ""
    while True:
        user_input = input()
        if user_input == "This game is very fun and I can't wait to play it":
            break
        else:
            print("Wrong.")
    print("\n Yippee!!!")
    print(("                                                                                                                                                           "
    "                                                                                                                                                           "
    "                                                                       @@@@@@@@@@:                                                                         "
    "                                                               @@@@@@##=         =@@@@#                                                                    "
    "                                                           @@@@                        @@@                                                                 "
    "                                                        *@@                               @@@                                                              "
    "                                                      @@+                                   @@@                                                            "
    "                                                     @+                                       @@                                                           "
    "                                                    @                                           @.                                                         "
    "                                                   @.                                            @@                                                        "
    "                                                  @@                                              @                                                        "
    "                                                  @          @@@@@@@+            @@@@@@@@         @@                                                       "
    "                                                 @:         @@.  @@@@@:         @@@  @@@@@@        @                                                       "
    "                                                 @-        @@   .@@@@@@        @@+   @@@@@@        @@                                                      "
    "                                                 @-        @@@@@@@@@@@@        @@@@@@@@@@@@        @@                                                      "
    "                                                 @:        @@@@@@@@@@@@        @@@@@@@@@@@@        @@                                                      "
    "                                                 @          @@@@@@@@@@          @@@@@@@@@          @@                                                      "
    "                                                @@                                                :@                                                       "
    "                                                 @@                                              .@                                                        "
    "                                                   @*                                           @@                                                         "
    "                                                    @@                  @@@@@@@               @@                                                           "
    "                                                      @@*                                   @@                                                             "
    "                                                        @@@                             @@@*                                                               "
    "                                                           @@:                  +@@@@@@@    =*%%+@@@                                                       "
    "                                                             @@@@.  ++@@@@@@@@+-                    @-                                                     "
    "                                                                 @@                                  @                                                     "
    "                                                                 @                                   @                                                     "
    "                                                                 @                                   @                                                     "
    "                                                                 @                                   @                                                     "
    "                                                                 @          @@        *%@@@@@=       @                                                     "
    "                                                                  @         @@       @@   +  @       @                                                     "
    "                                                                  @         @@       @@   @  @      @@                                                     "
    "                                                                  :@        @+       @+   @  @@     @                                                      "
    "                                                                   @        @ @      @@   @   @    -@                                                      "
    "                                                                   =@      @@ @@     @ @@@@   @@  @@                                                       "
    "                                                                    @@     @   @@   @-                                                                     "
    "                                                                      @@@@@      @@@@                                                                      "
    "                                                                                                                                                           "
    "                                                                                                                                                           "
    "                                                                                                                                                         "))