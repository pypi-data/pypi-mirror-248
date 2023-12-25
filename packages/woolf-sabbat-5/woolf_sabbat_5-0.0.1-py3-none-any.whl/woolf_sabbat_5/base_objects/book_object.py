from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):
    def add_contact(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def show_all(self):
        if self.data:
            print("\nAll Contacts:")
            return "\n".join(
                f"{name} - "
                f"Phone(s): {', '.join([phone.value for phone in value.phones])}, "
                f"E-mail(s): {', '.join([email.value for email in value.emails])}, "
                f"Address: {value.address}, "
                f"Birthday: {value.birthday}"
                for name, value in self.data.items())
        else:
            return "No contacts in the address book."

    def show_contact(self, name):
        if name in self.data:
            contact = self.data[name]
            return (f"\n{name}:\nPhone(s): {', '.join([phone.value for phone in contact.phones])}, "
                    f"E-mail(s): {', '.join([email.value for email in contact.emails if email != []])}, "
                    f"Address: {contact.address}, Birthday: {contact.birthday}")
        else:
            return f"Contact '{name}' not found."

    def show_phone(self, name):
        if name in self.data:
            contact = self.data[name]
            if contact.phones:
                return f"{name}'s phone(s): {', '.join([phone.value for phone in contact.phones])}"
            else:
                return f"{name} has no phone numbers."
        else:
            return f"Contact '{name}' not found."

    def show_email(self, name):
        if name in self.data:
            contact = self.data[name]
            if contact.emails:
                return f"{name}'s e-mail(s): {', '.join([email.value for email in contact.emails if email != []])}"
            else:
                return f"{name} has no email address."
        else:
            return f"Contact '{name}' not found."

    def show_address(self, name):
        if name in self.data:
            contact = self.data[name]
            if contact.address:
                print(f"\n{name}'s Address:")
                print(contact.address)
            else:
                print(f"{name} has no address.")
        else:
            print(f"Contact '{name}' not found.")

    def show_birthday(self, name):
        if name in self.data:
            contact = self.data[name]
            if contact.birthday:
                print(f"\n{name}'s Birthday:")
                print(contact.birthday)
            else:
                print(f"{name} has no birthday.")
        else:
            print(f"Contact '{name}' not found.")

    def upcoming_birthday(self, days):
        today = datetime.now()
        upcoming_birthdays = []

        for name, contact in self.data.items():
            if contact.birthday:
                birthday = contact.birthday.value.date()
                next_birthday = datetime(today.year, birthday.month, birthday.day)

                if next_birthday < today:
                    next_birthday = datetime(today.year + 1, birthday.month, birthday.day)

                days_until_birthday = (next_birthday - today).days

                if 0 < days_until_birthday <= days:
                    upcoming_birthdays.append((name, contact.birthday))
        print(upcoming_birthdays)
        return upcoming_birthdays

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Contact '{name}' deleted successfully.")
        else:
            print(f"Contact '{name}' not found.")