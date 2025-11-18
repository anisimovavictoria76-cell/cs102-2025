def encrypt_affine(plaintext, a, b):
    result = []

    for char in plaintext:
        if char.isupper():
            x = ord(char) - ord('A')
            encrypted = (a * x + b) % 26
            result.append(chr(encrypted + ord('A')))
        elif char.islower():
            x = ord(char) - ord('a')
            encrypted = (a * x + b) % 26
            result.append(chr(encrypted + ord('a')))
        else:
            result.append(char)

    return ''.join(result)


if __name__ == "__main__":
    plaintext = "HELLO"
    a = 5
    b = 8
    encrypted = encrypt_affine(plaintext, a, b)
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")