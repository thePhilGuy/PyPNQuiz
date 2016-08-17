class Host:
    def __init__(self, quiz_name, pubnub):
        self.name = quiz_name
        self.pn = pubnub
        # Get and parse question file from user
        filename = input("Please enter question file path"
                         "(see README): ")
        self.__parse_questions(filename)

        # Subscribe to availability request topic
        self.__listen_for_requests()

    def __parse_questions(self, filename):
        pass

    def __listen_for_requests(self):
        """Listen for availability requests"""
        def callback(message, channel):
            print("Received request: ", message)
            self.pn.publish(channel="pnquiz-available-list", message=self.name)
        self.pn.subscribe(channels="pnquiz-available", callback=callback)

    def __start_quiz():
        """Callback when there are enough players"""
        pass

    def __send_random_question():
        pass
