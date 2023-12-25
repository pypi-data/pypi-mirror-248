from datetime import datetime
from utilities.error_handler import BadPhoneNumber, PhoneNumberIsMissing, ValidationException, BadBirthdayFormat
from base_objects.main_objects import Name, Phone, Field, Birthday, Email, Address, Tag, Note


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if not new_phone.validate_phone():
            raise BadPhoneNumber(phone)
        self.phones.append(new_phone)

    def add_email(self, email):
        new_email = Email(email)
        if new_email.validate_email():
            self.emails.append(new_email)
        else:
            raise ValidationException(new_email)

    def add_address(self, address):
        self.address = Address(address)

    def add_birthday(self, birthday):
        new_birthday = Birthday(birthday)
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise BadBirthdayFormat(new_birthday)
        self.birthday = new_birthday

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            new_phone_obj = Phone(new_phone)
            if new_phone_obj.validate_phone():
                index = self.phones.index(old_phone)
                self.phones[index] = new_phone_obj
            else:
                raise ValidationException(new_phone_obj)
        else:
            raise PhoneNumberIsMissing(new_phone_obj)

    def edit_email(self, old_email, new_email):
        if old_email in self.emails:
            new_email_obj = Email(new_email)
            if new_email_obj.validate_email():
                index = self.emails.index(old_email)
                self.emails[index] = new_email_obj
            else:
                raise ValidationException(new_email_obj)
        else:
            raise ValidationException(new_email_obj)

    def edit_address(self, new_address):
        self.address = Field(new_address)

    def edit_birthday(self, new_birthday):
        try:
            datetime.strptime(new_birthday, "%d.%m.%Y")
        except ValueError:
            raise BadBirthdayFormat(new_birthday)
        self.birthday = new_birthday

    def delete_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise PhoneNumberIsMissing(phone)

    def delete_email(self, email):
        if email in self.emails:
            self.emails.remove(email)
        else:
            raise ValidationException(email)

    def delete_address(self):
        self.address = None

    def delete_birthday(self):
        self.address = None

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        emails_str = ', '.join(str(email) for email in self.emails)
        return (f"Record(name: {self.name}, phones: [{phones_str}], emails: [{emails_str}], address: {self.address}, "
                f"birthday: {self.birthday})")


class NoteRecord:
    def __init__(self, tag):
        self.tag = Tag(tag)
        self.note_memory = None

    def add_note_record(self, note):
        self.note_memory = Note(note)

    def edit_note(self, new_note):
        if self.note_memory:
            self.note_memory = Note(new_note)
        else:
            print("No note to edit. Use 'add_note_record' to add a new note.")

    def delete_note(self):
        self.note_memory = None

    def find(self, tag):
        return f"find {tag}"

    def search_by_title_note(self, title):
        return f"search_by_title {title}"