from pubnub import Pubnub
from host import Host
from guest import Guest
import time
import threading
import os


class Guest_thread(threading.Thread):
    def __init__(self, username, quiz_name):
        threading.Thread.__init__(self)
        self.quiz = Guest(username, quiz_name)

    def run(self):
        self.quiz.participate()


class Host_thread(threading.Thread):
    def __init__(self, quiz_name, num_players, question_file):
        threading.Thread.__init__(self)
        self.quiz = Host(quiz_name, num_players, question_file)

    def run(self):
        self.quiz.start()


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

        channel_string = "pnquiz-available-list-" + self.username
        self.pn.subscribe(channels=channel_string, callback=received)
        self.pn.publish(channel="pnquiz-available", message=channel_string)

        # Give hosts time to respond
        time.sleep(1)
        self.pn.unsubscribe(channel=channel_string)

    def start_quiz(self, tokens):
        if len(tokens) != 2:
            print("Usage: start quiz_name")
            return

        expected = input("Please enter the expected number of players: ")
        filename = input("Please enter question file path"
                         "(see README): ")
        # Start host and guest on separate threads
        host_thread = Host_thread(tokens[1], int(expected), filename)
        guest_thread = Guest_thread(self.username, tokens[1])

        host_thread.start()
        guest_thread.start()
        guest_thread.join()
        host_thread.join()

    def join_quiz(self, tokens):
        if len(tokens) != 2:
            print("Usage: join quiz_name")
            return
        # current_quiz = Guest(self.username, tokens[1])
        # current_quiz.participate()
        guest_thread = Guest_thread(self.username, tokens[1])
        guest_thread.start()
        guest_thread.join()

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
                os._exit(0)
            self.handle_command(line)
