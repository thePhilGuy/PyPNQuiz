import sys


def display_help(tokens=None):
    help_text = ("help: display this message\n"
                 "list: list quizes waiting for players\n"
                 "join quiz_name: join quiz by given name\n"
                 "start quiz_name: start a quiz with given name\n"
                 "quit: leave PNQuiz\n")
    print(help_text)


def handle_command(line):
    tokens = line.split(maxsplit=1)
    {"help": display_help
        # "list": list_quizes,
        # "join": join_quiz,
        # "start": start_quiz
     }[tokens[0]](tokens)


def run_menu():
    while(True):
        line = input("> ")
        if line == "quit":
            print("Goodbye.")
            sys.exit()
        handle_command(line)


if __name__ == "__main__":
    username = input("Please enter a username: ")
    print("Welcome to PNQuiz\n"
          "Use the following commands to interact with the system:")
    display_help()
    run_menu()
