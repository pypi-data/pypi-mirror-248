import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.exceptions as exceptions
import pdfriend.classes.cmdparsers as cmdparsers
import pdfriend.classes.info as info
from pdfriend.classes.platforms import Platform
import pathlib
import re


whitespace_pattern = re.compile(r"\s+")

def parse_command_string(command_string: str) -> list[str]:
    return re.split(whitespace_pattern, command_string)

def validate_page_num(pdf: wrappers.PDFWrapper, page_num: int):
    npages = pdf.len()
    if page_num > 0 or page_num <= npages:
        return
    raise exceptions.ExpectedError(
        f"page {page_num} doesn't exist in the PDF (total pages: {npages})"
    )

command_info = {
    "help": info.CommandInfo("help", "h", """[command?]
    display help message. If given a command, it will only display the help message for that command.

    examples:
        help rotate
            displays the help blurb for the rotate command
        help exit
            displays the help blurb for the exit command
    """),
    "exit": info.CommandInfo("exit", "e", """
    exits the edit mode
    """),
    "rotate": info.CommandInfo("rotate", "r", """[page_numbers] [angle]
    rotates page clockwise with the given numbers (starting from 1) by the given angle (in degrees). Can use negative angles to rotate counter-clockwise. DO NOT put extra spaces between the page numbers!

    examples:
        r 34 1.2
            rotates page 34 clockwise by 1.2 degrees
        r 1,3,8 -4
            rotates pages 1,3 and 8 counter-clockwise by 4 degrees
        r 3-18 90
            rotates pages 3 through 18 (INCLUDING 18) clockwise by 90 degrees
        r 1,13,5-7,2 54
            rotates pages 1,2,5,6,7,13 clockwise by 54 degrees
        r all -90
            rotates all pages counter-clockwise by 90 degrees
    """),
    "delete": info.CommandInfo("delete", "d", """[page_numbers]
    deletes all specified pages. DO NOT put extra spaces between the page numbers!

    examples:
        d 7
            deletes page 7
        d 4,8,1
            deletes pages 1, 4 and 8
        d 6-66
            deletes pages 6 through 66 (INCLUDING 66)
        d 4,17,3-6
            deletes pages 3,4,5,6 and 17
    """),
    "swap": info.CommandInfo("swap", "s", """[page_0] [page_1]
    swaps page_0 and page_1.
    """),
    "undo": info.CommandInfo("undo", "u", """[number?]
    undo the previous [number] commands.

    examples:
        u
            undoes the previous command
        u 3
            undoes the previous 3 commands
        u all
            undoes all commands issued this session (reverts document fully)
    """),
}

command_info_by_shorts = {cmd.short: cmd for name, cmd in command_info.items()}

def print_help(subcommand: str | None = None):
    if subcommand is None:
         print("pdfriend edit shell for quick changes. Commands:")
         for command, info in command_info.items():
             print(f"{command} (short: {info.short})")

         print("use h [command] to learn more about a specific command")
         return

    sub_info = None
    if subcommand in command_info_by_shorts:
        sub_info = command_info_by_shorts[subcommand]
    elif subcommand in command_info:
        sub_info = command_info[subcommand]
    else:
        raise exceptions.ExpectedError(f"command \"{subcommand}\" does not exist")

    print(f"{sub_info.name}|{sub_info.short} {sub_info.descr}")



def run_edit_command(pdf: wrappers.PDFWrapper, args: list[str]):
    no_command_msg = "No command specified! Type h or help for a list of the available commands"
    if len(args) == 0:
        raise exceptions.ExpectedError(no_command_msg)

    command = args[0]
    if command == "":
        raise exceptions.ExpectedError(no_command_msg)

    short = ""; long = ""
    if command in command_info_by_shorts:
        short = command
        long = command_info_by_shorts[command].name
    elif command in command_info:
        long = command
        short = command_info[command].short
    else:
        raise exceptions.ExpectedError(f"command \"{command}\" does not exist")

    cmd_parser = cmdparsers.CmdParser(long, args[1:])

    if short == "h":
        subcommand = cmd_parser.next_str_or(None)
        print_help(subcommand)

        # this is to prevent rewriting the file and appending
        # the command to the command stack
        raise exceptions.ShellContinue()
    if short == "e":
        raise exceptions.ShellExit()
    if short == "r":
        pages = cmd_parser.next_typed("PDF slice", lambda s: pdf.slice(s))
        angle = cmd_parser.next_float()

        for page in pages:
            validate_page_num(pdf, page)
            pdf.rotate_page(page, angle)
    if short == "d":
        pages = cmd_parser.next_typed("PDF slice", lambda s: pdf.slice(s))

        for page in pages:
            pdf.pop_page(page)
    if short == "s":
        page_0 = cmd_parser.next_int()
        validate_page_num(pdf, page_0)
        page_1 = cmd_parser.next_int()
        validate_page_num(pdf, page_1)

        pdf.swap_pages(page_0, page_1)
    if short == "u":
        # arg will be converted to int, unless it's "all". Defaults to 1
        num_of_commands = cmd_parser.next_int_or(1, unless = ["all"])

        raise exceptions.ShellUndo(num_of_commands)


def edit(infile: str):
    pdf = wrappers.PDFWrapper.Read(infile)
    command_stack = []

    # backup the file, because it will be overwritten
    backup_path = pdf.backup(infile)
    print(f"editing {infile}\nbackup created in {backup_path}")

    while True:
        try:
            args = parse_command_string(input(""))
            run_edit_command(pdf, args)
            command_stack.append(args)

            pdf.write(infile) # overwrites the file!
        except (KeyboardInterrupt, exceptions.ShellExit):
            return
        except exceptions.ShellContinue:
            continue
        except exceptions.ShellUndo as undo:
            if undo.num == "all":
                command_stack = []
            else:
                command_stack = command_stack[:-undo.num]

            pdf = wrappers.PDFWrapper.Read(backup_path)
            for args in command_stack:
                run_edit_command(pdf, args)

            pdf.write(infile)
        except exceptions.ExpectedError as e:
            print(e)
        except Exception as e:
            print(f"unexpected exception occured:\n{e}")

