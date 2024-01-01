class AffineCipher:
    def __init__(self, multiplier: int, shift: int):
        self._multiplier = multiplier
        self._shift = shift % 26

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier: int):
        self._multiplier = multiplier

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, shift: int):
        self._shift = shift % 26

    def _shift_char(self, char: chr):
        if char.isalpha():
            shifted = (self._multiplier * (ord(char) - ord('a')) + self._shift) % 26 + ord('a')
            if shifted > ord('z'):
                shifted -= 26
            return chr(shifted)
        return char

    def encrypt(self, plaintext: str) -> str:
        encrypted_text = ''.join([self._shift_char(char) for char in plaintext.lower()])
        return encrypted_text

    def decrypt(self, ciphertext: str) -> str:
        self._shift = -self._shift
        decrypted_text = ''.join([self._shift_char(char) for char in ciphertext.lower()])
        self._shift = -self._shift
        return decrypted_text


# Example usage:
if __name__ == "__main__":
    base = 1
    shift = 2
    message = "HELLO world 2024"
    cipher = AffineCipher(base, shift)
    encrypted_message = cipher.encrypt(message)
    decrypted_message = cipher.decrypt(encrypted_message)

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)
