# Розробіть систему для управління адресною книгою.


# Сутності:

# Field: Базовий клас для полів запису.
# Name: Клас для зберігання імені контакту. Обов'язкове поле.
# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# AddressBook: Клас для зберігання та управління записами.


# Функціональність:

# AddressBook:Додавання записів.
# Пошук записів за іменем.
# Видалення записів за іменем.
# Record:Додавання телефонів.
# Видалення телефонів.
# Редагування телефонів.
# Пошук телефону.
import re


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        self.value = self.normalize_name(value)

    def __str__(self):
        return self.value

    @staticmethod
    def normalize_name(name:    str) -> str:
        return name.title().strip()


class Phone(Field):
    def __init__(self, value):
        self.value = value

        if len(value) != 10:
            raise ValueError('Phone number must be 10 digits')

    def __str__(self):
        return self.value


class Alias(Field):
    def __init__(self, alias):
        self.alias = alias

    def __str__(self):
        return self.alias


class Record:
    def __init__(self, name, phones=None):
        self.name = name
        self.phones_dict = {}

    def add_phone(self, phone, phone_alias=None):
        phone_alias = input("Enter phone alias or press Enter to skip: ")
        phone_key = phone_alias if phone_alias else f"{
            len(self.phones_dict.keys()) + 1}"
        self.phones_dict[phone_key] = phone

        print(f"Phone number added to record: {self.name}, phone alias: {phone_key}",
              f"phone: {phone.value}")
        return self.phones_dict

    def change_record_name(self, new_name):
        self.name = new_name
        print(f"Name changed: {new_name}")

    def change_record_phone(self, new_phone=None):
        qty_of_phones = len(self.phones_dict)
        sing = "number"
        plural = "numbers"

        if qty_of_phones == 0:
            print("No phone numbers found for this record")
            return

        print(
            f'This record has {qty_of_phones} phone {plural}') if qty_of_phones > 1 else f'This record has {qty_of_phones} phone {sing}'
        what_to_change = input(
            f"Which phone number do you want to change? Enter one of those values ({', '.join(self.phones_dict.keys())}) or press Enter to skip: ")

        if what_to_change == "":
            print("No phone number changed")
            return

        if self.normalize_key(what_to_change) in self.phones_dict.keys():
            new_phone = input("Enter new phone number: ")
            self.phones_dict[what_to_change] = new_phone
            print(f"Phone number changed: {new_phone}")

    def __str__(self):
        phones = ", ".join(f"{key}: {phone}" for key,
                           phone in self.phones_dict.items())
        return f'{self.name}\n phones:\n {phones}'

    @staticmethod
    def is_valid_phone(phone_number):
        pattern = r"^\+?[0-9\s\-\(\)]+$"
        return bool(re.match(pattern, phone_number)) and len(phone_number) >= 10

    @staticmethod
    def normalize_key(key):
        return key.lower().strip()


class AddressBook:
    def __init__(self):
        self.records = set()

    def add_record(self, record):
        self.records.add(record)

    def prompt_add_new_record(self, name):
        user_input = input(
            f"Do you want to add a new record for {name}? (y/n): ")
        if user_input.lower() == 'y':
            new_record = Record(Name(name))
            while True:
                new_phone = input(
                    f"Provide a phone number for {new_record.name.value} or press Enter to skip: ")
                if new_phone == "":
                    print("No phone number added, but you can add it later.\n")
                    break

                elif Record.is_valid_phone(new_phone):
                    new_record.add_phone(Phone(new_phone))
                    print(f"Phone number added: {new_phone}")
                    break
                else:
                    print("No phone number added, but you can add it later.\n")
            self.add_record(new_record)
            print(f"Record added: {new_record}")
            return new_record, self.records
        elif user_input.lower() == 'n':
            return "Okay. Let me know if you need further assistance."

    def prompt_add_new_phone(self, record):
        user_input = input(
            f"Add new phone number to {record.name.value}? (y/n): ")
        if user_input.lower() == 'y':
            phone = Phone(input("Enter phone number: "))
            record.add_phone(phone)
            print(f"Updated record: {record}")
            return record

    def prompt_action(self, record):
        if record:
            action = input(
                f"{record.name.value} found. What do you want to do? "
                "(add phone, delete record, exit,change phone) (a/d/e/c): "
            )
            if action == 'a':
                return self.prompt_add_new_phone(record)
            elif action == 'd':
                return self.delete_record(record.name.value)

            elif action == 'e':
                return "Okay. Let me know if you need further assistance."

    def find_record(self, name):

        for record in self.records:
            if record.name == name:
                print(f"Found record: {record}")
                return record, self.prompt_action(record)
        return self.prompt_add_new_record(name)

    def find_record_by_phone(self, phone):
        for record in self.records:
            if phone in record.phones:
                print(f"Found record: {record}")
                return record

    def delete_record(self, name):
        record = self.find_record(name)
        if record:
            self.records.remove(record)
            print(f"Record deleted for {name}")
        return record

    # def change_record(self, name=None, phone=None):
        for record in self.records:
            if record.name.value == name:
                print('rectocha', record)
                for phone in record.phones:
                    print(phone)

            if record.name.value == name:
                print("change it", record)

                change_action = input("what to change? (n/p)")
                if change_action == 'n':
                    print(record.name.value)
                elif change_action == 'p':
                    print(record.phones)

    # def change_record(self, record):
    #     print(record)
    #     change_promt = input(
    #         "what to change name or phone(n/p) to exit press Enter")
    #     if change_promt == '':
    #         print('nothing changed')
    #         return
    #     elif change_promt == 'n':
    #         print("change name? ", record.name.value)
    #         new_name = input("pls provide name")
    #         record.name.value = new_name
    #         print(record)
    #     elif change_promt == 'p':
    #         print("change ph")

    def __str__(self):
        if not self.records:
            return "No records found."
        return '\n'.join(str(record) for record in self.records)


my_address_book = AddressBook()

record1 = Record(Name('jOhn'), [Phone('1234567890')])
record2 = Record(Name('Ann'), [Phone('1234567890')])
record3 = Record(Name('Johny'), [Phone('1234567895')])
# print(my_address_book.find_record(Name('John')))
# print(my_address_book.find_record(Name('Ann')))

record1.add_phone(Phone('1111111111'))
record1.add_phone(Phone('1111111112'))
record1.add_phone(Phone('1111111113'))
record2.add_phone(Phone('1111111114'))
record2.add_phone(Phone('1111111115'))
record2.add_phone(Phone('1111111116'))
record3.add_phone(Phone('1111111117'))
record3.add_phone(Phone('1111111118'))
record3.add_phone(Phone('1111111119'))
my_address_book.add_record(record1)
my_address_book.add_record(record2)
my_address_book.add_record(record3)

record1.change_record_name('Amelia')
record1.change_record_phone()
my_address_book.find_record('John')

# my_address_book.find_record(name='Johnatan')
# my_address_book.find_record_by_phone(phone='1111111111')
# my_address_book.change_record('Ann')
# print("adress_book", my_address_book, sep='\n')

# my_address_book.change_record('1234567890')
# my_address_book.change_record(record2)
# record1.change_record_name('Amelia')
# record1.change_record_phone(new_phone='9999999999')
print("my_address_book\n", my_address_book)
