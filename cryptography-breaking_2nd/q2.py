from q2_atm import ATM, ServerResponse, fast_exponent_and_modulus
import itertools
from math import ceil
def extract_PIN(encrypted_PIN) -> int:
    """Extracts the original PIN string from an encrypted PIN."""
    # brute force all the options for PIN
    for pin in range(10000):
        atm = ATM()
        encrypted_PIN_option = atm.encrypt_PIN(pin)
        # encryption is unique to PIN so checks if found the PIN of this encryption
        if encrypted_PIN_option == encrypted_PIN:
            return pin

def extract_credit_card(encrypted_credit_card) -> int:
    """Extracts a credit card number string from its ciphertext."""
    # encryption is power of 3
    return round(encrypted_credit_card ** (1/3))

def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.
    # first argument for get true in the first condition of the and in the verify and second argument to get true in the second condition of the and in the verify
    srvResponse = ServerResponse(1, 1)
    return srvResponse
