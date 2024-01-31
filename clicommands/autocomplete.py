#!.venv/bin/python
import click
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
current_directory = '/Users/jayro/Documents/santander/qs/CFTemplates/XXXXXXXX7434/dashboards'
@click.command()
def main():
    click.echo("Welcome to the File Printer CLI!")
    selected_file = select_file()
    # Print the contents of the selected file
    print_file_contents(selected_file)

def select_file():
    files = get_files_in_directory()

    if not files:
        click.echo("No files found in the directory. Exiting.")
        exit()

    # Use prompt with WordCompleter for file selection
    selected_file = prompt(
        "Select a file: ",
        completer=WordCompleter(files),
    )
    selected_file = f'{current_directory}/{selected_file}'
    # Return the selected file
    return selected_file

def get_files_in_directory():
    files = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]
    return files

def print_file_contents(selected_file):
    try:
        with open(selected_file, 'r') as file:
            content = file.read()
            click.echo(f"Contents of {selected_file}:\n{content}")
    except Exception as e:
        click.echo(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
