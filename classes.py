from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, name):
        self.__value = None
        self.value = name

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, name):
        self.__value = None
        self.value = name

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, name):
        if len(name) == 12 and name.isnumeric():
            self.__value = name

class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
           if datetime.strptime(value, '%d.%m.%Y'):
              self.__value = value
        except:
            self.__value = None

class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        user_phone = Phone(phone)
        if user_phone.value:
            self.phones.append(Phone(phone))
            return True
        
    def add_birthday(self, birthday):
        user_birthday = Birthday(birthday)
        if user_birthday.value:
            self.birthday = Birthday(birthday)
            return True

    def days_to_birthday(self):
        today = datetime.now().date()
        birthday_string = self.birthday.value
        birthday_list = birthday_string.split('.')
        day = int(birthday_list[0])
        month = int(birthday_list[1])
        year = int(birthday_list[2])
        next_birthday = datetime(year=today.year,
                                 month=month,
                                 day=day).date()
        delta = next_birthday - today
        return delta.days

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                if not self.add_phone(new_phone):
                    return False
                self.phones.remove(phone)
                return True

    def delete_phone(self, delete_phone):
        for phone in self.phones:
            if phone.value == delete_phone:
                self.phones.remove(phone)
                return True

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def iterator(self, n):
        i = 0
        if len(list(self.items())) < n:
            while i < len(list(self.items())):
                yield list(self.items())[i]
                i += 1
        else:
            while i < n:
                yield list(self.items())[i]
                i += 1

    def save_to_file(self, filename = None):
        if filename is None:
            filename = 'contacts.dat'
            
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def read_from_file(self, filename = None):
        if filename is None:
            filename = 'contacts.dat'
        
        try:
            with open(filename, 'rb') as file:
                address_book = pickle.load(file)
            return address_book
        except FileNotFoundError:
            return None