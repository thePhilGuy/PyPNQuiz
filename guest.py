from pubnub import Pubnub
import time


class Guest:

    pub_key = "demo"
    sub_key = "demo"

    def __init__(self, username, quiz_name):
        self.pn = Pubnub(publish_key=Guest.pub_key,
                         subscribe_key=Guest.sub_key)

        # Publish join message to quiz channel
        join_channel = "pnquiz-join-" + quiz_name
        self.pn.publish(channel=join_channel, message=username)

        # Subscribe to quiz channel
        def handle_message(message, channel):
            self.__handle_message(message)
        self.quiz_channel = "pnquiz-quiz-" + quiz_name
        self.pn.subscribe(channels=self.quiz_channel, callback=handle_message)
        self.finished = False

        # Block until quiz is over
        while not self.finished:
            time.sleep(1)

    def invalid_message(self, _):
        print("Received invalid message from Host.")

    def connect(self, tokens):
        msg_str = "Connected to quiz Host. "
        if len(tokens) == 2:
            wait_str = "Waiting for " + tokens[1] + " more players..."
        else:
            wait_str = "Waiting for more players..."
        print(msg_str + wait_str)

    def start(self, tokens):
        tokens = tokens[1].split(" ")
        msg_str = "Starting quiz with "
        for name in tokens:
            msg_str += name + " "
        print(msg_str)

    def stop(self, _):
        self.pn.unsubscribe(channel=self.quiz_channel)
        self.finished = True

    def prompt(self, tokens):
        tokens = tokens[1].split("\n")
        question = tokens[0]
        answers = [s for s in tokens[1:]]
        print(question)
        for i in range(len(answers)):
            print(i+1, ") ", answers[i])
        chosen = input("Answer #:")
        answer_msg = self.username + " " + chosen
        self.pn.publish(channel=self.quiz_channel, message=answer_msg)

    def correct(self, tokens):
        tokens = tokens[1].split(" ")
        recipient, msg = tokens[0], tokens[1]
        if (recipient == self.username):
            print(msg)

    def __handle_message(self, message):
        tokens = message.split(maxsplit=1)
        {"connect": self.connect,
         "start": self.start,
         "stop": self.stop,
         "prompt": self.prompt,
         "correct": self.correct}.get(tokens[0], self.invalid_message)(tokens)
