import os
import sys

from PyInquirer import prompt
from rsa import RSA, encrypt, decrypt


def generate_keys():
    rsa = RSA()
    print(f"Public Key: {rsa.publickey} Private Key: {rsa.privatekey}")


def encrypt_file_questions():
    questions = [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'Enter the path of the file to be encrypted',
            'validate': lambda filepath: os.path.exists(filepath) or 'The file does not exist!'
        },
        {
            'type': 'input',
            'name': 'publickey',
            'message': 'Enter the public key [Format: (e, n)]',
            'validate': lambda key: (type(eval(key)) == tuple) or 'Please enter the key in correct format'
        }
    ]

    answers = prompt(questions)

    filename = answers['filename']
    publickey = eval(answers['publickey'])
    encrypt(filename, publickey)
    print(f"{filename} has been encrypted!")


def decrypt_file_questions():
    questions = [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'Enter the path of the file to be decrypted',
            'validate': lambda filepath: os.path.exists(filepath) or 'The file does not exist!'
        },
        {
            'type': 'input',
            'name': 'privatekey',
            'message': 'Enter the private key [Format: (d, n)]',
            'validate': lambda key: (type(eval(key)) == tuple) or 'Please enter the key in correct format'
        }
    ]
    answers = prompt(questions)

    filename = answers['filename']
    privatekey = eval(answers['privatekey'])
    decrypt(filename, privatekey)
    print(f"{filename} has been decrypted!")


def main():
    choices = [
        {
            'type': 'list',
            'name': 'choice',
            'message': 'What do you want to do?',
            'choices': [
                '1.Generate keys',
                '2.Encrypt file',
                '3.Decrypt file',
                '4.Exit'
            ],
        }
    ]

    mapping = {
        '1': generate_keys,
        '2': encrypt_file_questions,
        '3': decrypt_file_questions,
        '4': sys.exit
    }
    while True:
        # Fetch the user's choice
        choice = prompt(choices)['choice'][0]

        # Call the function associated with the choice
        mapping[choice]()


if __name__=="__main__":
    main()