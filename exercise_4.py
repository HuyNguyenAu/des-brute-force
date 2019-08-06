# PiCryptodome only works with bytes for key, plaintext, and ciphertext.
from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

# Key Gen. Better than just using nested loops.
# https://docs.python.org/2/library/itertools.html#itertools.product
# I don't fully understand it.
from itertools import product

# Run in parallel.
from multiprocessing import Pool
from psutil import cpu_count

# Time.
from timeit import default_timer

def DecryptDES(key):
    # DES encryption and decryption.
    # Key Size: 64 bits, Block Size: 8 bytes, Mode: ECB.
    # We will use ECB mode since it is simple.
    # https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
    # https://pycryptodome.readthedocs.io/en/latest/src/cipher/des.html
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(b"ce126d2ddf2d1e64")


if __name__ == "__main__":
    # Number of physical cores for parallel processing.
    cpuCount = cpu_count(logical=False) - 1

    startTime = default_timer()

    # Generate all possible 8 byte combinations.
    # To do this, we first need to generate all the values possible in a byte.
    # That is, we need to generate a list of ints from 0 to 255.
    # To do this, we use range(256) which produces [0, ..., 255].
    # https://docs.python.org/3/library/functions.html#func-range
    # Next we need to generate all possible permutations of an 8 byte based on range(256).
    # That means that we need to repeat the product 8 times to produce a valid key of 8 bytes.
    # ie. [0, 0, 0, 0, 0, 0, 0, 0] ... [255, 255, 255, 255, 255, 255, 255, 255].
    # Same as 0 to 256 ^ 8.

    # We can try to distribute the load to all avaliable physical cores.
    # Fill a list equal to the number of physical cores.
    # ie. 4 physical cores = 4 items.
    keys = []
    for key in product(range(256), repeat=8):
        # Fill keys to number of physical cores.
        if len(keys) < cpuCount:
            # Convert the key to bytes.
            keys.append(bytearray(key))
        # Try out the keys and clear keys.
        else:
            with Pool(processes=cpuCount) as p:
                # Attempt to decode the plaintext. Skip all invalid ones.
                for i in p.map(DecryptDES, keys):              
                    try:
                        print(str(i, "utf-8"))
                    except Exception:
                        pass
            keys.clear()
    print(default_timer() - startTime)
