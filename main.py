from client import Client

if __name__ == "__main__":
    username = input("Please enter a username: ")
    PNQuiz = Client(username)
    PNQuiz.run_menu()
