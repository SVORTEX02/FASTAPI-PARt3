# # simple decoding 
# import base64
# original_string = "Hello, World! This is a simple test."

# string_bytes = original_string.encode('utf-8')

# encoded_bytes = base64.b64encode(string_bytes)
# encoded_string = encoded_bytes.decode('utf-8')

# print(f"Original String: {original_string}")
# print(f"Encoded String: {encoded_string}")



# base64_bytes = encoded_string.encode('utf-8')

# decoded_bytes = base64.b64decode(base64_bytes)


# decoded_string = decoded_bytes.decode('utf-8')

# print(f"Decoded String: {decoded_string}")


# encryption -decryption 
# 1 -> Hashlib Library for Secure Hashing

import hashlib
correct_password = "Ronaldo"
h1 = hashlib.sha256()
h1.update(correct_password.encode())
correct_hash = h1.hexdigest()

print(f"Correct Hashed: {correct_hash}")

user = input("Enter the password: ")

h2 = hashlib.sha256()
h2.update(user.encode())
user_hash = h2.hexdigest()



print(f"User Hashed:    {user_hash}")

if user_hash == correct_hash:
    print(" Password matched")
else:
    print(" Password incorrect")