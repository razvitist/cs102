import typing as tp

A = "abcdefghijklmnopqrstuvwxyz"
B = A.upper()


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    r = ""
    for i in plaintext:
        if i in A:
            r += A[(A.index(i) + shift) % 26]
        elif i in B:
            r += B[(B.index(i) + shift) % 26]
        else:
            r += i
    return r


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    r = ""
    for i in ciphertext:
        if i in A:
            r += A[(A.index(i) - shift) % 26]
        elif i in B:
            r += B[(B.index(i) - shift) % 26]
        else:
            r += i
    return r


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    m = 0
    for i in range(26):
        n = 0
        t = decrypt_caesar(ciphertext, i)
        for j in dictionary:
            if j in t:
                n += 1
        if n > m:
            m = n
            best_shift = i
    return best_shift
