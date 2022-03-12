def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    return 0 for all input files.

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    lst_program = list(program)
    specific_jne_relative_position = 0x596 # 0x6cb
    # patch the opcode of jne [0x75] to the opcode of jmp [0xE8]
    print(hex(lst_program[specific_jne_relative_position]))
    lst_program[specific_jne_relative_position] = 0xF6
    return bytes(lst_program) 


def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msgcheck-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
