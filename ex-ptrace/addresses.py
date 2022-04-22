import struct


def address_to_bytes(address: int) -> bytes:
    """Convert an address to bytes, in little endian."""
    return struct.pack('<L', address)


########### QUESTION 2 ##############

# Memory address where the check_if_virus function from (libvalidator.so) begins.
# USE THIS IN `q2.py`
CHECK_IF_VIRUS_CODE = 0xb7fc82a3


########### QUESTION 3 ##############

# Memory address of the GOT entry of check_if_virus inside antivirus.
# USE THIS IN `q3.py`
CHECK_IF_VIRUS_GOT = 0x804c00c

# Memory address of the function to use as an alternative for check_if_virus
# (i.e. a function with the same signature that you'll write to the GOT instead
# of the address of check_if_virus).
# This function is check_if_live_patch
CHECK_IF_VIRUS_ALTERNATIVE = 0xb7fc8362
