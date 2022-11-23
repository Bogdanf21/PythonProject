import functools
import string
import sys
import random
import getopt


def generate_password():
    password = ""
    # 18 and not 19 because only the letters besides the first can be of any kind
    password_length = random.randrange(11, 18)
    print("RANGE:", random.randrange(1, 2))

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
        pieces.append(random.choice(["!", "?", "#", "@"]))

    # shuffle and append the first uppercase letter
    random.shuffle(pieces)
    password += functools.reduce(lambda x, y: x + y, pieces)
    print("PASSWORD: ", password)


def generate_password_from_file():
    pass


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
        case 1:
            generate_password_from_file()


if __name__ == '__main__':
    main()
