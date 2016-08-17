import sys
import time
from pubnub import Pubnub

# Initialize pubnub context
pubnub = Pubnub(publish_key="demo",
                subscribe_key="demo")


def display_help(tokens=None):
    help_text = ("help: display this message\n"
                 "list: list quizes waiting for players\n"
                 "join quiz_name: join quiz by given name\n"
                 "start quiz_name: start a quiz with given name\n"
                 "quit: leave PNQuiz\n")
    print(help_text)


def list_quizes(tokens=None):
    def received(message, channel):
        """prints each available topic as they arrive"""
        print(message)

    def connected(message):
        print("Connected to availability topic")

    # Maybe change channel to be unique for the requester
    pubnub.subscribe(channels="pnquiz-available-list",
                     callback=received,
                     connect=connected)
    pubnub.publish(channel="pnquiz-available", message="list")

    # Give hosts time to respond
    time.sleep(1)
    pubnub.unsubscribe(channel="pnquiz-available")


def handle_command(line):
    tokens = line.split(maxsplit=1)
    {"help": display_help,
     "list": list_quizes,
        # "join": join_quiz,
        # "start": start_quiz
     }[tokens[0]](tokens)


def run_menu():
    while(True):
        line = input("> ")
        if line == "quit":
            print("Goodbye.")
            sys.exit()
        handle_command(line)


if __name__ == "__main__":
    username = input("Please enter a username: ")
    print("Welcome to PNQuiz\n"
          "Use the following commands to interact with the system:")
    display_help()

    run_menu()
