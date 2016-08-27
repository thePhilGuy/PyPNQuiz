# PyPNQuiz
This application is a client for a multiplayer quiz game using the PubNub python sdk.

## Setup
The only dependency for this application is python 3.5, as the pubnub library has been included in the __venv__ subdirectory.
Activate this virtual environment by running 
```sh
source bin/activate
```

## Usage
### Starting the application
Assuming that the virtual environment provided with the source code has been activate, run the application with the command:
```sh
python pnquiz.py
```
or 
```sh
python3 pnquiz.py
```
The application asks the user for a username. The application then displays a help message and prompts the user for a command.

### Commands
| Command         | Function |
|-----------------|----------|
| help            | Displays the help message |
| list            | Lists quizes waiting for players. |
| join quiz_name  | Join a quiz with given name |
| start quiz_name | Start a quiz with given name |
| quit            | Leave PNQuiz |

## Question File
When starting a quiz, the game prompts the user for a question file. This is a text file with the number of questions on the first line,
followed by questions and their answers. Questions are on a single line, followed by a number of answer options --each answer also on its own line--.
The correct answer should be prefixed with a __*__. Each block of question + answers is separated by an empty line.

The [_questions.txt_](questions.txt) file has been provided as an example.


