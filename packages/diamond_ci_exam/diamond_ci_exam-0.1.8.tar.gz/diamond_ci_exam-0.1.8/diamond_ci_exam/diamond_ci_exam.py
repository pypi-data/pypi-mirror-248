import sys


def diamond(letter):
    if not isinstance(letter, str) or not letter.isalpha():
        return "\033[91mVeuillez entrer un caractère de type lettre.\033[0m"

    if len(letter) != 1:
        return "\033[91mVeuillez entrer une seule lettre.\033[0m"

    n = ord(letter.upper()) - ord('A') + 1
    result = ""

    for i in range(1, n + 1):
        spaces = " " * (n - i)
        if i == 1:
            result += spaces + chr(ord('A')) + "\n" \
                if letter.upper() != 'A' else spaces + chr(ord('A')) + "\n"
        else:
            middle_spaces = " " * ((i - 1) * 2 - 1)
            result += spaces + chr(ord('A') + i - 1) \
                + middle_spaces + chr(ord('A') + i - 1) + "\n"

    for i in range(2, n):
        spaces = " " * (i - 1)
        middle_spaces = " " * ((n - i) * 2 - 1)
        result += spaces + chr(ord('A') + n - i)\
            + middle_spaces + chr(ord('A') + n - i) + "\n"

    result += " " * (n - 1) + chr(ord('A')) if letter.upper() != 'A' else ""

    return result


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: python diamond_ci_exam.py '<letter>'")
    elif len(sys.argv) == 2:
        letter = sys.argv[1]
        print(diamond(letter))
    else:
        print(diamond('f'))
