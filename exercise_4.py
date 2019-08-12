# PiCryptodome only works with bytes for key, plaintext, and ciphertext.
# DOES NOT WORK ON LINUX. HAS VERY BAD MEMORY LEAKS, WHERE 8Gb RAM 
# BECOMES FULL AFTER 30 MINS !!!
from Crypto.Cipher import DES

# Key Gen. Better than just using nested loops.
# https://docs.python.org/2/library/itertools.html#itertools.product
# I don't fully understand it.
from itertools import product
from binascii import b2a_uu
from gc import collect

# Regex
from re import search

# DES encryption and decryption.
# Key Size: 64 bits, Block Size: 8 bytes, Mode: ECB.
# We will use ECB mode since it is simple.
# https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/des.html

# Generate all possible 8 byte combination  s.
# To do this, we first need to generate all the values possible in a byte.
# That is, we need to generate a list of ints from 0 to 255.
# To do this, we use range(256) which produces [0, ..., 255].
# https://docs.python.org/3/library/functions.html#func-range
# Next we need to generate all possible permutations of an 8 byte based on range(256).
# That means that we need to repeat the product 8 times to produce a valid key of 8 bytes.
# ie. [0, 0, 0, 0, 0, 0, 0, 0] ... [255, 255, 255, 255, 255, 255, 255, 255].
# New hint for key: [?, ?, ?, ?, E5, F6, 66, ?] = [?, ?, ?, ?, 229, 246, 102, ?].
# Same as 0 to 256 ^ 8.

if __name__ == "__main__":
    for keyGen in product(range(256), repeat=5):
        try:
            key = bytearray(
                (keyGen[0], keyGen[1], keyGen[2], keyGen[3], 229, 246, 102, keyGen[4])
            )
            cipher = DES.new(key, DES.MODE_ECB)
            plaintext = cipher.decrypt(bytes.fromhex("ce126d2ddf2d1e64"))
            match = search("[A-Z]{4} [A-Z]{4}", b2a_uu(plaintext).decode())
            # DEBUG
            # print(f"{key.hex()} {b2a_uu(plaintext).decode()}")

            if match:
                with open("plaintext", "w") as file:
                    file.write(str(key.hex()) + " " + str(match) + "\n")
        except Exception:
            pass
        finally:        
            # Memory not being released sometimes. 
            collect()