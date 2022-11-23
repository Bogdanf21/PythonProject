import functools
import os
import string
import sys
import random

from os.path import join

min_size = 12
max_size = 18
special_characters = ["!", "?", "#", "@"]
usage_message = "Usage:\n - generate_password.py \n - generate_password.py -use_dict \"dictionar.txt\""


def test():
    max_length, min_length = 0, 999
    max_letter_count, min_letter_count = 0, 999
    max_special_characters, min_special_characters = 0, 999
    max_digit_count, min_digit_count = 0, 999

    for i in range(1000):
        pw = generate_password()
        letter_count = 0
        special_characters_count = 0
        number_count = 0
        for item in pw:
            if item in string.ascii_letters:
                letter_count += 1
            elif item in string.digits:
                number_count += 1
            else:
                special_characters_count += 1

        if max_letter_count < letter_count:
            max_letter_count = letter_count
        if min_letter_count > letter_count:
            min_letter_count = letter_count
        if special_characters_count > max_special_characters:
            max_special_characters = special_characters_count
        if special_characters_count < min_special_characters:
            min_special_characters = special_characters_count
        if min_digit_count > number_count:
            min_digit_count = number_count
        if max_digit_count < number_count:
            max_digit_count = number_count

        if max_length < len(pw):
            max_length = len(pw)
        if min_length > len(pw):
            min_length = len(pw)

    print(f"Min/max letter count:{min_letter_count}/{max_letter_count}")
    print(f"Min/max digit count:{min_digit_count}/{max_digit_count}")
    print(f"Min/max sp char count:{min_special_characters}/{max_special_characters}")
    print(f"Min/max length:{min_length}/{max_length}")





def generate_password():
    password = ""
    # 18 and not 19 because only the characters beside the first can be of any kind
    password_length = random.randrange(min_size - 1, max_size)

    # The first character will always be an uppercase letter
    first_letter = random.choice(string.ascii_uppercase)
    password += first_letter

    # letters:
    # letters can be of length 0, 2 ... password_length-2 (we already have an uppercase letter)
    # subtracting 2 in order to have at least
    # one number and one special character. So the range is (1, password_length - 1)
    letters_length = random.randrange(0, password_length - 1)

    pieces = []
    for i in range(letters_length):
        pieces.append(random.choice(string.ascii_letters))

    # Numbers: the range 1,n actually means 1...n-1, so it's ok, we have enough room for another letter
    numbers_length = random.randrange(1, password_length - letters_length)

    for i in range(numbers_length):
        pieces.append(random.choice(string.digits))

    # Special characters - the remainder
    special_characters_length = password_length - letters_length - numbers_length

    for i in range(password_length - letters_length - numbers_length):
        pieces.append(random.choice(special_characters))

    # shuffle and append the first uppercase letter
    random.shuffle(pieces)
    password += functools.reduce(lambda x, y: x + y, pieces)
    print(f"PASSWORD ({len(password)}): ", password)

    return password


def generate_password_from_file(file_name):
    file_path = get_file_abs_path(file_name)
    if file_path is None:
        print("File not found. Exiting...")
        return
    words = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            words += list(i for i in line.split(" ") if len(i) > 0)
    password_pieces = []
    random.shuffle(words)

    for word in words:
        # leave 2 for special characters and the digit
        if len(word) + sum(len(piece) for piece in password_pieces) <= max_size - 2:
            password_pieces.append(word)

    # We take this because we want to know the actual size and to extract the first part to be uppercase letter
    if len(password_pieces) == 0:
        first_word = random.choice(string.ascii_uppercase)
    else:
        first_word = password_pieces.pop(0).capitalize()  # first two are a digit and a special character

    password_pieces.append(random.choice(string.digits))
    password_pieces.append(random.choice(special_characters))

    current_password_length = sum(len(piece) for piece in password_pieces) + len(first_word)

    # We have the minimum requirements. But it will always contain only
    # a special character and a digit so just add some more characters
    remaining_digits = max_size - current_password_length
    if remaining_digits >= 1:
        if current_password_length >= 12:
            lower_bound_range = 1
        else:
            lower_bound_range = min_size - current_password_length
        more_digits = random.randrange(lower_bound_range, remaining_digits + 1)

        for i in range(more_digits):
            what_to_add = random.choice([0, 1])
            match what_to_add:
                case 0:
                    password_pieces.append(random.choice(string.digits))
                case 1:
                    password_pieces.append(random.choice(special_characters))
    random.shuffle(password_pieces)

    password = first_word + functools.reduce(lambda x, y: x + y, password_pieces)
    print(f"PASSWORD ({len(password)}): ", password)


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
    # Something like drives = ["G:\\"]
    drives = [root + os.sep]

    possible_files = []
    file = None
    for d in drives:
        possible_file = find_file(file_name, d)
        possible_files += possible_file
    if len(possible_files) == 0:
        print("Could not find your file!")
        return

    if len(possible_files) > 1:
        print(f"More files with the name \"{file_name}\" were found. Choose one:")
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
    argument_list = sys.argv[1:]
    if argument_list[0] == "test":
        test()
        return


    possible_first_argument = ['-use_dict']
    if len(argument_list) != 0 and len(argument_list) != 2:
        print("[ERROR] Invalid arguments\n" + usage_message)
        return

    match len(argument_list):
        case 0:
            generate_password()
        case 2:
            if argument_list[0] not in possible_first_argument:
                print(f"[ERROR] Argument {argument_list[0]} not found \n" + usage_message)
                return

            if argument_list[0] == '-use_dict':
                generate_password_from_file(argument_list[1])
            else:
                print(f"[ERROR] Argument {argument_list[0]} not found \n" + usage_message)
                return




if __name__ == '__main__':
    main()
