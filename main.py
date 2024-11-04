from helper_errors_classes import CommandValidator
from commands import execute_command, parse_input
from task1_hw_07 import AddressBook


def main():
    my_address_book = AddressBook()
    print("Welcome to the assistant bot!")
    print("You can use the following commands: \n"
          "hello - to start the program\n"
          "add - to add a contact\n"
          "all - to show all contacts\n"
          "change - to change a contact\n"
          "phone - to show a phone number\n"
          "close - to close the program\n"
          "exit - to exit the program\n"
          "help - to show all commands\n"
          "add-b - to add a birthday\n"
          "show-birthday - to show a birthday\n"
          "birthdays - to show all birthdays\n"
          "all-phones - to show all phones of a contact"
          )
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        try:
            validator = CommandValidator(command)
            validator.validate()
            execute_command(command)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
