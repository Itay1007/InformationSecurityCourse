def fix_message_data(data: bytes) -> bytes:
    """
    Implement this function to return the "fixed" message content. This message
    should have minimal differences from the original message, but should pass
    the check of `msgcheck`.

    :param data: The source message data.
    :return: The fixed message data.
    """
    lst_data = list(data)
    
    length = lst_data[0]
    verification_value = lst_data[1]
    metadata_length = 2
    accumulator_xors = 0xD9 # 0xD9 is the inital hardcoded value
    values_to_xor = lst_data[metadata_length:length + metadata_length]

    for value_to_xor in values_to_xor:
        accumulator_xors ^= value_to_xor
        accumulator_xors &= 0xFF
    
    if accumulator_xors == verification_value:
        return data

    lst_data[1] = accumulator_xors
    return bytes(lst_data)

def fix_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    fixed_data = fix_message_data(data)
    with open(path + '.fixed', 'wb') as writer:
        writer.write(fixed_data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    fix_message(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
