from VideogamePlayer import VideogamePlayer
import time
from LevelVision import LevelVision
from Log import Log


class Player1(VideogamePlayer):
    left_key = "a"
    right_key = "d"
    up_key = "w"
    down_key = "s"

    grab_place_key = "shift"
    interact_key = "ctrl"

    viewer: LevelVision = None

    def __init__(self, log_file, viewer: LevelVision):
        self.log_file = log_file
        self.viewer = viewer

    def fulfill_order(self, order_type):
        need_plate = self.viewer.need_plate_for_order(order_type)

        if order_type == "cod":
            self.make_cod(need_plate)
        elif order_type == "shrimp":
            self.make_shrimp(need_plate)
        else:
            self.log_file.error("Unknown order type: " + order_type)

    def make_cod(self, need_plate):
        if need_plate:
            self.move_direction("Down", 1)
            self.turn_character("Right")
            self.wait_for_clean_plate()
            self.grab()

            self.move_direction("Down", 1)
            self.move_direction("Left", 8)
            self.turn_character("Up")
            self.place()
            self.move_direction("Left", 2)
            self.move_direction("Up", 1)
        else:
            # Starting from conveyor belt, go to fish box
            self.move_direction("Down", 2)
            self.move_direction("Left", 10)
            self.move_direction("Up", 1)

        # Pick up fish
        self.turn_character("Left")
        self.grab()

        # Bring to cutting board and set down
        self.move_direction("Down", 2)
        self.place()

        # Chop
        chop_time = 1.35
        self.interact()
        time.sleep(chop_time)

        # Place on plate
        self.grab()
        self.move_direction("Right", 2)
        self.move_direction("Up", 1)
        self.place() # Set cod on plate
        self.grab() # Pick up plate

        # Serve
        self.move_direction("Right", 8)
        self.move_direction("Up", 2)
        self.turn_character("Right")
        self.place()

        self.log_file.log("Finished order of Cod")


    def make_shrimp(self, need_plate):
        if need_plate:
            self.move_direction("Down", 1)
            self.turn_character("Right")
            self.wait_for_clean_plate()
            self.grab()

            # place plate
            self.move_direction("Left", 1)
            self.place()

            #go to shrimp box
            self.move_direction("Right", 1)
            self.move_direction("Down", 1)
        else:
            # Starting from conveyor belt, go to shrimp box
            self.move_direction("Down", 2)



        # Pick up fish
        self.turn_character("Right")
        self.grab()

        # Bring to cutting board and set down
        self.move_direction("Down", 1)
        self.place()

        # Chop
        chop_time = 1.35
        self.interact()
        time.sleep(chop_time)

        # Place on plate
        self.grab()
        self.move_direction("Left", 2)
        self.move_direction("Up", 1)
        self.place()  # Set cod on plate
        self.grab()  # Pick up plate

        # Serve
        self.move_direction("Right", 2)
        self.move_direction("Up", 2)
        self.turn_character("Right")
        self.place()

        self.log_file.log("Finished order of Shrimp")

    def wait_for_clean_plate(self):
        self.log_file.error("In wait_for_clean_plate")

        has_clean_plate = False
        while not has_clean_plate:
            self.move_direction("Left", 1)
            has_clean_plate = self.viewer.check_for_clean_plate()
            self.move_direction("Right", 1)

            if not has_clean_plate:
                time.sleep(.5)

        self.log_file.error("Out of loop: clean plate? " + str(has_clean_plate))
        return has_clean_plate

    def automation(self, ):
        self.move_direction("Down", 1)
        self.move_direction("Right", 8)
        time.sleep(3)  # wait for camera to catch up

        count = 0
        next_order = self.viewer.determine_next_order()
        while next_order != "Unknown":
            self.fulfill_order(next_order)

            count += 1
            order_complete_animation_length = 1
            time.sleep(order_complete_animation_length)

            next_order = self.viewer.determine_next_order()

        self.log_file.error("Finished full automation of player1: " + str(count) + " orders served")