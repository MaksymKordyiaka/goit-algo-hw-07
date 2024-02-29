from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        try:
            if not value.isdigit() or len(value) != 10:
                raise ValueError("Phone number must contain 10 digits")
            super().__init__(value)
        except AttributeError:
            raise AttributeError('Invalid format number. Use 10 digits')

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        except TypeError:
            raise TypeError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, b_day):
        self.birthday = Birthday(b_day)

    def show_birthday(self, b_day):
        return

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = self.find_phone(old_phone)
        if old_phone_obj:
            if not new_phone.isdigit() or len(new_phone) != 10:
                raise ValueError("New phone number must contain 10 digits")
            old_phone_obj.value = new_phone
        else:
            raise ValueError("Phone number not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}, birthdate: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name '{name}' not found in the address book.")

    def get_upcoming_birthdays(self, users):
        today = datetime.today().date()
        birthdays = []
        for user in users:
            birth_date = user['birthday']
            birth_date = str(today.year) + birth_date[4:]
            birth_date = datetime.strptime(birth_date, '%Y.%m.%d').date()
            week_day = birth_date.isoweekday()
            difference_date = (birth_date - today).days
            if 0 <= difference_date <= 7:
                if week_day < 6:
                    birthdays.append({'name': user['name'], 'birthday': birth_date.strftime('%Y.%m.%d')})
                elif week_day == 6:
                    birthdays.append({'name': user['name'], 'birthday': (birth_date + timedelta(days=2)).strftime('%Y.%m.%d')})
                else:
                    birthdays.append({'name': user['name'], 'birthday': (birth_date + timedelta(days=1)).strftime('%Y.%m.%d')})
        return birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

# def input_error(func):
#     def inner(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except (KeyError, ValueError, IndexError) as error:
#             if isinstance(error, KeyError):
#                 return 'Key error'
#             elif isinstance(error, ValueError):
#                 return 'Error! if you want to:\n' \
#                        'add contact: you must input ("add" username phone).\n' \
#                        'change phone: you must input ("change" username phone) or no contacts.\n' \
#                        'get phone: you must input ("phone" username)\n'
#             elif isinstance(error, IndexError):
#                 return 'Index error'
#     return inner
#
# @input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

# @input_error
def change_phone(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return f"Phone number for '{name}' changed."
    else:
        return f"Contact {name} not found."

def show_all(contacts):
    if not contacts:
        return 'No contacts available, you need to (add "username" "phone")'
    else:
        result = ''
        for name, phone in contacts.items():
            result += f"{name}: {phone}\n"
        return result.strip()

# @input_error
def get_phone(args, contacts):
    name, = args
    phone = contacts.get(name)
    if phone:
        return f"Phone number for '{name}': {phone}"
    else:
        return f"Contact {name} not found."

# @input_error
def add_birthday(args, book):
    pass

# @input_error
def show_birthday(args, book):
    pass

# @input_error
def birthdays(args, book):
    pass

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            pass
        elif command == "phone":
            pass
        elif command == "all":
            pass
        elif command == "add-birthday":
            pass
        elif command == "show-birthday":
            pass
        elif command == "birthdays":
            pass
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
