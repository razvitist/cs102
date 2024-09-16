A = "abcdefghijklmnopqrstuvwxyz"
B = A.upper()


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
    chiphertext = ""
    for j, i in enumerate(plaintext):
        if i in A:
            chiphertext += A[(A.index(i) + A.index(keyword.lower()[j % len(keyword)])) % 26]
        elif i in B:
            chiphertext += B[(B.index(i) + B.index(keyword.upper()[j % len(keyword)])) % 26]
        else:
            chiphertext += i
    return chiphertext


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
    for j, i in enumerate(ciphertext):
        if i in A:
            plaintext += A[(A.index(i) - A.index(keyword.lower()[j % len(keyword)])) % 26]
        elif i in B:
            plaintext += B[(B.index(i) - B.index(keyword.upper()[j % len(keyword)])) % 26]
        else:
            plaintext += i
    return plaintext
