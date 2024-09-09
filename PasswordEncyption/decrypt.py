# Password Decryption program

import base64


def decrypt_pass(password):
    decoded_bytes = base64.b64decode(password)
    decode_data = decoded_bytes.decode()
    print(f"Your decrypted password is: {decode_data}")


encoded_string = input("Enter the base64 string: ")
decrypt_pass(encoded_string)
