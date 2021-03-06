import os
import time
import getpass
import json

import klips_checker
import lea_exceptions
import telegram_notificator


script_path = os.path.dirname(os.path.realpath(__file__))
# TODO: Make configurable
HISTORIES_PATH = os.path.join(script_path, "histories")
config_path = os.path.join(script_path, "conf.json")


def run(telegram_chat_id, klips_email, klips_password):
    with open(config_path) as fo:
        conf = json.load(fo)
    telegram_api_key = conf["telegram_api_key"]

    if not os.path.exists(HISTORIES_PATH):
        os.mkdir(HISTORIES_PATH)

    checkers = [
        klips_checker.KLIPSChecker(klips_email, klips_password, HISTORIES_PATH)
    ]

    notificators = [
        telegram_notificator.TelegramNotificator(telegram_api_key, telegram_chat_id)
    ]

    timer = 0

    while True:
        for c in checkers:
            if timer % c.get_interval_length() == 0:
                try:
                    diff_info = c.check()
                    if diff_info is not None:
                        print(diff_info)
                        for n in notificators:
                            n.send(str(diff_info))
                    else:
                        print("No change detected")
                except lea_exceptions.CheckingFailedException as e:
                    # TODO: Error handling
                    print(e)
        time.sleep(60)
        timer += 1


def run_from_config():
    with open(config_path) as fo:
        conf = json.load(fo)

    klips_email = conf["uni-email-address"]
    telegram_chat_id = conf["telegram_chat_id"]

    # Can this be read out when running? Maybe split the password into different variables so they
    # don't lie in one tracable register? Or a reversible encryption technique?
    klips_password = getpass.getpass("Enter your password: ")

    run(telegram_chat_id, klips_email, klips_password)


if __name__ == "__main__":
    run_from_config()
