from collections import UserDict


class NoteBook(UserDict):
    def add_note(self, note_record):
        self.data[note_record.tag.value] = note_record

    def find(self, tag):
        return self.data[tag]

    def show_all_notes(self):
        if self.data:
            print("\nAll Notes:")
            return "\n".join(
                f"{tag} - "
                f"Note: {record_note.note_memory.value}"
                for tag, record_note in self.data.items())
        else:
            return "No tag in the notebook book."

    def delete_note_by_tag(self, tag):
        if tag in self.data:
            del self.data[tag]
            print(f"Contact '{tag}' deleted successfully.")
        else:
            print(f"Contact '{tag}' not found.")