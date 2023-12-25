import pickle
from base_objects.book_object import AddressBook
from base_objects.note_object import NoteBook


class Storage:
    def __init__(self, filename):
        self._filename = f"{filename}.pkl"

    def save_to_disk(self, records_dict):
        try:
            with open(self._filename, "wb") as file:
                pickle.dump(records_dict, file)
        except Exception as e:
            pass

    def read_from_disk_contacts(self):
        try:
            with open(self._filename, "rb") as file:
                loaded_records = pickle.load(file)
            return loaded_records
        except FileNotFoundError:
            return AddressBook()
        except Exception as e:
            return {}

    def read_from_disk_notes(self):
        try:
            with open(self._filename, "rb") as file:
                loaded_records = pickle.load(file)
            return loaded_records
        except FileNotFoundError:
            return NoteBook()
        except Exception as e:
            return {}
