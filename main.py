import keyboard
import winsound
from threading import Thread

# Better way to import my own stuff?
from Player1 import Player1
from Player2 import Player2
from VideogamePlayer import VideogamePlayer
from Log import Log
from LevelVision import LevelVision



DEBUG = False
log_file = Log(DEBUG)
viewer = LevelVision(log_file)


def player1_thread():
    player1 = Player1(log_file, viewer)

    end_loop = False
    order = ""
    while not end_loop:
        key = keyboard.read_key()
        log_file.error("Key: " +  str(key))

        if key == "f6":
            player1.automation()
        elif key == "f8":
            player1.move_direction("Right", 8)
        elif key == "f12":
            end_loop = True

    log_file.error("Exiting player 1 thread")


def player2_thread():
    player2 = Player2(log_file, viewer)

    end_loop = False
    order = ""
    while not end_loop:
        key = keyboard.read_key()

        if key == "f6":
            player2.automation()
        elif key == "f12":
            end_loop = True

    log_file.error("Exiting player 2 thread")


def main():
    thread1 = Thread(target=player1_thread)
    # thread2 = Thread(target=player2_thread)

    thread1.start()
    # thread2.start()

    winsound.Beep(2500, 500)

    thread1.join()

    log_file.log("Program exiting normally")


if __name__ == '__main__':
    # main()
    viewer.test()
