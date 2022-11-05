from classes import AddressBook, Record

def input_error(handler):
    def wrapper(*args):
        try:
            return handler(*args)
        except Exception as e:
            error_string = e.args[0]
            if 'show_phone()' in error_string or 'days_to_birthday()' in error_string: 
                return 'enter name'
            elif 'add_birthday()' in error_string:
                return 'enter name and birthday'
            elif 'show_part()' in error_string:
                return 'enter number of contacts'
            elif 'find()' in error_string:
                return 'enter symbols to find'
            else:
                return 'enter name and phone' 
    return wrapper

def stop():
    save_to_file()
    return 'Good bye!'

def greeting():
    return 'How can I help you?' 

@input_error
def add(name, phone):
    if address_book.data.get(name):
        return 'Contact already exist' 
    
    record = Record(name)
    
    if not record.add_phone(phone):
        return 'phone must be in this format 381111111111'

    address_book.add_record(record)
    return 'new contact added'



@input_error
def add_phone(name, phone):
    if address_book.data.get(name):
        record = address_book.data[name]

        if not record.add_phone(phone):
            return 'phone must be in this format 381111111111'
        
        return f'A new phone {phone} has been added to contact {name}' 
    else:
        return 'Сontact does not exist'

@input_error
def add_birthday(name, birthday):
    if address_book.data.get(name):
        record = address_book.data[name]

        if not record.add_birthday(birthday):
            return 'birthday format must be dd.mm.yyyy'
            
        return f'birthday {birthday} has been added to contact {name}'
    else:
        return 'contact does not exist'

@input_error
def days_to_birthday(name):
    if address_book.data.get(name):
        record = address_book.data[name]
        if record.birthday:
            return record.days_to_birthday()
        else:
            return 'contact with empty birthday'
        
@input_error
def change(name, phone):
    new_phone = input('enter new phone\n')
    record = address_book.data[name]

    if record.change_phone(phone, new_phone) is True:
        return f'{name} phone number changed to {new_phone}' 
    else:
        return 'phone number does not exist' 

@input_error
def delete_phone(name, phone):
    record = address_book.data[name]

    if record.delete_phone(phone) is True:
        return f'contact: {name} phone {phone} deleted' 
    else:
        return 'phone number does not exist'

@input_error
def show_phone(name):
    if name in address_book.data.keys():
        phones_list = []
        for phone in address_book.data[name].phones:
            phones_list.append(phone.value)
        return phones_list 
    else:
        return 'no such name' 

def show_all():
    if not address_book.data:
        return 'nothing to show'

    all_contacts = ''
  
    for name, record in address_book.items():
        phones_list = []
        for phone in record.phones:
            phones_list.append(phone.value)
        
        if record.birthday:
            all_contacts += f'{name} | phones: {phones_list} | birthday: {record.birthday.value}\n'
        else:
            all_contacts += f'{name} | phones: {phones_list}\n'

    return all_contacts

@input_error
def show_part(part):
    if not address_book.data:
        return 'nothing to show'

    part_contacts = ''
    for name, record in address_book.iterator(int(part)):
        phones_list = []
        for phone in record.phones:
            phones_list.append(phone.value)
        
        if record.birthday:
            part_contacts += f'{name} | phones: {phones_list} | birthday: {record.birthday.value}\n'
        else:
            part_contacts += f'{name} | phones: {phones_list}\n'
            
    return part_contacts

def save_to_file(file = None):
    if not address_book.data:
        return 'nothing to save'

    address_book.save_to_file(file)
    return 'file saved'

def read_from_file(file = None):
    return address_book.read_from_file(file)

@input_error
def find(symbols):
    if not address_book.data:
        return 'nothing to show'

    finded_contacts = ''

    for name, record in address_book.items():
        phones_list = []

        for phone in record.phones:
            phones_list.append(phone.value)

        if symbols.isnumeric():
            for phone in phones_list:
                if symbols in phone:
                    finded_contacts += f'{name} | phones: {phones_list}\n'
                    break
        else:
            if symbols in name:
                finded_contacts += f'{name} | phones: {phones_list}\n'

    return finded_contacts

def main():  
    commands_without_input = {
      'hello': greeting,
      'exit': stop,
      'close': stop,
      'good bye': stop,
      'show all': show_all,
      'save': save_to_file,
    }

    commands_with_input = {
        'add': add,
        'add_phone': add_phone,
        'add_birthday': add_birthday,
        'days_to_birthday': days_to_birthday,
        'change': change,
        'phone': show_phone,
        'delete': delete_phone,
        'show_part': show_part,
        'find': find,
    }
    
    while True:
        user_command = input('...').lower()
        user_command_with_inputs = user_command.split(' ')
        command = user_command_with_inputs[0]
        user_inputs = user_command_with_inputs[1:]

        if user_command in ['exit', 'close', 'good bye']:
            print(stop())
            break
        
        if commands_without_input.get(user_command):
            result = commands_without_input[user_command]()
            print(result)
            continue
        elif commands_with_input.get(command):
            result = commands_with_input[command](*user_inputs)
            print(result)
            continue
        else:
            print('unknown command')
            continue

if __name__ == '__main__':
    address_book = AddressBook()
    loaded_address_book = read_from_file()
    address_book = loaded_address_book or address_book
    main()