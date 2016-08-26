import time
from pubnub import Pubnub
import os


class Host:

    pub_key = "demo"
    sub_key = "demo"

    def __init__(self, quiz_name):
        self.finished = False

        self.name = quiz_name
        self.quiz_channel = "pnquiz-quiz-" + quiz_name

        self.participants = {}
        self.expected = 2

        self.pn = Pubnub(publish_key=Host.pub_key, subscribe_key=Host.sub_key)
        # Get and parse question file from user
        # filename = input("Please enter question file path"
        #                  "(see README): ")
        filename = "questions.txt"
        if os.path.isfile(filename):
            self.__parse_questions(filename)

    def __parse_questions(self, filename):
        # Read question file into memory
        lines = [line.rstrip('\n') for line in open(filename)]

        num_questions = lines[0]
        questions = []
        j = 1

        for i in range(int(num_questions)):
            question = lines[j]
            answers = []
            correct = -1
            j += 1
            while j < len(lines) and len(lines[j]) > 0:
                answer = lines[j]
                # Keep track of the correct answer
                if answer[0] == '*':
                    correct = len(answers)
                    answer = answer[1:]
                answers.append(answer)
                j += 1
            # Put question in a dictionary
            questions.append({"question": question,
                              "answers": answers,
                              "correct": correct,
                              "expected": self.expected})
            j += 1
        self.questions = questions

    def start(self):
        # Subscribe to availability request topic
        self.__listen_for_requests()
        counter = 0
        while counter < 200 and not self.finished:
            counter += 1
            time.sleep(1)

    def __listen_for_requests(self):
        """Listen for availability requests"""
        def availability(channel_string, channel):
            print("Received request: ", channel_string)
            self.pn.publish(channel=channel_string, message=self.name)
        self.pn.subscribe(channels="pnquiz-available", callback=availability)

        join_channel = "pnquiz-join-" + self.name

        def join_request(username, channel):
            # This could benefit from some synchronization
            print("Received username: ", username)
            self.expected -= 1
            self.participants.update({username: 0})

            if self.expected == 0:
                print("All players have joined.")
                self.pn.unsubscribe(channel=join_channel)
                self.__start_quiz()
            else:
                connect_str = "connect " + str(self.expected)
                self.pn.publish(channel=self.quiz_channel, message=connect_str)

        self.pn.subscribe(channels=join_channel, callback=join_request)

    def __start_quiz(self):
        """Callback when there are enough players"""
        start_str = "start"
        for name in self.participants:
            start_str += " " + name
        self.pn.publish(channel=self.quiz_channel, message=start_str)
        self.__send_question(0)

    def __send_question(self, i):
        if i > len(self.questions) - 1:
            self.__end_quiz()
            return

        question = self.questions[i]
        question_channel = self.quiz_channel + 'q' + str(i)
        question_string = question["question"] + '\n'
        for answer in question["answers"]:
            question_string += answer + '\n'
        prompt_str = "prompt " + question_channel + '\n' + question_string[:-1]

        def on_connect(message):
            self.pn.publish(channel=self.quiz_channel, message=prompt_str)

        def on_receive(message, channel):
            print("Received answer: ", message)
            print("Expected #: ", question["expected"])
            question["expected"] -= 1
            # possible race condition here
            if question["expected"] < 1:
                self.__send_question(i + 1)

        self.pn.subscribe(channels=question_channel, connect=on_connect,
                          callback=on_receive)
        return question_channel

    def __end_quiz(self):
        print("Ending quiz")
        self.pn.publish(channel=self.quiz_channel, message="stop")
        self.finished = True
