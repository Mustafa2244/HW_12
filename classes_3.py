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
    def __init__(self, name: Name, phones=None, birthday=None):
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

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

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
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def add_record(self, record: Record):
        self.data[record.name.get_value()] = record

    def iterator(self, n):
        for i in range(0, len(self.data.keys()), n):
            yield [{key: value} for key, value in zip(list(self.data.keys())[i:i+n], list(self.data.values())[i:i+n])]

    def search(self, search_word):
        res = []
        for key, value in zip(self.data.keys(), self.data.values()):
            if search_word in str(key):
                res.append(key)
            else:
                for phone in value.phones:
                    if search_word in str(phone.get_value()):
                        if key not in res:
                            res.append(key)
        return res

    def save(self, filepath="address_book.pkl"):
        pickle.dump(self.data, open(filepath, "wb"), protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filepath="address_book.pkl"):
        self.data = pickle.load(open(filepath, "rb"))
