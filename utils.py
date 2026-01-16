import random
import string
import pyperclip
from tkinter import Tk

def generate_strong_password() -> str:
    #random 12-16 character password
    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!@#$%^&*()"

    password_list = [
        random.choice(letters),
        random.choice(numbers),
        random.choice(symbols)
    ]

    for _ in range(random.randint(10, 14)):
        password_list.append(random.choice(letters + numbers + symbols))

    random.shuffle(password_list)
    return "".join(password_list)

def copy_to_clipboard(text: str, root: Tk):
    pyperclip.copy(text)
    # clipboard clear after 60 seconds
    root.after(60000, lambda: pyperclip.copy(""))