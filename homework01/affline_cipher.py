"""Аффинный шифр (affine_cipher.py)"""


def encrypt_affine(plaintext, a, b):
    """Функция делает шифровку"""
    ALPHABET_SIZE = 26
    result = []

    for char in plaintext:
        if char.isupper():
            x = ord(char) - ord("A")
            encrypted = (a * x + b) % ALPHABET_SIZE
            result.append(chr(encrypted + ord("A")))
        elif char.islower():
            x = ord(char) - ord("a")
            encrypted = (a * x + b) % ALPHABET_SIZE
            result.append(chr(encrypted + ord("a")))
        else:
            result.append(char)

    return "".join(result)


if __name__ == "__main__":
    PLAINTEXT = "HELLO"
    A = 5
    B = 8
    ENCRYPTED = encrypt_affine(PLAINTEXT, A, B)
    print(f"Plaintext: {PLAINTEXT}")
    print(f"Encrypted: {ENCRYPTED}")
