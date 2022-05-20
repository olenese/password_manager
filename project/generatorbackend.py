import random
import string
import os
import sys

characters = list(string.ascii_letters + string.digits + "!@$%&#/\?*()")
special_characters = list("!@$%&#/\?*()")
special_characters_with_whitespace = list("!@$%&#/\?*() ")

def randomcharacter(length):
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    result = [ ]
    for x in password:
        case = random.randint(0,1)
        if case == 0:
            result.append(x.upper())
        else:
            result.append(x.lower())
    return "".join(result)

def passphraseNO(length):
    passphrase = []
    with open('wordlistNOB.txt') as f:
        line = f.readlines()
        random.shuffle(line)
        for i in range(length):
            passphrase.append(line[i].strip("\n"))
    return "-".join(passphrase)

def passhpraseEN(length):
    passphrase = []
    with open('wordlistEN.txt') as f:
        line = f.readlines()
        random.shuffle(line)
        for i in range(length):
            passphrase.append(line[i].strip("\n"))
    return "-".join(passphrase)
