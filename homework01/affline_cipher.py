def encrypt_affine(plaintext, a, b):
    m = 26

    def char_to_num(char):
        if char.isupper():
            return ord(char) - ord('A')
        elif char.islower():
            return ord(char) - ord('a')
        return None

    def num_to_char(num, is_upper):
        if is_upper:
            return chr(num + ord('A'))
        else:
            return chr(num + ord('a'))

    encrypted_chars = []

    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()

            x = char_to_num(char)

            encrypted_num = (a * x + b) % m

            encrypted_char = num_to_char(encrypted_num, is_upper)
            encrypted_chars.append(encrypted_char)
        else:
            encrypted_chars.append(char)

    return ''.join(encrypted_chars)


if __name__ == "__main__":
    plaintext = "HELLO"
    a = 5
    b = 8
    encrypted = encrypt_affine(plaintext, a, b)
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")

    plaintext2 = "Hello World"
    encrypted2 = encrypt_affine(plaintext2, a, b)
    print(f"Plaintext: {plaintext2}")
    print(f"Encrypted: {encrypted2}")