import os
import time
import getpass

import klips_checker

# TODO: Make configurable
HISTORIES_PATH = "histories"

if not os.path.exists(HISTORIES_PATH):
    os.mkdir(HISTORIES_PATH)

email = input("Enter your email: ")

# Can this be read out when running? Maybe split the password into different variables so they don't lie in one tracable register? Or a reversible encryption technique?
password = getpass.getpass("Enter your password: ")


### For Testing
checkers = [
    klips_checker.KLIPSChecker(email, password, HISTORIES_PATH)
]

timer = 0

while True:
    for c in checkers:
        if timer % c.get_interval_length() == 0:
            diff_info = c.check()
            if diff_info is not None:
                print(diff_info)
            else:
                print("No change detected")
    time.sleep(60)
    timer += 1

