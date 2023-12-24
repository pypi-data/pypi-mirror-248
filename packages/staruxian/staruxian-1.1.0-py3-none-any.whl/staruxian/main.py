import random
import string

def print_lines(n, text):
    for _ in range(n):
        print(text)

def hello():
    print("Welcome to Khurshed's pip!")

def generate_pass(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password