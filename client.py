from pubnub import Pubnub
from host import Host
from guest import Guest
import sys
import time
import os


class Client:
    pub_key = "demo"
    sub_key = "demo"

    def __init__(self, name):
        self.username = name
        self.pn = Pubnub(publish_key=Client.pub_key,
                         subscribe_key=Client.sub_key)
        print("Welcome to PNQuiz\n"
              "Use the following commands to interact with the system:")
        self.display_help()

    def display_help(self, _=None):
        help_text = ("help: display this message\n"
                     "list: list quizes waiting for players\n"
                     "join quiz_name: join quiz by given name\n"
                     "start quiz_name: start a quiz with given name\n"
                     "quit: leave PNQuiz\n")
        print(help_text)

    def list_quizes(self, _=None):

        def received(message, channel):
            print(message)

        def connected(message):
            print("Connected to availability topic")

        channel_string = "pnquiz-available-list-" + self.username
        self.pn.subscribe(channels=channel_string,
                          callback=received,
                          connect=connected)
        self.pn.publish(channel="pnquiz-available", message=channel_string)

        # Give hosts time to respond
        time.sleep(1)
        self.pn.unsubscribe(channel=channel_string)

    def start_quiz(self, tokens):
        if len(tokens) != 2:
            print("Usage: start quiz_name")
            return
        # Start host and guest on separate threads
        # Only host in first version
        current_quiz = Host(tokens[1])
        current_quiz.start()

    def join_quiz(self, tokens):
        if len(tokens) != 2:
            print("Usage: join quiz_name")
            return
        # start a guest thread
        current_quiz = Guest(self.username, tokens[1])
        current_quiz.participate()

    def invalid_command(self, tokens):
        print("Unsupported command: ", tokens[0])

    def handle_command(self, line):
        tokens = line.split(maxsplit=1)
        {"help": self.display_help,
         "list": self.list_quizes,
         "join": self.join_quiz,
         "start": self.start_quiz}.get(tokens[0], self.invalid_command)(tokens)

    def run_menu(self):
        while(True):
            line = input("> ")
            if line == "quit":
                print("Goodbye.")
                # sys.exit()
                os._exit(0)
            self.handle_command(line)
