def check_message(path: str) -> bool:
    """
    Return True if `msgcheck` would return 0 for the file at the specified path,
    return False otherwise.
    :param path: The file path.
    :return: True or False.
    """
    with open(path, 'rb') as reader:
        i = 0
        length = -1
        verification_value = -1
        accumulator_xors = 0xD9 # 0xD9 is the inital hardcoded value
        metadata_length = 2
        while(byte := reader.read(1)):
            if i == 0:
                length = int.from_bytes(byte, 'little')
            elif i == 1:
                verification_value = int.from_bytes(byte, 'little')
            elif i == length + metadata_length:
                break
            else:
                value_to_xor = int.from_bytes(byte, 'little')
                accumulator_xors ^= value_to_xor
                accumulator_xors &= 0xFF
            i += 1
    return accumulator_xors == verification_value            

def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    if check_message(path):
        print('valid message')
        return 0
    else:
        print('invalid message')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
