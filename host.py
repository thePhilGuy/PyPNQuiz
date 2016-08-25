import time
from pubnub import Pubnub


class Host:

    pub_key = "demo"
    sub_key = "demo"

    def __init__(self, quiz_name):
        self.finished = False
        self.name = quiz_name
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
        while counter < 100 or not self.finished:
            counter += 1
            time.sleep(1)

    def __parse_questions(self, filename):
        pass

    def __listen_for_requests(self):
        """Listen for availability requests"""
        def availability(message, channel):
            print("Received request: ", message)
            self.pn.publish(channel="pnquiz-available-list", message=self.name)

        self.pn.subscribe(channels="pnquiz-available", callback=availability)

        join_channel = "pnquiz-join-" + self.name

        def join_request(message, channel):
            print("Received username: ", message)
            # This could benefit from some synchronization
            self.expected -= 1
            if self.expected == 0:
                self.pn.unsubscribe(channel=join_channel)

        self.pn.subscribe(channels=join_channel, callback=join_request)

    def __start_quiz():
        """Callback when there are enough players"""
        pass

    def __send_random_question():
        pass
