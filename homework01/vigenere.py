A = "abcdefghijklmnopqrstuvwxyz"
B = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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
    r = ""
    for j, i in enumerate(plaintext):
        if i in A:
            r += A[(A.index(i) + A.index(keyword[j % len(keyword)])) % 26]
        elif i in B:
            r += B[(B.index(i) + B.index(keyword[j % len(keyword)])) % 26]
        else:
            r += i
    return r


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
    r = ""
    for j, i in enumerate(ciphertext):
        if i in A:
            r += A[(A.index(i) - A.index(keyword[j % len(keyword)])) % 26]
        elif i in B:
            r += B[(B.index(i) - B.index(keyword[j % len(keyword)])) % 26]
        else:
            r += i
    return r
