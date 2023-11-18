from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = self.validate(value)
    
    def validate(self, value):
        cleaned_value = ''.join(filter(str.isdigit, value))

        if len(cleaned_value) == 10:
            return cleaned_value
        elif len(cleaned_value) == 12 and cleaned_value.startswith('+38'):
            return cleaned_value
        else:
            raise ValueError('Invalid phone number. Phone should be 10 or 12 digits and may start with +38')
        

class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if not any(existing_phone.value == phone.value for existing_phone in self.phones):
            self.phones.append(phone)
            
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
   
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                try:
                    phone.validate(new_phone)
                    phone.value = new_phone
                    return new_phone
                except ValueError as e:
                    print(e)
        raise ValueError(f"Phone number {old_phone} not found.")
    
    def remove_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return phone.value
        raise ValueError(f"Phone number {phone_number} not found.")


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        
    def find(self, name):
        for record_name, record in self.data.items():
            if record_name == name:
                return record
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"The contact {name} deleted.")
        else:
            print(f"The contact {name} not found.")