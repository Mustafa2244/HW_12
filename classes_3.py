from collections import UserDict
import datetime
import pickle


class Field:
    def __init__(self, value=None):
        self.value = None
        self.set_value(value)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    def set_value(self, value):
        try:
            self.value = int(value)
            return self.value
        except Exception:
            return None


class Birthday(Field):
    def __init__(self, date):
        super().__init__(date)

    def set_value(self, value):
        try:
            if len(value) == 5 and int(value[:2]) and value[2] == "." and int(value[3:]):
                self.value = str(value)
            else:
                return None
            return self.value
        except Exception:
            return None


class Record:
    def __init__(self, name: Name, phones: list[Phone] = [], birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phones:
            if type(phones) == list:
                for phone in phones:
                    if phone.get_value():
                        self.phones.append(phone)
            else:
                self.phones.append(phones)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        for my_phone in self.phones:
            if my_phone.get_value() == phone:
                self.phones.remove(my_phone)

    def update_phone(self, old_phone, new_phone):
        for my_phone in self.phones:
            if my_phone.get_value() == old_phone:
                my_phone.set_value(new_phone)

    def days_to_birthday(self):
        if self.birthday.get_value():
            birthday = datetime.datetime.strptime(self.birthday.get_value(), "%d.%m").replace(
                year=datetime.datetime.today().year,
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            if (birthday - datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)).days < 0:
                new_birthday = datetime.datetime.strptime(
                    self.birthday.get_value(), "%d.%m"
                ).replace(
                    year=datetime.datetime.today().year+1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0
                )
                days = (new_birthday - datetime.datetime.today().replace(
                    hour=0, minute=0, second=0, microsecond=0)).days
            else:
                days = (birthday - datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)).days
            return days
        else:
            return None


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.get_value()] = record

    def iterator(self, n):
        for i in range(0, len(self.data.keys()), n):
            yield [{key: value} for key, value in zip(list(self.data.keys())[i:i+n], list(self.data.values())[i:i+n])]

    def search(self, search_word):
        res = []
        for key, value in zip(self.data.keys(), self.data.values()):
            if search_word.lower() in str(key).lower():
                res.append(key)
            else:
                for phone in value.phones:
                    if search_word.lower() in str(phone.get_value()).lower():
                        if key not in res:
                            res.append(key)
        return res

    def save(self, filepath="address_book.pkl"):
        pickle.dump(self.data, open(filepath, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filepath="address_book.pkl"):
        self.data = pickle.load(open(filepath, "rb"))


def input_error(func):
    def decorator_with_arguments(command=""):
        try:
            res = func(command)
            if res is None:
                return "Phone not found"
        except KeyError:
            return "KeyError"
        except ValueError:
            return "Phone not number"
        except IndexError:
            return "Give me name and phone please"
        return res
    return decorator_with_arguments


telephone_book = AddressBook()


def hello():
    return "How can I help you?"


@input_error
def add(command):
    name = command.split(" ")[1]
    phone_number = command.split(" ")[2]
    if len(command.split(" ")) == 4:
        day_to_birthday = command.split(" ")[3]
        telephone_book.add_record(Record(Name(name), [Phone(phone_number)], Birthday(day_to_birthday)))
    else:
        telephone_book.add_record(Record(Name(name), [Phone(phone_number)]))
    return "Phone was successfully added"


@input_error
def change(command):
    for key in telephone_book.keys():
        if key == command.split(" ")[1]:
            telephone_book[key].update_phone(telephone_book[key].phones[0].value, command.split(" ")[2])
    return "Phone was successfully changed"


@input_error
def phone(command):
    for user in telephone_book.keys():
        if user == command.split(" ")[1]:
            return ", ".join([ph.value for ph in telephone_book[user].phones])


@input_error
def days_to_birthday(command):
    for user in telephone_book:
        if user == command.split(" ")[3]:
            return telephone_book[user].days_to_birthday()


@input_error
def search(command):
    if telephone_book.search(command.split(" ")[1]):
        return ", ".join(telephone_book.search(command.split(" ")[1]))
    else:
        return "Not found"


def show_all():
    result = []
    for i, users in enumerate(telephone_book.iterator(10)):
        result.append(f"page {i + 1}:")
        for user in users:
            for key in user:
                result.append(f"{key}: {', '.join([str(ph.value) for ph in telephone_book[key].phones])}")
    return "\n".join(result)


def main():
    try:
        telephone_book.load()
    except:
        pass
    while True:
        command = input().lower()
        if command == "hello":
            print(hello())
        elif command.split(" ")[0] == "add":
            print(add(command))
        elif command.split(" ")[0] == "change":
            print(change(command))
        elif command.split(" ")[0] == "phone":
            print(phone(command))
        elif command.split(" ")[0] == "search":
            print(search(command))
        elif command == "show all":
            print(show_all())
        elif "days to birthday" in command:
            print(days_to_birthday(command))
        elif command == "exit" or command == "close" or command == "good bye" or command == ".":
            telephone_book.save()
            print("Good bye!")
            return


if __name__ == '__main__':
    main()
