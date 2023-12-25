import re
from datetime import datetime
from utilities.error_handler import BadPhoneNumber


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Tag(Field):
    def __init__(self, tag):
        super().__init__(tag)


class Note(Field):
    def __init__(self, value):
        super().__init__(value)


# ADD VALIDATION


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone():
            raise BadPhoneNumber(value)

    def validate_phone(self):
        phone_pattern = re.compile(r'^\+38\d{9,10}$')
        return bool(re.match(phone_pattern, self.value))


class Email(Field):
    def __init__(self, email):
        super().__init__(email)
        if not self.validate_email():
            raise ValueError("Invalid email format.")

    def validate_email(self):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, self.value) is not None


class Birthday:
    def __init__(self, value):
        if type(value) == str:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        elif type(value) == datetime:
            self.value = value

    def __str__(self):
        return str(self.value.strftime("%d.%m.%Y"))

    def __eq__(self, other):
        if type(other) == str:
            return self.value.date == datetime.strptime(other, "%d.%m.%Y").date
        elif type(other) == datetime:
            return self.value.date == other.value.date
        else:
            return False


class Address(Field):
    def __init__(self, address):
        super().__init__(address)
        if not self.validate_address(address):
            raise ValueError("The address cannot be empty.")

    @staticmethod
    def validate_address(address):
        if len(address) < 5 or len(address) > 100:
            raise ValueError("The address must contain from 5 to 100 characters.")
        if any(char in address for char in "!@#$%^&*()"):
            raise ValueError("The address contains invalid characters.")
        return address.strip()