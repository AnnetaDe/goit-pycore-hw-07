# Тож в фіналі наш бот повинен підтримувати наступний список команд:

# add[ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к контакту який вже існує.
# change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
# phone [ім'я]: Показати телефонні номери для вказаного контакту.
# all: Показати всі контакти в адресній книзі.
# add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
# show-birthday [ім'я]: Показати дату народження для вказаного контакту.
# birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
# hello: Отримати вітання від бота.
# close або exit: Закрити програму.


from regex_and_decorators import validate_phone, validate_birthday
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return self.value


class Phone(Field):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    @validate_phone
    def value(self, phone):
        self._value = phone

    def __str__(self):
        return self.value if self.value else "No phone number added"


class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @property
    def value(self):
        return self._value

    @value.setter
    @validate_birthday
    def value(self, birthday):
        self._value = birthday

    def __str__(self):
        return self._value if self._value else "No birthday added"


class Record(Name, Phone, Birthday):
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self._phones_dict = {}
        if phone:
            self.add_phone(phone)
        if birthday:
            self.add_record_birthday(birthday)

    @property
    def phones_dict(self):
        return self._phones_dict

    def add_phone(self, phone, phone_alias=None):
        print(f"Adding phone number {phone} to record: {self.name}")
        phone_alias = input(
            "You can add a phone alias for this phone number or press Enter to skip: ")
        phone_key = self.normalize_input(phone_alias) if phone_alias else f"{
            len(self.phones_dict.keys()) + 1}"
        new_phone = Phone(phone)
        self.phones_dict[phone_key] = new_phone
        print(f"Phone number added to record: {self.name}, phone alias: {phone_key}",
              f"phone: {new_phone.value}")
        return self.phones_dict

    def change_phone_alias(self, new_alias):
        if len(self.phones_dict) == 0:
            print("No phone numbers found for this record")
            return
        if new_alias in self.phones_dict.keys():
            print("Alias already exists")
            return
        alias_to_change = input(
            f"Which alias do you want to change? Enter one of those values ({', '.join(self.phones_dict.keys())}) or press Enter to skip: ")
        if alias_to_change == "":
            print("No alias changed")
            return
        if alias_to_change in self.phones_dict.keys():
            self.phones_dict[new_alias] = self.phones_dict.pop(alias_to_change)
            print(f"Record name:{self.name}")
            print(f"Changed to==> {new_alias}: {self.phones_dict[new_alias]}")
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
        print(self)

        what_to_change = input(
            f"Which phone number do you want to change? Enter one of those values ({', '.join(self.phones_dict.keys())}) or press Enter to skip: ")

        if what_to_change == "":
            print("No phone number changed")
            return

        if self.normalize_input(what_to_change) in self.phones_dict.keys():
            new_phone = input("Enter new phone number: ")
            self.phones_dict[what_to_change] = new_phone
            print(f"Phone number changed: {new_phone}")
            return self.phones_dict

    def add_record_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        print(f"Birthday added: {birthday}")

    def show_birthday(self):
        print(f"{self.name}\n BIRTHDAY: {self.birthday}")

    def show_all_record_phones(self):
        for key, phone in self.phones_dict.items():
            print(f"show{key}: {phone.value}")

    def __str__(self):
        phones = ", ".join(f"{key}: {phone}" for key,
                           phone in self.phones_dict.items())
        birthday = f"{
            self.birthday}" if self.birthday else "No birthday added"
        return f'{self.name}\n PHONES:\n {phones}\n BIRTHDAY: {birthday}'

    @staticmethod
    def normalize_input(key):
        return key.lower().strip()


class AddressBook:
    def __init__(self):
        self.records = set()

    def add_record(self, record):
        self.records.add(record)
        print(f"Record added: {record}")

    def add_phone(self, name, phone):
        record = self.find_record(name)
        if record:
            record.add_phone(phone)
            print(f"Updated record: {record}")
            return record

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
        print(f"Searching for {name} in records...")
        for record in self.records:
            if record.name.value == name:
                return record
            return self.prompt_add_new_record(name)

    def show_record_phones(self, name):
        record = self.find_record(name)
        if record:
            record.show_all_record_phones()
            return record

    def find_record_by_phone(self, phone):
        for record in self.records:
            for value in record.phones_dict.values():
                if value.value == phone:
                    return record

    def change_record_phone(self, name, phone):
        record = self.find_record(name)
        if record:
            record.change_record_phone(phone)
            return record

    def show_birthday(self, name):
        record = self.find_record(name)
        if record:
            record.show_birthday()
            return record

    def change_record_name(self, name):
        record = self.find_record(name)
        if record:
            new_name = input("Enter new name: ")
            record.change_record_name(new_name)
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

    def show_birthdays(self):
        upcoming_week_birthdays = []
        for record in self.records:
            if record.birthday.value:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                current_year = datetime.now().year
                congratulation_date = birthday.replace(year=current_year)

                if congratulation_date.weekday() == 5:
                    congratulation_date = congratulation_date.replace(
                        day=congratulation_date.day+2)

                elif congratulation_date.weekday() == 6:
                    congratulation_date = congratulation_date.replace(
                        day=congratulation_date.day+1)
                else:
                    congratulation_date = congratulation_date

                if congratulation_date >= datetime.now() and (datetime.now().isocalendar().week)+1 == congratulation_date.isocalendar().week:
                    person_to_greet = {
                        'name': record.name.value,
                        'congratulation_date': datetime.strftime(congratulation_date, '%Y.%m.%d')
                    }
                    upcoming_week_birthdays.append(person_to_greet)

        if upcoming_week_birthdays:
            print("Upcoming birthdays:", upcoming_week_birthdays)
        else:
            print("No birthdays in the upcoming week.")
        return upcoming_week_birthdays

    def add_birthday(self, name, birthday):
        record = self.find_record(name)
        if record:
            record.add_record_birthday(birthday)
            return record

    def __str__(self):
        if not self.records:
            return "No records found."
        return '\n'.join(str(record) for record in self.records)


# my_address_book = AddressBook()
# my_address_book.add_record(record=my_record)
