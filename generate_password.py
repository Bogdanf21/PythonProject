import functools
import os
import string
import sys
import random
import getopt
import time

from timeit import default_timer as timer

import subprocess
from os import listdir
from os.path import isfile, join, isdir

min_size = 12
max_size = 18
special_characters = ["!", "?", "#", "@"]


def generate_password():
    password = ""
    # 18 and not 19 because only the letters besides the first can be of any kind
    password_length = random.randrange(min_size - 1, max_size - 1)

    # The first character will always be an uppercase letter
    print("password_length:", password_length + 1)
    first_letter = random.choice(string.ascii_uppercase)
    password += first_letter

    # letters:
    # letters can be of length 1,2 ... password_length-2: subtracting 2 in order to have at least
    # one number and one special character. So the range is (1, password_length - 1)
    letters_length = random.randrange(1, password_length - 1)
    print("LETTERS_LENGTH:", letters_length)

    pieces = []
    for i in range(letters_length):
        pieces.append(random.choice(string.ascii_letters))

    # Numbers: the range 1,n actually means 1...n-1, so it's ok, we have enough room for another letter
    numbers_length = random.randrange(1, password_length - letters_length)
    print("NUMBERS_LENGTH:", numbers_length)

    for i in range(numbers_length):
        pieces.append(random.choice(string.digits))

    # Special characters - the remainder
    special_characters_length = password_length - letters_length - numbers_length

    print("SPECIAL_CHARACTERS_LENGTH:", special_characters_length)
    for i in range(password_length - letters_length - numbers_length):
        pieces.append(random.choice(special_characters))

    # shuffle and append the first uppercase letter
    random.shuffle(pieces)
    password += functools.reduce(lambda x, y: x + y, pieces)
    print("PASSWORD: ", password)


def generate_password_from_file(file_name):
    file_path = get_file_abs_path(file_name)
    words = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            words += list(i for i in line.split(" ") if len(i) > 0)
    password_pieces = []
    random.shuffle(words)

    password_pieces.append(random.choice(string.digits))
    password_pieces.append(random.choice(special_characters))
    for word in words:
        if len(word) + sum(len(piece) for piece in password_pieces) <= max_size:
            password_pieces.append(word)
    # We have the minimum requirements. But it will always contain only a special character and a digit so
    remaining_digits = max_size - sum(len(piece) for piece in password_pieces)
    if remaining_digits >= 1:
        more_digits = random.randrange(1, remaining_digits + 1)
        for i in range(more_digits):
            what_to_add = random.choice([0, 1])
            match what_to_add:
                case 0:
                    password_pieces.append(random.choice(string.digits))
                case 1:
                    password_pieces.append(random.choice(special_characters))
    random.shuffle(password_pieces)
    password = functools.reduce(lambda x, y: x + y, password_pieces)
    print("PASSWORD: ", password)


def find_file(file_name, root):
    possible_files = []
    for (root, dirs, files) in os.walk(root, topdown=True):
        if file_name in files:
            possible_files.append(join(root, file_name))
    return possible_files


def get_file_abs_path(file_name):
    # For all drives
    # driveStr = subprocess.check_output("fsutil fsinfo drives")
    # driveStr = driveStr.strip()
    # driveStr = driveStr.decode("utf-8").lstrip('Drives: ')
    # drives = driveStr.split()

    # For drive = same disk as the project
    root = os.path.abspath(os.curdir).split(os.sep)[0]
    # drives = [root + os.sep]
    drives = ["G:\\"]

    possible_files = []
    file = None
    for d in drives:
        possible_file = find_file(file_name, d)
        possible_files += possible_file
    if len(possible_files) == 0:
        print("Could not find your file!")
        return

    if len(possible_files) > 1:
        print("More files with this name were found. Choose one:")
        for i in range(len(possible_files)):
            print(f"{i}.{possible_files[i]}")
        print("Type x to exit\n")
        choice = input("Choice=")

        if not choice.isnumeric():
            print("Exiting...")
            return
        else:
            choice = int(choice)

        file = possible_files[choice]
    else:
        file = possible_files[0]
    return file


def main():
    argumentList = sys.argv[1:]
    possibleFirstArgument = ['-use_dict']
    if len(argumentList) != 0 and len(argumentList) != 2:
        print("[ERROR] Invalid arguments\n Usage:\n - generate_password.py \n - generate_password.py -use_dict "
              "\"dictionar.txt\"")
        return

    match len(argumentList):
        case 0:
            generate_password()
        case 2:
            generate_password_from_file("test.txt")


if __name__ == '__main__':
    main()

# def find_file(file_name, root):
#     folders = [root]
#     try:
#         while folders:
#             to_be_searched = folders.pop(0)
#             try:
#                 all_dirs = listdir(to_be_searched)
#             except PermissionError as e:
#                 # If I don't run this script as administrator my access may be denied in certain parts of the disks
#                 continue
#             for f in all_dirs:
#                 abs_path = join(to_be_searched, f)
#                 if isfile(abs_path):
#                     if f == file_name:
#                         return abs_path
#                 else:
#                     folders.append(abs_path)
#     except FileNotFoundError as e:
#         print(e)
#         return None
#     except NotADirectoryError as e:
#         print(e)
#         return None
