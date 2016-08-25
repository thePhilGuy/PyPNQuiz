from pubnub import Pubnub
import sys


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

    def display_help(self, tokens=None):
        help_text = ("help: display this message\n"
                     "list: list quizes waiting for players\n"
                     "join quiz_name: join quiz by given name\n"
                     "start quiz_name: start a quiz with given name\n"
                     "quit: leave PNQuiz\n")
        print(help_text)

    def list_quizes(self, tokens=None):
        """
        def received(message, channel):
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
        """
        pass

    def start_quiz(self, tokens=None):
        """
        # print("tokens: ", tokens)
        if len(tokens) != 2:
            print("Usage: start quiz_name")
            return
        current_quiz = host.Host(tokens[1])
        current_quiz.start()
        # # pass
        """
        pass

    def invalid_command(self, tokens):
        print("Unsupported command: ", tokens[0])

    def handle_command(self, line):
        tokens = line.split(maxsplit=1)
        {"help": self.display_help,
         "list": self.list_quizes,
            # "join": join_quiz,
         "start": self.start_quiz
         }.get(tokens[0], self.invalid_command)(tokens)

    def run_menu(self):
        while(True):
            line = input("> ")
            if line == "quit":
                print("Goodbye.")
                sys.exit()
            self.handle_command(line)
