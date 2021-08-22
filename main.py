import os
import sys

from PyInquirer import prompt
from rsa import RSA
from huffman import HuffmanEncoding


huff = HuffmanEncoding()


def generate_keys():
    publickey, privatekey = RSA.generatekeys()
    print(f"Public Key: {publickey} Private Key: {privatekey}")


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
    RSA.encrypt(filename, publickey)
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
    RSA.decrypt(filename, privatekey)
    print(f"{filename} has been decrypted!")


def compress_file_questions():
    questions = [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'Enter the path of the file to be compressed',
            'validate': lambda filepath: os.path.exists(filepath) or 'The file does not exist!'
        }
    ]
    answers = prompt(questions)

    filename = answers['filename']
    huff.compress(filename)
    print(f"{filename} has been compressed!")


def decompress_file_questions():
    questions = [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'Enter the path of the file to be decompressed',
            'validate': lambda filepath: os.path.exists(filepath) or 'The file does not exist!'
        }
    ]
    answers = prompt(questions)

    filename = answers['filename']
    huff.decompress(filename, "encoding.json")
    print(f"{filename} has been decompressed!")


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
                '4.Compress file',
                '5.Decompress file',
                '6.Exit'
            ],
        }
    ]

    mapping = {
        '1': generate_keys,
        '2': encrypt_file_questions,
        '3': decrypt_file_questions,
        '4': compress_file_questions,
        '5': decompress_file_questions,
        '6': sys.exit
    }
    
    while True:
        # Fetch the user's choice
        choice = prompt(choices)['choice'][0]
        # Call the function associated with the choice
        mapping[choice]()


if __name__=="__main__":
    main()