from rich import print
import inquirer
from pyfiglet import Figlet

def display_menu() -> str:
    f = Figlet(font='slant')
    print(f.renderText('IRACING'))
    choices = [
        ("Import Race Data", "1"),
        ("TBC", "2"),
    ]
    questions = [
        inquirer.List('choice',
                      message="What do you want to do?",
                      choices=choices
                      ),
    ]
    answers = inquirer.prompt(questions)
    if answers:
        return answers['choice']
    return None

def get_session_parameters(SUBSESSION_URL):
    questions = [
        inquirer.Text('session_id', message="Enter Session ID"),
        inquirer.Text('race', message="Enter Race Number"),
        inquirer.Text('group', message="Enter Group Number"),
    ]
    answers = inquirer.prompt(questions)

    if not answers:
        print("No data entered, exiting...")
        return None

    session_id = answers['session_id']
    race = answers['race']
    group = answers['group']

    url = f'{SUBSESSION_URL}{session_id}'
    return url, race, group
