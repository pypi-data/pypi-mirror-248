from rich.console import Console
from rich.table import Table
from rich import box


def birthday_output(upcoming_birthdays, book):
    console = Console()
    if upcoming_birthdays:
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
        table.add_column("Name", style="cyan", justify="center")
        table.add_column("Phone", style="green", justify="center")
        table.add_column("E-mail", style="red", justify="center")
        table.add_column("Address", style="yellow", justify="center")
        table.add_column("Birthday", style="red", justify="center")

        for name, birthday in upcoming_birthdays:
            contact = book.find(name)
            phones = ', '.join([phone.value for phone in contact.phones]) if contact.phones else ""
            emails = ', '.join(
                [email.value for email in contact.emails if email != []]) if contact.emails else ""
            address = contact.address if contact.address else ""

            table.add_row(name, phones, emails, address, str(birthday))

        console.print(table)
    else:
        console.print("No upcoming birthdays.")