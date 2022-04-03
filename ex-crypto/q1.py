import string
import itertools

class RepeatedKeyCipher:

    def __init__(self, key: bytes = bytes([0, 0, 0, 0, 0])):
        """Initializes the object with a list of integers between 0 and 255."""
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.key = list(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts a given plaintext string and returns the ciphertext."""
        text_bytes = plaintext.encode('latin-1')
        
        cipher = []
        j = 0   
        
        # go through all the plaintext
        for i in range(len(plaintext)):
            # make the repeat
            if j == len(self.key):
                j = 0
            # xor the values   
            cipher.append(text_bytes[i] ^ self.key[j])
            j += 1
        return bytes(cipher)

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts a given ciphertext string and returns the plaintext."""
        # encrypt(c, k) == c ^ k == (m ^ k) ^ k == m ^ (k ^ k) == m ^ 0 == m
        return self.encrypt(ciphertext.decode('latin-1')).decode('latin-1')


class BreakerAssistant:

    def plaintext_score(self, plaintext: str) -> float:
        """Scores a candidate plaintext string, higher means more likely."""
        score = 0

        for c in plaintext:
            #check for alpha
            if ord('A') <= ord(c) and ord(c) <= ord('Z'):
                score += 1
            if ord('a') <= ord(c) and ord(c) <= ord('z'):
                score += 2
            
            # check whitespaces
            if c == ' ' or c == '   ' or c == '\n' or c == '\r' or c == '\t':
                score += 1
            # check special characters
            if c == '.' or c == '?' or c =='!' or c == ',' or c == ';' or c == ':':
                score += 1
            # check parantesis
            if c == '(' or c == ')' or c == '{' or c == '}' or c == '[' or c == ']':
                score += 1
            # check digit
            if ord('0') <= ord('c') and ord('c') <= ord('9'):
                score += 1 

        return score

    def brute_force(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        max_score = 0
        max_score_plaintext = ""
        # brute force all the keys options and get the highest score
        for key in itertools.permutations(range(256), key_length):
            key_in_bytes = bytes(key)
            cipher = RepeatedKeyCipher(key_in_bytes)
            plaintext = cipher.decrypt(cipher_text)
            score = self.plaintext_score(plaintext)
            if score > max_score:
                max_score = score
                max_score_plaintext = plaintext 
                    
        return max_score_plaintext

    def smarter_break(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher any way you like."""
        key = [0] * key_length if key_length < len(cipher_text) else [0] * len(cipher_text)
        i = 0
        while i < len(cipher_text) and i < key_length:           
            max_score = 0
            # go through all options of byte
            for mini_key in itertools.permutations(range(256), 1):
                score = 0
                j = i
                mini_key_in_bytes = bytes([mini_key[0]])
                cipher = RepeatedKeyCipher(mini_key_in_bytes)
                # sum the highest score of the appropriate bytes in cipher for the specific key
                while True:
                    mini_cipher = bytes([cipher_text[j]])
                    mini_plaintext = cipher.decrypt(mini_cipher)
                    score += self.plaintext_score(mini_plaintext)
            
                    if j + key_length >= len(cipher_text):
                        break
                    j = j + key_length
                if score > max_score:
                    max_score = score
                    max_score_mini_key = mini_key[0]
            # get the key byte of the highest score
            key[i] = max_score_mini_key 
            i += 1
        key_in_bytes = bytes(key)
        cipher = RepeatedKeyCipher(key_in_bytes)
        plain_text = cipher.decrypt(cipher_text)
        return plain_text
