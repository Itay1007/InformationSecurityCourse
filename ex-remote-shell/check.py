from typing import Tuple, Iterable
from infosec.core import assemble

ASCII_MAX = 0x7f

DECODER_FILE_PATH = "decoder.asm"

NEW_LINE = "\n"

def encode(data: bytes) -> Tuple[bytes, Iterable[int]]:
    """Encode the given data to be valid ASCII.

    As we recommended in the exercise, the easiest way 
    non-ASCII bytes with 0xff, and have this function r
    and the indices that were XOR-ed.

    Tips:
    1. To return multiple values, do `return a, b`

    Args:
        data - The data to encode

    Returns:
        A tuple of [the encoded data, the indices that 
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


def decode(patched_data_and_patched_indexes: Tuple[bytes, Iterable[int]]) -> bytes:
    patched_data = patched_data_and_patched_indexes[0]
    patched_indexes = patched_data_and_patched_indexes[1]
    patched_data_lst = list(patched_data)
   
    for idx in patched_indexes:
        patched_data_lst[idx] ^= ASCII_MAX
    
    data = bytes(patched_data_lst)
    return data


def check_encode():
    shellcode = assemble.assemble_file("./shellcode.asm")
    patched_shellcode, indexes_list = encode(shellcode)
    new_old_shellcode = decode(((patched_shellcode, indexes_list)))

    is_equal = False 
    for byte1, byte2 in zip(list(shellcode), list(new_old_shellcode)):
        if byte1 != byte2:
            print("Not equal!")
    print("equal")

    if list(shellcode) == list(new_old_shellcode):
        return 0
    return 1


def get_decoder_code(indices: Iterable[int]) -> bytes:
    decoder_code = ""
    for idx in indices:
        # ascii bytes code that effectivly does:
        # mov bl, 0xff
        decoder_code += "push 0x100" + NEW_LINE
        decoder_code += "pop ebx" + NEW_LINE
        decoder_code += "dec ebx" + NEW_LINE
        # decode the byte with another xor of 0xff
        decoder_code += f"xor byte ptr [eax + {idx}], bl" + NEW_LINE
    with open(DECODER_FILE_PATH, "w") as writer:
        writer.write(decoder_code)
    return assemble.assemble_file(DECODER_FILE_PATH)


def check_decoder():
    shellcode = assemble.assemble_file("./shellcode.asm")
    placeholder, indexes_lst = encode(shellcode)
    decoder_code = get_decoder_code(indexes_lst)    
    print("indexes: ")
    print(indexes_lst)
    print("decoder code:")
    print(decoder_code)

def main():
    ret = check_encode()
    check_decoder()    
    return ret
if __name__ == "__main__":
    main()
