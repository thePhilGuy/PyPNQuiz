import client

if __name__ == "__main__":
    username = input("Please enter a username: ")
    PNQuiz = client.Client(username)
    PNQuiz.run_menu()
