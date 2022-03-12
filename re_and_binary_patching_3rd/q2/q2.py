from infosec.core import assemble


def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    execute lines starting with #!, and print all other lines as-is.

    Use the `assemble` module to translate assembly to bytes. For help, in the
    command line run:

        ipython3 -c 'from infosec.core import assemble; help(assemble)'

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    lst_program = list(program)
    deadzone1_position = 0x633
    deadzone2_position = 0x5CD
    opcodes_to_patch1 = list(assemble.assemble_file("patch1.asm"))
    opcodes_to_patch2 = list(assemble.assemble_file("patch2.asm"))
    #print(hex(lst_program[specific_jne_relative_position]))
    for i, opcode in enumerate(opcodes_to_patch1):
        lst_program[deadzone1_position + i] = opcode
    for i, opcode in enumerate(opcodes_to_patch2):
        lst_program[deadzone2_position + i] = opcode
    return bytes(lst_program)


def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
