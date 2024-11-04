from errors import input_error
from helper_errors_classes import ArgsNotEnought, CustomKeyError,  CustomAlreadyExistsError
from task1_hw_07 import Birthday, Name, Phone, Record, AddressBook

my_address_book = AddressBook()


def normalize_input(user_input):
    return user_input.strip().lower()


@input_error
def parse_input(user_input):
    if not user_input:
        return None, None
    if " " not in user_input:
        return normalize_input(user_input), None

    cmd, *args = user_input.split()
    cmd = normalize_input(cmd)

    return cmd, *args


@input_error
def add_record():
    name = input("Enter a name: ")
    phone = input("Enter a phone number: ")
    birthday = input("Enter a birthday in format DD.MM.YYYY: ")
    record = Record(name, phone, birthday)
    my_address_book.add_record(record)


def all_contacts():
    print(my_address_book)


@input_error
def change_record_phone():
    name_of_contact = input("Enter a name of contact: ")
    new_phone = input("Enter a new phone number: ")
    my_address_book.change_record_phone(name_of_contact, new_phone)


@input_error
def change_record_name():
    name_of_contact = input("Enter a name of contact: ")
    my_address_book.change_record_name(name_of_contact)


def add_phone():
    name_of_contact = input("Enter a name of contact: ")
    phone = input("Enter a phone number: ")
    my_address_book.add_phone(name_of_contact, phone)


def add_birthday():
    print("Enter a birthday in format DD.MM.YYYY")
    name_of_contact = input("Enter a name of contact: ")
    birthday = input("Enter a birthday: ")
    my_address_book.add_birthday(name_of_contact, birthday)


def phone():
    name_of_contact = input("Enter a name of contact: ")
    my_address_book.find_record(name_of_contact)


def show_record_phones():
    name_of_contact = input("Enter a name of contact: ")
    my_address_book.show_record_phones(name_of_contact)


def show_birthday():
    name_of_contact = input("Enter a name of contact: ")

    my_address_book.show_birthday(name_of_contact)


def birthdays():
    my_address_book.show_birthdays()


def execute_command(command):
    if command in ["close", "exit"]:
        print("Good bye!")
        return
    elif command == "hello":
        print("How can I help you?")
    elif command == "add":
        add_record()
    elif command == "all":
        all_contacts()
    elif command == 'all-phones':
        show_record_phones()
    elif command == "change":
        user_input = normalize_input(
            input("what do you want to change? name or phone(n/p):  "))
        if user_input == "n":
            change_record_name()
        elif user_input == "p":
            change_record_phone()

    elif command == "phone":
        phone()
    elif command == "show-birthday":
        show_birthday()
    elif command == "birthdays":
        birthdays()
    elif command == "add-b":
        add_birthday()
    elif command == 'add-p':
        add_phone()

    elif command == "help":
        print("Commands: hello, add, all, change, phone, close, exit, help, add-b, show-birthday, birthdays")
