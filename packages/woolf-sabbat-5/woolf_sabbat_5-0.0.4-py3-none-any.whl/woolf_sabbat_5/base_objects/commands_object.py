import re
from datetime import datetime
from base_objects.main_objects import Email
from utilities.error_handler import input_error, BadPhoneNumber, BadEmailFormat, BadBirthdayFormat
from base_objects.record_object import Record, NoteRecord
from utilities.help_message import help_message
from utilities.birtday_output import birthday_output


class Commands:
    @input_error
    def add_contact(self, data, book):
        phone = input("Enter the phone: ")
        email = input("Enter email: ")
        address = input("Enter the address: ")
        birthday = input("Enter a birthday: ")
        record = Record(data)

        if phone:
            record.add_phone(phone)
        if email:
            record.add_email(email)
        if address:
            record.add_address(address)
        if birthday:
            record.add_birthday(birthday)
        book.add_contact(record)
        return f"Contact {data} added successfully."

    @input_error
    def add_phone(self, name, book):
        phone = input("Enter the phone number: ")
        record = book.find(name)
        record.add_phone(phone)
        return f"Phone: {phone} added to contact {name}."

    @input_error
    def add_email(self, name, book):
        email = input("Enter the phone number: ")
        record = book.find(name)
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not re.match(email_pattern, email):
            raise BadEmailFormat(email)
        record.add_email(email)
        return f"Email: {email} added to contact {name}."

    @input_error
    def add_address(self, name, book):
        address = input("Enter the address: ")
        record = book.find(name)
        record.add_address(address)
        return f"Address: {address} added to contact {name}."

    @input_error
    def add_birthday(self, name, book):
        birthday = input("Enter the phone number: ")
        record = book.find(name)
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise BadBirthdayFormat(birthday)
        record.add_birthday(birthday)
        return f"Birthday: {birthday} added to contact {name}."

    @input_error
    def edit_phone(self, name, book):
        old_phone = input("Enter the old phone number: ")
        new_phone = input("Enter the new phone number: ")
        if name in book:
            record = book.find(name)
            phone_pattern = re.compile(r'^\+38\d{9,10}$')
            if not re.match(phone_pattern, new_phone):
                raise BadPhoneNumber(new_phone)
            record.edit_phone(old_phone, new_phone)
            return f"Contact {name} updated."
        else:
            return "Contact not found"

    @input_error
    def edit_email(self, name, book):
        old_email = input("Enter the old email address: ")
        new_email = input("Enter the new email address: ")
        if name in book:
            record = book.find(name)
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not re.match(email_pattern, new_email):
                raise BadEmailFormat(new_email)
            record.edit_email(Email(old_email), Email(new_email))
            return "Contact updated."
        else:
            return "Contact not found"

    @input_error
    def edit_address(self, name, book):
        address = input("Enter the address: ")
        if name in book:
            record = book.find(name)
            record.edit_address(address)
            return "Contact updated."
        else:
            return "Contact not found"

    @input_error
    def edit_birthday(self, name, book):
        birthday = input("Enter the birthday date: ")
        if name in book:
            record = book.find(name)
            try:
                datetime.strptime(birthday, "%d.%m.%Y")
            except ValueError:
                raise BadBirthdayFormat(birthday)
            record.edit_birthday(birthday)
            return "Contact updated."
        else:
            return "Contact not found"

    @input_error
    def show_all(self, book):
        return book.show_all()

    @input_error
    def show_contact(self, name, book):
        return book.show_contact(name)

    @input_error
    def show_phone(self, name, book):
        return book.show_phone(name)

    @input_error
    def show_email(self, name, book):
        return book.show_email(name)

    @input_error
    def show_address(self, name, book):
        return book.show_address(name)

    @input_error
    def show_birthday(self, name, book):
        return book.show_birthday(name)

    @input_error
    def delete_contact(self, name, book):
        return book.delete_contact(name)

    @input_error
    def delete_phone(self, name, book):
        phone = input("Enter the new phone number: ")
        record = book.find(name)
        return record.delete_phone(phone)

    @input_error
    def delete_email(self, name, book):
        email = input("Enter the new phone number: ")
        record = book.find(name)
        return record.delete_email(email)

    @input_error
    def delete_address(self, name, book):
        record = book.find(name)
        return record.delete_address()

    @input_error
    def delete_birthday(self, name, book):
        record = book.find(name)
        return record.delete_birthday()

    @input_error
    def upcoming_birthday(self, days, book):
        birthday_output(book.upcoming_birthday(int(days)), book)

    @staticmethod
    def help():
        return help_message()

    def add_new_note(self, data, notebook):
        note_input = input("Enter the note: ")
        note_record = NoteRecord(data)
        note_record.add_note_record(note_input)
        notebook.add_note(note_record)
        return f"Note {data} added successfully."

    def show_all_notes(self, notebook):
        return notebook.show_all_notes()

    def show_note(self, data, notebook):
        note_record = notebook.find(data)
        return note_record.show_note_by_tag()

    def edit_note(self, data, notebook):
        new_note = input("Enter new note: ")
        note_record = notebook.find(data)
        return note_record.edit_tag_note(new_note)

    def delete_note(self, data, notebook):
        return notebook.delete_note_by_tag(data)