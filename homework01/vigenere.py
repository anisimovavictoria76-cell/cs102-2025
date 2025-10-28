def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_upper = keyword.upper()
    key_length = len(keyword_upper)

    for i, char in enumerate(plaintext):
        if char.isalpha():
            key_char = keyword_upper[i % key_length]
            shift = ord(key_char) - ord('A')

            if char.isupper():
                base = ord('A')
                encrypted_char = chr((ord(char) - base + shift) % 26 + base)
                ciphertext += encrypted_char
            else:
                base = ord('a')
                encrypted_char = chr((ord(char) - base + shift) % 26 + base)
                ciphertext += encrypted_char
        else:
            ciphertext += char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_upper = keyword.upper()
    key_length = len(keyword_upper)

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = keyword_upper[i % key_length]
            shift = ord(key_char) - ord('A')

            if char.isupper():
                base = ord('A')
                decrypted_char = chr((ord(char) - base - shift) % 26 + base)
                plaintext += decrypted_char
            else:
                base = ord('a')
                decrypted_char = chr((ord(char) - base - shift) % 26 + base)
                plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext