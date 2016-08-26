import time
from pubnub import Pubnub


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
        # self.__parse_questions(filename)

    def start(self):
        # Subscribe to availability request topic
        self.__listen_for_requests()
        counter = 0
        while counter < 200 and not self.finished:
            counter += 1
            time.sleep(1)

    def __parse_questions(self, filename):
        pass

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

        prompt_str = "prompt "
        fake_question = "Do you have a minute?\n"
        fake_question += "Yes\n"
        fake_question += "No\n"
        fake_question += "What are you talking about?"
        prompt_str += self.quiz_channel + "-q1 "
        prompt_str += fake_question
        self.pn.publish(channel=self.quiz_channel, message=prompt_str)
        # subscribe to question listening

        time.sleep(10)
        print("Ending quiz")
        self.pn.publish(channel=self.quiz_channel, message="stop")
        self.finished = True

    def __send_random_question():
        pass
