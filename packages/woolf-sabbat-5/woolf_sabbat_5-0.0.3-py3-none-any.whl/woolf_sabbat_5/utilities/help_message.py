from rich.console import Console
from rich.table import Table
from rich.text import Text

def help_message():
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Available Commands", style="dim", width=50, justify="center")
    table.add_column("Info", style="dim", width=25, justify="center")

    commands_info = [
        ("add-contact <name> <address> <phone> <email> <birthday>",
         "Add contact"),
        ("exit",
         "Close program"),
        ("add-phone <name> <phone>",
         "Add phone to contact"),
        ("add-email <name> <email>",
         "Add email to contact"),
        ("add-address <name> <address>",
         "Add address to contact"),
        ("add-birthday <name> <birthday>",
         "Add birthday to contact"),
        ("edit-phone <name> <old_phone> <new_phone>",
         "Change phone number in contact"),
        ("edit-email <name> <old_email> <new_email>",
         "Add email to contact"),
        ("edit-address <name> <new_address>",
         "Change address in contact"),
        ("edit-birthday <name> <new_birthday>",
         "Change birthday in contact"),
        ("show-all",
         "Display all contacts"),
        ("show-phone <name>",
         "Display phone number by name"),
        ("show-email <name>",
         "Display email by name"),
        ("show-address <name>",
         "Display address by name"),
        ("show-birthday <name>",
         "Display birthday date by name"),
        ("delete-contact <name>",
         "Delete contact via name"),
        ("delete-phone <name> <phone>",
         "Delete phone in contact"),
        ("delete-email <name> <email>",
         "Delete email in contact"),
        ("delete-address <name>",
         "Delete address in contact"),
        ("add-note <note>",
         "Add new note to notebook"),
        ("show_all_notes", 
         "Show every notes total saved before"),
        ("delete-note <name>",
         "Delete note that saved"),
        ("edit-note <name>",
         "Edit current note"),
        ("show-note <name>",
         "Display one note"),
        ("help",
         "All possible commands"),
    ]

    for i, (left_part, right_part) in enumerate(commands_info):
        formatted_left = Text.from_markup(f"[bold green]{left_part}[/bold green]")
        formatted_right = Text.from_markup(f"[bold red]{right_part}[/bold red]")
        
        if i != 0: 
            table.add_row("-" * 50, "-" * 25)
        
        table.add_row(formatted_left, formatted_right)

    console.print(table)
