from VideogamePlayer import VideogamePlayer
import time
from LevelVision import LevelVision
from Log import Log


class Player2(VideogamePlayer):
    left_key = "left"
    right_key = "right"
    up_key = "up"
    down_key = "down"

    grab_place_key = "right shift"
    interact_key = "right ctrl"
    boost_key = "right alt"

    emote_key = "i"

    viewer: LevelVision

    def __init__(self, log_file, viewer):
        self.log_file = log_file
        self.viewer = viewer

    def automation(self):
        time.sleep(5)  # let player 1 start making orders for a while

        cod_plate_moved = False
        while not cod_plate_moved:
            if self.viewer.need_plate_for_order("cod"):
                self.move_direction("Left", 5.5)  # I think we always start with a cod order
                self.move_direction("Down", 1)
                self.grab()

                self.move_direction("Left", 1)
                self.turn_character("Down")
                self.place()
                cod_plate_moved = True
            else:
                time.sleep(1)

        self.move_direction("Right", 5)
        self.turn_character("Down")
        self.place()

        shrimp_plate_moved = False
        while not shrimp_plate_moved:
            if self.viewer.need_plate_for_order("shrimp"):
                self.move_direction("Right", 1)
                self.turn_character("Down")
                self.place()
                shrimp_plate_moved = True
            else:
                time.sleep(1)


        self.move_direction("Up", 1)
        self.move_direction("Left", 0.5)

        self.emote("OK")

        self.log_file.error("Exiting player 2 automation")
