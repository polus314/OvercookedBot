import keyboard
import time
from Log import Log


class VideogamePlayer:
    left_key = "a"
    right_key = "d"
    up_key = "w"
    down_key = "s"

    grab_place_key = "space"
    interact_key = "ctrl"
    boost_key = "alt"

    emote_key = "e"

    log_file: Log

    def __init__(self, log_file):
        self.log_file = log_file

    def move_direction(self, direction, distance_in_blocks):
        time_for_one_block = 0.20
        boost_distance = 3.65
        time_to_do_boost = .3

        key = ""
        if direction == "Left":
            key = self.left_key
        elif direction == "Right":
            key = self.right_key
        elif direction == "Up":
            key = self.up_key
        elif direction == "Down":
            key = self.down_key

        if distance_in_blocks > boost_distance + 1:
            num_boosts = int(distance_in_blocks / boost_distance)
            remaining_blocks = distance_in_blocks - (num_boosts * boost_distance)

            self.hold_button_in_game(key, remaining_blocks * time_for_one_block)

            keyboard.press(key)  # make sure we boost in correct direction
            for i in range(num_boosts):
                self.press_button_in_game(self.boost_key)
                time.sleep(time_to_do_boost)
            keyboard.release(key)

        else:
            self.hold_button_in_game(key, distance_in_blocks * time_for_one_block)

    def turn_character(self, direction):
        self.move_direction(direction, 0.1)

    def grab(self):
        self.press_button_in_game(self.grab_place_key)

    def place(self):
        self.press_button_in_game(self.grab_place_key)

    def interact(self):
        self.press_button_in_game(self.interact_key)

    def hold_button_in_game(self, key, duration):
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
        time.sleep(0.05)  # wait so next action is registered as well

    def press_button_in_game(self, key):
        keyboard.press(key)
        time.sleep(0.05)  # long enough for game to register
        keyboard.release(key)
        time.sleep(0.05)  # wait so next action is registered as well

    def emote(self, emote_type):
        if emote_type == "OK":
            keyboard.press(self.emote_key)
            keyboard.press(self.up_key)
            keyboard.press(self.right_key)

            time.sleep(0.05)

            keyboard.release(self.emote_key)
            keyboard.release(self.up_key)
            keyboard.release(self.right_key)