import base64

# The provided Base32 string
base32_string = "FU2TOUKGIZJVQOCLFM4SKL2FKNLEKOSGGZEEEOCUJJCVCSBZFIWUCUKXIVDFARKBIVCCIS2FI5IEKIBZIUZTGRJ2LE4DUSCBKJBDQMSCHBMCUNRPLA3FASSCG5DTM==="

# Decode the Base32 string
decoded_bytes = base64.b32decode(base32_string)

# Attempt to decode it as a string (assuming it could be ASCII/UTF-8 encoded)
try:
    decoded_string = decoded_bytes.decode('utf-8')
except UnicodeDecodeError:
    decoded_string = decoded_bytes  # If not a valid UTF-8 string, return raw bytes

decoded_string

