# Password Encryption program

import base64


def encrypt_pass(password):
    encoded_bytes = base64.b64encode(password.encode())
    print(f"Your Encrypted password is: {encoded_bytes}")


user_pass = input("Enter your password: ")
encrypt_pass(user_pass)
