from functions import email_functions
import subprocess

def ghunt_search(name):
    emails = email_functions.permutateEmail(name, 'gmail.com')
    for i in range(0, len(emails)):
        path = '../tmp/ghunt/' + name + str(i) + '.txt'
        with open(path, 'w+') as file:
            subprocess.call(['python3', '../modules/GHunt/hunt.py', emails[i]], stdout=file)



ghunt_search('Wojciech Padala')